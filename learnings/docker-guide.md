# Docker Learning Guide for HVAC Assistant

## Overview

This guide covers Docker fundamentals specifically tailored for the HVAC Assistant project. Docker will help us create a consistent, portable environment for our Python/PySpark/ML stack.

## Why Docker for HVAC Assistant

- **Consistent Environment**: Same Python/Java/Hadoop versions everywhere
- **Easy Deployment**: One command to run entire stack
- **Isolation**: Doesn't interfere with your existing PySpark setup
- **Portability**: Runs same on any machine

## Installation

### Docker Desktop for Windows
1. **Download**: https://www.docker.com/products/docker-desktop/
2. **System Requirements**: Windows 10/11 Pro, Enterprise, or Education with WSL2
3. **Installation**: Follow installer, enable WSL2 integration

## Learning Path

### 1. Docker Fundamentals (30-45 mins)
**Resource**: Docker's official tutorial: https://docs.docker.com/get-started/

**Key Concepts to Focus On:**
- **Images**: Templates for containers (like our Python 3.10 + dependencies)
- **Containers**: Running instances of images
- **Volumes**: Data persistence (for our PDFs, embeddings, logs)
- **Networks**: Container communication (future Streamlit UI)

### 2. Multi-stage Builds (20 mins)
**Resource**: https://docs.docker.com/build/building/multi-stage/

**Our Use Case:**
```dockerfile
# Stage 1: Base with system dependencies
FROM python:3.10-slim as base
RUN apt-get update && apt-get install -y openjdk-11-jre

# Stage 2: Dependencies
FROM base as dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Stage 3: Application
FROM dependencies as app
COPY . .
```

### 3. Docker Compose (Critical - 20 mins)
**Resource**: https://docs.docker.com/compose/gettingstarted/

**Our Stack Architecture:**
```yaml
services:
  hvac-assistant:
    build: .
    volumes:
      - ./data:/app/data
      - ./embeddings:/app/embeddings
    ports:
      - "8501:8501"  # Future Streamlit UI
```

### 4. Volume Mounting (10 mins)
**Resource**: https://docs.docker.com/storage/volumes/

**Our Data Persistence Needs:**
- PDF storage: `./data/raw_pdfs`
- Processed texts: `./data/processed_texts`
- Embeddings: `./embeddings`
- Logs: `./logs`

## Our Docker Architecture

```
HVAC Container:
├── Python 3.10-slim base
├── Java JRE (for PySpark compatibility)
├── Python dependencies (from requirements.txt)
├── Application code
└── Volume mounts for data persistence
```

## Hands-on Learning Exercise

After Docker installation, try this simple exercise:

```bash
# Pull Python 3.10 image
docker pull python:3.10-slim

# Run interactive Python container
docker run -it --rm python:3.10-slim python

# Test volume mounting
docker run -it --rm -v C:\Users\Johnr\Repos\hvac-assistant:/app python:3.10-slim ls /app
```

## Learning Priority Order

1. **Basic container concepts** (15 mins) - Understanding images vs containers
2. **Dockerfile syntax** (20 mins) - How to build our custom image
3. **Docker Compose** (20 mins) - Managing our multi-component application
4. **Volume mounting** (10 mins) - Data persistence for our ML pipeline

## Project-Specific Considerations

### Java Compatibility
- Our local setup uses Java JDK 19
- Docker will use Java JRE 11 (more stable for containers)
- PySpark 3.5.2 works with both versions

### Windows Path Handling
- Docker uses Linux paths internally
- Volume mounts: `C:\Users\Johnr\Repos\hvac-assistant:/app`
- Config files must handle both Windows and Linux paths

### Memory Configuration
- Container memory limits for Spark (16GB executor, 32GB driver)
- May need to adjust for container constraints

## Next Steps

1. Complete Docker installation
2. Work through fundamentals tutorial
3. Build our project's Dockerfile
4. Create docker-compose.yml for full stack
5. Test containerized development workflow

## Integration with Existing Environment

Docker will **complement** (not replace) your existing PySpark setup:
- **Development**: Use your local Python 3.10.9 + PySpark 3.5.2 + Java 19
- **Deployment**: Use Docker containers for consistent environments
- **Testing**: Use containers to validate cross-platform compatibility

## WSL-Specific Notes

**Container Access from Windows**: When running containers in WSL2, access them from Windows browsers using `http://127.0.0.1:PORT` instead of `http://localhost:PORT`. The `localhost` DNS resolution can be unreliable in the WSL-Windows bridge.