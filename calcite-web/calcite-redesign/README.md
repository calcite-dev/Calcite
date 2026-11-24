# Calcite website + Studio

## Before deploying
This is an initial implementation, not a security-audited production system. Public site works without Supabase; Studio requires setup. Do not replace your existing DNS until tested. No actual video IDs were visible in the screenshot, so the list starts empty until feed sync or manual entry. The logo is the original supplied image. Contact and community links are intentionally blank until verified. Do not collect private information in applications; public submissions have only a basic global hourly cap, not robust spam protection. Keep applications off until reviewed.

## Supabase
1. Create a fresh project. Run `schema.sql` once in SQL Editor.
2. In Authentication settings disable public signup. In Authentication > Users create the first user manually, with email `yourusername@calcite.invalid`, a unique strong password and auto-confirm enabled. The synthetic email is a login identifier, not a mailbox. No email recovery is available. Keep the password in a password manager; owner recovery is through your Supabase account. Use a username matching `[a-z0-9_.-]{3,40}`.
3. Copy the user's UUID and run (substitute both values):
   ```sql
   insert into public.profiles(id,username,owner) values('YOUR-AUTH-USER-UUID','yourusername',true);
   ```
4. Put the project URL and **publishable or anon key** in `config.js`. Never use a service-role or secret key there.
5. Deploy `supabase/functions/manage-users/index.ts` as the Edge Function `manage-users` using the Supabase CLI (`supabase login`, `supabase link --project-ref YOUR_REF`, `supabase functions deploy manage-users`). It verifies the caller's access token and owner role itself. Keep gateway JWT verification if compatible with your project's tokens; if it rejects valid tokens, deploy with `--no-verify-jwt` only because this function independently validates every token through Auth. The built-in service-role key stays on the server. Disable signup and test account creation, password reset, access revocation and publishing before going live.
6. Open Studio and sign in using username (not email). Create a restricted test user. Test that anonymous users cannot read drafts, profiles or applications, and a restricted user cannot publish or change permissions even by calling RPC directly. Do not give other staff the owner login. A revoked staff account may retain previously loaded data locally, but database access is checked on every request.

## GitHub Pages
1. Create a repository, upload the files (including hidden `.github/workflows/pages.yml`), use `main` as default branch. GitHub Pages free hosting generally requires a public repository: do not commit secrets or private data. Only the public files are deployed.
2. Settings > Pages > Build and deployment > Source: GitHub Actions. Run the Publish Calcite workflow manually. Test the provided Pages URL.
3. Find the channel ID starting UC in YouTube Studio advanced account settings. Set repository variable `YOUTUBE_CHANNEL_ID` in Settings > Secrets and variables > Actions > Variables. The workflow refreshes the public YouTube RSS feed approximately every six hours; schedules are best-effort and feed failures stop deployment to retain the previous site. Manual videos override duplicates. Auto-imported videos initially have Minecraft category; edit/curate as needed. It does not provide YouTube Studio analytics or upload videos to YouTube.
4. In Pages settings set custom domain `www.calcite.yt`; in Internet.bs change the www CNAME to YOUR-GITHUB-USERNAME.github.io. Verify current GitHub documentation for apex DNS if using calcite.yt without www; preserve unrelated MX/TXT records. Enable HTTPS after certificate issuance. Keep the existing site until the new one passes testing.

## Use Studio
Save each section as a draft, then Dashboard > Publish saved drafts. The database stores versions on publication (restore currently requires SQL/admin access). Features toggles control public sections. Account creation and permissions are owner-only. Passwords are handled by Supabase Auth. Application submissions are private to reviewers; questions use one line per question and optional questions start with `?`. Private roadmap items are removed by the public RPC. Staff can read the shared draft, but edit only assigned sections. Concurrent edits use revision checking.

## Not yet implemented
Media uploads, traffic analytics, contact inbox, automatic draft saving, timed publishing, visual preview of unpublished drafts, UI version restore, drag-and-drop, opening dates, full spam protection, and light theme. No production security testing or live deployment has been done. Free tiers have quotas and may change. GitHub Actions schedules can be delayed or disabled for inactive repositories; Supabase free projects may pause. Review current provider terms and eligibility with a parent/guardian if necessary.
