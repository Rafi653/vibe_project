"""
Authentication endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.schemas.auth import UserSignup, UserLogin, UserWithToken, UserResponse
from app.services.auth_service import AuthService
from app.core.dependencies import get_current_active_user
from app.models.user import User

router = APIRouter()


@router.post("/signup", response_model=UserWithToken, status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: UserSignup,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user account
    
    - **email**: Valid email address (must be unique)
    - **password**: Password (minimum 6 characters)
    - **full_name**: User's full name
    - **role**: User role (client, coach, or admin) - defaults to client
    
    Returns the created user and an access token
    """
    return await AuthService.signup_user(db, user_data)


@router.post("/login", response_model=UserWithToken)
async def login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    Authenticate user and return access token
    
    - **email**: User's email address
    - **password**: User's password
    
    Returns user info and an access token for subsequent requests
    """
    print("Login attempt for:", login_data)
    return await AuthService.login_user(db, login_data)


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current authenticated user information
    
    Requires valid JWT token in Authorization header
    
    Returns current user's profile information
    """
    return UserResponse.model_validate(current_user)


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_active_user)
):
    """
    Logout current user
    
    Note: With JWT tokens, logout is primarily handled on the client side
    by removing the token. This endpoint can be used for additional
    server-side logging or token blacklisting if needed in the future.
    
    Returns a success message
    """
    return {
        "message": "Successfully logged out",
        "detail": "Please remove the token from client storage"
    }
