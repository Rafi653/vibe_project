#!/usr/bin/env python3
"""
Script to create remaining sub-issues for the Fitness Coaching App project.
This script creates issues 7-12 as outlined in the parent issue #1.

Requirements:
    - Python 3.6+
    - requests library: pip install requests
    - GitHub Personal Access Token with 'repo' scope

Usage:
    python create-sub-issues.py
    
    Set the GITHUB_TOKEN environment variable or provide it when prompted.
"""

import os
import sys
import subprocess
from typing import Dict, List

REPO_OWNER = "Rafi653"
REPO_NAME = "vibe_project"
PARENT_ISSUE = 1

# Issue definitions
ISSUES = [
    {
        "number": 7,
        "title": "Authentication & Role-Based Access Control",
        "body": """Implement user authentication and role-based access control for the fitness coaching platform.

### Tasks:
- Implement signup/login/logout endpoints in the backend API
- Set up JWT-based authentication with secure token management
- Define three user roles: client, coach, and admin
- Implement role-based middleware for route protection
- Add password hashing and security best practices
- Create authentication UI components (login, signup, logout)
- Implement protected routes in the frontend based on user roles
- Add session management and token refresh logic

### Acceptance Criteria:
- Users can sign up with email/password and select their role
- Users can log in and receive a JWT token
- API endpoints are protected based on user roles
- Frontend routes are protected and redirect unauthorized users
- Passwords are securely hashed and stored
- Token expiration and refresh mechanisms are in place

### Context:
This is step 5 in the [Project Initialization and Enhancement Sequence for Fitness Coaching App](https://github.com/{repo_owner}/{repo_name}/issues/{parent_issue}).

**Dependencies:** Issues #4 (Backend Framework), #5 (Frontend Framework), #6 (Database Setup)"""
    },
    {
        "number": 8,
        "title": "Core Features Implementation",
        "body": """Implement the core features for all three user roles: client, coach, and admin.

### Tasks:

#### Client Features:
- Log workouts and diet entries
- View personal workout and diet logs
- Track progress metrics (weight, measurements, etc.)
- View assigned coach and workout/diet plans
- Update profile information

#### Coach Features:
- View assigned clients list
- Review client workout and diet logs
- Assign workout and diet plans to clients
- Track client progress and provide feedback
- Manage workout and diet plan templates

#### Admin Features:
- Manage all users (view, edit, delete)
- Assign coaches to clients
- View platform-wide metrics and usage statistics
- Manage system settings and configurations
- Generate reports

### Acceptance Criteria:
- All client features are functional and tested
- All coach features are functional and tested
- All admin features are functional and tested
- Features respect role-based access control
- UI is intuitive and user-friendly for each role
- Data validation is implemented on both frontend and backend

### Context:
This is step 6 in the [Project Initialization and Enhancement Sequence for Fitness Coaching App](https://github.com/{repo_owner}/{repo_name}/issues/{parent_issue}).

**Dependencies:** Issue #7 (Authentication & Role-Based Access Control)"""
    },
    {
        "number": 9,
        "title": "Charts and Dashboards",
        "body": """Integrate charting libraries and create dashboards for progress tracking and metrics visualization.

### Tasks:
- Choose and integrate a charting library (e.g., Chart.js, Recharts, D3.js)
- Create client dashboard with:
  - Progress charts (weight, body measurements over time)
  - Workout frequency and consistency graphs
  - Diet adherence metrics
  - Goal tracking visualizations
- Create coach dashboard with:
  - Client overview and progress summaries
  - Client engagement metrics
  - Plan assignment tracking
- Create admin dashboard with:
  - Platform usage statistics
  - User growth metrics
  - Coach performance metrics
  - System health indicators
- Make dashboards responsive and mobile-friendly
- Add export functionality for charts (PDF, PNG)

### Acceptance Criteria:
- Interactive charts are displayed on all role-specific dashboards
- Data is fetched efficiently from the backend API
- Charts update in real-time or near real-time
- Dashboards are responsive across devices
- Users can filter and customize chart views
- Performance is optimized for large datasets

### Context:
This is step 7 in the [Project Initialization and Enhancement Sequence for Fitness Coaching App](https://github.com/{repo_owner}/{repo_name}/issues/{parent_issue}).

**Dependencies:** Issue #8 (Core Features Implementation)"""
    },
    {
        "number": 10,
        "title": "Dockerization",
        "body": """Containerize the application components using Docker for consistent development and deployment.

### Tasks:
- Write Dockerfile for backend service
  - Include all dependencies and environment setup
  - Optimize for production use
- Write Dockerfile for frontend service
  - Include build process and serve configuration
  - Optimize image size
- Write Dockerfile for PostgreSQL database (or use official image)
  - Include initialization scripts
  - Configure volume mounting for data persistence
- Create docker-compose.yml for multi-container orchestration
  - Define all services (backend, frontend, database, redis if needed)
  - Configure networking between containers
  - Set up environment variables
  - Configure volume mounts
- Add .dockerignore files to exclude unnecessary files
- Update README.md with Docker instructions:
  - How to build and run containers locally
  - How to use docker-compose for development
  - Common Docker commands and troubleshooting
- Add health checks for services
- Configure development vs production Docker setups

### Acceptance Criteria:
- All services can be started with `docker-compose up`
- Containers communicate properly with each other
- Database data persists across container restarts
- Hot-reload works for development
- Documentation is clear and comprehensive
- Docker images are optimized for size and performance

### Context:
This is step 8 in the [Project Initialization and Enhancement Sequence for Fitness Coaching App](https://github.com/{repo_owner}/{repo_name}/issues/{parent_issue}).

**Dependencies:** Issues #4 (Backend), #5 (Frontend), #6 (Database)"""
    },
    {
        "number": 11,
        "title": "Testing & Documentation",
        "body": """Set up comprehensive testing infrastructure and complete project documentation.

### Tasks:

#### Testing:
- Set up unit testing framework for backend (e.g., pytest, Jest)
- Write unit tests for:
  - API endpoints
  - Database models
  - Business logic functions
  - Authentication middleware
- Set up integration tests for:
  - API workflows
  - Database interactions
  - Authentication flows
- Set up frontend testing (e.g., Jest, React Testing Library)
- Write component tests for UI elements
- Add end-to-end testing setup (e.g., Cypress, Playwright)
- Configure test coverage reporting
- Add CI/CD integration for automated testing

#### Documentation:
- Complete API documentation:
  - Document all endpoints with request/response examples
  - Use OpenAPI/Swagger for interactive API docs
- Create architecture documentation:
  - System architecture diagrams
  - Database schema documentation
  - Authentication flow diagrams
- Write developer guides:
  - Setup instructions for new developers
  - Coding standards and conventions
  - Contribution guidelines
- Create user guides for each role
- Document deployment processes
- Add inline code comments where necessary

### Acceptance Criteria:
- Test coverage is at least 70% for backend code
- All critical paths have integration tests
- Frontend components have unit tests
- CI/CD pipeline runs tests automatically
- API documentation is complete and up-to-date
- Architecture is well-documented
- New developers can set up the project using documentation

### Context:
This is step 9 in the [Project Initialization and Enhancement Sequence for Fitness Coaching App](https://github.com/{repo_owner}/{repo_name}/issues/{parent_issue}).

**Dependencies:** All previous issues (comprehensive testing and documentation of all features)"""
    },
    {
        "number": 12,
        "title": "Deployment Preparation",
        "body": """Prepare the application for production deployment with production-ready configurations and deployment documentation.

### Tasks:

#### Production Docker Configuration:
- Create production-optimized Dockerfiles
- Set up multi-stage builds to reduce image sizes
- Configure production environment variables
- Add security hardening to containers
- Set up logging and monitoring in containers

#### Cloud Deployment Setup:
- Choose cloud provider (AWS, GCP, Heroku, DigitalOcean, etc.)
- Set up production database (managed PostgreSQL)
- Configure Redis for caching and sessions
- Set up file storage (S3 or equivalent)
- Configure CDN for static assets
- Set up SSL/TLS certificates
- Configure domain and DNS settings

#### CI/CD Pipeline:
- Set up GitHub Actions or similar for automated deployment
- Configure automatic builds on push to main branch
- Add automated testing before deployment
- Set up staging and production environments
- Configure rollback procedures

#### Monitoring and Logging:
- Set up application monitoring (e.g., New Relic, DataDog)
- Configure error tracking (e.g., Sentry)
- Set up log aggregation and analysis
- Add health check endpoints
- Configure alerts for critical issues

#### Security:
- Implement rate limiting
- Add CORS configuration
- Set up security headers
- Configure firewall rules
- Add backup and disaster recovery procedures

#### Documentation:
- Write deployment runbook with step-by-step instructions
- Document environment variables and secrets management
- Create troubleshooting guide for common deployment issues
- Document scaling procedures
- Add monitoring and alerting documentation

### Acceptance Criteria:
- Application can be deployed to production with one command
- CI/CD pipeline is fully automated
- Monitoring and logging are properly configured
- Security best practices are implemented
- Deployment documentation is complete and tested
- Rollback procedures are documented and tested
- Staging environment mirrors production

### Context:
This is step 10 in the [Project Initialization and Enhancement Sequence for Fitness Coaching App](https://github.com/{repo_owner}/{repo_name}/issues/{parent_issue}).

**Dependencies:** Issues #10 (Dockerization), #11 (Testing & Documentation)"""
    }
]


def create_issues_with_gh_cli():
    """Create issues using GitHub CLI (gh)."""
    print(f"Creating remaining sub-issues for the Fitness Coaching App...")
    print(f"Repository: {REPO_OWNER}/{REPO_NAME}")
    print(f"Parent Issue: #{PARENT_ISSUE}")
    print()
    
    # Check if gh is available
    try:
        subprocess.run(['gh', '--version'], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: GitHub CLI (gh) is not installed or not in PATH.")
        print("Please install it from: https://cli.github.com/")
        return False
    
    created_count = 0
    for issue in ISSUES:
        print(f"Creating Issue {issue['number']}: {issue['title']}...")
        
        # Format the body with actual values
        body = issue['body'].format(
            repo_owner=REPO_OWNER,
            repo_name=REPO_NAME,
            parent_issue=PARENT_ISSUE
        )
        
        try:
            result = subprocess.run(
                [
                    'gh', 'issue', 'create',
                    '--repo', f"{REPO_OWNER}/{REPO_NAME}",
                    '--title', issue['title'],
                    '--label', 'enhancement',
                    '--body', body
                ],
                check=True,
                capture_output=True,
                text=True
            )
            print(f"✓ Issue {issue['number']} created")
            print(f"  URL: {result.stdout.strip()}")
            created_count += 1
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to create issue {issue['number']}")
            print(f"  Error: {e.stderr}")
        
        print()
    
    print(f"\nCompleted: {created_count}/{len(ISSUES)} issues created successfully!")
    if created_count > 0:
        print(f"Please verify the created issues at: https://github.com/{REPO_OWNER}/{REPO_NAME}/issues")
    
    return created_count == len(ISSUES)


def main():
    """Main entry point."""
    print("=" * 70)
    print("GitHub Sub-Issue Creator for Vibe Project - Fitness Coaching App")
    print("=" * 70)
    print()
    
    success = create_issues_with_gh_cli()
    
    if success:
        print("\n✓ All issues created successfully!")
        sys.exit(0)
    else:
        print("\n✗ Some issues failed to create. Please check the output above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
