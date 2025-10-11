"""
Feedback endpoints - for collecting user feedback and suggestions
"""

from fastapi import APIRouter, Depends, Request, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.db.base import get_db
from app.core.dependencies import get_current_user, require_admin
from app.core.security import decode_access_token
from app.models.user import User
from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackCreate, FeedbackResponse

router = APIRouter()


async def get_optional_current_user(
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """Get current user if authenticated, otherwise return None"""
    if not authorization:
        return None
    
    # Extract token from "Bearer <token>"
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            return None
    except ValueError:
        return None
    
    # Decode token
    payload = decode_access_token(token)
    if payload is None:
        return None
    
    user_id: Optional[int] = payload.get("user_id")
    if user_id is None:
        return None
    
    # Fetch user from database
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if user and user.is_active:
        return user
    
    return None


@router.post("/", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
async def submit_feedback(
    feedback_data: FeedbackCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    Submit feedback - can be submitted by authenticated or anonymous users
    
    - **message**: Feedback message (required)
    - **name**: Name (optional, auto-filled for authenticated users)
    - **email**: Email (optional, auto-filled for authenticated users)
    - **is_anonymous**: Submit anonymously (optional)
    - **page_url**: Current page URL (optional)
    """
    # Create feedback entry
    feedback = Feedback(
        user_id=current_user.id if current_user and not feedback_data.is_anonymous else None,
        name=feedback_data.name if feedback_data.name else (current_user.full_name if current_user and not feedback_data.is_anonymous else None),
        email=feedback_data.email if feedback_data.email else (current_user.email if current_user and not feedback_data.is_anonymous else None),
        message=feedback_data.message,
        is_anonymous=feedback_data.is_anonymous,
        page_url=feedback_data.page_url,
        user_agent=request.headers.get("user-agent", None)
    )
    
    db.add(feedback)
    await db.commit()
    await db.refresh(feedback)
    return feedback


@router.get("/", response_model=List[FeedbackResponse])
async def get_all_feedback(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all feedback submissions (Admin only)
    
    Returns a list of all feedback submissions with pagination
    """
    result = await db.execute(
        select(Feedback)
        .order_by(Feedback.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    feedback_list = result.scalars().all()
    return feedback_list
