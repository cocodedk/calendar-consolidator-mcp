"""
Google OAuth authentication - re-export from modular structure.
"""

from .google_auth import GoogleAuthenticator, CLIENT_ID, CLIENT_SECRET, SCOPES

__all__ = ['GoogleAuthenticator', 'CLIENT_ID', 'CLIENT_SECRET', 'SCOPES']
