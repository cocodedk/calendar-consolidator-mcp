/**
 * API client for credentials endpoints.
 */

/**
 * Get all credentials (masked).
 */
export async function getCredentials() {
    try {
        const response = await fetch('/api/credentials');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching credentials:', error);
        throw error;
    }
}

/**
 * Update credentials for a provider.
 */
export async function updateCredentials(provider, credentials) {
    try {
        const response = await fetch('/api/credentials', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ provider, credentials })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Failed to update credentials');
        }

        return data;
    } catch (error) {
        console.error('Error updating credentials:', error);
        throw error;
    }
}
