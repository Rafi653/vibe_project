# Testing Guide

This document provides comprehensive information about testing in the Vibe Fitness Platform.

## Table of Contents
- [Overview](#overview)
- [Backend Testing](#backend-testing)
- [Frontend Testing](#frontend-testing)
- [Integration Testing](#integration-testing)
- [CI/CD Pipeline](#cicd-pipeline)
- [Writing Tests](#writing-tests)
- [Best Practices](#best-practices)

## Overview

The Vibe Fitness Platform uses a comprehensive testing strategy to ensure code quality and reliability.

### Test Coverage Goals
- **Backend**: 70%+ code coverage (currently: **70%**)
- **Frontend**: 60%+ code coverage
- **Critical Paths**: 100% coverage for authentication, authorization, and payment flows

### Testing Frameworks
- **Backend**: pytest with pytest-cov for coverage
- **Frontend**: Jest with React Testing Library
- **E2E**: (Future) Playwright or Cypress

## Backend Testing

### Running Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run tests with coverage
pytest --cov=app tests/

# Run tests with detailed coverage report
pytest --cov=app tests/ --cov-report=term-missing

# Run tests with HTML coverage report
pytest --cov=app tests/ --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run tests matching a pattern
pytest -k "test_login"

# Run tests in verbose mode
pytest -v

# Run tests in parallel (requires pytest-xdist)
pytest -n auto
```

### Test Structure

```
backend/tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── test_auth.py             # Authentication tests
├── test_client.py           # Client endpoint tests
├── test_coach.py            # Coach endpoint tests
├── test_admin.py            # Admin endpoint tests
├── test_users.py            # User endpoint tests
├── test_models.py           # Database model tests
├── test_services.py         # Service layer tests
├── test_dependencies.py     # Dependency injection tests
├── test_security.py         # Security function tests
├── test_database.py         # Database utility tests
├── test_integration.py      # Integration tests
└── test_health.py           # Health check tests
```

### Test Categories

#### Unit Tests
Test individual functions and methods in isolation:
- Models (test_models.py)
- Services (test_services.py)
- Security functions (test_security.py)
- Dependencies (test_dependencies.py)

#### API Tests
Test API endpoints:
- Authentication (test_auth.py)
- Client operations (test_client.py)
- Coach operations (test_coach.py)
- Admin operations (test_admin.py)
- User management (test_users.py)

#### Integration Tests
Test complete workflows:
- Full user workflows (test_integration.py)
- Authentication flows
- Role-based access control
- Data isolation
- CRUD operations

### Writing Backend Tests

Example test structure:

```python
"""
Tests for specific feature
"""

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.fixture
async def test_user(test_db):
    """Create a test user fixture"""
    user = User(email="test@example.com", ...)
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    return user

@pytest.mark.asyncio
async def test_feature(test_user):
    """Test a specific feature"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(
            "/api/v1/endpoint",
            headers={"Authorization": f"Bearer {token}"}
        )
    
    assert response.status_code == 200
    assert response.json()["key"] == "expected_value"
```

### Test Database

Tests use an in-memory SQLite database that is:
- Created fresh for each test
- Isolated from production data
- Automatically cleaned up after tests

## Frontend Testing

### Running Frontend Tests

```bash
cd frontend

# Run tests in watch mode
npm test

# Run tests once
CI=true npm test

# Run tests with coverage
npm test -- --coverage --watchAll=false

# Run tests in verbose mode
npm test -- --verbose

# Run specific test file
npm test -- Login.test.js

# Update snapshots
npm test -- -u
```

### Test Structure

```
frontend/src/
├── App.test.js              # Main app tests
├── setupTests.js            # Test configuration
└── components/
    └── *.test.js            # Component tests
```

### Writing Frontend Tests

Example component test:

```javascript
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Login from './Login';

describe('Login Component', () => {
  test('renders login form', () => {
    render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>
    );
    
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
  });
  
  test('handles form submission', async () => {
    render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>
    );
    
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'test@example.com' }
    });
    
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'password123' }
    });
    
    fireEvent.click(screen.getByRole('button', { name: /login/i }));
    
    // Add assertions
  });
});
```

## Integration Testing

Integration tests verify that different parts of the system work together correctly.

### Authentication Flow Integration Test

```python
@pytest.mark.asyncio
async def test_full_client_workflow():
    """Test complete client workflow: signup -> login -> create logs -> get progress"""
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 1. Signup
        signup_response = await ac.post("/api/v1/auth/signup", json={...})
        token = signup_response.json()["access_token"]
        
        # 2. Create workout log
        workout_response = await ac.post(
            "/api/v1/client/workout-logs",
            headers={"Authorization": f"Bearer {token}"},
            json={...}
        )
        
        # 3. Get progress
        progress_response = await ac.get(
            "/api/v1/client/progress",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert progress_response.status_code == 200
```

## CI/CD Pipeline

### GitHub Actions

The project uses GitHub Actions for continuous integration and testing.

#### Workflow: `.github/workflows/tests.yml`

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

**Jobs:**
1. **Backend Tests**: Run pytest with coverage
2. **Frontend Tests**: Run Jest with coverage
3. **Linting**: Run code quality checks

#### Coverage Reporting

Coverage reports are uploaded to Codecov after each test run:
- Backend coverage tracked separately
- Frontend coverage tracked separately
- Historical coverage trends available

### Local CI Simulation

Run the same checks locally before pushing:

```bash
# Backend
cd backend
pytest --cov=app tests/ --cov-report=term

# Frontend
cd frontend
CI=true npm test -- --coverage --watchAll=false

# Linting
cd backend
flake8 app --count --select=E9,F63,F7,F82
black --check app
isort --check-only app
```

## Writing Tests

### Test Naming Conventions

- **File names**: `test_<feature>.py` or `<Component>.test.js`
- **Test functions**: `test_<action>_<expected_result>`
- **Fixtures**: Descriptive names like `test_user`, `client_token`

Examples:
- `test_signup_success`
- `test_login_with_wrong_password`
- `test_get_workout_logs_unauthorized`

### Test Organization

1. **Arrange**: Set up test data and preconditions
2. **Act**: Execute the code being tested
3. **Assert**: Verify the expected outcomes

```python
@pytest.mark.asyncio
async def test_create_workout_log(client_token):
    # Arrange
    workout_data = {
        "exercise_name": "Squats",
        "sets": 3,
        "reps": 10
    }
    
    # Act
    response = await ac.post(
        "/api/v1/client/workout-logs",
        headers={"Authorization": f"Bearer {client_token}"},
        json=workout_data
    )
    
    # Assert
    assert response.status_code == 201
    assert response.json()["exercise_name"] == "Squats"
```

### Using Fixtures

Fixtures provide reusable test data and setup:

```python
@pytest.fixture
async def admin_user(test_db):
    """Create an admin user for testing"""
    user = User(
        email="admin@example.com",
        role=UserRole.ADMIN,
        is_active=True
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    return user

@pytest.fixture
def admin_token(admin_user):
    """Create an access token for the admin user"""
    return create_access_token({
        "sub": admin_user.email,
        "user_id": admin_user.id
    })
```

## Best Practices

### General

1. **Write tests first** (TDD): Consider writing tests before implementation
2. **Test behavior, not implementation**: Focus on what the code does, not how
3. **Keep tests simple**: Each test should verify one thing
4. **Use descriptive names**: Test names should explain what is being tested
5. **Avoid test interdependence**: Tests should run independently
6. **Mock external dependencies**: Don't rely on external services in tests

### Backend Testing

1. **Use async/await**: All test functions should be async
2. **Clean up after tests**: Use fixtures that automatically clean up
3. **Test error cases**: Don't just test the happy path
4. **Use appropriate HTTP status codes**: Verify exact status codes
5. **Test authentication**: Verify auth is required where expected
6. **Test authorization**: Verify role-based access control

### Frontend Testing

1. **Test user interactions**: Use `fireEvent` or `userEvent`
2. **Query by accessibility**: Use `getByRole`, `getByLabelText`
3. **Avoid implementation details**: Don't test internal state
4. **Test async behavior**: Use `waitFor` for async operations
5. **Mock API calls**: Use `jest.mock()` or MSW
6. **Test error states**: Verify error handling

### Coverage Goals

Focus on covering:
- All API endpoints
- All business logic
- Authentication and authorization
- Error handling
- Edge cases
- Critical user workflows

Don't obsess over 100% coverage:
- Seed scripts and migrations don't need tests
- Simple getters/setters can be skipped
- Focus on behavior, not lines of code

### Continuous Improvement

1. **Review coverage reports**: Identify untested code
2. **Add tests for bugs**: Write a test that reproduces the bug
3. **Refactor tests**: Keep tests maintainable
4. **Update tests with code**: Tests should evolve with the codebase
5. **Document complex tests**: Add comments for non-obvious test logic

## Troubleshooting

### Common Issues

**Tests fail due to database connection**
```bash
# Ensure you're using the test database
# Check conftest.py configuration
```

**Frontend tests fail with module not found**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Coverage is lower than expected**
```bash
# Check which files are excluded in pyproject.toml or .coveragerc
# Ensure test files are in the correct location
```

**Tests hang or timeout**
```bash
# Check for unhandled async operations
# Increase timeout in pytest configuration
# Use pytest -vv to see which test is hanging
```

## Resources

### Documentation
- [pytest documentation](https://docs.pytest.org/)
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)

### Tools
- [pytest](https://pytest.org/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [Jest](https://jestjs.io/)
- [Codecov](https://codecov.io/)

## Getting Help

If you encounter issues with testing:
1. Check this documentation
2. Review existing tests for examples
3. Check test output for error messages
4. Ask the team for help

Remember: Good tests make refactoring safe and catch bugs early!
