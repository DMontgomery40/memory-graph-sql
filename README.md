# Memory Graph SQL with Enhanced Semantic Layer

A Model Context Protocol (MCP) compliant implementation that extends the standard memory server with a powerful semantic layer for enhanced graph relationships and validations.

## MCP Compliance

This implementation strictly follows the MCP specification while adding semantic capabilities:

### Core MCP Operations

All standard MCP operations are implemented and guaranteed to work:
- `create_entities`
- `create_relations`
- `add_observations`
- `delete_entities`
- `delete_observations`
- `delete_relations`
- `read_graph`
- `search_nodes`
- `open_nodes`

### Semantic Extensions

The semantic layer is implemented as non-blocking extensions that enhance but never interfere with core MCP functionality:

1. Type System:
   - Rich type hierarchies (IS_A, CAN_BE, IMPLEMENTS)
   - Optional attribute validation
   - Semantic inference capabilities

2. Validation Layer:
   - Non-blocking semantic validation
   - Advisory rules and suggestions
   - Compatibility with core MCP operations

3. Enhanced Relations:
   - Semantic relationship validation
   - Extended relation attributes
   - Inference engine for relationship discovery

## Architecture

```
semantic_graph_server/
├── mcp/                  # Core MCP implementation
│   ├── operations.py     # Standard MCP operations
│   └── validation.py     # MCP validation
├── semantic/            # Semantic extensions
│   ├── type_system.py   # Type hierarchies
│   ├── operations.py    # Enhanced operations
│   └── inference.py     # Semantic inference
└── core/               # Shared components
    ├── config.py       # Server configuration
    └── database.py     # Database management
```

## Usage

### Core MCP Operations

```python
# Standard MCP entity creation
response = await client.post("/entities", json={
    "entities": [{
        "name": "example_entity",
        "type": "Document",
        "observations": ["Content here"]
    }]
})
```

### Semantic Features

```python
# Optional semantic validation
response = await client.post("/semantic/validate", json={
    "entity": {
        "name": "example_entity",
        "type": "Document",
        "attributes": {
            "format": "markdown"
        }
    }
})

# Get type hierarchies
response = await client.get("/semantic/types")
```

## Configuration

The server can be configured through environment variables or a .env file:

```env
DATABASE_URL=sqlite+aiosqlite:///./semantic_graph.db
MCP_SERVER_PORT=8000
SEMANTIC_VALIDATION_ENABLED=true
TYPE_SYSTEM_CONFIG=config/types.json
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/DMontgomery40/memory-graph-sql.git
cd memory-graph-sql
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the environment:
```bash
cp .env.example .env
# Edit .env with your settings
```

4. Run migrations:
```bash
alembic upgrade head
```

5. Start the server:
```bash
uvicorn main:app --reload
```

## Testing

Run the test suite to verify both MCP compliance and semantic features:

```bash
pytest tests/
```

## Contributing

Contributions are welcome! Please ensure:
1. Core MCP operations remain unaffected by changes
2. Semantic features are implemented as non-blocking extensions
3. All tests pass
4. Documentation is updated

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.