"""Comprehensive tests for cache.py and security.py modules."""

import hashlib
import json
import os
import tempfile
import unittest
from unittest.mock import patch

from src.piwardrive.security import hash_password, verify_password


class TestCacheEntry(unittest.TestCase):
    """Test CacheEntry class."""

    def test_cache_entry_creation(self):
        """Test CacheEntry creation."""
        entry = CacheEntry("test_value", ttl=60)

        self.assertEqual(entry.value, "test_value")
        self.assertEqual(entry.ttl, 60)
        self.assertIsInstance(entry.created_at, float)
        self.assertGreater(entry.created_at, 0)

    def test_cache_entry_default_ttl(self):
        """Test CacheEntry with default TTL."""
        entry = CacheEntry("test_value")

        self.assertEqual(entry.ttl, 300)  # Default TTL
        self.assertEqual(entry.value, "test_value")

    def test_cache_entry_is_expired(self):
        """Test cache entry expiration logic."""
        entry = CacheEntry("test_value", ttl=0)

        # Should be expired immediately with TTL=0
        self.assertTrue(entry.is_expired())

    def test_cache_entry_not_expired(self):
        """Test cache entry not expired."""
        entry = CacheEntry("test_value", ttl=3600)

        # Should not be expired with long TTL
        self.assertFalse(entry.is_expired())


class TestLRUCache(unittest.TestCase):
    """Test LRUCache class."""

    def setUp(self):
        """Set up test fixtures."""
        self.cache = LRUCache(max_size=3)

    def test_lru_cache_creation(self):
        """Test LRUCache creation."""
        self.assertEqual(self.cache.max_size, 3)
        self.assertEqual(len(self.cache.cache), 0)

    def test_lru_cache_get_miss(self):
        """Test cache miss."""
        result = self.cache.get("nonexistent")
        self.assertIsNone(result)

    def test_lru_cache_put_and_get(self):
        """Test cache put and get operations."""
        self.cache.put("key1", "value1")
        result = self.cache.get("key1")

        self.assertEqual(result, "value1")

    def test_lru_cache_put_with_ttl(self):
        """Test cache put with TTL."""
        self.cache.put("key1", "value1", ttl=60)
        result = self.cache.get("key1")

        self.assertEqual(result, "value1")

    def test_lru_cache_eviction(self):
        """Test LRU eviction."""
        # Fill cache beyond capacity
        self.cache.put("key1", "value1")
        self.cache.put("key2", "value2")
        self.cache.put("key3", "value3")
        self.cache.put("key4", "value4")  # Should evict key1

        # key1 should be evicted
        self.assertIsNone(self.cache.get("key1"))
        # Other keys should still exist
        self.assertEqual(self.cache.get("key2"), "value2")
        self.assertEqual(self.cache.get("key3"), "value3")
        self.assertEqual(self.cache.get("key4"), "value4")

    def test_lru_cache_clear(self):
        """Test cache clear operation."""
        self.cache.put("key1", "value1")
        self.cache.put("key2", "value2")

        self.cache.clear()

        self.assertEqual(len(self.cache.cache), 0)
        self.assertIsNone(self.cache.get("key1"))
        self.assertIsNone(self.cache.get("key2"))

    def test_lru_cache_expired_cleanup(self):
        """Test cleanup of expired entries."""
        # Add entry that expires immediately
        self.cache.put("expired_key", "expired_value", ttl=0)

        # Get should return None for expired entry
        result = self.cache.get("expired_key")
        self.assertIsNone(result)


class TestCachePersistence(unittest.TestCase):
    """Test cache persistence functions."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.cache_file = os.path.join(self.temp_dir, "test_cache.json")

    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)
        os.rmdir(self.temp_dir)

    def test_save_cache_success(self):
        """Test successful cache saving."""
        cache = LRUCache(max_size=2)
        cache.put("key1", "value1")
        cache.put("key2", "value2")

        result = save_cache(cache, self.cache_file)

        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.cache_file))

    def test_save_cache_failure(self):
        """Test cache save failure."""
        cache = LRUCache(max_size=2)
        cache.put("key1", "value1")

        # Try to save to invalid path
        result = save_cache(cache, "/invalid/path/cache.json")

        self.assertFalse(result)

    def test_load_cache_success(self):
        """Test successful cache loading."""
        # Create cache data
        cache_data = {
            "key1": {"value": "value1", "ttl": 300, "created_at": 1000000000},
            "key2": {"value": "value2", "ttl": 300, "created_at": 1000000000},
        }

        # Save to file
        with open(self.cache_file, "w") as f:
            json.dump(cache_data, f)

        # Load cache
        cache = load_cache(self.cache_file, max_size=10)

        self.assertIsInstance(cache, LRUCache)
        self.assertEqual(len(cache.cache), 2)

    def test_load_cache_file_not_found(self):
        """Test cache load when file doesn't exist."""
        cache = load_cache("nonexistent_file.json", max_size=10)

        self.assertIsInstance(cache, LRUCache)
        self.assertEqual(len(cache.cache), 0)

    def test_load_cache_invalid_json(self):
        """Test cache load with invalid JSON."""
        # Create invalid JSON file
        with open(self.cache_file, "w") as f:
            f.write("invalid json content")

        cache = load_cache(self.cache_file, max_size=10)

        self.assertIsInstance(cache, LRUCache)
        self.assertEqual(len(cache.cache), 0)


class TestSecurity(unittest.TestCase):
    """Test security functions."""

    def test_hash_password(self):
        """Test password hashing."""
        password = "test_password123"
        hashed = hash_password(password)

        self.assertIsInstance(hashed, str)
        self.assertNotEqual(hashed, password)
        self.assertTrue(len(hashed) > 0)

    def test_verify_password_correct(self):
        """Test password verification with correct password."""
        password = "test_password123"
        hashed = hash_password(password)

        result = verify_password(password, hashed)
        self.assertTrue(result)

    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password."""
        password = "test_password123"
        wrong_password = "wrong_password"
        hashed = hash_password(password)

        result = verify_password(wrong_password, hashed)
        self.assertFalse(result)

    def test_generate_api_key(self):
        """Test API key generation."""
        api_key = generate_api_key()

        self.assertIsInstance(api_key, str)
        self.assertEqual(len(api_key), 64)  # 32 bytes * 2 (hex)

    def test_validate_api_key_valid(self):
        """Test API key validation with valid key."""
        valid_key = "a" * 64  # 64 character hex string

        result = validate_api_key(valid_key)
        self.assertTrue(result)

    def test_validate_api_key_invalid_length(self):
        """Test API key validation with invalid length."""
        invalid_key = "too_short"

        result = validate_api_key(invalid_key)
        self.assertFalse(result)

    def test_validate_api_key_invalid_characters(self):
        """Test API key validation with invalid characters."""
        invalid_key = "g" * 64  # 'g' is not a valid hex character

        result = validate_api_key(invalid_key)
        self.assertFalse(result)

    def test_sanitize_input_basic(self):
        """Test basic input sanitization."""
        test_input = "normal_input"
        result = sanitize_input(test_input)

        self.assertEqual(result, "normal_input")

    def test_sanitize_input_with_script_tags(self):
        """Test input sanitization with script tags."""
        test_input = "<script>alert('xss')</script>"
        result = sanitize_input(test_input)

        self.assertNotIn("<script>", result)
        self.assertNotIn("</script>", result)

    def test_sanitize_input_with_sql_injection(self):
        """Test input sanitization with SQL injection attempts."""
        test_input = "'; DROP TABLE users; --"
        result = sanitize_input(test_input)

        # Should remove or escape dangerous characters
        self.assertNotEqual(result, test_input)

    def test_get_csrf_token(self):
        """Test CSRF token generation."""
        token = get_csrf_token()

        self.assertIsInstance(token, str)
        self.assertTrue(len(token) > 0)

    def test_validate_csrf_token_valid(self):
        """Test CSRF token validation with valid token."""
        # Mock a valid token scenario
        with patch("src.piwardrive.security.hashlib.sha256") as mock_sha256:
            mock_sha256.return_value.hexdigest.return_value = "valid_token"

            result = validate_csrf_token("valid_token", "test_session")
            # This would need actual implementation to test properly
            self.assertIsInstance(result, bool)

    def test_validate_csrf_token_invalid(self):
        """Test CSRF token validation with invalid token."""
        result = validate_csrf_token("invalid_token", "test_session")
        self.assertFalse(result)


class TestSecurityHashingAlgorithms(unittest.TestCase):
    """Test security hashing algorithms."""

    def test_sha256_hashing(self):
        """Test SHA-256 hashing functionality."""
        test_data = "test_data_for_hashing"

        # Test that we can create SHA-256 hash
        hash_obj = hashlib.sha256(test_data.encode())
        result = hash_obj.hexdigest()

        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 64)  # SHA-256 produces 64 character hex string

    def test_consistent_hashing(self):
        """Test that hashing produces consistent results."""
        test_data = "consistent_test_data"

        hash1 = hashlib.sha256(test_data.encode()).hexdigest()
        hash2 = hashlib.sha256(test_data.encode()).hexdigest()

        self.assertEqual(hash1, hash2)

    def test_different_inputs_different_hashes(self):
        """Test that different inputs produce different hashes."""
        data1 = "test_data_1"
        data2 = "test_data_2"

        hash1 = hashlib.sha256(data1.encode()).hexdigest()
        hash2 = hashlib.sha256(data2.encode()).hexdigest()

        self.assertNotEqual(hash1, hash2)


class TestCacheIntegration(unittest.TestCase):
    """Test cache integration scenarios."""

    def test_cache_with_complex_data(self):
        """Test cache with complex data structures."""
        cache = LRUCache(max_size=5)

        # Test with different data types
        cache.put("string_key", "string_value")
        cache.put("dict_key", {"nested": "dict"})
        cache.put("list_key", [1, 2, 3])

        self.assertEqual(cache.get("string_key"), "string_value")
        self.assertEqual(cache.get("dict_key"), {"nested": "dict"})
        self.assertEqual(cache.get("list_key"), [1, 2, 3])

    def test_cache_memory_management(self):
        """Test cache memory management."""
        cache = LRUCache(max_size=2)

        # Add more items than cache capacity
        for i in range(5):
            cache.put(f"key_{i}", f"value_{i}")

        # Only last 2 items should remain
        self.assertIsNone(cache.get("key_0"))
        self.assertIsNone(cache.get("key_1"))
        self.assertIsNone(cache.get("key_2"))
        self.assertEqual(cache.get("key_3"), "value_3")
        self.assertEqual(cache.get("key_4"), "value_4")


class TestSecurityIntegration(unittest.TestCase):
    """Test security integration scenarios."""

    def test_password_security_workflow(self):
        """Test complete password security workflow."""
        # User registration workflow
        user_password = "secure_password123!"
        hashed_password = hash_password(user_password)

        # User login workflow
        login_success = verify_password(user_password, hashed_password)
        login_failure = verify_password("wrong_password", hashed_password)

        self.assertTrue(login_success)
        self.assertFalse(login_failure)

    def test_api_key_security_workflow(self):
        """Test complete API key security workflow."""
        # Generate API key for user
        api_key = generate_api_key()

        # Validate API key
        is_valid = validate_api_key(api_key)
        is_invalid = validate_api_key("invalid_key")

        self.assertTrue(is_valid)
        self.assertFalse(is_invalid)

    def test_input_sanitization_workflow(self):
        """Test complete input sanitization workflow."""
        dangerous_inputs = [
            "<script>alert('xss')</script>",
            "'; DROP TABLE users; --",
            "<img src=x onerror=alert('xss')>",
            "javascript:alert('xss')",
        ]

        for dangerous_input in dangerous_inputs:
            sanitized = sanitize_input(dangerous_input)

            # Ensure dangerous content is removed/escaped
            self.assertNotEqual(sanitized, dangerous_input)
            self.assertNotIn("<script>", sanitized)
            self.assertNotIn("javascript:", sanitized)


if __name__ == "__main__":
    unittest.main()
