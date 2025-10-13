/**
 * PUT credentials endpoint - saves encrypted credentials.
 */

import { execSync } from 'child_process';
import { validateCredentials } from './validate.js';

/**
 * Save credentials for a provider.
 */
function saveCredentials(provider, credentials) {
    try {
        const credsJson = JSON.stringify(credentials).replace(/"/g, '\\"');
        execSync(
            `python3 -c "from python.state.credentials_manager import save_credentials; import json; save_credentials('${provider}', json.loads('${credsJson}'))"`,
            { encoding: 'utf-8' }
        );
        return true;
    } catch (error) {
        console.error(`Error saving credentials for ${provider}:`, error.message);
        return false;
    }
}

/**
 * Handle PUT /api/credentials request.
 */
export async function handleUpdateCredentials(req, res) {
    try {
        const { provider, credentials } = req.body;

        // Validate provider
        if (!provider || !['google', 'microsoft', 'icloud'].includes(provider)) {
            return res.status(400).json({
                error: 'Invalid provider',
                message: 'Provider must be google, microsoft, or icloud'
            });
        }

        // Validate credentials format
        const validation = validateCredentials(provider, credentials);
        if (!validation.valid) {
            return res.status(400).json({
                error: 'Invalid credentials format',
                message: validation.error
            });
        }

        // Save encrypted credentials
        const success = saveCredentials(provider, credentials);
        if (!success) {
            return res.status(500).json({
                error: 'Failed to save credentials',
                message: 'Database or encryption error'
            });
        }

        res.json({
            success: true,
            message: `${provider} credentials updated successfully`
        });
    } catch (error) {
        console.error('Error updating credentials:', error);
        res.status(500).json({
            error: 'Failed to update credentials',
            message: error.message
        });
    }
}
