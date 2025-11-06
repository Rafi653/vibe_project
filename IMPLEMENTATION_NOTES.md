# Implementation Notes: Access Token Handling and Home Page Experience

## Overview
This document describes the changes made to improve access token handling and enhance the home page experience for the Vibe Fitness application.

## Changes Implemented

### 1. Backend Changes

#### Token Expiration Time (1 hour)
- **File Modified:** `backend/app/core/config.py`
  - Changed `ACCESS_TOKEN_EXPIRE_MINUTES` from 30 to 60
- **File Modified:** `backend/.env.example`
  - Updated default value to 60 minutes
- **File Modified:** `AUTHENTICATION.md`
  - Updated documentation to reflect 1 hour token expiration

### 2. Frontend Changes

#### Automatic Token Expiration Handling
- **New File:** `frontend/src/services/apiClient.js`
  - Created a global API client wrapper
  - Detects 401 errors (token expiration) across all API calls
  - Provides a callback mechanism for handling token expiration

- **File Modified:** `frontend/src/services/authService.js`
  - Updated all API calls to use the new `apiFetch` wrapper
  - Automatically triggers logout on 401 errors

- **File Modified:** `frontend/src/context/AuthContext.js`
  - Registers token expiration callback on mount
  - Handles automatic logout when token expires
  - Redirects user to home page (/) after token expiry
  - Clears all authentication state on expiration

#### Conditional CTA Display
- **File Modified:** `frontend/src/pages/common/Home.js`
  - Added `useAuth` hook to access authentication state
  - Wrapped "Ready to Start Your Journey?" CTA section with conditional rendering
  - CTA is hidden when `isAuthenticated` is true

- **File Modified:** `frontend/src/pages/common/FeatureDetails.js`
  - Added `useAuth` hook to access authentication state
  - Wrapped "Ready to Get Started?" CTA section with conditional rendering
  - CTA is hidden when `isAuthenticated` is true

## How It Works

### Token Expiration Flow
1. User makes an API request with an expired token
2. Backend returns 401 Unauthorized
3. `apiClient.js` intercepts the 401 response
4. Calls the registered callback in `AuthContext`
5. `AuthContext` clears local storage and state
6. User is redirected to home page (/)
7. An error message is set: "Your session has expired. Please log in again."

### CTA Display Logic
- **When logged out:** Users see signup/login CTAs on home and feature pages
- **When logged in:** CTAs are hidden, users see only the main content
- Home page remains publicly accessible in both states

## Testing

### Backend Tests
- All security tests pass (9/9)
- All auth tests pass (10/10)
- Token creation and expiration validation work correctly

### Frontend Build
- Build completed successfully without errors
- No linting issues
- Bundle size: ~159 KB (gzipped)

## Benefits

1. **Better Security:** 1-hour token life provides better balance between security and UX
2. **Improved UX:** Users aren't repeatedly logged out during active sessions
3. **Automatic Session Management:** Token expiry is handled automatically without user intervention
4. **Cleaner UI:** Logged-in users don't see redundant signup prompts
5. **Public Landing Page:** Home page remains accessible to all visitors

## Verification Steps

To verify these changes work:

1. **Token Expiration:**
   - Log in to the application
   - Wait for token to expire (or manually set a short expiry time for testing)
   - Make any API request
   - Verify user is automatically logged out and redirected to home

2. **CTA Display:**
   - Visit home page without logging in → CTA should be visible
   - Log in to the application
   - Visit home page → CTA should be hidden
   - Visit any feature page → CTA should be hidden
   - Log out
   - Visit home or feature page → CTA should be visible again

3. **Protected Routes:**
   - Log in to the application
   - Navigate to a protected route (e.g., /client, /coach, /admin)
   - Let token expire
   - Try to access the protected route → Should be redirected to login
