# Renovate Platform

## Project Overview
Platform for managing self-hosted Renovate installations with UI and API.

## Tech Stack
- Language: Python
- Framework: Flask
- Frontend: React
- Database: PostgreSQL
- API style: GraphQL - using Strawberry
- Documentation: mkdocs
- Git testing: Gitea

## Build & Run Commands
- Install: `docker compose build`
- Dev server: `docker compose up -d`
- Run Renovate: `docker compose --profile renovate up renovate`
- Test: pytest
- Lint: `pylint ./**/*.py`
- Docs (local): `mkdocs serve`

## Local Python Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r scripts/requirements.txt
pip install mkdocs-material  # for local docs development
```

## Utility Scripts
- Seed Gitea repos: `python scripts/seed_gitea.py --token <gitea-token>`

## Service Ports
| Service | Port | URL |
|---------|------|-----|
| React UI | 3000 | http://localhost:3000 |
| Flask API | 5000 | http://localhost:5000 |
| GraphQL | 5000 | http://localhost:5000/graphql |
| PostgreSQL | 5432 | localhost:5432 |
| Gitea | 3001 | http://localhost:3001 |
| Gitea SSH | 2222 | localhost:2222 |

## Project Structure
```
/src
  /api     - Flask API with Strawberry GraphQL
  /ui      - React frontend with Apollo Client
  /models  - Data models (dataclasses, convert to SQLAlchemy when needed)
/scripts   - Utility scripts (seed_gitea.py)
/docs      - mkdocs documentation source
/renovate  - Renovate bot configuration
/.github   - GitHub Actions workflows
/venv      - Python virtual environment (gitignored)
mkdocs.yml - Documentation configuration
```

## Architecture Decisions

### Docker Compose Services
- **api**: Python 3.12-slim with Flask + Strawberry GraphQL, hot reload enabled
- **ui**: Node 20-alpine with React 18 + Apollo Client, hot reload via polling
- **db**: PostgreSQL 16-alpine with persistent volume
- **gitea**: Latest Gitea with SQLite (simpler than shared PostgreSQL)
- **renovate**: Self-hosted Renovate bot (runs via `--profile renovate`)

### Documentation
- mkdocs-material hosted on GitHub Pages
- Local development: `mkdocs serve` (requires `pip install mkdocs-material`)
- Auto-deployed on push to main via GitHub Actions

### Configuration
- Environment variables via `.env` file (copy from `.env.example`)
- Default dev credentials provided for local development
- Health checks on API and database with proper service dependencies
- UI waits for API health before starting

### Gitea Setup
- Uses SQLite for simplicity (no shared database with main app)
- Default admin credentials configured via environment variables
- Requires manual token generation for Renovate integration

## Conventions
- Naming: snake_case
- Error handling approach: EAFP
- Testing requirements: Include tests for all functionality. Include installing Renovatebot locally in a container.

## Useful Claude Code Enhancements for this project

### Hooks (Auto-run commands)

Add to .claude/settings.json to auto-run linting/formatting after edits:

{
"hooks": {
    "postToolExecution": [
    {
        "matcher": "Edit|Write",
        "command": "pylint ${file} --exit-zero"
    }
    ]
}
}

### Custom Skills

Create /Users/kjenney/.claude/skills/ with custom slash commands. Example for your stack:

docker-logs.md - Quick container log access:
---
name: docker-logs
description: View logs from docker compose services
---
Run `docker compose logs --tail=50 ${service:-}` to show recent logs.

Also Consider

- Playwright MCP - useful for testing your React UI



