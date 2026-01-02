#!/usr/bin/env python3
"""Seed Gitea with test repositories for Renovate integration testing."""
import argparse
import base64
import os
from pathlib import Path
import sys
import time

from dotenv import load_dotenv
import requests


def load_env_file():
    """Load .env file from project root."""
    # Find project root (where .env file lives)
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    env_file = project_root / ".env"

    if env_file.exists():
        load_dotenv(env_file)
        print(f"Loaded .env from: {env_file}")
        return True
    print(f"Warning: .env file not found at {env_file}")
    return False


# Sample dependency files for different ecosystems
SAMPLE_FILES = {
    "python": {
        "requirements.txt": "flask==2.0.0\nrequests==2.25.0\npytest==7.0.0\n",
        "README.md": "# Python Test Repository\n\nTest repo for Renovate dependency updates.\n",
    },
    "node": {
        "package.json": """{
  "name": "test-node-app",
  "version": "1.0.0",
  "dependencies": {
    "express": "4.17.0",
    "lodash": "4.17.20"
  },
  "devDependencies": {
    "jest": "27.0.0"
  }
}
""",
        "README.md": "# Node.js Test Repository\n\nTest repo for Renovate dependency updates.\n",
    },
    "docker": {
        "Dockerfile": """FROM python:3.10-slim

RUN pip install flask==2.0.0

WORKDIR /app
COPY . .

CMD ["python", "app.py"]
""",
        "README.md": "# Docker Test Repository\n\nTest repo for Renovate Docker image updates.\n",
    },
    "mixed": {
        "requirements.txt": "django==3.2.0\ncelery==5.0.0\n",
        "package.json": """{
  "name": "mixed-app",
  "version": "1.0.0",
  "dependencies": {
    "react": "17.0.0",
    "axios": "0.21.0"
  }
}
""",
        "Dockerfile": "FROM node:16-alpine\n\nWORKDIR /app\nCOPY . .\n\nCMD [\"npm\", \"start\"]\n",
        "README.md": "# Mixed Dependencies Repository\n\nTest repo with Python, Node.js, and Docker dependencies.\n",
    },
}


def get_gitea_client(base_url, token):
    """Create a configured requests session for Gitea API."""
    session = requests.Session()
    session.headers.update({
        "Authorization": f"token {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    })
    session.base_url = base_url.rstrip("/")
    return session


def check_gitea_health(session):
    """Check if Gitea is accessible and token is valid."""
    try:
        url = f"{session.base_url}/api/v1/user"
        response = session.get(url)
        if response.status_code == 401 or response.status_code == 403:
            print(f"Authentication failed (HTTP {response.status_code})")
            print(f"  Check that GITEA_TOKEN is valid and has correct permissions")
            print(f"  Authorization header: {session.headers.get('Authorization', '(not set)')[:20]}...")
            return False
        response.raise_for_status()
        user = response.json()
        print(f"Authenticated as: {user.get('login', 'unknown')}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Gitea: {e}")
        return False


def create_repository(session, name, description, private=False):
    """Create a new repository in Gitea."""
    payload = {
        "name": name,
        "description": description,
        "private": private,
        "auto_init": True,
        "default_branch": "main",
        "readme": "Default",
    }

    response = session.post(
        f"{session.base_url}/api/v1/user/repos",
        json=payload,
    )

    if response.status_code == 201:
        repo = response.json()
        print(f"Created repository: {repo['full_name']}")
        return repo
    elif response.status_code == 409:
        print(f"Repository '{name}' already exists, skipping creation")
        # Get existing repo
        user_response = session.get(f"{session.base_url}/api/v1/user")
        user = user_response.json()
        repo_response = session.get(
            f"{session.base_url}/api/v1/repos/{user['login']}/{name}"
        )
        return repo_response.json() if repo_response.status_code == 200 else None
    else:
        print(f"Failed to create repository '{name}': {response.status_code}")
        print(f"Response: {response.text}")
        return None


def add_file_to_repo(session, owner, repo, filepath, content, message):
    """Add or update a file in a repository."""
    # Base64 encode the content
    encoded_content = base64.b64encode(content.encode()).decode()

    # Check if file exists
    check_response = session.get(
        f"{session.base_url}/api/v1/repos/{owner}/{repo}/contents/{filepath}"
    )

    payload = {
        "content": encoded_content,
        "message": message,
        "branch": "main",
    }

    if check_response.status_code == 200:
        # File exists, update it
        existing = check_response.json()
        payload["sha"] = existing["sha"]
        response = session.put(
            f"{session.base_url}/api/v1/repos/{owner}/{repo}/contents/{filepath}",
            json=payload,
        )
    else:
        # Create new file
        response = session.post(
            f"{session.base_url}/api/v1/repos/{owner}/{repo}/contents/{filepath}",
            json=payload,
        )

    if response.status_code in (200, 201):
        print(f"  Added file: {filepath}")
        return True
    else:
        print(f"  Failed to add file '{filepath}': {response.status_code}")
        return False


def seed_repository(session, repo, repo_type):
    """Add sample dependency files to a repository."""
    if repo_type not in SAMPLE_FILES:
        print(f"Unknown repository type: {repo_type}")
        return False

    owner = repo["owner"]["login"]
    repo_name = repo["name"]
    files = SAMPLE_FILES[repo_type]

    print(f"Seeding {owner}/{repo_name} with {repo_type} dependencies...")

    # Small delay to ensure repo is ready
    time.sleep(1)

    for filepath, content in files.items():
        add_file_to_repo(
            session,
            owner,
            repo_name,
            filepath,
            content,
            f"Add {filepath} for Renovate testing",
        )

    return True


def create_test_repositories(session, prefix="renovate-test"):
    """Create a set of test repositories for Renovate."""
    repos_config = [
        {
            "name": f"{prefix}-python",
            "description": "Python test repository for Renovate",
            "type": "python",
        },
        {
            "name": f"{prefix}-node",
            "description": "Node.js test repository for Renovate",
            "type": "node",
        },
        {
            "name": f"{prefix}-docker",
            "description": "Docker test repository for Renovate",
            "type": "docker",
        },
        {
            "name": f"{prefix}-mixed",
            "description": "Mixed dependencies test repository for Renovate",
            "type": "mixed",
        },
    ]

    created_repos = []
    for config in repos_config:
        repo = create_repository(
            session,
            config["name"],
            config["description"],
        )
        if repo:
            seed_repository(session, repo, config["type"])
            created_repos.append(repo)

    return created_repos


def main():
    """Main entry point."""
    # Load .env file from project root
    load_env_file()

    parser = argparse.ArgumentParser(
        description="Seed Gitea with test repositories for Renovate"
    )
    parser.add_argument(
        "--url",
        default=os.environ.get("GITEA_URL", "http://localhost:3001"),
        help="Gitea base URL (default: http://localhost:3001)",
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("GITEA_TOKEN"),
        help="Gitea API token (reads from .env or GITEA_TOKEN env var)",
    )
    parser.add_argument(
        "--prefix",
        default="renovate-test",
        help="Prefix for repository names (default: renovate-test)",
    )
    parser.add_argument(
        "--repo-type",
        choices=["python", "node", "docker", "mixed", "all"],
        default="all",
        help="Type of repository to create (default: all)",
    )

    args = parser.parse_args()

    if not args.token:
        print("Error: Gitea API token required. Set GITEA_TOKEN in .env or use --token")
        print(f"  GITEA_TOKEN from env: {os.environ.get('GITEA_TOKEN', '(not set)')}")
        sys.exit(1)

    # Show masked token for debugging
    masked_token = f"{args.token[:4]}...{args.token[-4:]}" if len(args.token) > 8 else "****"
    print(f"Using token: {masked_token}")

    session = get_gitea_client(args.url, args.token)

    print(f"Connecting to Gitea at {args.url}...")
    if not check_gitea_health(session):
        sys.exit(1)

    print()

    if args.repo_type == "all":
        repos = create_test_repositories(session, args.prefix)
    else:
        repo_name = f"{args.prefix}-{args.repo_type}"
        repo = create_repository(
            session,
            repo_name,
            f"{args.repo_type.title()} test repository for Renovate",
        )
        if repo:
            seed_repository(session, repo, args.repo_type)
            repos = [repo]
        else:
            repos = []

    print()
    print(f"Created {len(repos)} test repositories:")
    for repo in repos:
        print(f"  - {repo['html_url']}")

    print()
    print("Next steps:")
    print("1. Configure Renovate token in .env (RENOVATE_TOKEN)")
    print("2. Run: docker compose --profile renovate up renovate")


if __name__ == "__main__":
    main()
