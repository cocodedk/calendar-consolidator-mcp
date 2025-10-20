# Azure App Registration and Credentials Setup

## Purpose
Create Microsoft Entra ID (Azure AD) app credentials for Microsoft Graph so Calendar Consolidator MCP can connect to Outlook/Microsoft 365 calendars using device code flow.

---

## Before You Begin
- Azure account with permission to register applications
- Decide scope level:
  - Personal Microsoft accounts only, organization only, or both. We recommend “any organization directory and personal Microsoft accounts” for flexibility.
- You will collect three values to paste into the app later:
  - Application (client) ID
  - Directory (tenant) ID (or use `common`)
  - Client secret VALUE

---

## Step 1 — Register an Application
1. Go to https://portal.azure.com/
2. Open “Microsoft Entra ID” (formerly Azure Active Directory)
3. App registrations → New registration
4. Name: `Calendar Consolidator`
5. Supported account types: “Accounts in any organizational directory and personal Microsoft accounts”
6. Redirect URI: leave empty (device code flow doesn’t use redirects)
7. Click Register

After registration completes:
- Copy Application (client) ID (GUID)
- Copy Directory (tenant) ID (GUID)

Tip: You may use `common` instead of the tenant GUID if you want to allow both personal and work/school accounts. Use the tenant GUID to restrict to one tenant.

---

## Step 2 — Enable Public Client (Device Code) Flow
1. In your new app: Authentication
2. Advanced settings → Allow public client flows → Set to Yes
3. Save

Without this, device code authentication will fail with “application is not configured as a public client”.

---

## Step 3 — Add Microsoft Graph API Permissions
1. API permissions → Add a permission
2. Microsoft Graph → Delegated permissions
3. Add:
   - `Calendars.ReadWrite` (recommended)
   - Optionally `Calendars.Read` if you only need read access
4. Add permissions
5. If using an organizational tenant, an admin may need to click “Grant admin consent”

Note: Do not add `offline_access`, `openid`, or `profile` here for this app. The MSAL library manages refresh behavior for device code flows without requesting reserved scopes in this project.

---

## Step 4 — Create a Client Secret
1. Certificates & secrets → Client secrets
2. New client secret
3. Description: `Calendar Consolidator Secret`
4. Expiry: choose 12–24 months per your policy
5. Add, then immediately copy the Client secret VALUE (not the ID)

Important: You can’t see the secret value again later. Store it securely until you paste it into the app.

---

## Step 5 — Enter Credentials in Calendar Consolidator MCP
1. Start the app (`./run.sh` or `./run_windows.ps1`) and open the web UI
2. Go to Settings → “🔑 OAuth Credentials” → Microsoft card → Configure
3. Paste the values:
   - Client ID: your Application (client) ID (GUID)
   - Tenant ID: either your Directory (tenant) ID (GUID) or `common`
   - Client Secret: the secret VALUE from Step 4
4. Save. Expect a success confirmation.

Next, connect a Microsoft source:
1. Sources → Add Source → Microsoft Outlook/365
2. Follow the device code instructions shown (copy code, open verification URL, sign in, allow permissions)
3. Return to the app and complete selection of calendars

All credentials and tokens are stored encrypted at rest. See `0-docs/SSJ-Tests/CREDENTIAL_SECURITY_TEST.md` for verification steps.

---

## Where to Find Values Later
- Client ID and Tenant ID: App registrations → your app → Overview
- Client Secret (new one): App registrations → your app → Certificates & secrets (you must create a new one to get the VALUE again)

Accepted formats in this project’s validation:
- `client_id`: GUID format
- `tenant_id`: GUID format or the literal `common`

---

## Troubleshooting
- AADSTS700016 / invalid_client: Check Client ID and Tenant ID (or use `common`).
- “This application doesn’t exist” during auth: Ensure the app is multi-tenant or your account belongs to the specified tenant.
- “Application is not configured as a public client”: Enable Authentication → Allow public client flows = Yes.
- “Need admin approval” consent screen: An Azure admin must grant tenant-wide consent for `Calendars.ReadWrite`.
- Device code completes but app can’t list calendars: Verify Graph permissions, then re-run the add source flow.

---

## Revoking Access / Cleanup
- Revoke user consent: https://myaccount.microsoft.com/consents (personal) or tenant admin portal
- Expire or delete the client secret (Certificates & secrets)
- Remove API permissions or delete the App registration entirely if no longer needed

---

## Security Notes
- Calendar Consolidator encrypts credentials in the SQLite DB using a per-host key at `.encryption_key`
- Files like `.encryption_key` and `*.db` are ignored by git
- Validate storage with `0-docs/SSJ-Tests/CREDENTIAL_SECURITY_TEST.md`

