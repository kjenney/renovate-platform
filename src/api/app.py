"""Flask application with Strawberry GraphQL API."""
import os
from typing import Optional

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import strawberry
from strawberry.flask.views import GraphQLView

from gitea_client import GiteaClient


db = SQLAlchemy()


# GraphQL Types
@strawberry.type
class PullRequestType:
    """GraphQL type for a pull request."""

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


@strawberry.type
class RepositoryType:
    """GraphQL type for a repository."""

    id: int
    name: str
    full_name: str
    description: Optional[str]
    html_url: str
    clone_url: str
    default_branch: str
    owner_login: str


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Configuration
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"postgresql://{os.environ.get('POSTGRES_USER', 'renovate')}:"
        f"{os.environ.get('POSTGRES_PASSWORD', 'renovate_dev_password')}@"
        f"db:5432/{os.environ.get('POSTGRES_DB', 'renovate_platform')}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)

    # GraphQL Schema
    @strawberry.type
    class Query:
        @strawberry.field
        def health(self) -> str:
            return "OK"

        @strawberry.field
        def version(self) -> str:
            return "0.1.0"

        @strawberry.field
        def repositories(self) -> list[RepositoryType]:
            """Get all repositories from Gitea."""
            client = GiteaClient()
            repos = client.get_repositories()
            return [
                RepositoryType(
                    id=r.id,
                    name=r.name,
                    full_name=r.full_name,
                    description=r.description,
                    html_url=r.html_url,
                    clone_url=r.clone_url,
                    default_branch=r.default_branch,
                    owner_login=r.owner_login,
                )
                for r in repos
            ]

        @strawberry.field
        def open_pull_requests(self) -> list[PullRequestType]:
            """Get all open pull requests across all repositories."""
            client = GiteaClient()
            prs = client.get_all_open_pull_requests()
            return [
                PullRequestType(
                    id=pr.id,
                    number=pr.number,
                    title=pr.title,
                    body=pr.body,
                    state=pr.state,
                    html_url=pr.html_url,
                    created_at=pr.created_at,
                    updated_at=pr.updated_at,
                    user_login=pr.user_login,
                    user_avatar_url=pr.user_avatar_url,
                    repo_owner=pr.repo_owner,
                    repo_name=pr.repo_name,
                    head_branch=pr.head_branch,
                    base_branch=pr.base_branch,
                )
                for pr in prs
            ]

        @strawberry.field
        def pull_requests(
            self, owner: str, repo: str, state: str = "open"
        ) -> list[PullRequestType]:
            """Get pull requests for a specific repository."""
            client = GiteaClient()
            prs = client.get_pull_requests(owner, repo, state)
            return [
                PullRequestType(
                    id=pr.id,
                    number=pr.number,
                    title=pr.title,
                    body=pr.body,
                    state=pr.state,
                    html_url=pr.html_url,
                    created_at=pr.created_at,
                    updated_at=pr.updated_at,
                    user_login=pr.user_login,
                    user_avatar_url=pr.user_avatar_url,
                    repo_owner=pr.repo_owner,
                    repo_name=pr.repo_name,
                    head_branch=pr.head_branch,
                    base_branch=pr.base_branch,
                )
                for pr in prs
            ]

    schema = strawberry.Schema(query=Query)

    # Routes
    @app.route("/")
    def index():
        return {"status": "ok", "message": "Renovate Platform API"}

    @app.route("/health")
    def health():
        return {"status": "healthy"}

    # GraphQL endpoint
    app.add_url_rule(
        "/graphql",
        view_func=GraphQLView.as_view("graphql_view", schema=schema),
    )

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(host="0.0.0.0", port=5000, debug=True)
