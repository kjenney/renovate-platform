# GraphQL API

The Renovate Platform uses Strawberry GraphQL to provide a type-safe API.

## Endpoint

```
POST http://localhost:5000/graphql
```

## Interactive Playground

Visit [http://localhost:5000/graphql](http://localhost:5000/graphql) to explore the API interactively.

## Queries

### Health Check

```graphql
query {
  health
  version
}
```

Response:
```json
{
  "data": {
    "health": "OK",
    "version": "0.1.0"
  }
}
```

### List All Open Pull Requests

Get all open pull requests across all repositories:

```graphql
query {
  openPullRequests {
    id
    number
    title
    state
    htmlUrl
    createdAt
    updatedAt
    userLogin
    repoOwner
    repoName
    headBranch
    baseBranch
  }
}
```

Response:
```json
{
  "data": {
    "openPullRequests": [
      {
        "id": 1,
        "number": 2,
        "title": "Update flask to v3.0.1",
        "state": "open",
        "htmlUrl": "http://localhost:3001/gitea_admin/renovate-test-python/pulls/2",
        "createdAt": "2024-01-15T10:30:00Z",
        "updatedAt": "2024-01-15T10:30:00Z",
        "userLogin": "renovate",
        "repoOwner": "gitea_admin",
        "repoName": "renovate-test-python",
        "headBranch": "renovate/flask-3.x",
        "baseBranch": "main"
      }
    ]
  }
}
```

### List Pull Requests for a Repository

Get pull requests for a specific repository with optional state filter:

```graphql
query {
  pullRequests(owner: "gitea_admin", repo: "renovate-test-python", state: "open") {
    id
    number
    title
    state
    htmlUrl
    headBranch
    baseBranch
  }
}
```

### List Repositories

Get all repositories for the authenticated user:

```graphql
query {
  repositories {
    id
    name
    fullName
    description
    htmlUrl
    defaultBranch
    ownerLogin
  }
}
```

## Types

### PullRequestType

| Field | Type | Description |
|-------|------|-------------|
| id | Int | Pull request ID |
| number | Int | PR number in the repository |
| title | String | PR title |
| body | String | PR description (nullable) |
| state | String | State: "open" or "closed" |
| htmlUrl | String | URL to view PR in browser |
| createdAt | String | ISO timestamp of creation |
| updatedAt | String | ISO timestamp of last update |
| userLogin | String | Username of PR author |
| userAvatarUrl | String | Avatar URL of PR author |
| repoOwner | String | Repository owner |
| repoName | String | Repository name |
| headBranch | String | Source branch |
| baseBranch | String | Target branch |

### RepositoryType

| Field | Type | Description |
|-------|------|-------------|
| id | Int | Repository ID |
| name | String | Repository name |
| fullName | String | Full name (owner/repo) |
| description | String | Repository description (nullable) |
| htmlUrl | String | URL to view repo in browser |
| cloneUrl | String | Git clone URL |
| defaultBranch | String | Default branch name |
| ownerLogin | String | Repository owner username |

## Authentication

The API uses the `GITEA_TOKEN` environment variable to authenticate with Gitea. Ensure this is set in your `.env` file.
