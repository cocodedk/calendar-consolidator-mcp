/**
 * GET credentials endpoint - returns masked credentials.
 */

import { spawnSync } from 'child_process';
import { PYTHON_COMMAND, buildPythonEnv } from '../../python_bridge.js';

/**
 * Get masked credentials for a provider.
 */
function getMaskedCredentials(provider) {
    try {
        const pythonCode = [
            'from python.state.credentials_manager import get_masked_credentials',
            'import json, sys',
            'provider = sys.argv[1]',
            'result = get_masked_credentials(provider)',
            'print(json.dumps(result))'
        ].join('; ');

        const result = spawnSync(
            PYTHON_COMMAND,
            ['-c', pythonCode, provider],
            {
                encoding: 'utf-8',
                env: buildPythonEnv()
            }
        );

        if (result.error) {
            throw result.error;
        }

        if (result.status !== 0) {
            const stderr = result.stderr ? result.stderr.trim() : '';
            throw new Error(stderr || `Python exited with code ${result.status}`);
        }

        return JSON.parse(result.stdout.trim());
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
