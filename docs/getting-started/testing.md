# Testing Renovate Integration

This guide explains how to seed Gitea with test repositories and run Renovate to verify the integration.

## Prerequisites

1. All services running: `docker compose up -d`
2. Gitea accessible at http://localhost:3001
3. Gitea admin account created (first-time setup)

## Step 1: Create Gitea API Token

1. Open Gitea at http://localhost:3001
2. Complete the initial setup if this is your first time:
   - Set the Site Title
   - Create an admin account (use credentials from `.env`)
3. Go to **Settings** > **Applications** > **Manage Access Tokens**
4. Generate a new token with `Read and Write` for `repository` and `user` routes.
5. Copy the token

## Step 2: Configure Environment

Add the token to your `.env` file:

```bash
GITEA_TOKEN=your-gitea-token-here
```

The seeding script automatically reads from the `.env` file in the project root.

## Step 3: Set Up Python Virtual Environment

Create and activate a virtual environment for running the utility scripts:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Linux/macOS
# or
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install -r scripts/requirements.txt
```

## Step 4: Seed Test Repositories

Run the seeding script to create test repositories with outdated dependencies:

```bash
# Ensure venv is activated
source venv/bin/activate

# Run script (reads GITEA_TOKEN from .env automatically)
python scripts/seed_gitea.py

# Create specific repository types
python scripts/seed_gitea.py --repo-type python
python scripts/seed_gitea.py --repo-type node
python scripts/seed_gitea.py --repo-type docker
python scripts/seed_gitea.py --repo-type mixed
```

### Script Options

| Option | Default | Description |
|--------|---------|-------------|
| `--url` | http://localhost:3001 | Gitea base URL |
| `--token` | from `.env` | Gitea API token (override with CLI arg) |
| `--prefix` | renovate-test | Prefix for repository names |
| `--repo-type` | all | Type: python, node, docker, mixed, all |

### Created Repositories

The script creates repositories with intentionally outdated dependencies:

| Repository | Dependencies |
|------------|--------------|
| `renovate-test-python` | Flask 2.0.0, requests 2.25.0, pytest 7.0.0 |
| `renovate-test-node` | Express 4.17.0, lodash 4.17.20, jest 27.0.0 |
| `renovate-test-docker` | Python 3.10-slim, Flask 2.0.0 |
| `renovate-test-mixed` | Django, React, Node Docker image |

## Step 5: Run Renovate

Start the Renovate bot to scan repositories and create update PRs:

```bash
docker compose --profile renovate up renovate
```

Renovate will:

1. Discover all repositories in Gitea
2. Create onboarding PRs for new repositories
3. Scan for outdated dependencies
4. Create pull requests for updates

## Step 6: Verify Results

1. Open Gitea at http://localhost:3001
2. Navigate to your test repositories
3. Check the **Pull Requests** tab for Renovate PRs
4. Review the Dependency Dashboard issue (if enabled)

## Troubleshooting

### Renovate Can't Connect to Gitea

Check that Gitea is healthy:

```bash
docker compose ps gitea
curl http://localhost:3001/api/healthz
```

### Token Permission Issues

Ensure your token has the required scopes:

- `repo` - Full repository access
- `write:repository` - Create/update repository contents

### View Renovate Logs

```bash
docker compose --profile renovate logs renovate
```

## Running Renovate Continuously

For continuous monitoring, you can run Renovate on a schedule:

```bash
# Run every hour
while true; do
  docker compose --profile renovate up renovate
  sleep 3600
done
```

Or configure a cron job on your host system.
