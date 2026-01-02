# Installation

## Prerequisites

- Docker and Docker Compose
- Git

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/renovate-platform.git
   cd renovate-platform
   ```

2. Create environment file:
   ```bash
   cp .env.example .env
   ```

3. Build the containers:
   ```bash
   docker compose build
   ```

4. Start the services:
   ```bash
   docker compose up -d
   ```

## Verify Installation

Check that all services are running:

```bash
docker compose ps
```

Access the services:

- **UI**: [http://localhost:3000](http://localhost:3000)
- **API**: [http://localhost:5000](http://localhost:5000)
- **GraphQL Playground**: [http://localhost:5000/graphql](http://localhost:5000/graphql)
- **Gitea**: [http://localhost:3001](http://localhost:3001)
- **Documentation**: [http://localhost:8000](http://localhost:8000)
