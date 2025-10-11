"""
Tests for database configuration and utilities
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db, Base


@pytest.mark.asyncio
async def test_get_db_yields_session():
    """Test that get_db yields a valid async session"""
    async for session in get_db():
        assert isinstance(session, AsyncSession)
        assert session is not None
        break  # Only test the first yield


@pytest.mark.asyncio
async def test_base_class_exists():
    """Test that Base class exists and has expected attributes"""
    assert Base is not None
    assert hasattr(Base, 'metadata')
    assert hasattr(Base, '__table_args__')


@pytest.mark.asyncio
async def test_multiple_db_sessions_independent():
    """Test that multiple database sessions are independent"""
    sessions = []
    
    # Get two sessions
    async for session1 in get_db():
        sessions.append(session1)
        break
    
    async for session2 in get_db():
        sessions.append(session2)
        break
    
    # Sessions should be different instances
    assert len(sessions) == 2
    assert sessions[0] is not sessions[1]
