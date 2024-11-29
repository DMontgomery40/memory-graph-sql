# Semantic MCP Layer

An intelligent semantic layer that enhances the MCP memory server with advanced semantic capabilities.

## Features

### Type Inference
- Automatically infers entity types based on attributes and relationships
- Learns patterns from existing entities
- Maintains confidence scores and explanations for inferences

### Relationship Intelligence
- Suggests potential relationships between entities
- Identifies common relationship patterns
- Provides confidence scores for suggestions

### Semantic Pattern Learning
- Automatically learns patterns from entity interactions
- Improves accuracy over time through feedback
- Maintains a pattern database with success rates

### Attribute Derivation
- Derives additional attributes based on patterns
- Enhances entities with computed properties
- Maintains provenance of derived information

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Initialize the database:
```bash
alembic upgrade head
```

3. Start the server:
```bash
python start.py
```

## API Usage

### Enrich an Entity
```python
# Enrich an entity with semantic information
response = await client.post("/semantic/enrich", json={
    "id": "doc1",
    "type": "Document",
    "attributes": {
        "title": "Project Plan",
        "format": "pdf",
        "size": 1024
    }
})
```

### Learn Patterns
```python
# Learn patterns from a set of entities
response = await client.post("/semantic/learn", json={
    "entities": [
        {
            "id": "doc1",
            "type": "Document",
            "attributes": {...}
        },
        ...
    ]
})
```

### Get Semantic Patterns
```python
# Get learned patterns of a specific type
response = await client.get("/semantic/patterns/type_inference")
```

## Integration with MCP

This semantic layer seamlessly integrates with the MCP memory server:

1. Add to your MCP configuration:
```json
{
    "mcpServers": {
        "memory": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-memory"]
        },
        "semantic": {
            "command": "python",
            "args": ["start.py"]
        }
    }
}
```

2. The semantic layer will automatically enrich entities from the memory server

## How It Works

### Pattern Learning
The system learns patterns by analyzing:
- Attribute correlations
- Relationship structures
- Type hierarchies
- Common usage patterns

### Type Inference
Types are inferred using:
- Attribute patterns
- Relationship context
- Similar entity analysis
- Historical data

### Relationship Suggestions
Suggestions are based on:
- Pattern matching
- Graph analysis
- Semantic similarity
- Usage history

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Adding New Features
1. Create new pattern types in `semantic/patterns/`
2. Add corresponding inference logic in `semantic/engine.py`
3. Update API endpoints in `api/routes/semantic.py`
4. Add tests in `tests/`

## License
MIT License - see LICENSE file

## Contributing
Contributions welcome! Please read CONTRIBUTING.md