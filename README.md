# Mantis Shrimp Bot Control Center 🔥

**Manage your super-heated AI workforce with style.**

Mantis Shrimp Bot Control Center is a premium dashboard for monitoring and controlling Mantis Shrimp Bot AI agents. It features real-time telemetry, a sleek dark-mode UI, and powerful administrative tools.

## Features
- **Real-time Telemetry**: Monitor core temperatures and status.
- **Premium UI**: Dark mode with dynamic color-coding.
- **Live Task Feed**: Bots automatically pick up and complete tasks every 3 seconds (random success/failure).
- **Ops Console**: Django Admin actions to mass-shutdown or reheat bots.
- **Robust API**: RESTful endpoints for all data.

## Quick Start (Local)

### Prerequisites
- Docker & Docker Compose

### Running the App

1. **Clone & Enter**:
   ```bash
   git clone <repo>
   cd mantis-shrimp-bot
   ```

2. **Start Services**:
   ```bash
   docker compose up --build
   ```
   *This starts the Web, Worker, Beat, Redis, and MongoDB containers.*

3. **Pre-seed Data** (creates admin user + sample data):
   ```bash
   docker compose exec web python manage.py seed_data
   ```
   Creates admin user (`admin` / `admin`), sample organizations, bots, and executions. Use `--clear` to reset and re-seed.

4. **Access the Application**:
   - **Dashboard**: [http://localhost:8000/](http://localhost:8000/)
   - **Admin Panel**: [http://localhost:8000/admin/](http://localhost:8000/admin/) — log in with `admin` / `admin`

   For a custom admin user instead, run `docker compose exec web python manage.py createsuperuser`.

**Local development** (without Docker): Set `DATABASE_URL=sqlite:///db.sqlite3` and `MONGODB_HOST=mongodb://localhost:27017/` (requires MongoDB running locally). See `.env.example`.

## Development
- **Run Tests**:
  ```bash
  docker compose exec web python manage.py test
  ```
- **Linting**:
  Code follows standard PEP8.

## Database
- **MongoDB**: App data (organizations, bots, executions) via MongoEngine
- **SQLite**: Django auth, sessions, admin (file-based, no extra setup)

## Architecture
See [docs/architecture.md](docs/architecture.md) for details.
