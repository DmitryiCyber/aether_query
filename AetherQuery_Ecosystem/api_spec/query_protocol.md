# AetherQuery Protocol Specification

## Base URL

http://localhost:8000/api/v1


## Authentication
Currently no authentication required for development.

## Request Format
All requests must have:
- `Content-Type: application/json` header
- Valid JSON body according to schemas

## Response Format
All responses include:
- HTTP status code
- JSON body with standardized structure

## Error Handling
Errors follow consistent format:
```json
{
  "error": "ERROR_TYPE",
  "code": "SPECIFIC_ERROR_CODE", 
  "message": "Human readable message",
  "details": { ... },
  "timestamp": "2024-01-15T10:30:00Z"
}

Supported SQL
SELECT, INSERT, UPDATE, DELETE

Prepared statements with parameters

Transactions (via batch endpoints)
