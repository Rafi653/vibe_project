"""
Authentication service layer for business logic
"""

from typing import Optional
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.auth import UserSignup, UserLogin, UserWithToken, UserResponse
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.config import settings


class AuthService:
    """Service class for authentication operations"""
    
    @staticmethod
    async def signup_user(db: AsyncSession, user_data: UserSignup) -> UserWithToken:
        """
        Register a new user
        
        Args:
            db: Database session
            user_data: User signup data
            
        Returns:
            UserWithToken with user info and access token
            
        Raises:
            HTTPException: If email already exists
        """
        # Check if user already exists
        result = await db.execute(select(User).where(User.email == user_data.email))
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            role=user_data.role,
            is_active=True,
            is_verified=False
        )
        
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        # Create access token
        access_token = create_access_token(
            data={
                "sub": new_user.email,
                "user_id": new_user.id,
                "role": new_user.role.value
            }
        )
        
        return UserWithToken(
            user=UserResponse.model_validate(new_user),
            access_token=access_token
        )
    
    @staticmethod
    async def login_user(db: AsyncSession, login_data: UserLogin) -> UserWithToken:
        """
        Authenticate user and return token
        
        Args:
            db: Database session
            login_data: User login credentials
            
        Returns:
            UserWithToken with user info and access token
            
        Raises:
            HTTPException: If credentials are invalid
        """
        # Find user by email
        result = await db.execute(select(User).where(User.email == login_data.email))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verify password
        if not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user account"
            )
        
        # Create access token
        access_token = create_access_token(
            data={
                "sub": user.email,
                "user_id": user.id,
                "role": user.role.value
            }
        )
        
        return UserWithToken(
            user=UserResponse.model_validate(user),
            access_token=access_token
        )
    
    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """
        Get user by email address
        
        Args:
            db: Database session
            email: User email address
            
        Returns:
            User object if found, None otherwise
        """
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
