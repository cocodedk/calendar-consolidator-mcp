/**
 * iCloud credentials info component.
 */

export function createIcloudCredentialsInfo() {
    const info = document.createElement('div');
    info.className = 'credentials-info';

    info.innerHTML = `
        <h4>🍎 iCloud Calendar Setup</h4>
        <p class="help-text">
            iCloud doesn't require app-level OAuth credentials.
            Each user generates their own app-specific password when adding an iCloud source.
        </p>

        <div class="info-box">
            <h5>How it works:</h5>
            <ol>
                <li>Users enable Two-Factor Authentication on their Apple ID</li>
                <li>They generate an app-specific password at appleid.apple.com</li>
                <li>When adding an iCloud source, they enter their Apple ID and app-specific password</li>
            </ol>
        </div>

        <p class="help-text">
            <a href="#" class="help-link" onclick="window.showHelp('sources'); return false;">
                View detailed iCloud setup guide
            </a>
        </p>
    `;

    return info;
}
