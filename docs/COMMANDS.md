# Memory Graph MCP Tool Commands

## Command Reference

### 1. infer_type

Infers the type of a document based on its attributes.

**Parameters:**
```json
{
    "id": "string (required)",
    "attributes": {
        "title": "string (required)",
        "format": "string (required)",
        "author": "string (optional)",
        "pages": "integer (optional)"
    }
}
```

**Response:**
```json
{
    "status": "success",
    "data": {
        "inferred_types": {
            "Document": 0.85,
            "Report": 0.75
        },
        "best_match": "Document",
        "confidence": 0.85
    }
}
```

### 2. add_pattern

Adds a new pattern for document type matching.

**Parameters:**
```json
{
    "id": "string (required)",
    "type": "string (required)",
    "pattern_data": {
        "attribute_patterns": {
            "attribute_name": {
                "type": "string (required)",
                "required": "boolean",
                "values": ["array of allowed values"],
                "keywords": ["array of keywords"],
                "pattern": "regex pattern string"
            }
        }
    },
    "confidence": "number (0-1, optional, default: 0.7)"
}
```

### 3. get_patterns

Retrieves all registered patterns.

**Response:**
```json
{
    "status": "success",
    "data": [
        {
            "id": "string",
            "type": "string",
            "pattern_data": {
                "attribute_patterns": {...}
            },
            "confidence": "number"
        }
    ]
}
```

## Error Handling

All commands may return error responses in the following format:

```json
{
    "status": "error",
    "message": "Error description",
    "validation_errors": [ // Optional, present for validation errors
        {
            "loc": ["field_name"],
            "msg": "error message",
            "type": "error_type"
        }
    ]
}
```

## Usage with Claude

### Basic Pattern Recognition
```python
# Add a pattern for recognizing technical documents
await memory_graph.handle_request({
    'command': 'add_pattern',
    'parameters': {
        'id': 'tech_doc',
        'type': 'TechnicalDocument',
        'pattern_data': {
            'attribute_patterns': {
                'title': {
                    'type': 'string',
                    'required': True,
                    'keywords': ['technical', 'specification', 'documentation']
                },
                'format': {
                    'type': 'string',
                    'values': ['pdf', 'doc']
                }
            }
        }
    }
})

# Test document recognition
await memory_graph.handle_request({
    'command': 'infer_type',
    'parameters': {
        'id': 'doc1',
        'attributes': {
            'title': 'Technical Specification v1.0',
            'format': 'pdf'
        }
    }
})
```