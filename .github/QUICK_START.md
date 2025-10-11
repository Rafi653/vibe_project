# Quick Start: Creating Sub-Issues

This is a quick reference guide for creating the remaining sub-issues for the Vibe Project.

## What You Need to Create

6 sub-issues for steps 5-10 of the project roadmap:

- **Issue 7**: Authentication & Role-Based Access Control
- **Issue 8**: Core Features Implementation  
- **Issue 9**: Charts and Dashboards
- **Issue 10**: Dockerization
- **Issue 11**: Testing & Documentation
- **Issue 12**: Deployment Preparation

## How to Create Them

### Option 1: Automated (Easiest) 

```bash
cd .github
./create-sub-issues.sh
```

### Option 2: Python Script

```bash
cd .github
python3 create-sub-issues.py
```

### Option 3: Manual Creation

1. Go to https://github.com/Rafi653/vibe_project/issues/new
2. Open `ISSUE_TEMPLATES.md` in this directory
3. Copy the title and body for each issue (7-12)
4. Add the "enhancement" label
5. Submit

## Prerequisites

For automated creation:
- GitHub CLI (`gh`) installed
- Authenticated: `gh auth login`
- Write access to the repository

## What Happens Next

Once created, the issues will:
- Appear in the repository's issues list
- Be labeled as "enhancement"
- Reference the parent issue (#1)
- Show dependencies on prerequisite issues
- Provide clear tasks and acceptance criteria

## Need Help?

See the full documentation in `README.md` in this directory.
