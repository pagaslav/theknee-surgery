# Confidential attachments

New uploads use Cloudinary `resource_type=raw`, `type=authenticated`, random
public IDs including the file extension and `overwrite=False`. Filenames are
sanitized. No provider delivery URL is persisted or returned to the browser.
All supported files are stored as bytes without public image transformations.

Downloads go through `/files/<kind>/<document_id>`. The application rechecks
current owner/record permissions on every request, generates a 60-second signed
provider URL on the server and proxies the bytes as an attachment with no-store,
nosniff and a restrictive content policy. Provider redirects are refused; only
HTTPS Cloudinary API hosts are allowed, with connection/read timeouts and a
10 MiB byte limit even without Content-Length. Downloading consumes application
bandwidth/memory; capacity and hosting timeout limits need staging validation.

Record attachment deletion requires its assigned doctor or an admin and CSRF.
Patient ownership alone does not permit editing/deleting a medical record.
Provider deletion uses the stored delivery/resource type; the database entry is
removed only on confirmed success. No cloud operation is executed by this PR.

## Existing public uploads remain a separate incident risk

Files without authenticated/raw metadata return 410 through the application.
They are not silently treated as private, redirected or automatically migrated.
Previously shared public URLs/CDN copies may remain accessible. This PR does
not inspect, copy, rename, delete or invalidate real assets or database rows.
Blocking the application link does not revoke a public provider URL.

Before any approved release, use an isolated Cloudinary account and synthetic
PNG/JPEG/PDF/DOCX files to verify: unsigned original/derived URLs are denied;
allowed app downloads preserve bytes; unauthorized requests never contact the
provider; deletion targets authenticated/raw objects. Use dedicated test keys
and a disposable database. These provider checks are not covered by mocks.

A later explicitly authorized migration must privately inventory old assets,
map each to its record/owner, copy to authenticated raw storage with random IDs,
verify bytes and ACLs, update metadata and then revoke old public delivery and
invalidate cached originals/derivatives. Take a protected rollback copy first;
rollback must not reopen public delivery. Verify CDN invalidation and old-link
denial after propagation, and review backups/provider retention separately.
Do not run a bulk rename/delete based only on this document.

File extension checks and forced downloads do not provide malware scanning or
prove the contents are safe to open. Downloads already saved by an authorized
user cannot be remotely revoked. Production data and hosting remain untouched.

References:
- https://cloudinary.com/documentation/control_access_to_media
- https://cloudinary.com/documentation/upload_parameters
- https://cloudinary.com/documentation/image_upload_api_reference
