"""
Fixed comprehensive test suite for JWT utilities.

This module provides thorough testing for jwt_utils.py, including:
- JWT constant configuration
- Token creation (access and refresh)
- Token verification and validation
- Error handling and edge cases
- Security considerations
"""

import os

# Import the module under test
import sys
import time
import unittest
from unittest.mock import patch

import jwt as pyjwt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from piwardrive import jwt_utils


class TestJWTConstants(unittest.TestCase):
    """Test JWT configuration constants."""

    def test_default_secret(self):
        """Test default JWT secret."""
        with patch.dict(os.environ, {}, clear=True):
            # Reload the module to get fresh defaults
            import importlib

            importlib.reload(jwt_utils)
            self.assertEqual(jwt_utils.SECRET, "change-me")

    def test_custom_secret_from_env(self):
        """Test custom JWT secret from environment."""
        with patch.dict(os.environ, {"PW_JWT_SECRET": "custom-secret"}):
            import importlib

            importlib.reload(jwt_utils)
            self.assertEqual(jwt_utils.SECRET, "custom-secret")

    def test_default_algorithm(self):
        """Test default JWT algorithm."""
        with patch.dict(os.environ, {}, clear=True):
            import importlib

            importlib.reload(jwt_utils)
            self.assertEqual(jwt_utils.ALGORITHM, "HS256")

    def test_custom_algorithm_from_env(self):
        """Test custom JWT algorithm from environment."""
        with patch.dict(os.environ, {"PW_JWT_ALG": "HS512"}):
            import importlib

            importlib.reload(jwt_utils)
            self.assertEqual(jwt_utils.ALGORITHM, "HS512")

    def test_default_access_expire(self):
        """Test default access token expiry."""
        with patch.dict(os.environ, {}, clear=True):
            import importlib

            importlib.reload(jwt_utils)
            self.assertEqual(jwt_utils.ACCESS_EXPIRE, 3600)

    def test_custom_access_expire_from_env(self):
        """Test custom access token expiry from environment."""
        with patch.dict(os.environ, {"PW_JWT_EXPIRE": "7200"}):
            import importlib

            importlib.reload(jwt_utils)
            self.assertEqual(jwt_utils.ACCESS_EXPIRE, 7200)

    def test_default_refresh_expire(self):
        """Test default refresh token expiry."""
        with patch.dict(os.environ, {}, clear=True):
            import importlib

            importlib.reload(jwt_utils)
            self.assertEqual(jwt_utils.REFRESH_EXPIRE, 86400)

    def test_custom_refresh_expire_from_env(self):
        """Test custom refresh token expiry from environment."""
        with patch.dict(os.environ, {"PW_JWT_REFRESH": "172800"}):
            import importlib

            importlib.reload(jwt_utils)
            self.assertEqual(jwt_utils.REFRESH_EXPIRE, 172800)


class TestCreateAccessToken(unittest.TestCase):
    """Test access token creation."""

    def test_create_access_token_basic(self):
        """Test basic access token creation."""
        username = "testuser"
        token = jwt_utils.create_access_token(username)

        self.assertIsInstance(token, str)
        self.assertGreater(len(token), 0)

        # Verify it's a valid JWT structure
        parts = token.split(".")
        self.assertEqual(len(parts), 3)

    def test_create_access_token_custom_expiry(self):
        """Test access token creation with custom expiry."""
        username = "testuser"
        custom_expire = 1800  # 30 minutes

        # Mock time to control timing
        mock_time = 1000000
        with patch("time.time", return_value=mock_time):
            token = jwt_utils.create_access_token(username, expires_in=custom_expire)

        # Decode without verification for payload inspection
        payload = pyjwt.decode(token, options={"verify_signature": False})
        self.assertEqual(payload["sub"], username)
        self.assertEqual(payload["exp"], mock_time + custom_expire)

    def test_create_access_token_default_expiry(self):
        """Test access token creation with default expiry."""
        username = "testuser"

        mock_time = 1000000
        with patch("time.time", return_value=mock_time):
            token = jwt_utils.create_access_token(username)

        payload = pyjwt.decode(token, options={"verify_signature": False})
        self.assertEqual(payload["exp"], mock_time + jwt_utils.ACCESS_EXPIRE)

    def test_create_access_token_various_usernames(self):
        """Test access token creation with various usernames."""
        usernames = [
            "user1",
            "test_user",
            "admin@example.com",
            "user-with-dash",
            "123numeric",
            "MixedCase",
        ]

        for username in usernames:
            with self.subTest(username=username):
                token = jwt_utils.create_access_token(username)
                self.assertIsInstance(token, str)
                self.assertGreater(len(token), 0)

                payload = pyjwt.decode(token, options={"verify_signature": False})
                self.assertEqual(payload["sub"], username)

    def test_create_access_token_time_consistency(self):
        """Test that consecutive token creation has increasing timestamps."""
        username = "testuser"

        # Create tokens with small time differences
        times = [1000000, 1000001, 1000002]
        tokens = []

        for mock_time in times:
            with patch("time.time", return_value=mock_time):
                token = jwt_utils.create_access_token(username)
                tokens.append(token)

        # Verify timestamps are increasing
        payloads = [
            pyjwt.decode(token, options={"verify_signature": False}) for token in tokens
        ]
        for i in range(1, len(payloads)):
            self.assertGreater(payloads[i]["exp"], payloads[i - 1]["exp"])


class TestCreateRefreshToken(unittest.TestCase):
    """Test refresh token creation."""

    def test_create_refresh_token_basic(self):
        """Test basic refresh token creation."""
        username = "testuser"
        token = jwt_utils.create_refresh_token(username)

        self.assertIsInstance(token, str)
        self.assertGreater(len(token), 0)

        # Verify it's a valid JWT structure
        parts = token.split(".")
        self.assertEqual(len(parts), 3)

    def test_create_refresh_token_custom_expiry(self):
        """Test refresh token creation with custom expiry."""
        username = "testuser"
        custom_expire = 172800  # 2 days

        mock_time = 1000000
        with patch("time.time", return_value=mock_time):
            token = jwt_utils.create_refresh_token(username, expires_in=custom_expire)

        payload = pyjwt.decode(token, options={"verify_signature": False})
        self.assertEqual(payload["sub"], username)
        self.assertEqual(payload["exp"], mock_time + custom_expire)
        self.assertEqual(payload["type"], "refresh")

    def test_create_refresh_token_default_expiry(self):
        """Test refresh token creation with default expiry."""
        username = "testuser"

        mock_time = 1000000
        with patch("time.time", return_value=mock_time):
            token = jwt_utils.create_refresh_token(username)

        payload = pyjwt.decode(token, options={"verify_signature": False})
        self.assertEqual(payload["exp"], mock_time + jwt_utils.REFRESH_EXPIRE)

    def test_create_refresh_token_type_field(self):
        """Test that refresh tokens have the correct type field."""
        username = "testuser"
        token = jwt_utils.create_refresh_token(username)

        payload = pyjwt.decode(token, options={"verify_signature": False})
        self.assertEqual(payload["type"], "refresh")

    def test_create_refresh_token_vs_access_token(self):
        """Test differences between refresh and access tokens."""
        username = "testuser"

        mock_time = 1000000
        with patch("time.time", return_value=mock_time):
            access_token = jwt_utils.create_access_token(username)
            refresh_token = jwt_utils.create_refresh_token(username)

        access_payload = pyjwt.decode(access_token, options={"verify_signature": False})
        refresh_payload = pyjwt.decode(
            refresh_token, options={"verify_signature": False}
        )

        # Both should have same subject
        self.assertEqual(access_payload["sub"], refresh_payload["sub"])

        # Refresh token should have type field, access token shouldn't
        self.assertNotIn("type", access_payload)
        self.assertEqual(refresh_payload["type"], "refresh")

        # Refresh token should have longer expiry
        self.assertGreater(refresh_payload["exp"], access_payload["exp"])


class TestVerifyToken(unittest.TestCase):
    """Test token verification."""

    def test_verify_valid_access_token(self):
        """Test verification of valid access token."""
        username = "testuser"

        # Create token with sufficient expiry
        future_time = int(time.time()) + 3600
        with patch("time.time", return_value=future_time - 3600):
            token = jwt_utils.create_access_token(username)

        # Verify the token
        verified_username = jwt_utils.verify_token(token)
        self.assertEqual(verified_username, username)

    def test_verify_valid_refresh_token(self):
        """Test verification of valid refresh token."""
        username = "testuser"

        # Create token with sufficient expiry
        future_time = int(time.time()) + 86400
        with patch("time.time", return_value=future_time - 86400):
            token = jwt_utils.create_refresh_token(username)

        # Verify the token
        verified_username = jwt_utils.verify_token(token)
        self.assertEqual(verified_username, username)

    def test_verify_invalid_token(self):
        """Test verification of invalid token."""
        invalid_tokens = [
            "invalid.token.here",
            "not-a-jwt",
            "",
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid.signature",
        ]

        for token in invalid_tokens:
            with self.subTest(token=token[:20]):
                result = jwt_utils.verify_token(token)
                self.assertIsNone(result)

    def test_verify_expired_token(self):
        """Test verification of expired token."""
        username = "testuser"

        # Create token that's already expired
        past_time = int(time.time()) - 3600
        with patch("time.time", return_value=past_time):
            token = jwt_utils.create_access_token(username, expires_in=1)

        # Verify the expired token
        result = jwt_utils.verify_token(token)
        self.assertIsNone(result)

    def test_verify_token_wrong_secret(self):
        """Test verification with wrong secret."""
        username = "testuser"

        # Create token with current secret
        token = jwt_utils.create_access_token(username)

        # Try to verify with wrong secret
        with patch.object(jwt_utils, "SECRET", "wrong-secret"):
            result = jwt_utils.verify_token(token)
            self.assertIsNone(result)

    def test_verify_token_wrong_algorithm(self):
        """Test verification with wrong algorithm."""
        username = "testuser"

        # Create token with current algorithm
        token = jwt_utils.create_access_token(username)

        # Try to verify with wrong algorithm
        with patch.object(jwt_utils, "ALGORITHM", "HS512"):
            result = jwt_utils.verify_token(token)
            self.assertIsNone(result)

    def test_verify_malformed_token(self):
        """Test verification of malformed tokens."""
        malformed_tokens = [
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",  # Missing parts
            "header.payload",  # Missing signature
            "...",  # Empty parts
            "a.b.c.d",  # Too many parts
        ]

        for token in malformed_tokens:
            with self.subTest(token=token):
                result = jwt_utils.verify_token(token)
                self.assertIsNone(result)

    def test_verify_token_no_subject(self):
        """Test verification of token without subject."""
        # Create a token manually without subject
        payload = {"exp": int(time.time()) + 3600}
        token = pyjwt.encode(payload, jwt_utils.SECRET, algorithm=jwt_utils.ALGORITHM)

        result = jwt_utils.verify_token(token)
        self.assertIsNone(result)


class TestJWTSecurity(unittest.TestCase):
    """Test JWT security considerations."""

    def test_token_uniqueness(self):
        """Test that tokens are unique even for same user."""
        username = "testuser"
        tokens = []

        # Create tokens at different times to ensure uniqueness
        base_time = 1000000
        for i in range(5):
            with patch("time.time", return_value=base_time + i):
                token = jwt_utils.create_access_token(username)
                tokens.append(token)

        # All tokens should be unique
        self.assertEqual(len(set(tokens)), len(tokens))

    def test_token_structure_consistency(self):
        """Test that tokens have consistent structure."""
        usernames = ["user1", "user2", "admin"]

        for username in usernames:
            token = jwt_utils.create_access_token(username)
            parts = token.split(".")

            # Should have 3 parts (header, payload, signature)
            self.assertEqual(len(parts), 3)

            # Each part should be non-empty
            for part in parts:
                self.assertGreater(len(part), 0)

    def test_secret_not_exposed_in_token(self):
        """Test that the secret is not exposed in the token."""
        username = "testuser"
        token = jwt_utils.create_access_token(username)

        # Decode without verification to check payload
        payload = pyjwt.decode(token, options={"verify_signature": False})

        # Secret should not be in payload
        self.assertNotIn(jwt_utils.SECRET, str(payload))
        self.assertNotIn("secret", payload)
        self.assertNotIn("key", payload)

    def test_algorithm_consistency(self):
        """Test that the algorithm used is consistent."""
        username = "testuser"
        token = jwt_utils.create_access_token(username)

        # Decode header to check algorithm
        header = pyjwt.get_unverified_header(token)
        self.assertEqual(header["alg"], jwt_utils.ALGORITHM)
        self.assertEqual(header["typ"], "JWT")


class TestJWTEdgeCases(unittest.TestCase):
    """Test edge cases and error scenarios."""

    def test_empty_username(self):
        """Test token creation with empty username."""
        token = jwt_utils.create_access_token("")
        self.assertIsInstance(token, str)

        payload = pyjwt.decode(token, options={"verify_signature": False})
        self.assertEqual(payload["sub"], "")

    def test_very_long_username(self):
        """Test token creation with very long username."""
        long_username = "a" * 1000
        token = jwt_utils.create_access_token(long_username)
        self.assertIsInstance(token, str)

        payload = pyjwt.decode(token, options={"verify_signature": False})
        self.assertEqual(payload["sub"], long_username)

    def test_unicode_username(self):
        """Test token creation with unicode username."""
        unicode_usernames = [
            "用户",  # Chinese
            "пользователь",  # Russian
            "ユーザー",  # Japanese
            "🔐👤",  # Emojis
        ]

        for username in unicode_usernames:
            with self.subTest(username=username):
                token = jwt_utils.create_access_token(username)
                self.assertIsInstance(token, str)

                payload = pyjwt.decode(token, options={"verify_signature": False})
                self.assertEqual(payload["sub"], username)

    def test_zero_expiry(self):
        """Test token creation with zero expiry."""
        username = "testuser"

        mock_time = 1000000
        with patch("time.time", return_value=mock_time):
            token = jwt_utils.create_access_token(username, expires_in=0)

        payload = pyjwt.decode(token, options={"verify_signature": False})
        self.assertEqual(payload["exp"], mock_time)

    def test_negative_expiry(self):
        """Test token creation with negative expiry."""
        username = "testuser"

        mock_time = 1000000
        with patch("time.time", return_value=mock_time):
            token = jwt_utils.create_access_token(username, expires_in=-3600)

        payload = pyjwt.decode(token, options={"verify_signature": False})
        self.assertEqual(payload["exp"], mock_time - 3600)

        # This token should be considered expired
        result = jwt_utils.verify_token(token)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
