#!/bin/bash
# Database migration helper script

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if alembic is available
if ! command -v alembic &> /dev/null; then
    echo -e "${RED}Error: alembic not found. Please activate your virtual environment.${NC}"
    exit 1
fi

# Function to display usage
usage() {
    echo "Usage: $0 {upgrade|downgrade|current|history|revision|autogenerate} [options]"
    echo ""
    echo "Commands:"
    echo "  upgrade [revision]    - Upgrade to a later version (default: head)"
    echo "  downgrade [revision]  - Revert to a previous version (default: -1)"
    echo "  current              - Display current revision"
    echo "  history              - List migration history"
    echo "  revision <message>   - Create a new blank migration"
    echo "  autogenerate <msg>   - Auto-generate migration from model changes"
    echo ""
    echo "Examples:"
    echo "  $0 upgrade           # Upgrade to latest"
    echo "  $0 downgrade         # Downgrade by one version"
    echo "  $0 current           # Show current version"
    echo "  $0 autogenerate \"add user phone\" # Auto-create migration"
    exit 1
}

# Check arguments
if [ $# -eq 0 ]; then
    usage
fi

COMMAND=$1

case $COMMAND in
    upgrade)
        REVISION=${2:-head}
        echo -e "${GREEN}Upgrading database to: $REVISION${NC}"
        alembic upgrade "$REVISION"
        echo -e "${GREEN}✓ Database upgraded successfully!${NC}"
        ;;
    
    downgrade)
        REVISION=${2:--1}
        echo -e "${YELLOW}Downgrading database to: $REVISION${NC}"
        alembic downgrade "$REVISION"
        echo -e "${GREEN}✓ Database downgraded successfully!${NC}"
        ;;
    
    current)
        echo -e "${GREEN}Current database revision:${NC}"
        alembic current
        ;;
    
    history)
        echo -e "${GREEN}Migration history:${NC}"
        alembic history --verbose
        ;;
    
    revision)
        if [ -z "$2" ]; then
            echo -e "${RED}Error: Please provide a message for the migration${NC}"
            echo "Example: $0 revision \"add user phone number\""
            exit 1
        fi
        echo -e "${GREEN}Creating new migration: $2${NC}"
        alembic revision -m "$2"
        echo -e "${GREEN}✓ Migration created successfully!${NC}"
        ;;
    
    autogenerate)
        if [ -z "$2" ]; then
            echo -e "${RED}Error: Please provide a message for the migration${NC}"
            echo "Example: $0 autogenerate \"add user phone number\""
            exit 1
        fi
        echo -e "${GREEN}Auto-generating migration: $2${NC}"
        alembic revision --autogenerate -m "$2"
        echo -e "${GREEN}✓ Migration auto-generated successfully!${NC}"
        echo -e "${YELLOW}⚠ Please review the generated migration file before applying!${NC}"
        ;;
    
    *)
        echo -e "${RED}Error: Unknown command '$COMMAND'${NC}"
        usage
        ;;
esac
