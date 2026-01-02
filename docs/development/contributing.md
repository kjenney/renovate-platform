# Contributing

## Development Setup

1. Fork and clone the repository
2. Copy `.env.example` to `.env`
3. Run `docker compose up -d`

## Code Style

### Python

- Use snake_case for variables and functions
- Follow EAFP (Easier to Ask Forgiveness than Permission)
- Run linting: `pylint ./**/*.py`

### JavaScript/React

- Use functional components with hooks
- Use Apollo Client for GraphQL

## Testing

Run tests with pytest:

```bash
docker compose exec api pytest
```

## Pull Requests

1. Create a feature branch
2. Write tests for new functionality
3. Ensure linting passes
4. Submit a pull request

## Project Structure

```
/src
  /api     - Flask API endpoints
  /ui      - React frontend components
  /models  - Data models
/docs      - mkdocs documentation
/renovate  - Renovate configuration
```
