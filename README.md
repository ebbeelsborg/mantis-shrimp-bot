# Moltenbot Control Center 🔥

**Manage your super-heated AI workforce with style.**

Moltenbot Control Center is a premium dashboard for monitoring and controlling "Moltenbot" AI agents. It features real-time telemetry, a sleek dark-mode UI, and powerful administrative tools.

![Dashboard Preview](docs/dashboard-preview.png)

## Features
- **Real-time Telemetry**: Monitor core temperatures and status.
- **Premium UI**: Dark mode with dynamic color-coding.
- **Ops Console**: Django Admin actions to mass-shutdown or reheat bots.
- **Robust API**: RESTful endpoints for all data.

## Quick Start (Local)

### Prerequisites
- Docker & Docker Compose

### Running the App

1. **Clone & Enter**:
   ```bash
   git clone <repo>
   cd moltenbot-dashboard
   ```

2. **Start Services**:
   ```bash
   docker-compose up --build
   ```
   *This will start the Database and Web containers.*

3. **Access the Application**:
   - **Dashboard**: [http://localhost:8000/](http://localhost:8000/)
   - **Admin Panel**: [http://localhost:8000/admin/](http://localhost:8000/admin/)
     - *Note: You'll need to create a superuser inside the container to log in.*

4. **Create a Superuser**:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

## Development
- **Run Tests**:
  ```bash
  docker-compose exec web python manage.py test
  ```
- **Linting**:
  Code follows standard PEP8.

## Architecture
See [docs/architecture.md](docs/architecture.md) for details.
