#!/usr/bin/env python3

"""
Comprehensive test suite for jwt_utils.py module.
Tests JWT token creation, verification, and security functionality.
"""

import pytest
import sys
import time
import os
import unittest.mock as mock
from unittest.mock import patch, Mock
from pathlib import Path

# Add source directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import jwt as pyjwt

# We need to import after setting up the path
from piwardrive import jwt_utils


class TestJWTConstants:
    """Test JWT module constants and configuration."""

    def test_default_secret(self):
        """Test default SECRET value."""
        with patch.dict(os.environ, {}, clear=True):
            # Re-import to get fresh environment values
            import importlib
            importlib.reload(jwt_utils)
            assert jwt_utils.SECRET == "change-me"

    def test_custom_secret_from_env(self):
        """Test SECRET from environment variable."""
        custom_secret = "my-secret-key-123"
        with patch.dict(os.environ, {"PW_JWT_SECRET": custom_secret}, clear=True):
            import importlib
            importlib.reload(jwt_utils)
            assert jwt_utils.SECRET == custom_secret

    def test_default_algorithm(self):
        """Test default ALGORITHM value."""
        with patch.dict(os.environ, {}, clear=True):
            import importlib
            importlib.reload(jwt_utils)
            assert jwt_utils.ALGORITHM == "HS256"

    def test_custom_algorithm_from_env(self):
        """Test ALGORITHM from environment variable."""
        custom_alg = "HS512"
        with patch.dict(os.environ, {"PW_JWT_ALG": custom_alg}, clear=True):
            import importlib
            importlib.reload(jwt_utils)
            assert jwt_utils.ALGORITHM == custom_alg

    def test_default_access_expire(self):
        """Test default ACCESS_EXPIRE value."""
        with patch.dict(os.environ, {}, clear=True):
            import importlib
            importlib.reload(jwt_utils)
            assert jwt_utils.ACCESS_EXPIRE == 3600

    def test_custom_access_expire_from_env(self):
        """Test ACCESS_EXPIRE from environment variable."""
        custom_expire = "7200"
        with patch.dict(os.environ, {"PW_JWT_EXPIRE": custom_expire}, clear=True):
            import importlib
            importlib.reload(jwt_utils)
            assert jwt_utils.ACCESS_EXPIRE == 7200

    def test_default_refresh_expire(self):
        """Test default REFRESH_EXPIRE value."""
        with patch.dict(os.environ, {}, clear=True):
            import importlib
            importlib.reload(jwt_utils)
            assert jwt_utils.REFRESH_EXPIRE == 86400

    def test_custom_refresh_expire_from_env(self):
        """Test REFRESH_EXPIRE from environment variable."""
        custom_refresh = "172800"
        with patch.dict(os.environ, {"PW_JWT_REFRESH": custom_refresh}, clear=True):
            import importlib
            importlib.reload(jwt_utils)
            assert jwt_utils.REFRESH_EXPIRE == 172800


class TestCreateAccessToken:
    """Test create_access_token function."""

    def test_create_access_token_basic(self):
        """Test basic access token creation."""
        username = "testuser"
        token = jwt_utils.create_access_token(username)
        
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Verify token can be decoded
        payload = pyjwt.decode(token, jwt_utils.SECRET, algorithms=[jwt_utils.ALGORITHM])
        assert payload["sub"] == username
        assert "exp" in payload

    def test_create_access_token_custom_expiry(self):
        """Test access token creation with custom expiry."""
        username = "testuser"
        custom_expire = 1800  # 30 minutes
        
        with patch('time.time', return_value=1000000):
            token = jwt_utils.create_access_token(username, expires_in=custom_expire)
        
        payload = pyjwt.decode(token, jwt_utils.SECRET, algorithms=[jwt_utils.ALGORITHM])
        assert payload["sub"] == username
        assert payload["exp"] == 1000000 + custom_expire

    def test_create_access_token_default_expiry(self):
        """Test access token creation with default expiry."""
        username = "testuser"
        
        with patch('time.time', return_value=1000000):
            token = jwt_utils.create_access_token(username)
        
        payload = pyjwt.decode(token, jwt_utils.SECRET, algorithms=[jwt_utils.ALGORITHM])
        assert payload["exp"] == 1000000 + jwt_utils.ACCESS_EXPIRE

    def test_create_access_token_various_usernames(self):
        """Test access token creation with various usernames."""
        usernames = [
            "admin",
            "user123",
            "test@example.com",
            "user_with_underscores",
            "user-with-hyphens",
        ]
        
        for username in usernames:
            token = jwt_utils.create_access_token(username)
            payload = pyjwt.decode(token, jwt_utils.SECRET, algorithms=[jwt_utils.ALGORITHM])
            assert payload["sub"] == username

    def test_create_access_token_time_consistency(self):
        """Test that token expiry is based on current time."""
        username = "testuser"
        current_time = int(time.time())
        
        token = jwt_utils.create_access_token(username)
        payload = pyjwt.decode(token, jwt_utils.SECRET, algorithms=[jwt_utils.ALGORITHM])
        
        # Allow for small time differences during test execution
        assert abs(payload["exp"] - (current_time + jwt_utils.ACCESS_EXPIRE)) <= 2


class TestCreateRefreshToken:
    """Test create_refresh_token function."""

    def test_create_refresh_token_basic(self):
        """Test basic refresh token creation."""
        username = "testuser"
        token = jwt_utils.create_refresh_token(username)
        
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Verify token can be decoded
        payload = pyjwt.decode(token, jwt_utils.SECRET, algorithms=[jwt_utils.ALGORITHM])
        assert payload["sub"] == username
        assert payload["type"] == "refresh"
        assert "exp" in payload

    def test_create_refresh_token_custom_expiry(self):
        """Test refresh token creation with custom expiry."""
        username = "testuser"
        custom_expire = 172800  # 2 days
        
        with patch('time.time', return_value=1000000):
            token = jwt_utils.create_refresh_token(username, expires_in=custom_expire)
        
        payload = pyjwt.decode(token, jwt_utils.SECRET, algorithms=[jwt_utils.ALGORITHM])
        assert payload["sub"] == username
        assert payload["type"] == "refresh"
        assert payload["exp"] == 1000000 + custom_expire

    def test_create_refresh_token_default_expiry(self):
        """Test refresh token creation with default expiry."""
        username = "testuser"
        
        with patch('time.time', return_value=1000000):
            token = jwt_utils.create_refresh_token(username)
        
        payload = pyjwt.decode(token, jwt_utils.SECRET, algorithms=[jwt_utils.ALGORITHM])
        assert payload["exp"] == 1000000 + jwt_utils.REFRESH_EXPIRE

    def test_create_refresh_token_type_field(self):
        """Test that refresh tokens have correct type field."""
        username = "testuser"
        token = jwt_utils.create_refresh_token(username)
        
        payload = pyjwt.decode(token, jwt_utils.SECRET, algorithms=[jwt_utils.ALGORITHM])
        assert payload["type"] == "refresh"

    def test_create_refresh_token_vs_access_token(self):
        """Test difference between refresh and access tokens."""
        username = "testuser"
        
        access_token = jwt_utils.create_access_token(username)
        refresh_token = jwt_utils.create_refresh_token(username)
        
        access_payload = pyjwt.decode(access_token, jwt_utils.SECRET, algorithms=[jwt_utils.ALGORITHM])
        refresh_payload = pyjwt.decode(refresh_token, jwt_utils.SECRET, algorithms=[jwt_utils.ALGORITHM])
        
        # Both should have same username
        assert access_payload["sub"] == refresh_payload["sub"] == username
        
        # Only refresh token should have type field
        assert "type" not in access_payload
        assert refresh_payload["type"] == "refresh"
        
        # Refresh token should expire later than access token
        assert refresh_payload["exp"] > access_payload["exp"]


class TestVerifyToken:
    """Test verify_token function."""

    def test_verify_valid_access_token(self):
        """Test verification of valid access token."""
        username = "testuser"
        token = jwt_utils.create_access_token(username)
        
        result = jwt_utils.verify_token(token)
        assert result == username

    def test_verify_valid_refresh_token(self):
        """Test verification of valid refresh token."""
        username = "testuser"
        token = jwt_utils.create_refresh_token(username)
        
        result = jwt_utils.verify_token(token)
        assert result == username

    def test_verify_invalid_token(self):
        """Test verification of invalid token."""
        invalid_token = "invalid.jwt.token"
        
        result = jwt_utils.verify_token(invalid_token)
        assert result is None

    def test_verify_expired_token(self):
        """Test verification of expired token."""
        username = "testuser"
        
        # Create token that expires immediately
        with patch('time.time', return_value=1000000):
            token = jwt_utils.create_access_token(username, expires_in=0)
        
        # Wait a bit to ensure expiry
        time.sleep(0.1)
        
        result = jwt_utils.verify_token(token)
        assert result is None

    def test_verify_token_wrong_secret(self):
        """Test verification with wrong secret."""
        username = "testuser"
        
        # Create token with current secret
        token = jwt_utils.create_access_token(username)
        
        # Try to verify with different secret
        wrong_secret = "wrong-secret"
        try:
            pyjwt.decode(token, wrong_secret, algorithms=[jwt_utils.ALGORITHM])
            assert False, "Should have raised exception"
        except pyjwt.PyJWTError:
            pass  # Expected
        
        # Our verify function should return None for invalid signature
        with patch.object(jwt_utils, 'SECRET', wrong_secret):
            result = jwt_utils.verify_token(token)
            assert result is None

    def test_verify_token_wrong_algorithm(self):
        """Test verification with wrong algorithm."""
        username = "testuser"
        token = jwt_utils.create_access_token(username)
        
        # Try to decode with wrong algorithm - should fail in jwt.decode
        try:
            pyjwt.decode(token, jwt_utils.SECRET, algorithms=["HS512"])
            assert False, "Should have raised exception"
        except pyjwt.PyJWTError:
            pass  # Expected

    def test_verify_malformed_token(self):
        """Test verification of malformed tokens."""
        malformed_tokens = [
            "",
            "not.a.jwt",
            "header.payload",  # Missing signature
            "header.payload.signature.extra",  # Too many parts
            "invalid_base64.invalid_base64.invalid_base64",
        ]
        
        for token in malformed_tokens:
            result = jwt_utils.verify_token(token)
            assert result is None

    def test_verify_token_no_subject(self):
        """Test verification of token without subject."""
        # Create token manually without 'sub' field
        payload = {"exp": int(time.time()) + 3600}
        token = pyjwt.encode(payload, jwt_utils.SECRET, algorithm=jwt_utils.ALGORITHM)
        
        result = jwt_utils.verify_token(token)
        assert result is None


class TestJWTSecurity:
    """Test JWT security aspects."""

    def test_token_uniqueness(self):
        """Test that tokens are unique for same user."""
        username = "testuser"
        
        # Create multiple tokens with slight time differences
        tokens = []
        for _ in range(5):
            tokens.append(jwt_utils.create_access_token(username))
            time.sleep(0.01)  # Small delay to ensure different timestamps
        
        # All tokens should be different
        assert len(set(tokens)) == len(tokens)

    def test_secret_isolation(self):
        """Test that different secrets produce different tokens."""
        username = "testuser"
        
        # Create token with default secret
        token1 = jwt_utils.create_access_token(username)
        
        # Create token with different secret
        with patch.object(jwt_utils, 'SECRET', 'different-secret'):
            token2 = jwt_utils.create_access_token(username)
        
        assert token1 != token2
        
        # First token should not verify with second secret
        with patch.object(jwt_utils, 'SECRET', 'different-secret'):
            result = jwt_utils.verify_token(token1)
            assert result is None

    def test_algorithm_isolation(self):
        """Test that different algorithms produce different tokens."""
        username = "testuser"
        
        # Create token with HS256
        with patch.object(jwt_utils, 'ALGORITHM', 'HS256'):
            token1 = jwt_utils.create_access_token(username)
        
        # Create token with HS512 (but same secret)
        with patch.object(jwt_utils, 'ALGORITHM', 'HS512'):
            token2 = jwt_utils.create_access_token(username)
        
        assert token1 != token2


class TestJWTIntegration:
    """Test JWT module integration scenarios."""

    def test_full_token_lifecycle(self):
        """Test complete token creation and verification cycle."""
        username = "integration_test_user"
        
        # Create access token
        access_token = jwt_utils.create_access_token(username)
        assert isinstance(access_token, str)
        
        # Create refresh token
        refresh_token = jwt_utils.create_refresh_token(username)
        assert isinstance(refresh_token, str)
        
        # Verify both tokens
        assert jwt_utils.verify_token(access_token) == username
        assert jwt_utils.verify_token(refresh_token) == username
        
        # Tokens should be different
        assert access_token != refresh_token

    def test_environment_configuration(self):
        """Test JWT configuration from environment variables."""
        test_config = {
            "PW_JWT_SECRET": "test-secret-123",
            "PW_JWT_ALG": "HS512",
            "PW_JWT_EXPIRE": "1800",
            "PW_JWT_REFRESH": "604800",
        }
        
        with patch.dict(os.environ, test_config, clear=True):
            import importlib
            importlib.reload(jwt_utils)
            
            username = "envtest"
            token = jwt_utils.create_access_token(username)
            
            # Verify token with new configuration
            result = jwt_utils.verify_token(token)
            assert result == username
            
            # Check that new values are used
            assert jwt_utils.SECRET == "test-secret-123"
            assert jwt_utils.ALGORITHM == "HS512"
            assert jwt_utils.ACCESS_EXPIRE == 1800
            assert jwt_utils.REFRESH_EXPIRE == 604800

    def test_error_handling_scenarios(self):
        """Test various error scenarios."""
        username = "errortest"
        
        # Test with None input
        result = jwt_utils.verify_token(None)
        assert result is None
        
        # Test with empty string
        result = jwt_utils.verify_token("")
        assert result is None
        
        # Test with non-string input (should cause PyJWTError)
        with pytest.raises(AttributeError):
            jwt_utils.verify_token(12345)


if __name__ == "__main__":
    pytest.main([__file__])
