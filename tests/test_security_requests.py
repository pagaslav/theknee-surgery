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
        self.cloud = patch.object(self.module.cloudinary.uploader, "upload", side_effect=lambda file, **options: {"public_id": options["public_id"], "secure_url": "https://example.invalid/never-disclose", "type": "authenticated", "resource_type": "raw"}).start()
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

    def private_document(self, kind='record'):
        document = {'file_id': 'medical/synthetic.pdf', 'file_name': 'test.pdf', 'delivery_type': 'authenticated', 'resource_type': 'raw'}
        collection = self.db.medical_record_files if kind == 'record' else self.db.user_files
        document['record_id' if kind == 'record' else 'user_id'] = self.record['_id'] if kind == 'record' else self.patient['_id']
        collection.insert_one(document)
        return document, f'/files/{kind}/{document["_id"]}'

    def mock_download(self, chunks=(b'synthetic private file',), status=200, headers=None):
        from unittest.mock import MagicMock
        remote = MagicMock()
        remote.status_code = status
        remote.headers = headers or {}
        remote.iter_content.return_value = iter(chunks)
        remote.__enter__.return_value = remote
        sign = patch.object(self.module.cloudinary.utils, 'private_download_url', return_value='https://api.cloudinary.com/v1_1/test/raw/download?signature=synthetic').start()
        get = patch.object(self.module.requests, 'get', return_value=remote).start()
        return sign, get, remote

    def test_all_upload_paths_use_authenticated_raw_storage_and_no_provider_url(self):
        self.login_as(self.doctor)
        self.post(f'/upload_medical_record_file/{self.record["_id"]}', data={'file': (io.BytesIO(b'one'), 'report.pdf')})
        self.post(f'/update_medical_record/{self.record["_id"]}', data={'description': 'synthetic', 'treatment': 'synthetic', 'record_date': '2026-10-26', 'file': (io.BytesIO(b'two'), 'report.pdf')})
        self.login_as(self.patient)
        response = self.post('/upload_file_ajax', data={'user_id': str(self.patient['_id']), 'file': (io.BytesIO(b'three'), 'report.pdf')})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['file_url'].startswith('/files/user/'))
        self.assertNotIn('example.invalid', response.get_data(as_text=True))
        self.assertEqual(self.cloud.call_count, 3)
        public_ids = set()
        for call in self.cloud.call_args_list:
            self.assertEqual(call.kwargs['type'], 'authenticated')
            self.assertEqual(call.kwargs['resource_type'], 'raw')
            self.assertFalse(call.kwargs['overwrite'])
            self.assertFalse(call.kwargs['use_filename'])
            self.assertNotIn('report', call.kwargs['public_id'])
            public_ids.add(call.kwargs['public_id'])
        self.assertEqual(len(public_ids), 3)
        documents = list(self.db.user_files.find()) + list(self.db.medical_record_files.find())
        self.assertEqual(len(documents), 3)
        for document in documents:
            self.assertNotIn('file_url', document)
            self.assertEqual(document['delivery_type'], 'authenticated')

    def test_unconfirmed_storage_response_is_not_persisted_or_disclosed(self):
        self.cloud.side_effect = None
        self.cloud.return_value = {'type': 'upload', 'resource_type': 'raw', 'secure_url': 'https://example.invalid/public'}
        self.login_as(self.patient)
        response = self.post('/upload_file_ajax', data={'user_id': str(self.patient['_id']), 'file': (io.BytesIO(b'test'), 'report.pdf')})
        self.assertEqual(response.status_code, 502)
        self.assertNotIn('example.invalid', response.get_data(as_text=True))
        self.assertEqual(self.db.user_files.count_documents({}), 0)

    def test_empty_or_disallowed_uploads_do_not_call_provider(self):
        self.login_as(self.patient)
        for content, filename in [(b'', 'empty.pdf'), (b'code', 'script.html')]:
            self.post('/upload_file_ajax', data={'user_id': str(self.patient['_id']), 'file': (io.BytesIO(content), filename)})
        self.cloud.assert_not_called()
        self.assertEqual(self.db.user_files.count_documents({}), 0)

    def test_record_file_read_permissions_and_revocation(self):
        document, url = self.private_document()
        outsider = {'_id': ObjectId(), 'email': 'outside@example.invalid', 'role': 'doctor'}
        self.db.doctors.insert_one(outsider)
        for actor, expected in [(None,403),(self.other,403),(outsider,403),(self.patient,200),(self.doctor,200),(self.admin,200)]:
            with self.subTest(actor=actor and actor['email']):
                self.login_as(actor)
                sign, get, remote = self.mock_download()
                self.assertEqual(self.client.get(url).status_code, expected)
                if expected != 200:
                    sign.assert_not_called()
                    get.assert_not_called()
        self.login_as(self.doctor)
        self.db.medical_records.update_one({'_id': self.record['_id']}, {'$set': {'doctor_id': outsider['_id']}})
        sign, get, _ = self.mock_download()
        self.assertEqual(self.client.get(url).status_code, 403)
        get.assert_not_called()
        sign.assert_not_called()

    def test_user_file_only_owner_and_admin_can_download(self):
        _, url = self.private_document('user')
        for actor, expected in [(None,403),(self.other,403),(self.doctor,403),(self.patient,200),(self.admin,200)]:
            self.login_as(actor)
            sign, get, _ = self.mock_download()
            self.assertEqual(self.client.get(url).status_code, expected)
            if expected != 200:
                sign.assert_not_called()
                get.assert_not_called()

    def test_download_keeps_signature_server_side_and_forces_safe_headers(self):
        _, url = self.private_document()
        self.login_as(self.patient)
        sign, get, remote = self.mock_download()
        with patch.object(self.module, 'time', SimpleNamespace(time=lambda: 2000000000)):
            result = self.client.get(url)
        self.assertEqual(result.data, b'synthetic private file')
        self.assertNotIn('Location', result.headers)
        self.assertEqual(result.content_type, 'application/octet-stream')
        self.assertEqual(result.headers['Cache-Control'], 'private, no-store')
        self.assertEqual(result.headers['Referrer-Policy'], 'no-referrer')
        self.assertEqual(result.headers['X-Content-Type-Options'], 'nosniff')
        self.assertIn('attachment', result.headers['Content-Disposition'])
        self.assertEqual(sign.call_args.kwargs['expires_at'], 2000000060)
        self.assertEqual(sign.call_args.kwargs['type'], 'authenticated')
        self.assertEqual(sign.call_args.kwargs['resource_type'], 'raw')
        self.assertFalse(get.call_args.kwargs['allow_redirects'])
        self.assertEqual(get.call_args.kwargs['timeout'], (3, 10))
        remote.__exit__.assert_called_once()

    def test_legacy_files_fail_closed_without_using_stored_url(self):
        result = self.db.user_files.insert_one({'user_id': self.patient['_id'], 'file_url': 'http://127.0.0.1/private', 'file_id': 'legacy'})
        self.login_as(self.patient)
        sign, get, _ = self.mock_download()
        self.assertEqual(self.client.get(f'/files/user/{result.inserted_id}').status_code, 410)
        sign.assert_not_called()
        get.assert_not_called()
        self.assertEqual(self.db.user_files.count_documents({}), 1)

    def test_download_rejects_redirects_errors_and_oversized_streams(self):
        _, url = self.private_document()
        self.login_as(self.patient)
        self.app.config['MAX_CONTENT_LENGTH'] = 16
        for chunks, status, headers in [((b'body',),302,{'Location':'http://localhost/'}),((b'body',),500,{}),((b'x'*17,),200,{}),((b'body',),200,{'Content-Length':'100'}),((b'body',),200,{'Content-Length':'invalid'})]:
            with self.subTest(status=status, headers=headers):
                self.mock_download(chunks, status, headers)
                self.assertEqual(self.client.get(url).status_code, 502)

    def test_download_never_requests_untrusted_signing_hosts(self):
        _, url = self.private_document()
        self.login_as(self.patient)
        sign, get, _ = self.mock_download()
        for unsafe in ['http://api.cloudinary.com/private', 'https://localhost/private', 'https://api.cloudinary.com.evil.invalid/private', 'https://user@api.cloudinary.com/private']:
            sign.return_value = unsafe
            self.assertEqual(self.client.get(url).status_code, 502)
        get.assert_not_called()

    def test_download_timeout_does_not_disclose_provider_url(self):
        _, url = self.private_document()
        self.login_as(self.patient)
        sign, get, _ = self.mock_download()
        get.side_effect = self.module.requests.Timeout('signature=synthetic-must-not-leak')
        result = self.client.get(url)
        self.assertEqual(result.status_code, 502)
        self.assertNotIn(b'synthetic-must-not-leak', result.data)

    def test_record_file_delete_requires_writer_csrf_and_confirmed_provider_success(self):
        document, _ = self.private_document()
        url = f'/medical_record_files/{document["_id"]}/delete'
        with patch.object(self.module.cloudinary.uploader, 'destroy', return_value={'result':'ok'}) as destroy:
            for actor in (None,self.patient,self.other):
                self.login_as(actor)
                self.assertEqual(self.post(url).status_code, 403)
            self.login_as(self.doctor)
            self.assertEqual(self.client.get(url).status_code, 405)
            self.assertEqual(self.client.post(url).status_code, 403)
            destroy.assert_not_called()
            destroy.return_value = {'result': 'error'}
            self.assertEqual(self.post(url).status_code, 502)
            self.assertIsNotNone(self.db.medical_record_files.find_one({'_id':document['_id']}))
            destroy.return_value = {'result':'ok'}
            self.assertEqual(self.post(url).status_code, 302)
            destroy.assert_called_with(document['file_id'], invalidate=True, type='authenticated', resource_type='raw')
            self.assertIsNone(self.db.medical_record_files.find_one({'_id':document['_id']}))

    def test_private_user_file_delete_uses_authenticated_resource_type(self):
        document, _ = self.private_document('user')
        self.login_as(self.patient)
        with patch.object(self.module.cloudinary.uploader, 'destroy', return_value={'result':'ok'}) as destroy:
            self.assertEqual(self.post('/delete_file', data={'file_id':document['file_id']}).status_code, 200)
            destroy.assert_called_once_with(document['file_id'], invalidate=True, type='authenticated', resource_type='raw')
            self.assertEqual(self.db.user_files.count_documents({}), 0)

    def test_invalid_or_missing_file_ids_do_not_contact_provider(self):
        self.login_as(self.patient)
        _, get, _ = self.mock_download()
        for url in ['/files/user/invalid', f'/files/user/{ObjectId()}', f'/files/unknown/{ObjectId()}']:
            self.assertEqual(self.client.get(url).status_code, 404)
        get.assert_not_called()

    def test_real_sdk_generates_signed_raw_download_without_a_format(self):
        from urllib.parse import urlsplit, parse_qs
        config = self.module.cloudinary.config()
        with patch.object(config, 'cloud_name', 'synthetic-cloud'), patch.object(config, 'api_key', 'synthetic-key'), patch.object(config, 'api_secret', 'synthetic-secret'):
            url = self.module.cloudinary.utils.private_download_url('medical/synthetic.pdf', None, resource_type='raw', type='authenticated', expires_at=2000000060, attachment=True, secure=True)
        parsed = urlsplit(url)
        self.assertEqual(parsed.scheme, 'https')
        self.assertEqual(parsed.hostname, 'api.cloudinary.com')
        self.assertIn('/raw/download', parsed.path)
        query = parse_qs(parsed.query)
        self.assertEqual(query['public_id'], ['medical/synthetic.pdf'])
        self.assertEqual(query['type'], ['authenticated'])
        self.assertEqual(query['expires_at'], ['2000000060'])
        self.assertIn('signature', query)
        self.assertNotIn('format', query)
        self.assertNotIn('synthetic-secret', url)

    def test_attachment_templates_render_only_application_download_links(self):
        document, url = self.private_document()
        with self.app.test_request_context('/'):
            html = self.app.jinja_env.get_template('medical_record_detail.html').render(files=[document], record=self.record, patient=self.patient, doctor=self.doctor, current_user=self.doctor, csrf_token=lambda:'test-token')
        self.assertIn(url, html)
        self.assertNotIn('file.file_url', html)
        self.assertNotIn('res.cloudinary.com', html)

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

    def test_real_login_route_enforces_shared_budget_before_password_check(self):
        self.login_as(None)
        with patch.object(self.module, 'check_password_hash', return_value=False) as verify:
            for _ in range(10):
                self.assertEqual(self.post('/login', data={'email':self.patient['email'], 'password':'wrong'}).status_code, 302)
            self.assertEqual(self.post('/login', data={'email':self.patient['email'], 'password':'wrong'}).status_code, 429)
            self.assertEqual(verify.call_count, 10)


if __name__ == '__main__':
    unittest.main()
