/**
 * Validation functions for OAuth credentials.
 */

/**
 * Validate Google credentials format.
 */
function validateGoogleCredentials(creds) {
    if (!creds.client_id || !creds.client_secret) {
        return { valid: false, error: 'Missing client_id or client_secret' };
    }

    if (!creds.client_id.endsWith('.apps.googleusercontent.com')) {
        return {
            valid: false,
            error: 'Invalid Google client_id format'
        };
    }

    if (!creds.client_secret.startsWith('GOCSPX-')) {
        return {
            valid: false,
            error: 'Invalid Google client_secret format'
        };
    }

    return { valid: true };
}

/**
 * Validate Microsoft credentials format.
 */
function validateMicrosoftCredentials(creds) {
    if (!creds.client_id || !creds.client_secret || !creds.tenant_id) {
        return {
            valid: false,
            error: 'Missing client_id, client_secret, or tenant_id'
        };
    }

    // Basic GUID validation
    const guidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

    if (!guidRegex.test(creds.client_id) && creds.client_id !== 'common') {
        return {
            valid: false,
            error: 'Invalid Microsoft client_id format'
        };
    }

    if (!guidRegex.test(creds.tenant_id) && creds.tenant_id !== 'common') {
        return {
            valid: false,
            error: 'Invalid Microsoft tenant_id format'
        };
    }

    if (creds.client_secret.length < 8) {
        return {
            valid: false,
            error: 'Invalid Microsoft client_secret format'
        };
    }

    return { valid: true };
}

/**
 * Validate credentials based on provider.
 */
function validateCredentials(provider, credentials) {
    switch (provider) {
        case 'google':
            return validateGoogleCredentials(credentials);
        case 'microsoft':
            return validateMicrosoftCredentials(credentials);
        case 'icloud':
            // iCloud doesn't need app-level credentials
            return { valid: true };
        default:
            return { valid: false, error: `Unknown provider: ${provider}` };
    }
}

export {
    validateCredentials,
    validateGoogleCredentials,
    validateMicrosoftCredentials
};
