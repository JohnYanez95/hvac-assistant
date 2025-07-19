# HVAC Assistant - Claude Context

## Project Overview
This is an NLP project using LangChain and Docker to create a locally deployable assistant for answering technical questions about HVAC furnace models. The system uses retrieval-augmented generation (RAG) with scraped PDF manuals.

## Technology Stack
- **Language**: Python 3.11+
- **ML Framework**: LangChain
- **Embeddings**: SentenceTransformers (all-MiniLM-L6-v2)
- **Vector DB**: FAISS (primary) or ChromaDB
- **Containerization**: Docker & Docker Compose
- **PDF Processing**: pdfplumber
- **Web Scraping**: requests, BeautifulSoup4

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