# SmartDoc AI - API Documentation

## Base URL

```
http://localhost:8000/api
```

## Authentication

All endpoints (except `/auth/register` and `/auth/login`) require a valid JWT token in the `Authorization` header:

```
Authorization: Bearer <your_access_token>
```

---

## Authentication Endpoints

### Register User

**Endpoint:** `POST /auth/register`

**Description:** Create a new user account

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "created_at": "2026-08-20T12:00:00"
}
```

**Error Responses:**
- `400 Bad Request` - Validation error
- `409 Conflict` - User already exists

---

### Login

**Endpoint:** `POST /auth/login`

**Description:** Authenticate user and get JWT token

**Request Body:**
```json
{
  "username": "john_doe",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid credentials

---

### Get Current User

**Endpoint:** `GET /auth/me`

**Description:** Get information about the currently authenticated user

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "created_at": "2026-08-20T12:00:00"
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid or expired token

---

## Document Endpoints

### Upload Document

**Endpoint:** `POST /documents/upload`

**Description:** Upload a document (PDF or TXT)

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

**Request Parameters:**
- `file` (file, required) - PDF or TXT file to upload
- `title` (string, optional) - Document title

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/api/documents/upload" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@document.pdf" \
  -F "title=My Document"
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "My Document",
  "filename": "document_1692547200.pdf",
  "file_size": 102400,
  "file_type": "pdf",
  "pages": 5,
  "created_at": "2026-08-20T12:00:00",
  "updated_at": "2026-08-20T12:00:00"
}
```

**Error Responses:**
- `400 Bad Request` - Invalid file format
- `413 Payload Too Large` - File exceeds size limit
- `401 Unauthorized` - Invalid token

---

### List Documents

**Endpoint:** `GET /documents/`

**Description:** Get list of all user's documents

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `skip` (integer, optional, default: 0) - Number of records to skip
- `limit` (integer, optional, default: 10) - Number of records to return

**Example:**
```bash
curl -X GET "http://localhost:8000/api/documents/?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response (200 OK):**
```json
{
  "total": 2,
  "documents": [
    {
      "id": 1,
      "title": "My Document",
      "filename": "document_1692547200.pdf",
      "file_size": 102400,
      "file_type": "pdf",
      "pages": 5,
      "created_at": "2026-08-20T12:00:00",
      "updated_at": "2026-08-20T12:00:00"
    }
  ]
}
```

---

### Get Document Details

**Endpoint:** `GET /documents/{document_id}`

**Description:** Get detailed information about a specific document

**Headers:**
```
Authorization: Bearer <access_token>
```

**Path Parameters:**
- `document_id` (integer, required) - Document ID

**Example:**
```bash
curl -X GET "http://localhost:8000/api/documents/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "My Document",
  "filename": "document_1692547200.pdf",
  "file_size": 102400,
  "file_type": "pdf",
  "pages": 5,
  "content_preview": "First 500 characters of document...",
  "created_at": "2026-08-20T12:00:00",
  "updated_at": "2026-08-20T12:00:00"
}
```

**Error Responses:**
- `404 Not Found` - Document not found
- `401 Unauthorized` - Invalid token

---

### Delete Document

**Endpoint:** `DELETE /documents/{document_id}`

**Description:** Delete a document

**Headers:**
```
Authorization: Bearer <access_token>
```

**Path Parameters:**
- `document_id` (integer, required) - Document ID

**Example:**
```bash
curl -X DELETE "http://localhost:8000/api/documents/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response (200 OK):**
```json
{
  "message": "Document deleted successfully"
}
```

**Error Responses:**
- `404 Not Found` - Document not found
- `401 Unauthorized` - Invalid token

---

## Search Endpoints

### Semantic Search

**Endpoint:** `POST /search/semantic`

**Description:** Perform semantic search across user's documents

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "query": "machine learning algorithms",
  "top_k": 5,
  "document_ids": [1, 2]
}
```

**Request Parameters:**
- `query` (string, required) - Search query
- `top_k` (integer, optional, default: 5) - Number of results to return
- `document_ids` (array, optional) - Filter results to specific documents

**Example:**
```bash
curl -X POST "http://localhost:8000/api/search/semantic" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "machine learning",
    "top_k": 5
  }'
```

**Response (200 OK):**
```json
{
  "query": "machine learning algorithms",
  "results": [
    {
      "rank": 1,
      "score": 0.8756,
      "document_id": 1,
      "document_title": "ML Basics",
      "content": "Machine learning is a subset of artificial intelligence...",
      "start_char": 0,
      "end_char": 150
    }
  ],
  "total_results": 1,
  "search_time_ms": 145
}
```

---

### Ask Question

**Endpoint:** `POST /search/ask`

**Description:** Ask a question about documents and get an answer

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "question": "What is machine learning?",
  "use_context": true,
  "top_k": 3,
  "document_ids": [1]
}
```

**Request Parameters:**
- `question` (string, required) - Question to ask
- `use_context` (boolean, optional, default: true) - Include document context
- `top_k` (integer, optional, default: 3) - Number of context chunks to use
- `document_ids` (array, optional) - Filter to specific documents

**Example:**
```bash
curl -X POST "http://localhost:8000/api/search/ask" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is machine learning?",
    "use_context": true
  }'
```

**Response (200 OK):**
```json
{
  "question": "What is machine learning?",
  "answer": "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience...",
  "context_sources": [
    {
      "document_id": 1,
      "document_title": "ML Basics",
      "content": "Machine learning is a subset of artificial intelligence...",
      "relevance_score": 0.92
    }
  ],
  "confidence": 0.85
}
```

---

### Search History

**Endpoint:** `GET /search/history`

**Description:** Get user's search history

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `skip` (integer, optional, default: 0) - Number of records to skip
- `limit` (integer, optional, default: 10) - Number of records to return

**Example:**
```bash
curl -X GET "http://localhost:8000/api/search/history?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response (200 OK):**
```json
{
  "total": 5,
  "history": [
    {
      "id": 1,
      "query": "machine learning",
      "search_type": "semantic",
      "results_count": 3,
      "created_at": "2026-08-20T12:00:00"
    }
  ]
}
```

---

## Error Responses

All endpoints follow consistent error response format:

### 400 Bad Request
```json
{
  "detail": "Validation error details"
}
```

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 403 Forbidden
```json
{
  "detail": "Access denied"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limiting

The API currently has no rate limiting. For production, consider implementing:
- Request rate limiting per user
- Token refresh mechanisms
- Request timeout limits

---

## Pagination

List endpoints support pagination:
- `skip` - Number of items to skip (default: 0)
- `limit` - Number of items to return (default: 10, max: 100)

Example:
```bash
# Get items 11-20
curl "http://localhost:8000/api/documents/?skip=10&limit=10"
```

---

## Data Types

### Document
```json
{
  "id": 1,
  "title": "string",
  "filename": "string",
  "file_size": 0,
  "file_type": "pdf|txt",
  "pages": 0,
  "created_at": "2026-08-20T12:00:00",
  "updated_at": "2026-08-20T12:00:00"
}
```

### User
```json
{
  "id": 1,
  "username": "string",
  "email": "string",
  "created_at": "2026-08-20T12:00:00"
}
```

### Search Result
```json
{
  "rank": 0,
  "score": 0.0,
  "document_id": 0,
  "document_title": "string",
  "content": "string",
  "start_char": 0,
  "end_char": 0
}
```

---

## Best Practices

1. **Always include error handling** - Check status codes and error details
2. **Cache tokens** - Reuse access tokens until expiration
3. **Use pagination** - For large result sets
4. **Optimize file size** - Keep documents under 50MB
5. **Handle timeouts** - Large documents may take time to process
6. **Keep queries concise** - Better search results with focused queries

---

## Support

For API issues or questions:
- Check Swagger documentation: `http://localhost:8000/docs`
- Review examples in this documentation
- Check GitHub issues: https://github.com/Oliedambaz/SmartDoc-AI/issues

---

**Last Updated:** August 20, 2026
**API Version:** 1.0.0
