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

1. Clone the repository
2. Set up your environment (see [Docker Learning Guide](learnings/docker-guide.md) for containerized deployment)
3. Complete legal compliance research (in progress)
4. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

## Learning Resources

- **[Docker Guide](learnings/docker-guide.md)** - Complete Docker setup and learning path for this project

## Future Roadmap

- Streamlit web interface
- Continuous deployment pipeline
- Multi-modal support (images, diagrams)
- Real-time data updates 
