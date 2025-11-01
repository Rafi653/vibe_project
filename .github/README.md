# GitHub Issue Management

This directory contains templates and scripts for managing GitHub issues for the Vibe Project - Fitness Coaching App.

## Files

- **ISSUE_TEMPLATES.md**: Contains detailed templates for all remaining sub-issues (steps 5-10)
- **create-sub-issues.sh**: Shell script to automatically create all remaining sub-issues using GitHub CLI

## Creating Sub-Issues

### Method 1: Using the Automated Script (Recommended)

The easiest way to create all remaining sub-issues at once is to use the provided shell script:

```bash
# Navigate to the .github directory
cd .github

# Run the script (requires GitHub CLI to be installed and authenticated)
./create-sub-issues.sh
```

**Prerequisites:**
- GitHub CLI (`gh`) must be installed
- You must be authenticated with `gh auth login`
- You must have write access to the repository

### Method 2: Manual Creation

If you prefer to create issues manually or the automated script doesn't work:

1. Open the `ISSUE_TEMPLATES.md` file
2. For each issue template (7-12):
   - Go to https://github.com/Rafi653/vibe_project/issues/new
   - Copy the title from the template
   - Copy the body content (without the markdown code fences)
   - Add the "enhancement" label
   - Click "Submit new issue"

### Method 3: Using GitHub CLI Manually

You can also use the GitHub CLI to create issues one by one:

```bash
gh issue create \
  --repo Rafi653/vibe_project \
  --title "Authentication & Role-Based Access Control" \
  --label "enhancement" \
  --body "$(cat issue7_body.txt)"
```

## Issue Structure

Each sub-issue follows this structure:

- **Title**: Clear, concise description of the task
- **Tasks**: Bullet-pointed list of specific tasks to complete
- **Acceptance Criteria**: Clear criteria for when the issue can be considered complete
- **Context**: Reference to the parent issue and step number
- **Dependencies**: Links to prerequisite issues that should be completed first
- **Label**: "enhancement" to categorize as a feature request

## Issue Sequence

The recommended order for completing sub-issues:

1. ✅ **Issue #3**: Initialize Repository Structure (CLOSED)
2. ✅ **Issue #4**: Set Up Backend Framework (OPEN)
3. ✅ **Issue #5**: Set Up Frontend Framework (OPEN)
4. ✅ **Issue #6**: Database Setup (OPEN)
5. ⬜ **Issue #7**: Authentication & Role-Based Access Control (TO BE CREATED)
6. ⬜ **Issue #8**: Core Features Implementation (TO BE CREATED)
7. ⬜ **Issue #9**: Charts and Dashboards (TO BE CREATED)
8. ⬜ **Issue #10**: Dockerization (TO BE CREATED)
9. ⬜ **Issue #11**: Testing & Documentation (TO BE CREATED)
10. ⬜ **Issue #12**: Deployment Preparation (TO BE CREATED)

## Troubleshooting

### GitHub CLI Not Authenticated

If you get an authentication error:
```bash
gh auth login
```

Follow the prompts to authenticate with GitHub.

### Permission Denied

If you get a permission error when running the script:
```bash
chmod +x create-sub-issues.sh
```

### Script Fails to Create Issues

Check that:
1. You have write access to the repository
2. GitHub CLI is properly authenticated
3. You're connected to the internet
4. The repository name is correct in the script

## Contributing

When creating new issues or modifying templates:
1. Follow the established structure
2. Keep tasks specific and actionable
3. Include clear acceptance criteria
4. Reference dependencies and parent issues
5. Use appropriate labels

## Support

For questions or issues with the templates or scripts, please contact the project maintainers or open a discussion in the repository.
