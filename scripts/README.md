# Scripts Directory

This directory contains utility scripts for the Vibe Fitness Platform.

## Available Scripts

### start-ngrok.sh

Starts ngrok tunnels for public app sharing.

**Purpose:**
- Exposes local frontend (port 3000) and backend (port 8000) to the internet
- Enables easy sharing with testers and friends
- Useful for mobile device testing and remote collaboration

**Usage:**
```bash
# From project root
./scripts/start-ngrok.sh
```

**Prerequisites:**
- ngrok installed (see [NGROK_SETUP.md](../NGROK_SETUP.md))
- App running on ports 3000 (frontend) and 8000 (backend)
- ngrok.yml configured with your auth token

**What it does:**
1. Checks if ngrok is installed
2. Validates ngrok.yml configuration
3. Warns if auth token is not set
4. Starts both frontend and backend tunnels

**See Also:**
- [NGROK_SETUP.md](../NGROK_SETUP.md) - Complete ngrok setup guide
- [QUICK_START.md](../QUICK_START.md) - Getting started guide

## Adding New Scripts

When adding new scripts to this directory:

1. Make them executable: `chmod +x script-name.sh`
2. Add shebang line: `#!/bin/bash`
3. Include helpful comments and error messages
4. Document in this README
5. Follow the existing naming convention (kebab-case)
6. Add usage examples

## Script Conventions

- **Location:** All project-wide scripts go here
- **Naming:** Use kebab-case (e.g., `start-ngrok.sh`)
- **Permissions:** Executable (`chmod +x`)
- **Documentation:** Add description to this README
- **Error Handling:** Include helpful error messages
- **Dependencies:** Check for required tools before running
