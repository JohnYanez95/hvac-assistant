# HVAC Assistant - Claude Context

## Project Overview
This is an NLP project using LangChain and Docker to create a locally deployable assistant for answering technical questions about HVAC furnace models. The system uses retrieval-augmented generation (RAG) with scraped PDF manuals.

## Technology Stack
- **Language**: Python 3.10.9
- **Big Data**: PySpark 3.5.2 + Hadoop 3.3.5 + Java JDK 19
- **ML Framework**: LangChain
- **Embeddings**: SentenceTransformers (all-MiniLM-L6-v2)
- **Vector DB**: FAISS (primary) or ChromaDB
- **Containerization**: Docker & Docker Compose
- **PDF Processing**: pdfplumber
- **Web Scraping**: requests, BeautifulSoup4

## Environment Setup Prerequisites

### Option 1: Native Windows Setup
For a detailed Windows native installation, see the **[Native Windows Setup section in README.md](README.md#native-windows-setup)** which covers:
- Python 3.10.9 installation
- Java JDK 19 installation with Oracle/OpenJDK options
- Apache Hadoop 3.3.5 with Windows utilities (winutils.exe)
- PySpark 3.5.2 via pip
- Complete environment variable configuration (GUI and CLI methods)
- Full verification steps

### Option 2: WSL2 Setup (Recommended for Windows Users)
For the best development experience on Windows, use WSL2 (Windows Subsystem for Linux):

**Initial Setup:**
```cmd
# In PowerShell (as Administrator)
wsl --install Ubuntu-22.04
wsl --set-default-version 2
```

**Important WSL Nuances:**
- After installation, create a UNIX username (doesn't need to match Windows username)
- WSL may start in Windows directories (`/mnt/c/...`) - use `cd ~` to get to Linux home
- Start WSL properly with `wsl ~` (not just `wsl`) to begin in home directory
- Use Windows Terminal for better WSL integration
- Git is pre-installed in Ubuntu 22.04
- Multi-line command pasting works seamlessly

**WSL Environment Setup:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.10 (if not already installed)
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install -y python3.10 python3.10-venv python3.10-dev python3-pip

# Install Java JDK 19
sudo mkdir -p /opt/java
cd /tmp
wget https://download.oracle.com/java/19/archive/jdk-19.0.2_linux-x64_bin.tar.gz
sudo tar -xzf jdk-19.0.2_linux-x64_bin.tar.gz -C /opt/java/
sudo ln -sf /opt/java/jdk-19.0.2 /opt/java/current

# Install Hadoop 3.3.5
sudo mkdir -p /opt/hadoop
wget https://archive.apache.org/dist/hadoop/common/hadoop-3.3.5/hadoop-3.3.5.tar.gz
sudo tar -xzf hadoop-3.3.5.tar.gz -C /opt/hadoop/
sudo ln -sf /opt/hadoop/hadoop-3.3.5 /opt/hadoop/current

# Configure environment variables
# Note: ~/.bashrc is your shell configuration file that runs every time you open a terminal
# The >> operator appends these export commands to make variables persistent across sessions
echo 'export JAVA_HOME=/opt/java/current' >> ~/.bashrc
echo 'export HADOOP_HOME=/opt/hadoop/current' >> ~/.bashrc
echo 'export PATH=$PATH:$JAVA_HOME/bin:$HADOOP_HOME/bin' >> ~/.bashrc
source ~/.bashrc  # Reload the configuration to apply changes immediately

# Clean up downloads
rm /tmp/*.tar.gz

# Configure git (if not already done)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global init.defaultBranch main

# Create Repos directory and clone project
mkdir -p ~/Repos
cd ~/Repos
git clone https://github.com/JohnYanez95/hvac-assistant.git

# Install Docker
# curl downloads the Docker install script (-f=fail on errors, -s=silent, -S=show errors, -L=follow redirects)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
# usermod adds your user to docker group (-a=append, -G=group, $USER=your username)
sudo usermod -aG docker $USER

# Important: Exit and restart WSL to apply group changes
# exit
# wsl ~
# docker --version
```


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
├── embeddings/
│   └── faiss_index/       # FAISS vector database storage
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── TODO.md
```

## Current Development Status

### Legal Compliance Research (In Progress)
**Target Manufacturers**: Carrier, Goodman, Trane, Amana, American Standard, Fuji, Rheem, York, Daikin, Heil, Bryant, Coleman, Lennox
**Status**: Researching robots.txt, Terms of Service, and public documentation access for each manufacturer
**Approach**: Prioritize manufacturers with clearly public documentation libraries

### Learning Phase
**Docker**: Following structured learning path in `learnings/docker-guide.md`
**Next**: Complete Docker fundamentals before implementation

## Development Commands

### Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Docker commands (after learning Docker)
docker-compose up --build
docker-compose down
```

### Testing Commands
```bash
# Run individual scripts
python scripts/scrape_pdfs.py
python scripts/parse_and_chunk.py
python scripts/generate_embeddings.py
python scripts/query_pipeline.py

# Test queries
python scripts/query_pipeline.py --query "What is the BTU rating for furnace model XYZ?"
```

### Documentation Commands
```bash
# Review all markdown files
cat *.md

# Review specific documentation
cat README.md TODO.md CLAUDE.md
```

### Development Guidelines
- Use type hints throughout the codebase
- Follow PEP 8 style guidelines
- Add docstrings to all functions and classes
- Implement proper error handling and logging
- Use environment variables for configuration
- Write modular, testable code

## Key Dependencies
- `langchain>=0.1.0` - RAG framework
- `sentence-transformers>=2.2.2` - Embedding models
- `faiss-cpu>=1.7.4` - Vector similarity search
- `pdfplumber>=0.9.0` - PDF text extraction
- `beautifulsoup4>=4.12.0` - Web scraping
- `requests>=2.31.0` - HTTP requests

## Future Enhancements
- Streamlit web interface
- Continuous deployment pipeline
- Multi-modal support (images, diagrams)
- Real-time data updates

## Notes
- Keep Docker images lightweight
- Implement incremental updates for new PDFs
- Focus on modular, maintainable code
- Plan for Streamlit UI integration

## Claude's Memories
- Let's add that information in as well.