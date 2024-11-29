# Semantic MCP Layer

A working implementation of a semantic layer that enhances the MCP memory server with real pattern matching and type inference capabilities.

## Features

- SQLite-based pattern storage
- Real-time type inference with confidence scoring
- Pattern matching with attribute validation
- API endpoints for inference and pattern management

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1. Start the server:
```bash
python src/api.py
```

2. Test the functionality:
```bash
python tests/test_semantic.py
```

## API Endpoints

### Infer Types
POST `/infer`
```json
{
    "id": "doc1",
    "attributes": {
        "title": "Project Document",
        "format": "pdf"
    }
}
```

### Get Patterns
GET `/patterns`

## How It Works

1. Pattern Matching:
   - Validates required attributes
   - Checks string patterns and values
   - Applies keyword matching

2. Confidence Scoring:
   - Weights required vs optional attributes
   - Adjusts for pattern specificity
   - Considers attribute match quality

3. Storage:
   - Patterns stored in SQLite
   - Inference results cached
   - Pattern confidence tracked

## Development

- Add new patterns in `semantic_core.py`
- Extend pattern matching in `_match_value`
- Add new API endpoints in `api.py`