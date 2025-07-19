# HVAC Assistant

A local-first, open-source NLP assistant for answering technical questions about HVAC furnace models using LangChain and Docker.

## Overview

This project creates a locally deployable assistant capable of answering technical questions about HVAC furnace models by scraping, processing, and querying furnace manuals and specifications using retrieval-augmented generation (RAG).

## Features

- **PDF Scraping**: Automated collection of HVAC furnace PDFs from manufacturer websites
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
├── embeddings/
│   └── faiss_index/       # FAISS vector database storage
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── TODO.md               # Development roadmap
```

## Technology Stack

- **Language**: Python 3.11+
- **ML Framework**: LangChain
- **Embeddings**: SentenceTransformers (all-MiniLM-L6-v2 recommended)
- **Vector DB**: FAISS or ChromaDB
- **Containerization**: Docker & Docker Compose
- **PDF Processing**: PyPDF2/pdfplumber
- **Web Scraping**: requests, BeautifulSoup4

## Quick Start

1. Clone the repository
2. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

## Future Roadmap

- Streamlit web interface
- Continuous deployment pipeline
- Multi-modal support (images, diagrams)
- Real-time data updates 
