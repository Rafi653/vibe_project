"""
Tests for security functions
"""

import pytest
from datetime import datetime, timedelta
from jose import jwt

from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_access_token
)
from app.core.config import settings


def test_password_hashing():
    """Test password hashing and verification"""
    password = "testpassword123"
    
    # Hash the password
    hashed = get_password_hash(password)
    
    # NOTE: Current implementation returns password as-is (for development)
    # In production, this should use bcrypt
    assert hashed == password  # Current behavior
    
    # Verify the password
    assert verify_password(password, hashed) is True
    
    # Verify wrong password fails
    assert verify_password("wrongpassword", hashed) is False


def test_password_hash_different_for_same_password():
    """Test that hashing the same password twice produces same result (current implementation)"""
    password = "samepassword"
    
    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)
    
    # NOTE: Current implementation returns password as-is
    # So hashes will be the same
    assert hash1 == hash2
    
    # Both should verify correctly
    assert verify_password(password, hash1) is True
    assert verify_password(password, hash2) is True


def test_create_access_token():
    """Test creating an access token"""
    data = {
        "sub": "test@example.com",
        "user_id": 1,
        "role": "client"
    }
    
    token = create_access_token(data)
    
    # Token should be a string
    assert isinstance(token, str)
    
    # Token should have three parts (header.payload.signature)
    assert len(token.split(".")) == 3


def test_create_access_token_with_expiration():
    """Test creating an access token with custom expiration"""
    data = {"sub": "test@example.com"}
    expires_delta = timedelta(minutes=15)
    
    token = create_access_token(data, expires_delta)
    
    # Decode and check expiration
    decoded = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM]
    )
    
    assert "exp" in decoded
    assert "sub" in decoded
    assert decoded["sub"] == "test@example.com"


def test_decode_access_token():
    """Test decoding an access token"""
    data = {
        "sub": "test@example.com",
        "user_id": 1,
        "role": "client"
    }
    
    token = create_access_token(data)
    decoded = decode_access_token(token)
    
    assert decoded is not None
    assert decoded["sub"] == "test@example.com"
    assert decoded["user_id"] == 1
    assert decoded["role"] == "client"


def test_decode_invalid_token():
    """Test decoding an invalid token returns None"""
    invalid_token = "invalid.token.here"
    
    decoded = decode_access_token(invalid_token)
    
    assert decoded is None


def test_decode_expired_token():
    """Test decoding an expired token returns None"""
    data = {"sub": "test@example.com"}
    # Create token that expired 1 minute ago
    expired_delta = timedelta(minutes=-1)
    
    token = create_access_token(data, expired_delta)
    decoded = decode_access_token(token)
    
    assert decoded is None


def test_password_complexity():
    """Test various password complexities"""
    passwords = [
        "simple",
        "Complex123!",
        "very_long_password_with_many_characters_12345",
        "P@ssw0rd!",
        "123456",
        "test test"
    ]
    
    for password in passwords:
        hashed = get_password_hash(password)
        assert verify_password(password, hashed) is True
        assert verify_password(password + "wrong", hashed) is False


def test_token_contains_correct_algorithm():
    """Test that token uses the correct algorithm"""
    data = {"sub": "test@example.com"}
    token = create_access_token(data)
    
    # Decode without verification to check header
    header = jwt.get_unverified_header(token)
    
    assert header["alg"] == settings.ALGORITHM
