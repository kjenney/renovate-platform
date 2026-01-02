# Configuration

## Environment Variables

The platform uses environment variables for configuration. Copy `.env.example` to `.env` and modify as needed.

### PostgreSQL

| Variable | Default | Description |
|----------|---------|-------------|
| `POSTGRES_USER` | renovate | Database user |
| `POSTGRES_PASSWORD` | renovate_dev_password | Database password |
| `POSTGRES_DB` | renovate_platform | Database name |

### Flask

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_ENV` | development | Flask environment |
| `FLASK_DEBUG` | 1 | Enable debug mode |
| `SECRET_KEY` | dev-secret-key | Flask secret key |

### Gitea

| Variable | Default | Description |
|----------|---------|-------------|
| `GITEA_ADMIN_USER` | gitea_admin | Admin username |
| `GITEA_ADMIN_PASSWORD` | gitea_admin_password | Admin password |
| `GITEA_ADMIN_EMAIL` | admin@localhost | Admin email |

### Renovate

| Variable | Default | Description |
|----------|---------|-------------|
| `RENOVATE_TOKEN` | - | Gitea API token |
| `RENOVATE_PLATFORM` | gitea | Platform type |
| `RENOVATE_ENDPOINT` | http://gitea:3000 | Gitea URL |

## Running Renovate

The Renovate service uses a Docker Compose profile. To run it:

```bash
docker compose --profile renovate up renovate
```
