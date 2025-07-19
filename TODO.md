# HVAC Assistant Development TODO

## Phase 1: Core Infrastructure & MVP

### 1. Environment Setup
- [ ] Create requirements.txt with all dependencies
- [ ] Set up Docker configuration (Dockerfile + docker-compose.yml)
- [ ] Create project directory structure
- [ ] Initialize git repository with proper .gitignore

### 2. Data Collection & Processing
- [ ] Implement PDF scraping script (`scripts/scrape_pdfs.py`)
  - [ ] Identify target HVAC manufacturer websites
  - [ ] Implement robust scraping with rate limiting
  - [ ] Add error handling and retry logic
  - [ ] Save PDFs to `data/raw_pdfs/`
  
- [ ] Build PDF parsing and chunking (`scripts/parse_and_chunk.py`)
  - [ ] Extract text from PDFs (handle different formats)
  - [ ] Implement intelligent text chunking strategy
  - [ ] Clean and preprocess text
  - [ ] Save processed text to `data/processed_texts/`

### 3. Embedding & Vector Database
- [ ] Set up embedding generation (`scripts/generate_embeddings.py`)
  - [ ] Initialize SentenceTransformers model (all-MiniLM-L6-v2)
  - [ ] Generate embeddings for text chunks
  - [ ] Implement FAISS index creation and storage
  - [ ] Add metadata tracking for chunks

### 4. Query Pipeline
- [ ] Build LangChain retrieval system (`scripts/query_pipeline.py`)
  - [ ] Set up vector similarity search
  - [ ] Implement retrieval-augmented generation
  - [ ] Add query preprocessing and response formatting
  - [ ] Create simple CLI interface for testing

### 5. Testing & Validation
- [ ] Test end-to-end pipeline with sample HVAC manuals
- [ ] Validate embedding quality and retrieval accuracy
- [ ] Performance optimization and error handling
- [ ] Create sample queries and expected responses

## Phase 2: Enhanced Features

### 6. Advanced Processing
- [ ] Improve text chunking with semantic awareness
- [ ] Add support for tables and structured data
- [ ] Implement multi-document reasoning
- [ ] Add query expansion and synonym handling

### 7. Data Management
- [ ] Implement incremental updates for new PDFs
- [ ] Add data versioning and change tracking
- [ ] Create data validation and quality checks
- [ ] Implement backup and recovery procedures

## Phase 3: User Interface

### 8. Streamlit Web Interface
- [ ] Design and implement web UI
- [ ] Add file upload functionality
- [ ] Create query interface with history
- [ ] Implement result visualization and export

### 9. Deployment & Operations
- [ ] Set up continuous integration/deployment
- [ ] Add monitoring and logging
- [ ] Implement health checks and metrics
- [ ] Create user documentation and tutorials

## Dependencies & Versions

### Core Dependencies
- `langchain>=0.1.0`
- `sentence-transformers>=2.2.2`
- `faiss-cpu>=1.7.4` or `chromadb>=0.4.0`
- `pdfplumber>=0.9.0`
- `beautifulsoup4>=4.12.0`
- `requests>=2.31.0`
- `streamlit>=1.28.0` (Phase 3)

### Development Dependencies
- `pytest>=7.4.0`
- `black>=23.0.0`
- `flake8>=6.0.0`
- `pre-commit>=3.0.0`

## Recommended Models & Tools

### Embedding Models
- **Primary**: `all-MiniLM-L6-v2` (fast, good quality, 384 dimensions)
- **Alternative**: `all-mpnet-base-v2` (higher quality, 768 dimensions)

### Vector Databases
- **FAISS**: Fast, lightweight, good for MVP
- **ChromaDB**: More features, better for production

### Docker Setup
- Base image: `python:3.11-slim`
- Multi-stage build for smaller production image
- Volume mounts for data persistence
- Environment variable configuration

## Success Criteria

### MVP Success
- [ ] Successfully scrape and process 50+ HVAC manuals
- [ ] Answer 80%+ of technical questions accurately
- [ ] Response time under 3 seconds for queries
- [ ] Containerized deployment works on any system

### Production Ready
- [ ] Web interface with intuitive UX
- [ ] Continuous data updates
- [ ] 95%+ uptime and reliability
- [ ] Comprehensive documentation and testing