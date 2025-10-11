# Contributing to Vibe Fitness Platform

Thank you for your interest in contributing to the Vibe Fitness Platform! This document provides guidelines and instructions for contributing to the project.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Submitting Changes](#submitting-changes)
- [Review Process](#review-process)

## Code of Conduct

### Our Pledge
We are committed to providing a welcoming and inclusive environment for all contributors.

### Expected Behavior
- Be respectful and professional
- Welcome newcomers and help them get started
- Accept constructive criticism gracefully
- Focus on what is best for the project
- Show empathy towards other community members

### Unacceptable Behavior
- Harassment, discrimination, or offensive comments
- Personal attacks or insults
- Publishing others' private information
- Any conduct that could be considered inappropriate in a professional setting

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

**Backend:**
- Python 3.11 or higher
- pip (Python package manager)
- PostgreSQL 16+ (or Docker)

**Frontend:**
- Node.js 18 or higher
- npm or yarn

**Tools:**
- Git
- Docker and Docker Compose (recommended)

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/vibe_project.git
   cd vibe_project
   ```

3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/Rafi653/vibe_project.git
   ```

4. Create a new branch for your work:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy the environment file:
   ```bash
   cp .env.example .env
   ```

5. Start the database (using Docker):
   ```bash
   cd ..
   docker-compose up -d db
   ```

6. Run database migrations:
   ```bash
   cd backend
   alembic upgrade head
   ```

7. Start the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at http://localhost:8000

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Copy the environment file:
   ```bash
   cp .env.example .env
   ```

4. Start the development server:
   ```bash
   npm start
   ```

   The app will be available at http://localhost:3000

### Docker Setup (Recommended)

For a complete setup using Docker:

```bash
# Start all services
docker-compose up

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

See [DOCKER_SETUP.md](DOCKER_SETUP.md) for detailed Docker instructions.

## Development Workflow

### 1. Check for Existing Issues

Before starting work, check if an issue exists for your planned changes:
- Browse [existing issues](https://github.com/Rafi653/vibe_project/issues)
- If no issue exists, create one to discuss your proposed changes

### 2. Create a Branch

Create a new branch from `main`:

```bash
git checkout main
git pull upstream main
git checkout -b type/description
```

Branch naming conventions:
- `feature/feature-name` - New features
- `fix/bug-name` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring
- `test/description` - Adding or updating tests

### 3. Make Your Changes

- Write clean, readable code
- Follow the project's coding standards
- Add tests for new functionality
- Update documentation as needed
- Keep commits atomic and focused

### 4. Test Your Changes

Before submitting:

**Backend:**
```bash
cd backend
pytest --cov=app tests/
```

**Frontend:**
```bash
cd frontend
npm test
npm run build  # Ensure build succeeds
```

**Linting:**
```bash
# Backend
cd backend
flake8 app
black --check app
isort --check-only app

# Frontend
cd frontend
npm run lint
```

### 5. Commit Your Changes

Write clear, descriptive commit messages:

```bash
git add .
git commit -m "feat: add user profile update functionality"
```

Commit message format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Adding or updating tests
- `refactor:` - Code refactoring
- `style:` - Formatting changes
- `chore:` - Maintenance tasks

### 6. Push and Create Pull Request

```bash
git push origin your-branch-name
```

Then create a pull request on GitHub.

## Coding Standards

### Python (Backend)

#### Code Style

Follow **PEP 8** with these specific guidelines:

- **Line length**: 100 characters maximum
- **Indentation**: 4 spaces
- **Quotes**: Double quotes for strings
- **Imports**: Group and sort imports (use `isort`)

```python
# Good
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.models.user import User


# Function definition
async def get_user_profile(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    """
    Get a user's profile.
    
    Args:
        user_id: The ID of the user
        db: Database session
        current_user: The authenticated user
        
    Returns:
        UserResponse containing user data
        
    Raises:
        HTTPException: If user not found
    """
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.model_validate(user)
```

#### Type Hints

Always use type hints:

```python
# Good
def calculate_bmi(weight: float, height: float) -> float:
    return weight / (height ** 2)

# Avoid
def calculate_bmi(weight, height):
    return weight / (height ** 2)
```

#### Async/Await

Use async/await for I/O operations:

```python
# Good
async def get_users(db: AsyncSession) -> List[User]:
    result = await db.execute(select(User))
    return result.scalars().all()

# Avoid
def get_users(db: Session) -> List[User]:
    return db.query(User).all()
```

#### Error Handling

Use appropriate HTTP exceptions:

```python
from fastapi import HTTPException, status

# Good
if not user.is_active:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="User account is inactive"
    )
```

### JavaScript/React (Frontend)

#### Code Style

- **Indentation**: 2 spaces
- **Quotes**: Single quotes for strings
- **Semicolons**: Optional but be consistent
- **Component names**: PascalCase
- **File names**: Match component names

```javascript
// Good
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const UserProfile = ({ userId }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchUser();
  }, [userId]);

  const fetchUser = async () => {
    try {
      setLoading(true);
      const data = await userService.getUser(userId);
      setUser(data);
    } catch (error) {
      console.error('Failed to fetch user:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (!user) return <div>User not found</div>;

  return (
    <div className="user-profile">
      <h2>{user.name}</h2>
      <p>{user.email}</p>
    </div>
  );
};

export default UserProfile;
```

#### Component Structure

1. Imports
2. Component definition
3. State and hooks
4. Event handlers
5. Effects
6. Helper functions
7. Render/return

#### Naming Conventions

- **Components**: `UserProfile`, `LoginForm`
- **Hooks**: `useAuth`, `useFetchData`
- **Event handlers**: `handleClick`, `handleSubmit`
- **Boolean props**: `isLoading`, `hasError`

### API Design

#### Endpoint Naming

- Use nouns for resources: `/api/v1/users`, `/api/v1/workouts`
- Use HTTP methods for actions: GET, POST, PUT, DELETE
- Use kebab-case for URLs: `/api/v1/workout-plans`
- Version your API: `/api/v1/...`

#### Response Format

```json
{
  "status": "success",
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com"
    }
  }
}
```

For errors:

```json
{
  "status": "error",
  "message": "User not found",
  "code": "USER_NOT_FOUND"
}
```

### Database

#### Model Naming

- Model classes: Singular PascalCase (`User`, `WorkoutPlan`)
- Table names: Plural snake_case (`users`, `workout_plans`)
- Foreign keys: `user_id`, `workout_plan_id`

#### Migrations

Create migrations for schema changes:

```bash
alembic revision --autogenerate -m "Add workout_plans table"
alembic upgrade head
```

## Testing Guidelines

### Test Coverage

- **Minimum**: 70% for backend, 60% for frontend
- **Focus**: Critical paths should have 100% coverage
- **Priority**: Authentication, authorization, data integrity

### Writing Tests

See [TESTING.md](TESTING.md) for detailed testing guidelines.

Quick checklist:
- [ ] All new features have tests
- [ ] All bug fixes have regression tests
- [ ] Tests are clear and well-named
- [ ] Tests run quickly (< 5 seconds per test)
- [ ] Tests are independent and can run in any order

### Running Tests Locally

```bash
# Backend
cd backend
pytest --cov=app tests/ -v

# Frontend
cd frontend
npm test -- --coverage
```

## Submitting Changes

### Before Submitting

Checklist:
- [ ] Code follows project standards
- [ ] All tests pass
- [ ] Coverage meets requirements
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] Branch is up to date with main

### Pull Request Process

1. **Update your branch**:
   ```bash
   git checkout main
   git pull upstream main
   git checkout your-branch
   git rebase main
   ```

2. **Create Pull Request**:
   - Use a clear, descriptive title
   - Reference related issues
   - Describe what changed and why
   - Include screenshots for UI changes
   - Add testing instructions

3. **PR Template**:
   ```markdown
   ## Description
   Brief description of changes
   
   ## Related Issue
   Fixes #123
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update
   
   ## Testing
   - [ ] Unit tests added/updated
   - [ ] Integration tests added/updated
   - [ ] Manual testing performed
   
   ## Screenshots (if applicable)
   
   ## Checklist
   - [ ] Code follows project standards
   - [ ] Tests pass locally
   - [ ] Documentation updated
   ```

## Review Process

### What to Expect

1. **Initial Review**: Within 2-3 business days
2. **Feedback**: Reviewers may request changes
3. **Discussion**: Be open to feedback and discussion
4. **Approval**: Changes approved by at least one maintainer
5. **Merge**: Maintainer will merge the PR

### Responding to Feedback

- Address all comments
- Ask questions if something is unclear
- Update the PR with requested changes
- Mark conversations as resolved when addressed

### After Merge

1. Delete your branch:
   ```bash
   git branch -d your-branch-name
   git push origin --delete your-branch-name
   ```

2. Update your fork:
   ```bash
   git checkout main
   git pull upstream main
   git push origin main
   ```

## Project Structure

```
vibe_project/
├── backend/                # FastAPI backend
│   ├── app/
│   │   ├── api/           # API routes
│   │   ├── core/          # Core utilities
│   │   ├── models/        # Database models
│   │   ├── schemas/       # Pydantic schemas
│   │   └── services/      # Business logic
│   ├── tests/             # Backend tests
│   └── alembic/           # Database migrations
├── frontend/              # React frontend
│   ├── public/
│   └── src/
│       ├── components/    # React components
│       ├── pages/         # Page components
│       ├── services/      # API services
│       └── context/       # React context
└── docs/                  # Documentation

```

## Getting Help

### Resources

- **Documentation**: Check the docs/ directory
- **Issues**: Browse or create [GitHub issues](https://github.com/Rafi653/vibe_project/issues)
- **Discussions**: Use GitHub Discussions for questions

### Communication

- Be respectful and professional
- Provide context and details
- Search for existing answers first
- Share what you've tried

## License

By contributing, you agree that your contributions will be licensed under the project's license.

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions

Thank you for contributing to Vibe Fitness Platform! 🎉
