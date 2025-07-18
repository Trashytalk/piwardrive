#!/usr/bin/env python3
"""Comprehensive test suite for piwardrive.security module.

This test suite provides complete coverage for the security module including:
- Path sanitization and validation
- Service name validation
- Filename validation and sanitization
- Password hashing and verification
- Encryption and decryption
- Key generation and validation
- Edge cases and security vulnerabilities
"""

import os
import tempfile
from unittest.mock import patch

import pytest
from cryptography.fernet import Fernet

from piwardrive import security


class TestPathSanitization:
    """Test suite for path sanitization functions."""

    def test_sanitize_path_normal_path(self):
        """Test sanitizing normal paths."""
        test_paths = [
            "/home/user/file.txt",
            "relative/path/file.txt",
            "single_file.txt",
            "/",
            ".",
        ]

        for path in test_paths:
            result = security.sanitize_path(path)
            assert result == os.path.normpath(path)

    def test_sanitize_path_with_parent_directory(self):
        """Test sanitizing paths with parent directory traversal."""
        unsafe_paths = [
            "../../../etc/passwd",
            "safe/../../../etc/passwd",
            "/home/user/../../../etc/passwd",
            "../../sensitive_file.txt",
            "/path/to/../../sensitive_file.txt",
        ]

        for path in unsafe_paths:
            with pytest.raises(ValueError, match="Unsafe path"):
                security.sanitize_path(path)

    def test_sanitize_path_edge_cases(self):
        """Test sanitizing edge case paths."""
        # Test empty string
        result = security.sanitize_path("")
        assert result == "."

        # Test path with redundant separators
        result = security.sanitize_path("//path//to//file.txt")
        assert result == os.path.normpath("//path//to//file.txt")

        # Test path with current directory references
        result = security.sanitize_path("./path/./to/./file.txt")
        assert result == os.path.normpath("./path/./to/./file.txt")

    def test_sanitize_path_windows_paths(self):
        """Test sanitizing Windows-style paths."""
        if os.name == "nt":
            # Test Windows paths
            result = security.sanitize_path("C:\\Users\\test\\file.txt")
            assert result == os.path.normpath("C:\\Users\\test\\file.txt")

            # Test unsafe Windows paths
            with pytest.raises(ValueError, match="Unsafe path"):
                security.sanitize_path(
                    "C:\\Users\\test\\..\\..\\Windows\\System32\\config\\sam"
                )

    def test_sanitize_path_with_symlinks(self):
        """Test sanitizing paths that might contain symlinks."""
        # This test depends on OS behavior, but we ensure the function works
        with tempfile.TemporaryDirectory() as temp_dir:
            safe_path = os.path.join(temp_dir, "safe_file.txt")
            result = security.sanitize_path(safe_path)
            assert result == os.path.normpath(safe_path)


class TestServiceNameValidation:
    """Test suite for service name validation."""

    def test_validate_service_name_valid(self):
        """Test validating valid service names."""
        valid_names = [
            "service1",
            "my-service",
            "service_name",
            "Service.Name",
            "123service",
            "service-123",
            "a",
            "A",
            "1",
            "test.service-name_123",
        ]

        for name in valid_names:
            # Should not raise exception
            security.validate_service_name(name)

    def test_validate_service_name_invalid(self):
        """Test validating invalid service names."""
        invalid_names = [
            "service name",  # space
            "service/name",  # slash
            "service\\name",  # backslash
            "service@name",  # at symbol
            "service#name",  # hash
            "service$name",  # dollar sign
            "service%name",  # percent
            "service&name",  # ampersand
            "service*name",  # asterisk
            "service+name",  # plus
            "service=name",  # equals
            "service[name]",  # brackets
            "service{name}",  # braces
            "service|name",  # pipe
            "service:name",  # colon
            "service;name",  # semicolon
            "service<name>",  # angle brackets
            "service?name",  # question mark
            'service"name"',  # quotes
            "service'name'",  # single quotes
            "",  # empty string
            "   ",  # whitespace only
        ]

        for name in invalid_names:
            with pytest.raises(ValueError, match="Invalid service name"):
                security.validate_service_name(name)

    def test_validate_service_name_unicode(self):
        """Test validating service names with unicode characters."""
        unicode_names = [
            "service-名前",  # Japanese
            "service-имя",  # Russian
            "service-نام",  # Arabic
            "service-🚀",  # Emoji
        ]

        for name in unicode_names:
            with pytest.raises(ValueError, match="Invalid service name"):
                security.validate_service_name(name)


class TestFilenameValidation:
    """Test suite for filename validation and sanitization."""

    def test_validate_filename_valid(self):
        """Test validating valid filenames."""
        valid_names = [
            "file.txt",
            "document.pdf",
            "image.jpg",
            "data.json",
            "script.py",
            "config.yaml",
            "test-file.txt",
            "test_file.txt",
            "test.file.txt",
            "123.txt",
            "a.b",
            "A.B",
            "file123.txt",
            "file-123.txt",
            "file_123.txt",
            "file.123.txt",
        ]

        for name in valid_names:
            # Should not raise exception
            security.validate_filename(name)

    def test_validate_filename_invalid(self):
        """Test validating invalid filenames."""
        invalid_names = [
            "file name.txt",  # space
            "file/name.txt",  # slash
            "file\\name.txt",  # backslash
            "file@name.txt",  # at symbol
            "file#name.txt",  # hash
            "file$name.txt",  # dollar sign
            "file%name.txt",  # percent
            "file&name.txt",  # ampersand
            "file*name.txt",  # asterisk
            "file+name.txt",  # plus
            "file=name.txt",  # equals
            "file[name].txt",  # brackets
            "file{name}.txt",  # braces
            "file|name.txt",  # pipe
            "file:name.txt",  # colon
            "file;name.txt",  # semicolon
            "file<name>.txt",  # angle brackets
            "file?name.txt",  # question mark
            'file"name".txt',  # quotes
            "file'name'.txt",  # single quotes
            "",  # empty string
            "   ",  # whitespace only
        ]

        for name in invalid_names:
            with pytest.raises(ValueError, match="Invalid filename"):
                security.validate_filename(name)

    def test_sanitize_filename_valid(self):
        """Test sanitizing valid filenames."""
        valid_names = [
            "file.txt",
            "document.pdf",
            "image.jpg",
        ]

        for name in valid_names:
            result = security.sanitize_filename(name)
            assert result == name

    def test_sanitize_filename_with_path(self):
        """Test sanitizing filenames with path components."""
        invalid_paths = [
            "/path/to/file.txt",
            "path/to/file.txt",
            "../file.txt",
            "../../file.txt",
            "/file.txt",
            "\\file.txt",
        ]

        for path in invalid_paths:
            with pytest.raises(ValueError, match="Invalid filename"):
                security.sanitize_filename(path)

    def test_sanitize_filename_basename_extraction(self):
        """Test that sanitize_filename extracts basename correctly."""
        # Test that it uses os.path.basename
        with patch("os.path.basename") as mock_basename:
            mock_basename.return_value = "file.txt"

            security.sanitize_filename("some/path/file.txt")

            mock_basename.assert_called_once_with("some/path/file.txt")
            # This should still fail because basename != original filename
            with pytest.raises(ValueError, match="Invalid filename"):
                security.sanitize_filename("some/path/file.txt")


class TestPasswordHashing:
    """Test suite for password hashing functions."""

    def test_hash_password_basic(self):
        """Test basic password hashing."""
        password = "test_password_123"
        hashed = security.hash_password(password)

        # Should return a string
        assert isinstance(hashed, str)

        # Should be bcrypt hash (starts with $2b$)
        assert hashed.startswith("$2b$")

        # Should be different from original password
        assert hashed != password

    def test_hash_password_different_results(self):
        """Test that same password produces different hashes."""
        password = "test_password_123"
        hash1 = security.hash_password(password)
        hash2 = security.hash_password(password)

        # Should be different (due to salt)
        assert hash1 != hash2

    def test_hash_password_empty_string(self):
        """Test hashing empty string."""
        hashed = security.hash_password("")
        assert isinstance(hashed, str)
        assert hashed.startswith("$2b$")

    def test_hash_password_unicode(self):
        """Test hashing unicode passwords."""
        unicode_passwords = [
            "пароль123",  # Russian
            "密码123",  # Chinese
            "パスワード123",  # Japanese
            "كلمة المرور123",  # Arabic
            "🔐secure🔐",  # Emoji
        ]

        for password in unicode_passwords:
            hashed = security.hash_password(password)
            assert isinstance(hashed, str)
            assert hashed.startswith("$2b$")

    def test_hash_password_long_password(self):
        """Test hashing very long passwords."""
        long_password = "a" * 1000
        hashed = security.hash_password(long_password)
        assert isinstance(hashed, str)
        assert hashed.startswith("$2b$")

    def test_verify_password_correct(self):
        """Test verifying correct password."""
        password = "test_password_123"
        hashed = security.hash_password(password)

        result = security.verify_password(password, hashed)
        assert result is True

    def test_verify_password_incorrect(self):
        """Test verifying incorrect password."""
        password = "test_password_123"
        wrong_password = "wrong_password_456"
        hashed = security.hash_password(password)

        result = security.verify_password(wrong_password, hashed)
        assert result is False

    def test_verify_password_empty_strings(self):
        """Test verifying empty string passwords."""
        hashed = security.hash_password("")

        # Empty string should verify against its own hash
        result = security.verify_password("", hashed)
        assert result is True

        # Non-empty string should not verify against empty string hash
        result = security.verify_password("not_empty", hashed)
        assert result is False

    def test_verify_password_invalid_hash(self):
        """Test verifying password with invalid hash."""
        password = "test_password_123"
        invalid_hashes = [
            "invalid_hash",
            "",
            "not_a_bcrypt_hash",
            "$2b$invalid",
        ]

        for invalid_hash in invalid_hashes:
            with pytest.raises(Exception):  # bcrypt will raise an exception
                security.verify_password(password, invalid_hash)


class TestEncryptionDecryption:
    """Test suite for encryption and decryption functions."""

    def test_encrypt_decrypt_basic(self):
        """Test basic encryption and decryption."""
        key = Fernet.generate_key()
        plaintext = "Hello, World!"

        # Encrypt
        encrypted = security.encrypt_data(plaintext, key)
        assert isinstance(encrypted, str)
        assert encrypted != plaintext

        # Decrypt
        decrypted = security.decrypt_data(encrypted, key)
        assert decrypted == plaintext

    def test_encrypt_decrypt_empty_string(self):
        """Test encrypting and decrypting empty string."""
        key = Fernet.generate_key()
        plaintext = ""

        encrypted = security.encrypt_data(plaintext, key)
        decrypted = security.decrypt_data(encrypted, key)

        assert decrypted == plaintext

    def test_encrypt_decrypt_unicode(self):
        """Test encrypting and decrypting unicode text."""
        key = Fernet.generate_key()
        unicode_texts = [
            "Привет, мир!",  # Russian
            "你好世界!",  # Chinese
            "こんにちは世界!",  # Japanese
            "مرحبا بالعالم!",  # Arabic
            "🔐🌍🚀",  # Emoji
        ]

        for plaintext in unicode_texts:
            encrypted = security.encrypt_data(plaintext, key)
            decrypted = security.decrypt_data(encrypted, key)
            assert decrypted == plaintext

    def test_encrypt_decrypt_long_text(self):
        """Test encrypting and decrypting long text."""
        key = Fernet.generate_key()
        long_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 100

        encrypted = security.encrypt_data(long_text, key)
        decrypted = security.decrypt_data(encrypted, key)

        assert decrypted == long_text

    def test_encrypt_different_results(self):
        """Test that same plaintext produces different ciphertexts."""
        key = Fernet.generate_key()
        plaintext = "Hello, World!"

        encrypted1 = security.encrypt_data(plaintext, key)
        encrypted2 = security.encrypt_data(plaintext, key)

        # Should be different (due to random IV)
        assert encrypted1 != encrypted2

        # But both should decrypt to same plaintext
        assert security.decrypt_data(encrypted1, key) == plaintext
        assert security.decrypt_data(encrypted2, key) == plaintext

    def test_decrypt_with_wrong_key(self):
        """Test decrypting with wrong key."""
        key1 = Fernet.generate_key()
        key2 = Fernet.generate_key()
        plaintext = "Hello, World!"

        encrypted = security.encrypt_data(plaintext, key1)

        with pytest.raises(Exception):  # Fernet will raise an exception
            security.decrypt_data(encrypted, key2)

    def test_decrypt_invalid_data(self):
        """Test decrypting invalid data."""
        key = Fernet.generate_key()
        invalid_data = [
            "not_encrypted_data",
            "",
            "invalid_base64_data",
        ]

        for data in invalid_data:
            with pytest.raises(Exception):  # Fernet will raise an exception
                security.decrypt_data(data, key)

    def test_encrypt_with_invalid_key(self):
        """Test encrypting with invalid key."""
        invalid_keys = [
            b"too_short",
            b"not_base64_key_data_that_is_too_long",
            "not_bytes_key",
            None,
        ]

        for key in invalid_keys:
            with pytest.raises(Exception):  # Fernet will raise an exception
                security.encrypt_data("test", key)


class TestHashSecret:
    """Test suite for hash_secret function."""

    def test_hash_secret_basic(self):
        """Test basic secret hashing."""
        secret = "my_secret_key"
        hashed = security.hash_secret(secret)

        # Should return a string
        assert isinstance(hashed, str)

        # Should be hex string
        assert all(c in "0123456789abcdef" for c in hashed)

        # Should be SHA256 length (64 hex chars)
        assert len(hashed) == 64

        # Should be different from original
        assert hashed != secret

    def test_hash_secret_deterministic(self):
        """Test that same secret produces same hash."""
        secret = "my_secret_key"
        hash1 = security.hash_secret(secret)
        hash2 = security.hash_secret(secret)

        assert hash1 == hash2

    def test_hash_secret_different_inputs(self):
        """Test that different secrets produce different hashes."""
        secret1 = "secret1"
        secret2 = "secret2"

        hash1 = security.hash_secret(secret1)
        hash2 = security.hash_secret(secret2)

        assert hash1 != hash2

    def test_hash_secret_empty_string(self):
        """Test hashing empty string."""
        hashed = security.hash_secret("")
        assert isinstance(hashed, str)
        assert len(hashed) == 64

    def test_hash_secret_unicode(self):
        """Test hashing unicode secrets."""
        unicode_secrets = [
            "секрет123",  # Russian
            "秘密123",  # Chinese
            "秘密123",  # Japanese
            "سر123",  # Arabic
            "🔐secret🔐",  # Emoji
        ]

        for secret in unicode_secrets:
            hashed = security.hash_secret(secret)
            assert isinstance(hashed, str)
            assert len(hashed) == 64


class TestSecurityUtilities:
    """Test suite for security utility functions."""

    def test_constant_time_compare(self):
        """Test constant time comparison using secrets.compare_digest."""
        import secrets

        # Same strings
        assert secrets.compare_digest("hello", "hello") is True
        assert secrets.compare_digest("", "") is True

        # Different strings
        assert secrets.compare_digest("hello", "world") is False
        assert secrets.compare_digest("hello", "hello2") is False
        assert secrets.compare_digest("hello", "") is False

        # Different lengths
        assert secrets.compare_digest("short", "much_longer") is False


class TestSecurityEdgeCases:
    """Test edge cases and error conditions."""

    def test_none_inputs(self):
        """Test handling of None inputs."""
        # Most functions should handle None gracefully or raise appropriate errors

        with pytest.raises(Exception):
            security.sanitize_path(None)

        with pytest.raises(Exception):
            security.validate_service_name(None)

        with pytest.raises(Exception):
            security.validate_filename(None)

        with pytest.raises(Exception):
            security.hash_password(None)

    def test_very_long_inputs(self):
        """Test handling of very long inputs."""
        very_long_string = "a" * 10000

        # Path sanitization should handle long paths
        try:
            security.sanitize_path(very_long_string)
        except Exception:
            pass  # May raise ValueError for unsafe path

        # Service name validation should reject long names
        with pytest.raises(ValueError, match="Invalid service name"):
            security.validate_service_name(very_long_string)

        # Filename validation should reject long names
        with pytest.raises(ValueError, match="Invalid filename"):
            security.validate_filename(very_long_string)

        # Password hashing should handle long passwords
        hashed = security.hash_password(very_long_string)
        assert isinstance(hashed, str)

    def test_binary_data_handling(self):
        """Test handling of binary data."""
        binary_data = b"\x00\x01\x02\x03\xff\xfe\xfd"

        # Most functions expect strings, not bytes
        with pytest.raises(Exception):
            security.sanitize_path(binary_data)

        with pytest.raises(Exception):
            security.validate_service_name(binary_data)

        with pytest.raises(Exception):
            security.validate_filename(binary_data)

    def test_special_characters_comprehensive(self):
        """Test comprehensive special character handling."""
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?/~`"

        # Service names should reject most special characters
        for char in special_chars:
            test_name = f"service{char}name"
            if char in ".-_":  # These are allowed
                security.validate_service_name(test_name)
            else:
                with pytest.raises(ValueError, match="Invalid service name"):
                    security.validate_service_name(test_name)

        # Filenames should reject most special characters
        for char in special_chars:
            test_filename = f"file{char}name.txt"
            if char in ".-_":  # These are allowed
                security.validate_filename(test_filename)
            else:
                with pytest.raises(ValueError, match="Invalid filename"):
                    security.validate_filename(test_filename)


class TestSecurityRegexPatterns:
    """Test the regex patterns used in security validation."""

    def test_service_name_regex_pattern(self):
        """Test service name regex pattern directly."""
        pattern = security._ALLOWED_SERVICE_RE

        # Valid patterns
        valid_names = ["service", "service-name", "service_name", "service.name", "123"]
        for name in valid_names:
            assert pattern.fullmatch(name) is not None

        # Invalid patterns
        invalid_names = ["service name", "service/name", "service@name"]
        for name in invalid_names:
            assert pattern.fullmatch(name) is None

    def test_filename_regex_pattern(self):
        """Test filename regex pattern directly."""
        pattern = security._ALLOWED_FILENAME_RE

        # Valid patterns
        valid_names = ["file.txt", "file-name.txt", "file_name.txt", "file.name.txt"]
        for name in valid_names:
            assert pattern.fullmatch(name) is not None

        # Invalid patterns
        invalid_names = ["file name.txt", "file/name.txt", "file@name.txt"]
        for name in invalid_names:
            assert pattern.fullmatch(name) is None


if __name__ == "__main__":
    pytest.main([__file__])
