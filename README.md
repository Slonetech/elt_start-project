# elt_start-project

# Phase 0, Task 0.3: Documentation

Let's create honest, comprehensive documentation that reflects current reality while showing the path forward.

---

## **Step 1: Create Comprehensive README.md**

Replace your existing `README.md` with this:

```markdown
# ELT Pipeline Project

A foundational Extract-Load-Transform (ELT) data pipeline built to learn modern data engineering practices. Currently handles small-scale PostgreSQL replication with plans to scale to distributed big data processing.

## Project Status

**Current Phase:** Phase 0 - Foundation (Repository Hygiene)  
**Data Scale:** ~113 rows across 5 tables  
**Architecture:** Single-node Docker Compose  

This is a **learning project** progressing toward production-grade distributed data processing.

## What This Project Does

Extracts data from a source PostgreSQL database and loads it into a destination database with:
- Environment-based configuration
- Structured JSON logging
- Health check orchestration
- Dockerized deployment

**Currently Missing (Roadmap):**
- Transformation layer (dbt - Phase 1)
- Orchestration/scheduling (Airflow - Phase 2)
- Distributed processing (Spark - Phase 3)
- Monitoring/observability (Grafana - Phase 4)

## Architecture

```
┌─────────────────┐         ┌──────────────┐         ┌─────────────────────┐
│  Source DB      │         │  ELT Script  │         │  Destination DB     │
│  (PostgreSQL)   │────────▶│  (Python)    │────────▶│  (PostgreSQL)       │
│  Port: 5437     │         │  pg_dump     │         │  Port: 5438         │
│                 │         │  psql        │         │                     │
└─────────────────┘         └──────────────┘         └─────────────────────┘
                                    │
                                    ▼
                            JSON Structured Logs
```

### Current Components

1. **Source PostgreSQL Database**
   - Pre-populated with sample data (users, films, actors)
   - Initialized via SQL script

2. **ELT Script (Python)**
   - Uses `pg_dump` for extraction
   - Uses `psql` for loading
   - Structured logging with python-json-logger
   - Environment variable configuration

3. **Destination PostgreSQL Database**
   - Empty database that receives data
   - Schema created during load

### Technology Stack

- **Containerization:** Docker, Docker Compose
- **Languages:** Python 3.12, SQL
- **Databases:** PostgreSQL 17
- **Logging:** python-json-logger
- **Version Control:** Git

## Prerequisites

- Docker Desktop (Windows/Mac) or Docker Engine + Docker Compose (Linux)
- Git
- 2GB RAM minimum
- Ports 5437, 5438 available

## Quick Start

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd elt_start-project
```

### 2. Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your credentials (default values work for local development)
```

### 3. Start Pipeline

```bash
# Build and run all services
docker compose up --build

# Or run in detached mode
docker compose up -d --build
```

### 4. Verify Success

Look for this log message:
```json
{"message": "ELT pipeline completed successfully", "source": "source_postgres/source_db", "destination": "destination_postgres/destination_db"}
```

### 5. Inspect Destination Database

```bash
# Connect to destination database
docker exec -it destination_postgres psql -U postgres -d destination_db

# Query transferred data
\dt                           # List tables
SELECT COUNT(*) FROM users;   # Should return 14
SELECT COUNT(*) FROM films;   # Should return 20
```

## Project Structure

```
elt_start-project/
├── .env                    # Environment variables (gitignored)
├── .env.example            # Template for environment setup
├── .gitignore              # Git ignore rules
├── docker-compose.yaml     # Container orchestration
├── README.md               # This file
├── LICENSE                 # Project license
├── elt/
│   ├── Dockerfile          # ELT script container definition
│   ├── elt_script.py       # Main pipeline logic
│   ├── logger_config.py    # Structured logging setup
│   ├── requirements.txt    # Python dependencies
│   └── .dockerignore       # Docker build exclusions
└── source_db_init/
    └── init.sql            # Source database seed data
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SOURCE_POSTGRES_HOST` | Source database hostname | `source_postgres` |
| `SOURCE_POSTGRES_DB` | Source database name | `source_db` |
| `SOURCE_POSTGRES_USER` | Source database user | `postgres` |
| `SOURCE_POSTGRES_PASSWORD` | Source database password | `secret` |
| `DESTINATION_POSTGRES_HOST` | Destination hostname | `destination_postgres` |
| `DESTINATION_POSTGRES_DB` | Destination database name | `destination_db` |
| `DESTINATION_POSTGRES_USER` | Destination user | `postgres` |
| `DESTINATION_POSTGRES_PASSWORD` | Destination password | `secret` |

### Health Checks

Databases include health checks with:
- **Interval:** 10 seconds
- **Timeout:** 5 seconds  
- **Retries:** 5 attempts
- **Start Period:** 60 seconds

ELT script waits for healthy databases before executing.

## Development

### Making Changes

```bash
# Edit code in elt/elt_script.py or elt/logger_config.py

# Rebuild and test
docker compose down
docker compose up --build

# Check logs
docker compose logs -f elt_script
```

### Adding Dependencies

```bash
# Add to elt/requirements.txt
echo "new-package==1.0.0" >> elt/requirements.txt

# Rebuild
docker compose up --build
```

### Debugging

```bash
# View all logs
docker compose logs

# View specific service logs
docker compose logs source_postgres
docker compose logs destination_postgres
docker compose logs elt_script

# Execute commands in running container
docker compose exec source_postgres psql -U postgres -d source_db

# Inspect container
docker compose exec elt_script /bin/bash
```

## Roadmap

### Phase 0: Repository Hygiene ✅ (Current)
- [x] Task 0.1: Secrets management with .env
- [x] Task 0.2: Structured JSON logging
- [ ] Task 0.3: Documentation (in progress)
- [ ] Task 0.4: Data quality validation

### Phase 1: Transformation Layer (Weeks 3-5)
- [ ] Integrate dbt for SQL transformations
- [ ] Create staging models
- [ ] Build dimensional models (star schema)
- [ ] Add data quality tests

### Phase 2: Orchestration (Weeks 6-8)
- [ ] Deploy Apache Airflow
- [ ] Create DAGs for pipeline scheduling
- [ ] Implement dependency management
- [ ] Add alerting on failures

### Phase 3: Distributed Processing (Weeks 9-12)
- [ ] Add MinIO for data lake storage
- [ ] Integrate Apache Spark
- [ ] Implement medallion architecture (bronze/silver/gold)
- [ ] Scale to 100GB+ datasets

### Phase 4: Monitoring & Observability (Weeks 13-14)
- [ ] Deploy Prometheus for metrics
- [ ] Add Grafana dashboards
- [ ] Centralized logging with ELK stack
- [ ] Performance profiling

### Future Enhancements
- [ ] Incremental loading strategy (CDC)
- [ ] Stream processing with Kafka
- [ ] Cloud deployment (AWS/GCP)
- [ ] CI/CD pipeline
- [ ] Data catalog integration

## Learning Goals

This project teaches:
- Docker containerization and orchestration
- PostgreSQL database operations
- Python scripting for data pipelines
- Environment-based configuration
- Structured logging practices
- Git version control
- Modern data stack tools (dbt, Airflow, Spark)

## Known Limitations

1. **Scale:** Currently processes ~113 rows. Not suitable for production big data.
2. **No transformations:** Pure Extract-Load, missing the "T" in ELT.
3. **Full dumps:** No incremental loading or change data capture.
4. **Single-threaded:** No parallel processing.
5. **No recovery:** No checkpointing or idempotency guarantees.
6. **Local only:** Runs on single machine, not distributed.

## Contributing

This is a personal learning project, but suggestions welcome via issues.

## License

MIT License - see LICENSE file

## Contact

[Your Name] - [Your Email]  
Project Link: [Your GitHub URL]

---

**Last Updated:** October 6, 2025  
**Version:** 0.2.0 (Phase 0, Task 0.2 Complete)
```

---

## **Step 2: Create CHANGELOG.md**

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Data quality validation (Phase 0, Task 0.4)
- dbt transformation layer (Phase 1)
- Airflow orchestration (Phase 2)

## [0.2.0] - 2025-10-06

### Added
- Structured JSON logging with python-json-logger
- `logger_config.py` module for centralized logging configuration
- Contextual metadata in log messages (host, attempt, error details)
- Timestamps on all log entries

### Changed
- Replaced print() statements with structured logger calls
- Updated `elt_script.py` to use logger.info/warning/error
- Enhanced error messages with detailed context

### Technical Details
- Log format: JSON with ISO timestamps
- Log levels: INFO, WARNING, ERROR
- Output: stdout (container logs)

## [0.1.0] - 2025-10-06

### Added
- Environment-based secrets management
- `.env` file for credential storage
- `.env.example` template for repository
- `.gitignore` to exclude sensitive files
- Docker Compose environment variable integration

### Changed
- Externalized all hardcoded credentials to environment variables
- Updated `docker-compose.yaml` to use ${VAR} syntax
- Modified `elt_script.py` to read from `os.environ`
- Changed ports to 5437/5438 to avoid conflicts
- Improved health checks (60s start period, 5 retries)

### Removed
- Hardcoded database credentials from source code
- Obsolete `version: '3.8'` from docker-compose.yaml

### Fixed
- Dockerfile merge conflict artifacts
- Variable naming consistency

### Security
- Credentials no longer tracked in Git
- Passwords read from environment at runtime

## [0.0.1] - 2025-10-05

### Added
- Initial project structure
- Docker Compose with 3 services (source DB, destination DB, ELT script)
- Basic Extract-Load pipeline using pg_dump and psql
- Source database initialization script with sample data
- PostgreSQL 17 containers
- Python 3.12 ELT script
- Health check configuration
- Basic documentation

### Technical Details
- Data: 113 rows across 5 tables (users, films, actors, film_category, film_actors)
- Extraction: pg_dump
- Loading: psql
- Orchestration: Docker Compose

---

## Version Number Format

**MAJOR.MINOR.PATCH**

- **MAJOR:** Incompatible API/architecture changes
- **MINOR:** New functionality (backward-compatible)
- **PATCH:** Bug fixes (backward-compatible)

## Release Notes

### v0.2.0 - Structured Logging
Pipeline now outputs structured JSON logs suitable for log aggregation tools (ELK, Splunk, CloudWatch). All logging follows consistent format with contextual metadata.

### v0.1.0 - Secrets Management
Credentials externalized to environment variables. No secrets in version control. Foundation for secure deployment practices.

### v0.0.1 - MVP
Basic working pipeline that transfers data between PostgreSQL instances using Docker Compose.
```

---

## **Step 3: Save Files**

```powershell
# Create CHANGELOG.md
New-Item -Path CHANGELOG.md -ItemType File -Force
code CHANGELOG.md  # Paste content

# README.md should already exist - replace its contents
code README.md  # Paste content

# Verify both files
Get-ChildItem -Filter *.md
```

---

## **Step 4: Add Inline Code Comments**

Open `elt/elt_script.py` in VS Code and ensure it has detailed comments. Here's the improved version:

```python
"""
ELT Pipeline: PostgreSQL Source → Destination
Extracts data using pg_dump and loads into destination database

This is a foundational pipeline demonstrating:
- Environment-based configuration
- Structured logging
- Health check integration
- Docker orchestration

Future enhancements: incremental loading, dbt transformations, Airflow scheduling
"""

import subprocess
import time
import os
from logger_config import setup_logger

# Initialize structured logger
logger = setup_logger()


def wait_for_postgres(host, max_retries=5, delay=5):
    """
    Wait for PostgreSQL to become available before proceeding
    
    Uses pg_isready to check database availability. Critical for Docker Compose
    orchestration where services start in parallel but have dependencies.
    
    Args:
        host (str): Database hostname (e.g., 'source_postgres')
        max_retries (int): Maximum connection attempts before giving up
        delay (int): Seconds to wait between retry attempts
    
    Returns:
        bool: True if database is ready, False if max retries exceeded
    
    Example:
        if not wait_for_postgres('source_postgres'):
            logger.error('Cannot proceed without source database')
            return
    """
    retries = 0
    while retries < max_retries:
        try:
            # pg_isready returns 0 if database accepts connections
            result = subprocess.run(
                ['pg_isready', '-h', host, '-U', os.environ.get('SOURCE_POSTGRES_USER', 'postgres')],
                check=True,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info(
                    'Database connection successful',
                    extra={
                        'host': host,
                        'attempt': retries + 1,
                        'max_retries': max_retries
                    }
                )
                return True
                
        except subprocess.CalledProcessError as e:
            retries += 1
            logger.warning(
                'Database not ready, retrying',
                extra={
                    'host': host,
                    'attempt': retries,
                    'max_retries': max_retries,
                    'error': str(e)
                }
            )
            time.sleep(delay)
    
    # Max retries exceeded
    logger.error(
        'Failed to connect to database',
        extra={
            'host': host,
            'total_attempts': max_retries
        }
    )
    return False


def extract_and_load():
    """
    Main ELT function: Extract from source and load into destination
    
    Process:
    1. Load configuration from environment variables
    2. Wait for both databases to be healthy
    3. Extract data using pg_dump (creates SQL file)
    4. Load data using psql (executes SQL file)
    
    Error Handling:
    - Logs all failures with context
    - Returns early on any error (no partial loads)
    - Uses subprocess environment to pass passwords securely
    
    Future Improvements:
    - Add checkpointing for recovery
    - Implement incremental loading
    - Add data validation checks
    - Support parallel extraction/loading
    """
    logger.info('Starting ELT pipeline')
    
    # Read configuration from environment variables
    # Defaults provided for local development
    source_config = {
        'host': os.environ.get('SOURCE_POSTGRES_HOST', 'source_postgres'),
        'database': os.environ.get('SOURCE_POSTGRES_DB', 'source_db'),
        'user': os.environ.get('SOURCE_POSTGRES_USER', 'postgres'),
        'password': os.environ.get('SOURCE_POSTGRES_PASSWORD', 'secret')
    }
    
    destination_config = {
        'host': os.environ.get('DESTINATION_POSTGRES_HOST', 'destination_postgres'),
        'database': os.environ.get('DESTINATION_POSTGRES_DB', 'destination_db'),
        'user': os.environ.get('DESTINATION_POSTGRES_USER', 'postgres'),
        'password': os.environ.get('DESTINATION_POSTGRES_PASSWORD', 'secret')
    }
    
    # Log configuration (without passwords)
    logger.info('Configuration loaded from environment', extra={
        'source_db': source_config['database'],
        'destination_db': destination_config['database']
    })
    
    # Wait for databases to be ready
    # Docker Compose starts services in parallel, so we must wait
    logger.info('Waiting for databases to be ready')
    
    if not wait_for_postgres(source_config['host']):
        return
    
    if not wait_for_postgres(destination_config['host']):
        return
    
    # ===== EXTRACT PHASE =====
    # Use pg_dump to create SQL dump of source database
    logger.info('Starting data extraction from source database')
    dump_command = [
        'pg_dump',
        '-h', source_config['host'],        # Host
        '-U', source_config['user'],        # User
        '-d', source_config['database'],    # Database name
        '-f', 'data_dump.sql',              # Output file
        '-w'                                # Never prompt for password (use PGPASSWORD env var)
    ]
    
    # Set password in subprocess environment (not visible in ps/logs)
    subprocess_env = os.environ.copy()
    subprocess_env['PGPASSWORD'] = source_config['password']
    
    try:
        subprocess.run(dump_command, env=subprocess_env, check=True, capture_output=True)
        logger.info('Data extraction completed successfully')
    except subprocess.CalledProcessError as e:
        logger.error(
            'Data extraction failed',
            extra={'error': str(e), 'returncode': e.returncode}
        )
        return
    
    # ===== LOAD PHASE =====
    # Use psql to execute the SQL dump against destination database
    logger.info('Starting data load into destination database')
    load_command = [
        'psql',
        '-h', destination_config['host'],
        '-U', destination_config['user'],
        '-d', destination_config['database'],
        '-a',                               # Echo all input
        '-f', 'data_dump.sql'              # Execute this file
    ]
    
    # Update password for destination
    subprocess_env['PGPASSWORD'] = destination_config['password']
    
    try:
        subprocess.run(load_command, env=subprocess_env, check=True, capture_output=True)
        logger.info(
            'ELT pipeline completed successfully',
            extra={
                'source': f"{source_config['host']}/{source_config['database']}",
                'destination': f"{destination_config['host']}/{destination_config['database']}"
            }
        )
    except subprocess.CalledProcessError as e:
        logger.error(
            'Data load failed',
            extra={'error': str(e), 'returncode': e.returncode}
        )
        return


if __name__ == '__main__':
    extract_and_load()
```

---

## **Step 5: Commit Everything**

```powershell
# Check status
git status

# Stage all documentation changes
git add README.md CHANGELOG.md elt/elt_script.py

# Commit
git commit -m "docs: complete Phase 0, Task 0.3 - Documentation

Added:
- Comprehensive README.md with honest assessment of current capabilities
- CHANGELOG.md following Keep a Changelog format
- Detailed inline code comments in elt_script.py

Documentation includes:
- Quick start guide
- Architecture diagram
- Configuration reference
- Development workflow
- Complete roadmap (Phases 0-4)
- Known limitations
- Learning goals

Approach: Honest about current scale (~113 rows) while showing
path to distributed big data processing."

# View commits
git log --oneline -4
```

---

**Task 0.3 Complete.** Your project now has professional documentation that's honest about current state while showing the growth path.

Ready for Task 0.4 (Data Quality Validation)?