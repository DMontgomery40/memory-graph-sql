# Memory Graph SQL with MCP Support

This repository combines the original Memory Graph SQL implementation with Model Context Protocol (MCP) support for Claude Desktop integration.

## Features

- SQLite-based pattern storage
- Real-time type inference with confidence scoring
- Pattern matching with attribute validation
- MCP integration for Claude Desktop
- API endpoints for standalone usage

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### As a Standalone API

1. Start the server:
```bash
python src/api.py
```

2. Test the functionality:
```bash
python tests/test_semantic.py
```

### With Claude Desktop (MCP)

1. Register the MCP tool:
```python
from src.mcp_adapter import MemoryGraphMCP
from mcp_core import register_tool

# Initialize the tool
memory_graph = MemoryGraphMCP()

# Register with Claude Desktop
register_tool('memory_graph', memory_graph)
```

2. Use in Claude Desktop with commands:

```python
# Infer types
response = await memory_graph.handle_request({
    'command': 'infer',
    'parameters': {
        'id': 'doc1',
        'attributes': {
            'title': 'Project Document',
            'format': 'pdf'
        }
    }
})

# Add pattern
response = await memory_graph.handle_request({
    'command': 'add_pattern',
    'parameters': {
        'id': 'pdf_doc',
        'type': 'Document',
        'pattern_data': {
            'attribute_patterns': {
                'title': {'type': 'string', 'required': True},
                'format': {'type': 'string', 'values': ['pdf']}
            }
        },
        'confidence': 0.8
    }
})

# Get patterns
response = await memory_graph.handle_request({
    'command': 'get_patterns',
    'parameters': {}
})
```

## Testing

Run all tests:
```bash
python -m unittest discover tests
```

## API Documentation

### REST API Endpoints

1. `/infer` (POST)
2. `/patterns` (GET)

### MCP Commands

1. `infer` - Infer types for a document
2. `add_pattern` - Add a new pattern
3. `get_patterns` - List all patterns

## Development

- Add new patterns in `semantic_core.py`
- Extend pattern matching in `_match_value`
- Add new API endpoints in `api.py`
- Modify MCP integration in `mcp_adapter.py`
