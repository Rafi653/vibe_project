# Authentication & Role-Based Access Control

This document describes the authentication and authorization system implemented in the Vibe Fitness Platform.

## Overview

The platform uses JWT (JSON Web Token) based authentication with role-based access control (RBAC). Users can sign up, log in, and access different parts of the application based on their assigned roles.

## User Roles

The system supports three user roles:

1. **Client** - Users looking for fitness coaching
2. **Coach** - Fitness coaches providing coaching services  
3. **Admin** - Platform administrators with full access

## Backend Implementation

### Architecture

- **Security Layer** (`app/core/security.py`): Password hashing and JWT token utilities
- **Authentication Service** (`app/services/auth_service.py`): Business logic for signup/login
- **Dependencies** (`app/core/dependencies.py`): Middleware for authentication and role checking
- **API Routes** (`app/api/v1/auth.py`): REST endpoints for authentication
- **Schemas** (`app/schemas/auth.py`): Request/response validation

### API Endpoints

#### Sign Up
```http
POST /api/v1/auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "full_name": "John Doe",
  "role": "client"
}
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "client",
    "is_active": true,
    "is_verified": false
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Login
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "client",
    "is_active": true,
    "is_verified": false
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Get Current User
```http
GET /api/v1/auth/me
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "client",
  "is_active": true,
  "is_verified": false
}
```

#### Logout
```http
POST /api/v1/auth/logout
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "message": "Successfully logged out",
  "detail": "Please remove the token from client storage"
}
```

### Protected Routes

To protect an endpoint, use the dependency injection system:

```python
from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_active_user, require_admin, require_coach
from app.models.user import User

router = APIRouter()

# Require any authenticated user
@router.get("/profile")
async def get_profile(current_user: User = Depends(get_current_active_user)):
    return {"user": current_user}

# Require admin role
@router.get("/admin/stats")
async def get_admin_stats(current_user: User = Depends(require_admin)):
    return {"stats": "admin data"}

# Require coach or admin role
@router.get("/coach/clients")
async def get_clients(current_user: User = Depends(require_coach)):
    return {"clients": []}
```

### Available Role Dependencies

- `get_current_user` - Get authenticated user (may be inactive)
- `get_current_active_user` - Get authenticated and active user
- `require_admin` - Requires ADMIN role
- `require_coach` - Requires COACH or ADMIN role
- `require_client` - Requires CLIENT, COACH, or ADMIN role

### Custom Role Requirements

You can create custom role requirements:

```python
from app.core.dependencies import require_role
from app.models.user import UserRole

# Require specific roles
coach_or_client = require_role(UserRole.COACH, UserRole.CLIENT)

@router.get("/custom")
async def custom_route(current_user: User = Depends(coach_or_client)):
    return {"data": "custom"}
```

## Frontend Implementation

### Architecture

- **Auth Context** (`context/AuthContext.js`): Global authentication state
- **Auth Service** (`services/authService.js`): API integration
- **Protected Routes** (`components/ProtectedRoute.js`): Route protection
- **Login/Signup** (`components/Login.js`, `components/Signup.js`): UI components

### Using the Auth Context

```javascript
import { useAuth } from '../context/AuthContext';

function MyComponent() {
  const { 
    user, 
    isAuthenticated, 
    login, 
    logout,
    hasRole,
    isAdmin,
    isCoach,
    isClient
  } = useAuth();

  // Check authentication
  if (!isAuthenticated) {
    return <div>Please log in</div>;
  }

  // Check specific role
  if (!hasRole('admin')) {
    return <div>Admin access required</div>;
  }

  return <div>Welcome, {user.email}!</div>;
}
```

### Protected Routes

```javascript
import ProtectedRoute from './components/ProtectedRoute';

// Require authentication only
<Route 
  path="/dashboard" 
  element={
    <ProtectedRoute>
      <Dashboard />
    </ProtectedRoute>
  } 
/>

// Require specific role
<Route 
  path="/admin" 
  element={
    <ProtectedRoute requiredRole="admin">
      <AdminDashboard />
    </ProtectedRoute>
  } 
/>

// Require one of multiple roles
<Route 
  path="/coach" 
  element={
    <ProtectedRoute requiredRole={['coach', 'admin']}>
      <CoachDashboard />
    </ProtectedRoute>
  } 
/>
```

## Security Features

### Password Security
- Passwords are hashed using bcrypt with automatic salt generation
- Minimum password length: 6 characters
- Passwords are never stored in plain text or logged

### JWT Tokens
- Tokens are signed using HS256 algorithm
- Default expiration: 30 minutes (configurable)
- Tokens include user ID, email, and role in payload
- Tokens are validated on every protected request

### Token Storage
- Tokens are stored in browser's localStorage
- Automatically included in API requests via Authorization header
- Cleared on logout

### CORS Configuration
- Configured to allow frontend origin (http://localhost:3000)
- Credentials are allowed for cookie-based authentication (if needed)

## Configuration

### Backend Configuration

Edit `backend/.env`:

```env
# Security
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Frontend Configuration

Edit `frontend/.env`:

```env
REACT_APP_API_URL=http://localhost:8000
```

## Testing

### Backend Tests

```bash
cd backend
pytest tests/test_auth.py -v
```

Test coverage includes:
- Successful signup
- Duplicate email handling
- Role-based signup
- Successful login
- Wrong password handling
- Non-existent user handling
- Getting current user with valid token
- Getting current user without token
- Getting current user with invalid token
- Logout functionality

### Manual Testing

1. **Start Backend:**
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

2. **Start Frontend:**
   ```bash
   cd frontend
   npm start
   ```

3. **Test Workflow:**
   - Visit http://localhost:3000
   - Click "Sign Up" and create an account
   - Try accessing protected routes
   - Log out and log back in
   - Test role-based access control

## Sample Credentials

When using the seed script:

```bash
cd backend
python -m app.db.seed
```

Sample accounts are created:
- **Admin:** admin@vibe.com / admin123
- **Coach:** coach@vibe.com / coach123
- **Client:** client@vibe.com / client123

## Common Issues

### Token Expiration
If you get "Could not validate credentials" errors, your token may have expired. Log out and log back in.

### CORS Errors
Make sure your frontend URL is in the `ALLOWED_ORIGINS` list in backend configuration.

### 401 Unauthorized
Check that:
1. You're logged in
2. Your token is valid
3. The Authorization header is properly formatted: `Bearer <token>`

### 403 Forbidden
You don't have the required role to access the endpoint. Check the role requirements.

## Future Enhancements

Potential improvements to the authentication system:

- [ ] Token refresh mechanism
- [ ] Email verification
- [ ] Password reset flow
- [ ] Two-factor authentication (2FA)
- [ ] OAuth integration (Google, GitHub)
- [ ] Rate limiting on auth endpoints
- [ ] Session management on backend
- [ ] Token blacklisting for revocation
- [ ] Remember me functionality
- [ ] Account lockout after failed attempts

## Resources

- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [JWT.io](https://jwt.io/) - JWT token decoder
- [bcrypt](https://github.com/pyca/bcrypt/) - Password hashing
- [python-jose](https://python-jose.readthedocs.io/) - JWT for Python
