"""
Tests for security functions and authentication.
"""

import pytest
import os
import tempfile
from unittest.mock import Mock, patch, mock_open
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from piwardrive.security import (
    hash_password, verify_password, generate_token, verify_token,
    sanitize_path, validate_input, encrypt_data, decrypt_data,
    check_permissions, audit_log
)
from piwardrive.errors import SecurityError


class TestPasswordSecurity:
    """Test password hashing and verification."""

    def test_hash_password(self):
        """Test password hashing."""
        password = "test_password_123"
        hashed = hash_password(password)
        
        assert hashed is not None
        assert hashed != password
        assert len(hashed) > 20  # Should be a reasonable hash length

    def test_verify_password_correct(self):
        """Test password verification with correct password."""
        password = "test_password_123"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password."""
        password = "test_password_123"
        wrong_password = "wrong_password"
        hashed = hash_password(password)
        
        assert verify_password(wrong_password, hashed) is False

    def test_hash_empty_password(self):
        """Test hashing empty password."""
        with pytest.raises(ValueError):
            hash_password("")

    def test_hash_none_password(self):
        """Test hashing None password."""
        with pytest.raises((ValueError, TypeError)):
            hash_password(None)

    def test_password_strength_validation(self):
        """Test password strength validation."""
        # Weak passwords should be rejected
        weak_passwords = [
            "123",
            "password",
            "abc",
            "admin"
        ]
        
        for weak_pwd in weak_passwords:
            with pytest.raises(ValueError):
                hash_password(weak_pwd)

    def test_password_different_hashes(self):
        """Test that same password produces different hashes (salt)."""
        password = "test_password_123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        # Hashes should be different due to salt
        assert hash1 != hash2
        
        # But both should verify correctly
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True


class TestTokenSecurity:
    """Test token generation and verification."""

    def test_generate_token(self):
        """Test token generation."""
        token = generate_token()
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 10

    def test_verify_token_valid(self):
        """Test token verification with valid token."""
        token = generate_token()
        
        # Should verify immediately after generation
        assert verify_token(token) is True

    def test_verify_token_invalid(self):
        """Test token verification with invalid token."""
        invalid_token = "invalid_token_12345"
        
        assert verify_token(invalid_token) is False

    def test_token_expiration(self):
        """Test token expiration."""
        import time
        
        # Generate token with short expiration
        token = generate_token(expiration=0.1)  # 100ms
        
        # Should be valid immediately
        assert verify_token(token) is True
        
        # Wait for expiration
        time.sleep(0.2)
        
        # Should be invalid after expiration
        assert verify_token(token) is False

    def test_token_uniqueness(self):
        """Test that tokens are unique."""
        token1 = generate_token()
        token2 = generate_token()
        
        assert token1 != token2

    def test_token_payload(self):
        """Test token with payload."""
        payload = {"user_id": 123, "role": "admin"}
        token = generate_token(payload=payload)
        
        verified_payload = verify_token(token, return_payload=True)
        assert verified_payload is not None
        assert verified_payload["user_id"] == 123
        assert verified_payload["role"] == "admin"


class TestPathSecurity:
    """Test path sanitization and validation."""

    def test_sanitize_path_normal(self):
        """Test path sanitization with normal paths."""
        safe_paths = [
            "/var/log/piwardrive/app.log",
            "/home/user/documents/file.txt",
            "relative/path/file.txt"
        ]
        
        for path in safe_paths:
            sanitized = sanitize_path(path)
            assert sanitized == path

    def test_sanitize_path_traversal(self):
        """Test path sanitization with directory traversal attempts."""
        dangerous_paths = [
            "../../../etc/passwd",
            "/var/log/../../etc/shadow",
            "file.txt/../../../sensitive.txt"
        ]
        
        for path in dangerous_paths:
            with pytest.raises(SecurityError):
                sanitize_path(path)

    def test_sanitize_path_absolute_outside_allowed(self):
        """Test path sanitization with absolute paths outside allowed areas."""
        allowed_dirs = ["/var/log/piwardrive", "/tmp/piwardrive"]
        
        dangerous_paths = [
            "/etc/passwd",
            "/root/sensitive",
            "/var/log/system.log"
        ]
        
        for path in dangerous_paths:
            with pytest.raises(SecurityError):
                sanitize_path(path, allowed_dirs=allowed_dirs)

    def test_sanitize_path_null_bytes(self):
        """Test path sanitization with null bytes."""
        dangerous_path = "/var/log/app.log\x00../../../etc/passwd"
        
        with pytest.raises(SecurityError):
            sanitize_path(dangerous_path)

    def test_sanitize_path_symlink_attack(self):
        """Test path sanitization with symlink attacks."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a symlink to sensitive area
            symlink_path = os.path.join(temp_dir, "evil_symlink")
            try:
                os.symlink("/etc", symlink_path)
                
                # Should detect and reject symlink to unauthorized area
                target_path = os.path.join(symlink_path, "passwd")
                with pytest.raises(SecurityError):
                    sanitize_path(target_path, allowed_dirs=[temp_dir])
            except OSError:
                # Skip test if symlinks not supported
                pytest.skip("Symlinks not supported on this system")


class TestInputValidation:
    """Test input validation functions."""

    def test_validate_input_safe(self):
        """Test input validation with safe inputs."""
        safe_inputs = [
            "normal_string",
            "123456",
            "user@example.com",
            "file_name.txt"
        ]
        
        for input_str in safe_inputs:
            assert validate_input(input_str) is True

    def test_validate_input_dangerous(self):
        """Test input validation with dangerous inputs."""
        dangerous_inputs = [
            "<script>alert('xss')</script>",
            "'; DROP TABLE users; --",
            "$(rm -rf /)",
            "javascript:alert('xss')",
            "%3Cscript%3E"
        ]
        
        for input_str in dangerous_inputs:
            assert validate_input(input_str) is False

    def test_validate_input_sql_injection(self):
        """Test input validation against SQL injection."""
        sql_injection_attempts = [
            "1' OR '1'='1",
            "admin'--",
            "'; DELETE FROM users; --",
            "1; DROP TABLE sessions;"
        ]
        
        for attempt in sql_injection_attempts:
            assert validate_input(attempt) is False

    def test_validate_input_xss(self):
        """Test input validation against XSS."""
        xss_attempts = [
            "<script>alert('xss')</script>",
            "<img src=x onerror=alert('xss')>",
            "javascript:alert('xss')",
            "<iframe src='javascript:alert(1)'></iframe>"
        ]
        
        for attempt in xss_attempts:
            assert validate_input(attempt) is False

    def test_validate_input_command_injection(self):
        """Test input validation against command injection."""
        command_injection_attempts = [
            "; rm -rf /",
            "| cat /etc/passwd",
            "&& rm important_file",
            "`whoami`",
            "$(id)"
        ]
        
        for attempt in command_injection_attempts:
            assert validate_input(attempt) is False

    def test_validate_input_length_limits(self):
        """Test input validation with length limits."""
        # Very long input should be rejected
        long_input = "a" * 10000
        assert validate_input(long_input, max_length=1000) is False
        
        # Normal length should be accepted
        normal_input = "a" * 100
        assert validate_input(normal_input, max_length=1000) is True


class TestDataEncryption:
    """Test data encryption and decryption."""

    def test_encrypt_decrypt_string(self):
        """Test encrypting and decrypting strings."""
        original_data = "sensitive information"
        key = "test_encryption_key_32_chars!!"
        
        encrypted = encrypt_data(original_data, key)
        assert encrypted != original_data
        assert encrypted is not None
        
        decrypted = decrypt_data(encrypted, key)
        assert decrypted == original_data

    def test_encrypt_decrypt_json(self):
        """Test encrypting and decrypting JSON data."""
        original_data = {"user": "admin", "password": "secret123"}
        key = "test_encryption_key_32_chars!!"
        
        encrypted = encrypt_data(original_data, key)
        assert encrypted != original_data
        
        decrypted = decrypt_data(encrypted, key)
        assert decrypted == original_data

    def test_encrypt_wrong_key(self):
        """Test decryption with wrong key."""
        original_data = "sensitive information"
        key1 = "test_encryption_key_32_chars!!"
        key2 = "different_key_32_characters!!!"
        
        encrypted = encrypt_data(original_data, key1)
        
        with pytest.raises(SecurityError):
            decrypt_data(encrypted, key2)

    def test_encrypt_empty_data(self):
        """Test encrypting empty data."""
        key = "test_encryption_key_32_chars!!"
        
        encrypted = encrypt_data("", key)
        decrypted = decrypt_data(encrypted, key)
        
        assert decrypted == ""

    def test_encrypt_invalid_key(self):
        """Test encryption with invalid key."""
        data = "test data"
        
        with pytest.raises(ValueError):
            encrypt_data(data, "short_key")  # Too short
        
        with pytest.raises(ValueError):
            encrypt_data(data, None)


class TestPermissions:
    """Test permission checking functions."""

    def test_check_permissions_allowed(self):
        """Test permission checking for allowed operations."""
        user = {"role": "admin", "permissions": ["read", "write", "delete"]}
        
        assert check_permissions(user, "read") is True
        assert check_permissions(user, "write") is True
        assert check_permissions(user, "delete") is True

    def test_check_permissions_denied(self):
        """Test permission checking for denied operations."""
        user = {"role": "user", "permissions": ["read"]}
        
        assert check_permissions(user, "read") is True
        assert check_permissions(user, "write") is False
        assert check_permissions(user, "delete") is False

    def test_check_permissions_role_based(self):
        """Test role-based permission checking."""
        admin_user = {"role": "admin"}
        regular_user = {"role": "user"}
        guest_user = {"role": "guest"}
        
        # Admin should have all permissions
        assert check_permissions(admin_user, "admin_action") is True
        
        # Regular user should have limited permissions
        assert check_permissions(regular_user, "user_action") is True
        assert check_permissions(regular_user, "admin_action") is False
        
        # Guest should have minimal permissions
        assert check_permissions(guest_user, "read") is True
        assert check_permissions(guest_user, "write") is False

    def test_check_permissions_invalid_user(self):
        """Test permission checking with invalid user."""
        with pytest.raises(ValueError):
            check_permissions(None, "read")
        
        with pytest.raises(ValueError):
            check_permissions({}, "read")  # No role

    def test_check_permissions_resource_based(self):
        """Test resource-based permission checking."""
        user = {"role": "user", "user_id": 123}
        
        # User should be able to access their own resources
        assert check_permissions(user, "read", resource_owner=123) is True
        
        # User should not be able to access other's resources
        assert check_permissions(user, "read", resource_owner=456) is False


class TestAuditLogging:
    """Test audit logging functionality."""

    @patch('piwardrive.security.logger')
    def test_audit_log_success(self, mock_logger):
        """Test audit logging for successful operations."""
        user = {"user_id": 123, "username": "testuser"}
        action = "login"
        
        audit_log(user, action, success=True)
        
        mock_logger.info.assert_called_once()
        call_args = mock_logger.info.call_args[0][0]
        assert "login" in call_args
        assert "123" in call_args
        assert "SUCCESS" in call_args

    @patch('piwardrive.security.logger')
    def test_audit_log_failure(self, mock_logger):
        """Test audit logging for failed operations."""
        user = {"user_id": 123, "username": "testuser"}
        action = "delete_file"
        
        audit_log(user, action, success=False, details="Permission denied")
        
        mock_logger.warning.assert_called_once()
        call_args = mock_logger.warning.call_args[0][0]
        assert "delete_file" in call_args
        assert "123" in call_args
        assert "FAILED" in call_args
        assert "Permission denied" in call_args

    @patch('piwardrive.security.logger')
    def test_audit_log_with_ip(self, mock_logger):
        """Test audit logging with IP address."""
        user = {"user_id": 123, "username": "testuser"}
        action = "api_access"
        ip_address = "192.168.1.100"
        
        audit_log(user, action, success=True, ip_address=ip_address)
        
        mock_logger.info.assert_called_once()
        call_args = mock_logger.info.call_args[0][0]
        assert ip_address in call_args

    @patch('piwardrive.security.logger')
    def test_audit_log_anonymous_user(self, mock_logger):
        """Test audit logging for anonymous users."""
        action = "public_access"
        
        audit_log(None, action, success=True)
        
        mock_logger.info.assert_called_once()
        call_args = mock_logger.info.call_args[0][0]
        assert "anonymous" in call_args.lower()


class TestSecurityIntegration:
    """Test security integration with other systems."""

    @patch('piwardrive.security.DatabaseManager')
    def test_database_security_integration(self, mock_db):
        """Test security integration with database."""
        mock_db_instance = Mock()
        mock_db.return_value = mock_db_instance
        
        # Test secure database query
        user_input = "'; DROP TABLE users; --"
        
        # Should sanitize input before database query
        with pytest.raises(SecurityError):
            validate_input(user_input)

    @patch('piwardrive.security.ConfigManager')
    def test_config_security_integration(self, mock_config):
        """Test security integration with configuration."""
        mock_config_instance = Mock()
        mock_config.return_value = mock_config_instance
        
        # Test secure configuration access
        config_path = "../../../etc/passwd"
        
        with pytest.raises(SecurityError):
            sanitize_path(config_path)

    def test_api_security_integration(self):
        """Test security integration with API endpoints."""
        # Test API token validation
        valid_token = generate_token()
        invalid_token = "invalid_token"
        
        assert verify_token(valid_token) is True
        assert verify_token(invalid_token) is False

    def test_file_security_integration(self):
        """Test security integration with file operations."""
        # Test secure file path validation
        safe_path = "/var/log/piwardrive/app.log"
        dangerous_path = "../../../etc/passwd"
        
        assert sanitize_path(safe_path) == safe_path
        
        with pytest.raises(SecurityError):
            sanitize_path(dangerous_path)


class TestSecurityConfiguration:
    """Test security configuration and settings."""

    def test_security_config_validation(self):
        """Test security configuration validation."""
        valid_config = {
            "password_min_length": 8,
            "token_expiration": 3600,
            "max_login_attempts": 5,
            "audit_logging": True
        }
        
        # Configuration should be valid
        assert validate_security_config(valid_config) is True

    def test_security_config_invalid(self):
        """Test invalid security configuration."""
        invalid_configs = [
            {"password_min_length": 3},  # Too short
            {"token_expiration": -1},    # Negative
            {"max_login_attempts": 0},   # Zero attempts
        ]
        
        for config in invalid_configs:
            with pytest.raises(ValueError):
                validate_security_config(config)

    def test_security_defaults(self):
        """Test security default values."""
        from piwardrive.security import get_security_defaults
        
        defaults = get_security_defaults()
        
        assert defaults["password_min_length"] >= 8
        assert defaults["token_expiration"] > 0
        assert defaults["audit_logging"] is True


def validate_security_config(config):
    """Validate security configuration."""
    if config.get("password_min_length", 8) < 8:
        raise ValueError("Password minimum length too short")
    
    if config.get("token_expiration", 3600) <= 0:
        raise ValueError("Token expiration must be positive")
    
    if config.get("max_login_attempts", 5) <= 0:
        raise ValueError("Max login attempts must be positive")
    
    return True


if __name__ == '__main__':
    pytest.main([__file__])
