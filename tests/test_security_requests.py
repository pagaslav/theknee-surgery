"""Request regressions with disposable in-memory MongoDB and blocked cloud calls."""
import importlib.util
import io
import os
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

import mongomock
from bson import ObjectId
from werkzeug.security import generate_password_hash


class MedicalAccessTests(unittest.TestCase):
    def setUp(self):
        self.db = mongomock.MongoClient().security_test
        spec = importlib.util.spec_from_file_location("medical_app", Path(__file__).resolve().parents[1] / "app.py")
        self.module = importlib.util.module_from_spec(spec)
        with patch.dict(os.environ, {"SECRET_KEY": "unit-test-only"}, clear=True), patch("flask_pymongo.PyMongo", return_value=SimpleNamespace(db=self.db)):
            spec.loader.exec_module(self.module)
        self.app = self.module.app
        self.app.config.update(TESTING=True)
        self.render = patch.object(self.module, "render_template", return_value="rendered").start()
        self.cloud = patch.object(self.module.cloudinary.uploader, "upload", return_value={"public_id": "test", "secure_url": "https://example.invalid/test"}).start()
        self.addCleanup(patch.stopall)
        self.patient = {"_id": ObjectId(), "email": "a@example.invalid", "role": "patient", "name": "A", "password": generate_password_hash("TestPassword1")}
        self.other = {"_id": ObjectId(), "email": "b@example.invalid", "role": "patient", "name": "B"}
        self.doctor = {"_id": ObjectId(), "email": "doctor@example.invalid", "role": "doctor", "name": "Doctor"}
        self.admin = {"_id": ObjectId(), "email": "admin@example.invalid", "role": "admin", "name": "Admin"}
        self.db.users.insert_many([self.patient, self.other, self.admin])
        self.db.doctors.insert_one(self.doctor)
        self.record = {"_id": ObjectId(), "patient_id": self.patient["_id"], "doctor_id": self.doctor["_id"]}
        self.db.medical_records.insert_one(self.record)
        self.client = self.app.test_client()

    def login_as(self, actor):
        with self.client.session_transaction() as session:
            session.clear()
            if actor:
                session["user"] = actor["email"]
                if actor.get("_id"):
                    session["actor_id"] = str(actor["_id"])
                    session["actor_collection"] = "doctors" if actor.get("role") == "doctor" else "users"
            session["_csrf_token"] = "test-token"

    def post(self, url, **kwargs):
        return self.client.post(url, headers={"X-CSRF-Token": "test-token"}, **kwargs)

    def test_record_read_matrix(self):
        for actor, expected in [(None, 403), (self.patient, 200), (self.other, 403), (self.doctor, 200), (self.admin, 200)]:
            with self.subTest(actor=actor and actor["role"], email=actor and actor["email"]):
                self.login_as(actor)
                self.assertEqual(self.client.get(f'/medical_record/{self.record["_id"]}').status_code, expected)

    def test_unassigned_doctor_cannot_read_or_write(self):
        outsider = {"_id": ObjectId(), "email": "outsider@example.invalid", "role": "doctor"}
        self.db.doctors.insert_one(outsider)
        self.login_as(outsider)
        for path in ("medical_record", "edit_medical_record"):
            self.assertEqual(self.client.get(f'/{path}/{self.record["_id"]}').status_code, 403)
        self.assertEqual(self.post(f'/update_medical_record/{self.record["_id"]}').status_code, 403)

    def test_patient_cannot_edit_own_record(self):
        self.login_as(self.patient)
        self.assertEqual(self.client.get(f'/edit_medical_record/{self.record["_id"]}').status_code, 403)

    def test_denied_uploads_have_no_side_effects(self):
        for actor in (None, self.patient, self.other):
            self.login_as(actor)
            response = self.post(f'/upload_medical_record_file/{self.record["_id"]}', data={"file": (io.BytesIO(b"test"), "test.pdf")})
            self.assertEqual(response.status_code, 403)
        self.cloud.assert_not_called()
        self.assertEqual(self.db.medical_record_files.count_documents({}), 0)

    def test_assigned_doctor_can_upload(self):
        self.login_as(self.doctor)
        self.assertEqual(self.post(f'/upload_medical_record_file/{self.record["_id"]}', data={"file": (io.BytesIO(b"test"), "test.pdf")}).status_code, 302)
        self.cloud.assert_called_once()
        self.assertEqual(self.db.medical_record_files.count_documents({"record_id": self.record["_id"]}), 1)

    def test_missing_invalid_ids_and_unknown_session(self):
        self.login_as(self.patient)
        for value in ("invalid", str(ObjectId())):
            self.assertEqual(self.client.get('/medical_record/' + value).status_code, 404)
        self.login_as({"email": "deleted@example.invalid"})
        self.assertEqual(self.client.get(f'/medical_record/{self.record["_id"]}').status_code, 403)

    def test_csrf_blocks_authorized_upload(self):
        self.login_as(self.doctor)
        self.assertEqual(self.client.post(f'/upload_medical_record_file/{self.record["_id"]}').status_code, 403)
        self.cloud.assert_not_called()

    def test_profile_isolation_and_assignment(self):
        self.login_as(self.other)
        self.assertEqual(self.client.get('/profile/' + self.patient["email"]).status_code, 403)
        self.login_as(self.doctor)
        self.assertEqual(self.client.get('/profile/' + self.patient["email"]).status_code, 403)
        self.db.appointments.insert_one({"patient_id": self.patient["_id"], "assigned_doctor_id": self.doctor["_id"]})
        self.assertEqual(self.client.get('/profile/' + self.patient["email"]).status_code, 200)

    def test_foreign_user_upload_and_file_delete_denied(self):
        self.login_as(self.other)
        self.db.user_files.insert_one({"file_id": "private-file", "user_id": self.patient["_id"]})
        with patch.object(self.module, "delete_from_cloudinary") as delete:
            self.assertEqual(self.post('/delete_file', data={"file_id": "private-file"}).status_code, 403)
            delete.assert_not_called()
        self.assertEqual(self.post('/upload_file_ajax', data={"user_id": str(self.patient["_id"])}).status_code, 403)

    def test_email_cannot_adopt_patient_doctor_or_admin_identity(self):
        self.login_as(self.patient)
        for target in (self.other, self.doctor, self.admin):
            self.assertEqual(self.post('/edit_user_ajax', json={"user_id": str(self.patient["_id"]), "email": target["email"], "current_password": "TestPassword1"}).status_code, 409)
        self.assertEqual(self.db.users.find_one({"_id": self.patient["_id"]})["email"], self.patient["email"])

    def test_signup_cannot_duplicate_doctor_identity(self):
        self.login_as(None)
        response = self.post('/signup', data={"email": self.doctor["email"]})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.db.users.count_documents({"email": self.doctor["email"]}), 0)

    def test_password_change_is_bound_to_actor(self):
        self.login_as(self.other)
        self.assertEqual(self.post('/change_password', data={"user_id": str(self.patient["_id"])}).status_code, 403)

    def test_real_login_binds_collection_and_id_and_rotates_csrf(self):
        self.login_as(None)
        result = self.post('/login', data={'email': self.patient['email'], 'password': 'TestPassword1'})
        self.assertEqual(result.status_code, 302)
        with self.client.session_transaction() as session:
            self.assertEqual(session['actor_id'], str(self.patient['_id']))
            self.assertEqual(session['actor_collection'], 'users')
            self.assertNotIn('_csrf_token', session)
        self.assertEqual(self.client.get(f'/medical_record/{self.record["_id"]}').status_code, 200)

    def test_old_email_only_sessions_are_rejected_and_cleared(self):
        with self.client.session_transaction() as session:
            session['user'] = self.admin['email']
        self.assertEqual(self.client.get('/admin/users').status_code, 403)
        with self.client.session_transaction() as session:
            self.assertNotIn('user', session)

    def test_email_reuse_does_not_transfer_a_session(self):
        self.login_as(self.patient)
        self.db.users.update_one({'_id': self.patient['_id']}, {'$set': {'email': 'renamed@example.invalid'}})
        self.db.users.update_one({'_id': self.admin['_id']}, {'$set': {'email': self.patient['email']}})
        self.assertEqual(self.client.get('/admin/users').status_code, 302)
        self.render.assert_not_called()
        self.assertEqual(self.client.get(f'/medical_record/{self.record["_id"]}').status_code, 200)
        with self.client.session_transaction() as session:
            self.assertEqual(session['user'], 'renamed@example.invalid')
            self.assertEqual(session['actor_id'], str(self.patient['_id']))

    def test_deleted_actor_cannot_adopt_recreated_email(self):
        self.login_as(self.patient)
        self.db.users.delete_one({'_id': self.patient['_id']})
        self.db.users.insert_one({'email': self.patient['email'], 'role': 'admin'})
        self.assertEqual(self.client.get('/admin/users').status_code, 403)

    def test_login_rejects_ambiguous_email_across_and_within_collections(self):
        for collection in ('doctors', 'users'):
            with self.subTest(collection=collection):
                duplicate = {'email': self.patient['email'].upper(), 'role': 'admin', 'password': generate_password_hash('TestPassword1')}
                result = self.db[collection].insert_one(duplicate)
                self.login_as(None)
                self.assertEqual(self.post('/login', data={'email': self.patient['email'], 'password': 'TestPassword1'}).status_code, 302)
                with self.client.session_transaction() as session:
                    self.assertNotIn('actor_id', session)
                self.db[collection].delete_one({'_id': result.inserted_id})

    def test_database_role_revocation_is_effective_on_next_request(self):
        self.login_as(self.admin)
        self.db.users.update_one({'_id': self.admin['_id']}, {'$set': {'role': 'patient'}})
        self.assertEqual(self.client.get('/admin/users').status_code, 302)
        self.render.assert_not_called()

    def test_collection_binding_prevents_cross_collection_id_collision(self):
        self.login_as(self.patient)
        self.db.doctors.insert_one({'_id': self.patient['_id'], 'email': 'collision@example.invalid', 'role': 'admin'})
        self.assertEqual(self.client.get('/admin/users').status_code, 302)
        self.render.assert_not_called()

    def test_logout_removes_immutable_binding(self):
        self.login_as(self.patient)
        self.assertEqual(self.client.get('/logout').status_code, 302)
        with self.client.session_transaction() as session:
            self.assertNotIn('actor_id', session)
            self.assertNotIn('actor_collection', session)
            self.assertNotIn('user', session)

    def test_profile_target_is_bound_before_a_concurrent_email_reassignment(self):
        self.login_as(self.patient)
        original = self.module._email_accounts
        def race(email):
            matches = original(email)
            self.db.users.update_one({'_id': self.patient['_id']}, {'$set': {'email': 'renamed@example.invalid'}})
            self.db.users.update_one({'_id': self.other['_id']}, {'$set': {'email': self.patient['email']}})
            return matches
        with patch.object(self.module, '_email_accounts', side_effect=race):
            response = self.client.get('/profile/' + self.patient['email'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.render.call_args.kwargs['user']['_id'], self.patient['_id'])


if __name__ == '__main__':
    unittest.main()
