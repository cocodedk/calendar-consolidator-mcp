"""Encryption strength tests - modular structure."""

from .test_keyring_usage import (
    test_encryption_uses_keyring,
    test_encryption_key_is_random
)
from .test_data_storage import test_encrypted_data_not_plaintext
from .test_decryption import test_decryption_requires_correct_identifier
from .test_key_rotation import test_encryption_handles_key_rotation

__all__ = [
    'test_encryption_uses_keyring',
    'test_encryption_key_is_random',
    'test_encrypted_data_not_plaintext',
    'test_decryption_requires_correct_identifier',
    'test_encryption_handles_key_rotation'
]
