"""
User management endpoints (example of protected routes)
"""

from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_active_user, require_admin
from app.models.user import User
from app.schemas.auth import UserResponse

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_my_profile(current_user: User = Depends(get_current_active_user)):
    """
    Get current user's profile
    
    Requires authentication
    """
    return UserResponse.model_validate(current_user)


@router.get("/admin/users", response_model=list[UserResponse])
async def list_all_users(current_user: User = Depends(require_admin)):
    """
    List all users (admin only)
    
    Requires ADMIN role
    """
    # This is a placeholder - in real implementation, query the database
    return []


@router.get("/stats")
async def get_user_stats(current_user: User = Depends(get_current_active_user)):
    """
    Get user statistics
    
    Requires authentication
    Returns different stats based on user role
    """
    stats = {
        "user_id": current_user.id,
        "role": current_user.role.value,
    }
    
    if current_user.role.value == "client":
        stats.update({
            "workout_count": 0,
            "diet_logs": 0,
        })
    elif current_user.role.value == "coach":
        stats.update({
            "clients": 0,
            "active_plans": 0,
        })
    elif current_user.role.value == "admin":
        stats.update({
            "total_users": 0,
            "active_coaches": 0,
            "active_clients": 0,
        })
    
    return stats
