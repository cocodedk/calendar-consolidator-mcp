/**
 * GET credentials endpoint - returns masked credentials.
 */

import { execSync } from 'child_process';

/**
 * Get masked credentials for a provider.
 */
function getMaskedCredentials(provider) {
    try {
        const result = execSync(
            `python3 -c "from python.state.credentials_manager import get_masked_credentials; import json; print(json.dumps(get_masked_credentials('${provider}')))"`,
            { encoding: 'utf-8' }
        );
        return JSON.parse(result.trim());
    } catch (error) {
        console.error(`Error getting credentials for ${provider}:`, error.message);
        return null;
    }
}

/**
 * Handle GET /api/credentials request.
 */
export async function handleGetCredentials(req, res) {
    try {
        const google = getMaskedCredentials('google');
        const microsoft = getMaskedCredentials('microsoft');

        const response = {
            google: google ? { ...google, configured: true } : { configured: false },
            microsoft: microsoft ? { ...microsoft, configured: true } : { configured: false },
            icloud: { configured: false }  // iCloud doesn't have app-level creds
        };

        res.json(response);
    } catch (error) {
        console.error('Error fetching credentials:', error);
        res.status(500).json({
            error: 'Failed to fetch credentials',
            message: error.message
        });
    }
}
