# MindFlow // Premium Productivity Dashboard

MindFlow is a premium, interactive personal productivity web dashboard designed for logging daily mood states, drafting persistent thoughts/notes, and tracking flow tasks. It is implemented using Python Flask (Frontend & Web API service) and PostgreSQL (Stateful Database service).

## Deployment Requirements
* **Docker Engine** / **Docker Desktop** (v20.10.0 or higher) installed and running.
* **Bash shell** or terminal emulator (Git Bash, WSL, Linux, or macOS terminal) to run the scripts.
* **Docker Compose** (optional, if you prefer running via `docker-compose up`).

## Application Description
MindFlow is designed with modern glassmorphism UI styling, high contrast colors, and smooth micro-animations. It provides:
1. **Task Flow**: A persistent task manager allowing creation, toggle completion, and deletion of checklist tasks.
2. **Daily Mood State**: A mood logger representing current productivity focus, zen energy, tireness, or high performance with interactive icons.
3. **Thoughts & Ideas**: A quick note-taking system storing ideas and text records in the persistent relational database.

All states (tasks, notes, mood history) are saved directly in a PostgreSQL relational database.

## Network and Volume Details
* **Virtual Network (`mindflow-network`)**: A dedicated bridge network facilitating isolated, secure communication using DNS aliases between the web application service container and the database container.
* **Named Volume (`mindflow-db-data`)**: A persistent Docker volume mounted to the PostgreSQL database container at `/var/lib/postgresql/data`. This ensures that all database state persists across restarts, rebuilds, and stops.

## Container Configuration
* **Database Container (`mindflow-db`)**: Runs PostgreSQL 15 on port `5432`. Uses the `on-failure` restart policy and has the named volume attached for persistent relational storage.
* **Web Container (`mindflow-web`)**: Runs Flask server on port `5000`. Configured via environment variables to target the database container host (`mindflow-db`). Uses the `on-failure` restart policy.

## Container List
| Container Name | Service Role | Image | Port (Host:Container) | Volume Mounts |
|---|---|---|---|---|
| **mindflow-db** | PostgreSQL Relational Database | `postgres:15-alpine` | `5432:5432` | `mindflow-db-data` -> `/var/lib/postgresql/data` |
| **mindflow-web** | Flask Web Server & UI Frontend | `mindflow-web:latest` (Custom Build) | `5000:5000` | None |

## Instructions

### 1. Create Application Resources (Prepare)
Run the script to build the web application image, prepare the virtual network, and create the named volume:
```bash
./prepare-app.sh
```

### 2. Run the Application
Start the PostgreSQL and Flask services:
```bash
./start-app.sh
```

### 3. Accessing the Application
Open your web browser and navigate to:
**[http://localhost:5000](http://localhost:5000)**

### 4. Pause the Application
Stop all services without losing your notes, tasks, or mood history:
```bash
./stop-app.sh
```

### 5. Delete All Application Resources
Remove all resources, including networks, custom build images, containers, and persistent volumes:
```bash
./remove-app.sh
```

---

## Example Workflow

```bash
# Create application resources
$ ./prepare-app.sh
Preparing app ...
Creating network 'mindflow-network'...
Creating persistent volume 'mindflow-db-data'...
Building web service image 'mindflow-web'...
[Docker build output...]
Preparation complete! Ready to start the application.

# Run the application
$ ./start-app.sh
Running app ...
Starting Database Service (PostgreSQL)...
Starting Web Service (Flask)...

==========================================================
 The app is available at http://localhost:5000
==========================================================

# Open a web browser and interact with the application

# Pause the application
$ ./stop-app.sh
Stopping app ...
App paused. Containers stopped. Persistent data is preserved.

# Delete all application resources
$ ./remove-app.sh
Removing app resources ...
Removing containers...
Removing network...
Removing volume...
Removing custom image...
Removed app.
```