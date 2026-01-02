# Renovate Platform

An open-source platform for managing self-hosted Renovate installations with a modern UI and GraphQL API.

## Features

- **Pull Request Dashboard**: View all open Renovate PRs across all repositories in one place
- **GraphQL API**: Programmatic access to repositories and pull requests via Strawberry GraphQL
- **Gitea Integration**: Built-in Git server for testing Renovate workflows
- **Docker-based**: Easy deployment with Docker Compose
- **Auto-refresh**: Dashboard updates automatically every 30 seconds

## Quick Start

```bash
# Clone the repository
git clone https://github.com/your-org/renovate-platform.git
cd renovate-platform

# Copy environment template
cp .env.example .env

# Build and start all services
docker compose build
docker compose up -d

# Access the services
# UI: http://localhost:3000
# API: http://localhost:5000
# GraphQL: http://localhost:5000/graphql
# Gitea: http://localhost:3001
```

## Architecture

| Service | Port | Description |
|---------|------|-------------|
| UI | 3000 | React frontend with PR dashboard |
| API | 5000 | Flask + Strawberry GraphQL |
| Database | 5432 | PostgreSQL |
| Gitea | 3001 | Git server for testing |

## UI Features

### Pull Request Dashboard

The main dashboard displays all open pull requests from Renovate across your repositories:

- View PR title, repository, and branch information
- Click to open PR directly in Gitea
- Auto-refreshes every 30 seconds
- Manual refresh button available

## Development

All services support hot reload for development:

- **API**: Python files auto-reload on save
- **UI**: React dev server with HMR

### Local Documentation

To run documentation locally:

```bash
pip install mkdocs-material
mkdocs serve
```

Then visit http://localhost:8000
