"""
Google OAuth authentication module - barrel exports.
"""

from .authenticator import GoogleAuthenticator
from .config import CLIENT_ID, CLIENT_SECRET, SCOPES

__all__ = ['GoogleAuthenticator', 'CLIENT_ID', 'CLIENT_SECRET', 'SCOPES']

