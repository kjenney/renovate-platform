"""Gitea API client for fetching repositories and pull requests."""
import os
from dataclasses import dataclass
from typing import Optional

import requests


@dataclass
class PullRequest:
    """Represents a pull request from Gitea."""

    id: int
    number: int
    title: str
    body: Optional[str]
    state: str
    html_url: str
    created_at: str
    updated_at: str
    user_login: str
    user_avatar_url: str
    repo_owner: str
    repo_name: str
    head_branch: str
    base_branch: str


@dataclass
class Repository:
    """Represents a repository from Gitea."""

    id: int
    name: str
    full_name: str
    description: Optional[str]
    html_url: str
    clone_url: str
    default_branch: str
    owner_login: str


class GiteaClient:
    """Client for interacting with Gitea API."""

    def __init__(self, base_url: Optional[str] = None, token: Optional[str] = None):
        self.base_url = (base_url or os.environ.get("GITEA_URL", "http://gitea:3000")).rstrip("/")
        self.external_url = os.environ.get("GITEA_EXTERNAL_URL", "http://localhost:3001").rstrip("/")
        self.token = token or os.environ.get("GITEA_TOKEN", "")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"token {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def _to_external_url(self, url: str) -> str:
        """Convert internal Docker URL to external browser-accessible URL."""
        return url.replace(self.base_url, self.external_url)

    def _get(self, endpoint: str, params: Optional[dict] = None) -> dict | list:
        """Make a GET request to the Gitea API."""
        url = f"{self.base_url}/api/v1{endpoint}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_repositories(self) -> list[Repository]:
        """Get all repositories for the authenticated user."""
        data = self._get("/user/repos")
        return [
            Repository(
                id=repo["id"],
                name=repo["name"],
                full_name=repo["full_name"],
                description=repo.get("description"),
                html_url=self._to_external_url(repo["html_url"]),
                clone_url=repo["clone_url"],
                default_branch=repo.get("default_branch", "main"),
                owner_login=repo["owner"]["login"],
            )
            for repo in data
        ]

    def get_pull_requests(self, owner: str, repo: str, state: str = "open") -> list[PullRequest]:
        """Get pull requests for a specific repository."""
        data = self._get(f"/repos/{owner}/{repo}/pulls", params={"state": state})
        return [
            PullRequest(
                id=pr["id"],
                number=pr["number"],
                title=pr["title"],
                body=pr.get("body"),
                state=pr["state"],
                html_url=self._to_external_url(pr["html_url"]),
                created_at=pr["created_at"],
                updated_at=pr["updated_at"],
                user_login=pr["user"]["login"],
                user_avatar_url=self._to_external_url(pr["user"]["avatar_url"]),
                repo_owner=owner,
                repo_name=repo,
                head_branch=pr["head"]["ref"],
                base_branch=pr["base"]["ref"],
            )
            for pr in data
        ]

    def get_all_open_pull_requests(self) -> list[PullRequest]:
        """Get all open pull requests across all repositories."""
        repos = self.get_repositories()
        all_prs = []
        for repo in repos:
            try:
                prs = self.get_pull_requests(repo.owner_login, repo.name, state="open")
                all_prs.extend(prs)
            except requests.exceptions.RequestException:
                # Skip repos that fail (e.g., no access)
                continue
        return all_prs
