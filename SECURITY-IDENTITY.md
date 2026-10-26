# Immutable session identity

Sessions bind the MongoDB document ID and source collection. Email is a display
and navigation value only. Every authenticated request reloads the account and
role from the database, so renaming, reusing or deleting an email cannot transfer
the session to another user. Old email-only sessions are rejected and cleared;
users must sign in again after an eventual approved release.

Login refuses ambiguous email matches across users and doctors, including case
variants. Existing duplicates are not inspected or changed by this PR. Source
checks on signup/profile changes still cannot enforce a cross-collection unique
constraint under concurrent writes. A separately reviewed account-data migration
or central identity registry remains needed to prevent duplicate records. Such
collisions now deny login instead of selecting the first account.

The request tests use artificial identities and an in-memory MongoDB substitute.
This PR does not migrate or connect to any real database, rotate credentials,
merge branches, deploy code or change a hosted environment.
