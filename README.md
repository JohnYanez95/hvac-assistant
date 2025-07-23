# HVAC Assistant

A local-first, open-source NLP assistant for answering technical questions about HVAC furnace models using LangChain and Docker.

## Overview

This project creates a locally deployable assistant capable of answering technical questions about HVAC furnace models by scraping, processing, and querying furnace manuals and specifications using retrieval-augmented generation (RAG).

## Features

- **Legal-Compliant PDF Collection**: Automated collection of HVAC furnace PDFs from manufacturer websites with full legal compliance review
- **Multi-Manufacturer Support**: Targeting 14+ major HVAC manufacturers (Carrier, Goodman, Trane, Amana, American Standard, Fuji, Rheem, York, Daikin, Heil, Bryant, Coleman, Lennox, and more)
- **Document Processing**: Parse PDFs into plain text and chunk appropriately for embedding
- **Local Embeddings**: Use open-source embedding models (SentenceTransformers) for semantic search
- **Vector Database**: Store embeddings in local FAISS or ChromaDB for fast retrieval
- **LangChain Pipeline**: Natural language query interface with retrieval-augmented generation
- **Containerized**: Fully Docker-containerized for easy deployment and reproducibility

## Project Structure

```
hvac-assistant/
├── data/
│   ├── raw_pdfs/          # Downloaded PDF manuals
│   └── processed_texts/   # Extracted and chunked text
├── scripts/
│   ├── scrape_pdfs.py     # PDF scraping from manufacturer sites
│   ├── parse_and_chunk.py # PDF parsing and text chunking
│   ├── generate_embeddings.py # Embedding generation and storage
│   └── query_pipeline.py  # LangChain retrieval pipeline
├── utils/
│   ├── __init__.py        # Package initialization
│   ├── config_loader.py   # Configuration management
│   └── spark_utils.py     # PySpark session utilities
├── embeddings/
│   └── faiss_index/       # FAISS vector database storage
├── logs/                  # Application logs
├── temp/                  # Temporary processing files
├── config.yaml           # Configuration settings
├── requirements.txt      # Python dependencies
├── Dockerfile
├── docker-compose.yml
├── CLAUDE.md             # Development context
└── TODO.md               # Development roadmap
```

## Technology Stack

- **Language**: Python 3.10.9 (leveraging existing PySpark environment)
- **Data Processing**: PySpark 3.5.2 + Delta Lake + Hadoop 3.3.5 + Java JDK 19
- **ML Framework**: LangChain
- **Embeddings**: SentenceTransformers (all-MiniLM-L6-v2 recommended)
- **Vector DB**: FAISS (primary) or ChromaDB
- **Containerization**: Docker & Docker Compose
- **PDF Processing**: pdfplumber + PySpark for parallel processing
- **Web Scraping**: requests, BeautifulSoup4
- **Configuration**: YAML-based with environment-specific settings

## Current Status

**Phase**: Legal compliance research and Docker learning  
**Status**: Researching legal compliance for 14+ HVAC manufacturers before implementation  
**Next Steps**: Complete Docker learning path, finalize compliant manufacturer list, begin core infrastructure

## Quick Start

### For Windows Users (Recommended)

**WSL2 Development Environment:**
1. Follow the **[WSL2 Setup Guide](learnings/wsl-guide.md)** for the complete development environment used by this project
2. This guide covers:
   - WSL2 installation and configuration
   - Python 3.10, Java JDK 19, Hadoop 3.3.5, and PySpark 3.5.2 setup
   - Docker integration options
   - Claude Code installation for WSL development
   - VS Code WSL integration
   - Comprehensive Linux command reference for Windows users

### Native Windows Setup

**Step-by-Step Windows Installation:**

#### 1. Python 3.10.9 Installation
1. Download Python 3.10.9 from [python.org](https://www.python.org/downloads/release/python-3109/)
2. During installation:
   - Check "Add Python 3.10 to PATH"
   - Choose "Customize installation"
   - Check "Add Python to environment variables"
3. Verify: Open Command Prompt and run `python --version`

#### 2. Java JDK 19 Installation
1. Download Java JDK 19 from [Oracle Archive](https://www.oracle.com/java/technologies/javase/jdk19-archive-downloads.html)
   - Choose: Windows x64 Installer (jdk-19_windows-x64_bin.exe)
   - Alternative: [OpenJDK 19](https://jdk.java.net/archive/) for open-source option
2. Install to default location: `C:\Program Files\Java\jdk-19`
3. Set environment variables (see Environment Variables section below)

#### 3. Apache Hadoop 3.3.5 Installation
1. Download Hadoop 3.3.5 from [Apache Archive](https://archive.apache.org/dist/hadoop/common/hadoop-3.3.5/)
   - File: `hadoop-3.3.5.tar.gz`
2. Extract to `C:\hadoop\` (final path: `C:\hadoop\hadoop-3.3.5`)
3. Download Windows utilities for Hadoop:
   - Get winutils.exe from [steveloughran/winutils](https://github.com/steveloughran/winutils/tree/master/hadoop-3.0.0/bin)
   - Place in `C:\hadoop\hadoop-3.3.5\bin\`
4. Set environment variables (see below)

#### 4. PySpark 3.5.2 Installation

**Important: Choose ONE of these approaches based on your needs:**

**Option A: Virtual Environment Installation (Recommended)**
```cmd
# Skip global PySpark installation
# Install PySpark later in your project's virtual environment
# This avoids version conflicts between projects
```

**Option B: Global Installation (For system-wide PySpark)**
```cmd
# Install globally ONLY if you need PySpark available system-wide
pip install pyspark==3.5.2
```

**Note**: If you choose Option A (recommended), you'll install PySpark in your virtual environment during project setup (Step 7)

#### 5. Environment Variables Configuration

**Method 1: System Properties GUI**
1. Right-click "This PC" → Properties → Advanced system settings
2. Click "Environment Variables"
3. Under "System variables", add these NEW variables:

| Variable | Value |
|----------|-------|
| `JAVA_HOME` | `C:\Program Files\Java\jdk-19` |
| `HADOOP_HOME` | `C:\hadoop\hadoop-3.3.5` |
| `PYSPARK_PYTHON` | `python` |
| `HADOOP_COMMON_LIB_NATIVE_DIR` | `%HADOOP_HOME%\lib\native` |

**Note about SPARK_HOME:**
- **If using virtual environments (Option A)**: Do NOT set SPARK_HOME globally
- **If using global PySpark (Option B)**: Set `SPARK_HOME` to `%USERPROFILE%\AppData\Local\Programs\Python\Python310\Lib\site-packages\pyspark`

4. Edit the `Path` variable and ADD these entries:
   - `%JAVA_HOME%\bin`
   - `%HADOOP_HOME%\bin`
   - `%HADOOP_HOME%\sbin`
   - `%SPARK_HOME%\bin` (Only if using global PySpark - Option B)

**Method 2: Command Line (Run as Administrator)**

**For Virtual Environment Setup (Option A - Recommended):**
```cmd
# Set Java environment
setx JAVA_HOME "C:\Program Files\Java\jdk-19" /M
setx PATH "%PATH%;%JAVA_HOME%\bin" /M

# Set Hadoop environment
setx HADOOP_HOME "C:\hadoop\hadoop-3.3.5" /M
setx HADOOP_COMMON_LIB_NATIVE_DIR "%HADOOP_HOME%\lib\native" /M
setx PATH "%PATH%;%HADOOP_HOME%\bin;%HADOOP_HOME%\sbin" /M

# Set PySpark Python
setx PYSPARK_PYTHON "python" /M
```

**For Global PySpark Setup (Option B):**
```cmd
# Run all commands from Option A above, then add:
setx SPARK_HOME "%USERPROFILE%\AppData\Local\Programs\Python\Python310\Lib\site-packages\pyspark" /M
setx PATH "%PATH%;%SPARK_HOME%\bin" /M
```

**Important**: After setting environment variables, close and reopen Command Prompt/PowerShell

#### 6. Verification
Open a new Command Prompt and verify each component:

```cmd
# Java verification
java -version
# Expected: openjdk version "19.0.2" or java version "19.0.2"

# Hadoop verification
hadoop version
# Expected: Hadoop 3.3.5

# Python verification
python --version
# Expected: Python 3.10.9

# PySpark verification (skip if using Option A - venv approach)
python -c "import pyspark; print(pyspark.__version__)"
# Expected: 3.5.2 (only if globally installed)

# Test PySpark functionality (skip if using Option A - venv approach)
pyspark
# Expected: Spark shell should start without errors

# Note: For Option A users, PySpark verification happens after venv activation in Step 7
```

#### 7. Project Setup
```cmd
# Clone repository
git clone https://github.com/JohnYanez95/hvac-assistant.git
cd hvac-assistant

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# IMPORTANT: If you chose Option A (virtual environment approach)
# Install PySpark in the virtual environment now
pip install pyspark==3.5.2

# Install all project dependencies
pip install -r requirements.txt

# Run environment test
python tests\test_pyspark.py
```

**Virtual Environment Benefits:**
- Isolated PySpark version per project
- No conflicts with other Python projects
- SPARK_HOME automatically set within venv
- PySpark finds Java/Hadoop through JAVA_HOME and HADOOP_HOME

### Alternative Setup Methods

**Docker Setup:**
1. Use [Docker Learning Guide](learnings/docker-guide.md) for containerized deployment
2. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

## Development Environment

This project is actively developed using:
- **WSL2 (Ubuntu 22.04)** on Windows
- **Python 3.10.12** in virtual environments
- **Java JDK 19** + **Hadoop 3.3.5** + **PySpark 3.5.2**
- **Docker Desktop** with WSL2 integration
- **VS Code** with WSL extension
- **Claude Code** for AI-assisted development

For the exact setup used during development, follow the [WSL2 Setup Guide](learnings/wsl-guide.md).

## Environment Verification

After completing your setup, verify your PySpark environment is working correctly:

```bash
# Activate virtual environment
source venv/bin/activate

# Install project dependencies
pip install -r requirements.txt

# Run PySpark environment test
python3 tests/test_pyspark.py
```

The test script validates:
- Python 3.10.x compatibility
- Java/Hadoop environment variables
- PySpark 3.5.2 installation and functionality
- DataFrame operations with sample HVAC data
- Spark session management

**Expected Output:** All 5 tests should pass with "🎉 All tests passed! PySpark environment is ready for HVAC Assistant development."

## Learning Resources

- **[WSL2 Setup Guide](learnings/wsl-guide.md)** - Complete Windows development environment setup (recommended)
- **[Docker Guide](learnings/docker-guide.md)** - Docker fundamentals and containerized deployment

## Future Roadmap

- Streamlit web interface
- Continuous deployment pipeline
- Multi-modal support (images, diagrams)
- Real-time data updates 
