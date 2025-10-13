/**
 * API client module.
 * Handles communication with backend API.
 */

const API_BASE = '/api';

/**
 * Make API request.
 */
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const config = {
        headers: {
            'Content-Type': 'application/json',
            ...options.headers
        },
        ...options
    };

    try {
        const response = await fetch(url, config);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Request failed');
        }

        return data;
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

/**
 * Configuration API calls.
 */
const API = {
    async getConfig() {
        return apiRequest('/config');
    },

    async addSource(sourceData) {
        return apiRequest('/source', {
            method: 'POST',
            body: JSON.stringify(sourceData)
        });
    },

    async removeSource(sourceId) {
        return apiRequest(`/source/${sourceId}`, {
            method: 'DELETE'
        });
    },

    async setTarget(targetData) {
        return apiRequest('/target', {
            method: 'POST',
            body: JSON.stringify(targetData)
        });
    },

    async previewSync(sourceId = null) {
        return apiRequest('/preview', {
            method: 'POST',
            body: JSON.stringify({ sourceId })
        });
    },

    async executeSync(sourceId = null) {
        return apiRequest('/sync', {
            method: 'POST',
            body: JSON.stringify({ sourceId })
        });
    },

    async getLogs(limit = 50) {
        return apiRequest(`/logs?limit=${limit}`);
    },

    async getStatus() {
        return apiRequest('/status');
    },

    async updateSettings(settings) {
        return apiRequest('/settings', {
            method: 'POST',
            body: JSON.stringify(settings)
        });
    }
};

window.API = API;
