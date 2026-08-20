# Contributing to SmartDoc AI

Thank you for your interest in contributing to SmartDoc AI! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please read our code of conduct before participating.

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples to demonstrate those steps**
- **Describe the behavior you observed after following the steps**
- **Explain which behavior you expected to see instead and why**
- **Include screenshots if possible**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Explain why this enhancement would be useful**
- **List some other applications where this enhancement exists**

### Pull Requests

- Fill in the required template
- Follow Python style guides
- Include appropriate test cases
- Document new code
- End all files with a newline

## Development Setup

### Prerequisites

- Python 3.9+
- pip and virtualenv
- Git

### Local Development

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/SmartDoc-AI.git
   cd SmartDoc-AI
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov black flake8 mypy
   ```

4. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

5. **Make your changes**

6. **Test your changes**
   ```bash
   pytest
   pytest --cov=app
   ```

7. **Format your code**
   ```bash
   black app/
   flake8 app/
   mypy app/
   ```

8. **Commit your changes**
   ```bash
   git commit -m "Add your commit message here"
   ```

9. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

10. **Submit a pull request**

## Style Guide

### Python Style

We follow PEP 8 with the following tools:

- **Black** - Code formatting
- **Flake8** - Code linting
- **MyPy** - Type checking

### Code Style Rules

```python
# Use type hints
def process_document(file_path: str, user_id: int) -> Dict[str, Any]:
    """
    Process a document file.
    
    Args:
        file_path: Path to the document file
        user_id: ID of the user uploading the file
        
    Returns:
        Dictionary containing processing results
    """
    pass

# Use descriptive variable names
documents = []  # Good
docs = []       # Avoid

# Use docstrings for all functions
def calculate_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    pass

# Use constants for magic numbers
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
TOP_K_RESULTS = 5
```

### Naming Conventions

- **Classes**: `PascalCase` (e.g., `DocumentProcessor`)
- **Functions/Methods**: `snake_case` (e.g., `process_document`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_FILE_SIZE`)
- **Private methods**: `_leading_underscore` (e.g., `_process_chunk`)

## Testing

All new features should include tests.

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run specific test
pytest tests/test_auth.py::test_user_registration
```

### Writing Tests

```python
import pytest
from app.security import hash_password, verify_password

def test_password_hashing():
    """Test password hashing and verification."""
    password = "test_password_123"
    hashed = hash_password(password)
    
    assert hashed != password
    assert verify_password(password, hashed)

def test_password_verification_fails_with_wrong_password():
    """Test that verification fails with incorrect password."""
    password = "correct_password"
    hashed = hash_password(password)
    
    assert not verify_password("wrong_password", hashed)
```

## Commit Messages

Use clear and descriptive commit messages:

```
# Good
Add semantic search functionality to document search

Implement vector embeddings using Sentence Transformers
and add semantic search API endpoint.

- Add vector_search.py module
- Implement embedding generation
- Add semantic search endpoint
- Add tests for search functionality

# Avoid
fix bug
update code
changes
```

## Documentation

All contributions should include documentation:

1. **Docstrings** for all public functions and classes
2. **Comments** for complex logic
3. **Update README.md** if adding new features
4. **Update API_DOCUMENTATION.md** for API changes

### Docstring Format

```python
def upload_document(file: UploadFile, user_id: int) -> DocumentResponse:
    """
    Upload and process a document for a user.
    
    This function handles file validation, storage, and initial
    text extraction for both PDF and TXT files.
    
    Args:
        file: The uploaded file object
        user_id: ID of the user uploading the file
        
    Returns:
        DocumentResponse containing document metadata
        
    Raises:
        ValueError: If file type is not supported
        FileSizeError: If file exceeds maximum size limit
        
    Example:
        >>> response = upload_document(file, user_id=1)
        >>> print(response.document_id)
        1
    """
    pass
```

## Project Structure

When adding new features, follow the existing structure:

```
app/
├── routes/           # API route handlers
│   └── new_feature.py
├── models.py         # Database models (update as needed)
├── schemas.py        # Pydantic schemas (update as needed)
└── new_module.py     # New functionality
```

## Database Changes

If your changes require database modifications:

1. Update `app/models.py`
2. Document the schema change
3. Test with fresh database initialization
4. Include migration notes in PR description

## API Changes

If adding or modifying API endpoints:

1. Update `API_DOCUMENTATION.md`
2. Include example requests and responses
3. Document all parameters and error responses
4. Add FastAPI docstrings to route handlers

## Security Considerations

- Never commit secrets or API keys
- Use environment variables for sensitive data
- Always hash passwords before storing
- Validate and sanitize user input
- Use parameterized queries (SQLAlchemy handles this)
- Add security tests for authentication features

## Performance

Consider performance when making changes:

- Use appropriate data structures
- Avoid N+1 queries
- Cache expensive operations when appropriate
- Profile code for bottlenecks
- Document performance implications in PR

## Troubleshooting

### Common Issues

**Virtual environment not activating**
```bash
# Try full path
source /full/path/to/venv/bin/activate
```

**Import errors after changes**
```bash
pip install -e .
```

**Database errors**
```bash
# Reset database
rm smartdoc.db
python -m uvicorn app.main:app --reload
```

## Getting Help

- **Questions**: Open a discussion on GitHub
- **Issues**: Check existing issues first
- **Documentation**: See README.md and SETUP.md
- **API Help**: Check API_DOCUMENTATION.md

## Review Process

1. **Automated Checks**: GitHub Actions runs tests and linting
2. **Code Review**: Maintainers review for quality and correctness
3. **Approval**: Requires at least one approval
4. **Merge**: Maintainers merge after approval

## Release Process

- Releases follow semantic versioning
- Version updates in `app/__init__.py`
- Changelog entries in release notes
- Tags are created for releases

## Areas for Contribution

### High Priority
- [ ] LLM integration (Ollama, GPT)
- [ ] PostgreSQL support
- [ ] Advanced search filters
- [ ] Performance optimization

### Medium Priority
- [ ] Multi-language support
- [ ] Document collaboration
- [ ] Enhanced analytics
- [ ] Export functionality

### Low Priority
- [ ] UI improvements
- [ ] Documentation enhancements
- [ ] Example notebooks
- [ ] Community tools

## Questions?

Feel free to:
1. Check existing documentation
2. Open an issue with your question
3. Start a discussion on GitHub
4. Review existing code and PRs

## License

By contributing to SmartDoc AI, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to SmartDoc AI! 🎉**

We appreciate your time and effort to make this project better.
