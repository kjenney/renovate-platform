# Renovate Platform

An open-source platform for managing a self-hosted Renovate installation. This includes both a User Interface as well as an Application Programming Interface.

## Features

- **Pull Request Dashboard**: View all open Renovate PRs across repositories
- **GraphQL API**: Query repositories and pull requests programmatically
- **Gitea Integration**: Built-in Git server for testing Renovate
- **Docker-based**: Easy deployment with Docker Compose

## Quick Start

```bash
# Copy environment template
cp .env.example .env

# Build and start all services
docker compose build
docker compose up -d
```

## Services

| Service | URL | Description |
|---------|-----|-------------|
| UI | http://localhost:3000 | React dashboard |
| API | http://localhost:5000 | Flask + GraphQL |
| GraphQL | http://localhost:5000/graphql | Interactive playground |
| Gitea | http://localhost:3001 | Git server |

## Documentation

Documentation is hosted on GitHub Pages and auto-deployed on push to main.

For local development:
```bash
pip install mkdocs-material
mkdocs serve
```

Then visit http://localhost:8000

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
