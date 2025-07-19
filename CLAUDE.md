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

### Core Dependencies (Required)
- **Python 3.10.9**: Download from [python.org](https://www.python.org/downloads/release/python-3109/)
- **Java JDK 19**: Download from [Oracle JDK](https://www.oracle.com/java/technologies/javase/jdk19-archive-downloads.html) or [OpenJDK](https://jdk.java.net/archive/)
- **Apache Hadoop 3.3.5**: Download from [Apache Hadoop](https://hadoop.apache.org/releases.html)
- **Apache Spark 3.5.2**: Included with PySpark installation via pip

### Environment Variables (Windows)
```cmd
set JAVA_HOME=C:\Program Files\Java\jdk-19
set HADOOP_HOME=C:\hadoop\hadoop-3.3.5
set PYSPARK_HOME=C:\Users\%USERNAME%\spark\spark-3.5.2-bin-hadoop3
set SPARK_HOME=C:\Users\%USERNAME%\spark\spark-3.5.2-bin-hadoop3
```

### Path Configuration
Add to Windows PATH:
- %JAVA_HOME%\bin
- %HADOOP_HOME%\bin
- %SPARK_HOME%\bin

### Optional Tools
- **Docker Desktop**: [Download for Windows](https://www.docker.com/products/docker-desktop/)
- **Git**: [Download for Windows](https://git-scm.com/download/win)

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

## Development Commands

### Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Docker commands
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