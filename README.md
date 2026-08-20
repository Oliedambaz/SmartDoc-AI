# SmartDoc AI

AI-Powered Document Search and Question Answering System

## Overview

SmartDoc AI is a intelligent document processing platform that enables users to upload documents (PDF, TXT) and perform advanced semantic searches and question answering. The system uses modern AI techniques including embeddings, vector search, and language models to provide accurate and contextual responses.

## Key Features

🚀 **Core Capabilities**
- **Document Upload**: Support for PDF and TXT files
- **Semantic Search**: AI-powered search using embeddings
- **Question Answering**: Get answers from your documents
- **User Authentication**: Secure JWT-based authentication
- **Document Management**: Upload, organize, and manage documents
- **Search History**: Track all searches and questions

🔒 **Security**
- Password hashing with bcrypt
- JWT token authentication
- User document isolation
- Secure file handling

⚡ **Performance**
- Vector embeddings for fast search
- Optimized database queries
- Async/await support
- Scalable architecture

## Technology Stack

### Backend
- **Framework**: FastAPI
- **Server**: Uvicorn
- **Database**: SQLAlchemy ORM with SQLite
- **Authentication**: JWT with python-jose
- **Password Security**: Passlib with bcrypt
- **Validation**: Pydantic

### AI/ML
- **Embeddings**: Sentence Transformers
- **Vector Search**: NumPy with cosine similarity
- **Text Processing**: PyPDF2 for PDF extraction

### Frontend
- **HTML5/CSS3**: Modern responsive interface
- **JavaScript**: Vanilla JS (no dependencies)

## Quick Start

### Installation

1. **Clone Repository**
```bash
git clone https://github.com/Oliedambaz/SmartDoc-AI.git
cd SmartDoc-AI
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Run Application**
```bash
python -m uvicorn app.main:app --reload
```

5. **Access Application**
- Web Interface: http://localhost:8000/index.html
- API Docs: http://localhost:8000/docs

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get token
- `GET /api/auth/me` - Get current user

### Documents
- `POST /api/documents/upload` - Upload document
- `GET /api/documents/` - List documents
- `GET /api/documents/{id}` - Get document details
- `DELETE /api/documents/{id}` - Delete document

### Search
- `POST /api/search/semantic` - Semantic search
- `POST /api/search/ask` - Ask questions
- `GET /api/search/history` - Search history

## Project Structure

```
SmartDoc-AI/
├── app/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Configuration
│   ├── database.py          # Database setup
│   ├── models.py            # DB models
│   ├── schemas.py           # Pydantic schemas
│   ├── security.py          # Authentication
│   ├── document_processor.py # File processing
│   ├── vector_search.py     # Search engine
│   └── routes/
│       ├── auth.py
│       ├── documents.py
│       └── search.py
├── index.html               # Frontend
├── requirements.txt         # Dependencies
├── .env.example             # Config template
├── README.md                # This file
└── SETUP.md                 # Setup guide
```

## Usage Examples

### 1. Register User
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"user1","email":"user@example.com","password":"pass123"}'
```

### 2. Login
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"user1","password":"pass123"}'
```

### 3. Upload Document
```bash
curl -X POST "http://localhost:8000/api/documents/upload" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@document.pdf" \
  -F "title=My Document"
```

### 4. Semantic Search
```bash
curl -X POST "http://localhost:8000/api/search/semantic" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"find information about topic X","top_k":5}'
```

### 5. Ask Question
```bash
curl -X POST "http://localhost:8000/api/search/ask" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question":"What is the main topic?","use_context":true}'
```

## Configuration

Create `.env` file (see `.env.example`):

```env
# Database
DATABASE_URL=sqlite:///./smartdoc.db

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
DEBUG=True
HOST=0.0.0.0
PORT=8000

# File Upload
MAX_UPLOAD_SIZE_MB=50

# Embedding
EMBEDDING_MODEL=all-MiniLM-L6-v2

# LLM
LLM_MODEL=mistral
OLLAMA_BASE_URL=http://localhost:11434
```

## Dependencies

See `requirements.txt` for complete list:

- fastapi==0.104.1
- uvicorn==0.24.0
- sqlalchemy==2.0.23
- pydantic==2.5.0
- python-jose==3.3.0
- passlib==1.7.4
- PyPDF2==3.17.1
- sentence-transformers==2.2.2
- numpy==1.24.3
- python-dotenv==1.0.0

## Features in Detail

### Document Processing
- Extracts text from PDF and TXT files
- Splits documents into chunks for better search
- Automatic text preprocessing

### Vector Search
- Uses Sentence Transformers for embeddings
- Cosine similarity for ranking results
- Fast in-memory search with numpy

### Authentication
- Secure password hashing with bcrypt
- JWT token-based authentication
- Token expiration management

### Database
- SQLAlchemy ORM for type safety
- SQLite for easy setup
- Easily upgradeable to PostgreSQL

## Future Enhancements

- [ ] Real LLM integration (Ollama, GPT)
- [ ] Document collaboration features
- [ ] Advanced filtering and analytics
- [ ] Multi-language support
- [ ] Document annotations
- [ ] Export functionality
- [ ] WebSocket for real-time updates
- [ ] API rate limiting
- [ ] Advanced caching strategies

## Performance Notes

- **First run**: Embedding model (~100MB) downloads automatically
- **Search speed**: Sub-second queries on typical documents
- **Concurrent users**: SQLite suitable for <10 concurrent users
- **Production**: Use PostgreSQL for better scalability

## Troubleshooting

### Common Issues

**Port already in use**
```bash
python -m uvicorn app.main:app --reload --port 8001
```

**Module not found**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

**Database errors**
- Delete `smartdoc.db` and restart application

**Slow embedding generation**
- First run caches model (~30 seconds)
- Subsequent runs are faster

## Development

### Code Quality
```bash
# Format code
black app/

# Lint
flake8 app/

# Type checking
mypy app/
```

### Testing
```bash
pytest
pytest --cov=app
```

## Deployment

### Docker
```bash
docker build -t smartdoc-ai .
docker run -p 8000:8000 smartdoc-ai
```

### Production Server
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

## Security Considerations

⚠️ **Important for Production**
- Change `SECRET_KEY` to a strong random value
- Set `DEBUG=False`
- Use HTTPS
- Use PostgreSQL instead of SQLite
- Set up proper CORS origins
- Add rate limiting
- Regular security audits

## Support

For issues and feature requests:
- 📝 [GitHub Issues](https://github.com/Oliedambaz/SmartDoc-AI/issues)
- 💬 [Discussions](https://github.com/Oliedambaz/SmartDoc-AI/discussions)

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Author

**Oliedambaz**
- GitHub: [@Oliedambaz](https://github.com/Oliedambaz)

---

**Made with ❤️ for better document management**

Visit [SETUP.md](SETUP.md) for detailed installation and configuration instructions.
