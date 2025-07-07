"""Tests for cache.py and security.py modules."""

import hashlib
import base64
import unittest
from unittest.mock import AsyncMock, patch

import pytest
from cryptography.fernet import Fernet

from src.piwardrive.cache import RedisCache
from src.piwardrive.security import (
    hash_password, 
    verify_password, 
    sanitize_path,
    validate_service_name,
    validate_filename,
    sanitize_filename,
    encrypt_data,
    decrypt_data,
    hash_secret
)


class TestRedisCache(unittest.TestCase):
    """Test RedisCache class."""

    def setUp(self):
        """Set up test fixtures."""
        self.cache = RedisCache(prefix="test")

    def test_cache_creation(self):
        """Test RedisCache creation."""
        self.assertEqual(self.cache._prefix, "test")

    def test_cache_key_generation(self):
        """Test cache key generation."""
        key = self.cache._key("test_key")
        self.assertEqual(key, "test:test_key")

    @patch('src.piwardrive.cache._get_redis_client')
    def test_cache_get_success(self, mock_get_client):
        """Test successful cache get."""
        mock_client = AsyncMock()
        mock_client.get.return_value = '{"test": "value"}'
        mock_get_client.return_value = mock_client
        
        # Run the async test
        import asyncio
        async def run_test():
            result = await self.cache.get("test_key")
            self.assertEqual(result, {"test": "value"})
            mock_client.get.assert_called_once_with("test:test_key")
        
        asyncio.run(run_test())

    @patch('src.piwardrive.cache._get_redis_client')
    def test_cache_get_no_client(self, mock_get_client):
        """Test cache get when no client available."""
        mock_get_client.return_value = None
        
        import asyncio
        async def run_test():
            result = await self.cache.get("test_key")
            self.assertIsNone(result)
        
        asyncio.run(run_test())

    @patch('src.piwardrive.cache._get_redis_client')
    def test_cache_set_success(self, mock_get_client):
        """Test successful cache set."""
        mock_client = AsyncMock()
        mock_get_client.return_value = mock_client
        
        import asyncio
        async def run_test():
            await self.cache.set("test_key", {"test": "value"})
            mock_client.set.assert_called_once_with("test:test_key", '{"test": "value"}', ex=None)
        
        asyncio.run(run_test())

    @patch('src.piwardrive.cache._get_redis_client')
    def test_cache_clear(self, mock_get_client):
        """Test cache clear."""
        mock_client = AsyncMock()
        mock_client.keys.return_value = ["test:key1", "test:key2"]
        mock_get_client.return_value = mock_client
        
        import asyncio
        async def run_test():
            await self.cache.clear()
            mock_client.keys.assert_called_once_with("test:*")
            mock_client.delete.assert_called_once_with("test:key1", "test:key2")
        
        asyncio.run(run_test())


class TestSecurity(unittest.TestCase):
    """Test security functions."""

    def test_hash_password(self):
        """Test password hashing."""
        password = "test_password123"
        hashed = hash_password(password)
        
        self.assertIsInstance(hashed, str)
        self.assertNotEqual(hashed, password)
        self.assertTrue(hashed.startswith("$2"))  # bcrypt format

    def test_verify_password_correct(self):
        """Test password verification with correct password."""
        password = "test_password123"
        hashed = hash_password(password)
        
        result = verify_password(password, hashed)
        self.assertTrue(result)

    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password."""
        password = "test_password123"
        hashed = hash_password(password)
        
        result = verify_password("wrong_password", hashed)
        self.assertFalse(result)

    def test_verify_password_legacy_pbkdf2(self):
        """Test password verification with legacy PBKDF2 hash."""
        password = "test_password123"
        
        # Create a legacy PBKDF2 hash
        salt = b"test_salt_16_chr"
        digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
        legacy_hash = base64.b64encode(salt + digest).decode()
        
        result = verify_password(password, legacy_hash)
        self.assertTrue(result)

    def test_sanitize_path_valid(self):
        """Test path sanitization with valid path."""
        path = "/valid/path/to/file"
        result = sanitize_path(path)
        
        self.assertEqual(result, path)

    def test_sanitize_path_unsafe(self):
        """Test path sanitization with unsafe path."""
        # This path would be normalized to /etc/passwd which doesn't contain ".."
        # Let's use a path that would still contain ".." after normalization
        path = "../../etc/passwd"
        
        with self.assertRaises(ValueError):
            sanitize_path(path)

    def test_validate_service_name_valid(self):
        """Test service name validation with valid name."""
        valid_names = ["valid_service", "service-name", "service.name"]
        
        for name in valid_names:
            validate_service_name(name)  # Should not raise

    def test_validate_service_name_invalid(self):
        """Test service name validation with invalid name."""
        invalid_names = ["invalid service", "service@name"]
        
        for name in invalid_names:
            with self.assertRaises(ValueError):
                validate_service_name(name)

    def test_validate_filename_valid(self):
        """Test filename validation with valid filename."""
        valid_filenames = ["valid_file.txt", "file-name.log"]
        
        for filename in valid_filenames:
            validate_filename(filename)  # Should not raise

    def test_validate_filename_invalid(self):
        """Test filename validation with invalid filename."""
        invalid_filenames = ["invalid file.txt", "file@name.log"]
        
        for filename in invalid_filenames:
            with self.assertRaises(ValueError):
                validate_filename(filename)

    def test_sanitize_filename_valid(self):
        """Test filename sanitization with valid filename."""
        filename = "valid_file.txt"
        result = sanitize_filename(filename)
        
        self.assertEqual(result, filename)

    def test_sanitize_filename_with_path(self):
        """Test filename sanitization with path components."""
        filename = "/path/to/file.txt"
        
        with self.assertRaises(ValueError):
            sanitize_filename(filename)

    def test_encrypt_decrypt_data(self):
        """Test data encryption and decryption."""
        original_data = "sensitive_data_123"
        key = Fernet.generate_key()
        
        encrypted = encrypt_data(original_data, key)
        decrypted = decrypt_data(encrypted, key)
        
        self.assertNotEqual(encrypted, original_data)
        self.assertEqual(decrypted, original_data)

    def test_hash_secret(self):
        """Test secret hashing."""
        secret = "my_secret_key"
        hashed = hash_secret(secret)
        
        self.assertIsInstance(hashed, str)
        self.assertEqual(len(hashed), 64)  # SHA256 hex digest length
        self.assertNotEqual(hashed, secret)

    def test_hash_secret_consistency(self):
        """Test that hashing produces consistent results."""
        secret = "consistent_secret"
        
        hash1 = hash_secret(secret)
        hash2 = hash_secret(secret)
        
        self.assertEqual(hash1, hash2)


if __name__ == "__main__":
    unittest.main()
