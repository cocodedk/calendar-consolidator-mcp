"""
Tests for iCloud authenticator.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from python.connectors.icloud_auth.authenticator import ICloudAuthenticator


class TestICloudAuthenticator:
    """Test iCloud authentication functionality."""

    def test_init(self):
        """Test authenticator initialization."""
        auth = ICloudAuthenticator()
        assert auth.caldav_url == "https://caldav.icloud.com/"

    def test_init_custom_url(self):
        """Test authenticator with custom CalDAV URL."""
        custom_url = "https://custom.caldav.com/"
        auth = ICloudAuthenticator(caldav_url=custom_url)
        assert auth.caldav_url == custom_url

    @patch('python.connectors.icloud_auth.authenticator.caldav.DAVClient')
    def test_validate_credentials_success(self, mock_client_class):
        """Test successful credential validation."""
        # Setup mock
        mock_client = Mock()
        mock_principal = Mock()
        mock_principal.url = "https://caldav.icloud.com/123456/principal/"
        mock_client.principal.return_value = mock_principal
        mock_client_class.return_value = mock_client

        # Test
        auth = ICloudAuthenticator()
        result = auth.validate_credentials(
            "test@icloud.com",
            "abcd-efgh-ijkl-mnop"
        )

        # Assert
        assert result['username'] == "test@icloud.com"
        assert result['password'] == "abcd-efgh-ijkl-mnop"
        assert result['caldav_url'] == "https://caldav.icloud.com/"
        assert 'principal_url' in result

    @patch('python.connectors.icloud_auth.authenticator.caldav.DAVClient')
    def test_validate_credentials_auth_error(self, mock_client_class):
        """Test credential validation with authorization error."""
        # Setup mock to raise auth error
        mock_client = Mock()
        mock_client.principal.side_effect = Exception("Authorization failed")
        mock_client_class.return_value = mock_client

        # Test
        auth = ICloudAuthenticator()
        with pytest.raises(Exception) as exc_info:
            auth.validate_credentials("bad@icloud.com", "wrong-password")

        assert "Failed to connect" in str(exc_info.value)

    @patch('python.connectors.icloud_auth.authenticator.caldav.DAVClient')
    def test_get_credentials_dict(self, mock_client_class):
        """Test getting credentials dictionary."""
        # Setup mock
        mock_client = Mock()
        mock_principal = Mock()
        mock_principal.url = "https://caldav.icloud.com/123456/principal/"
        mock_client.principal.return_value = mock_principal
        mock_client_class.return_value = mock_client

        # Test
        auth = ICloudAuthenticator()
        result = auth.get_credentials_dict(
            "test@icloud.com",
            "abcd-efgh-ijkl-mnop"
        )

        # Assert
        assert result['type'] == 'icloud'
        assert result['username'] == "test@icloud.com"
        assert result['password'] == "abcd-efgh-ijkl-mnop"
        assert result['caldav_url'] == "https://caldav.icloud.com/"
