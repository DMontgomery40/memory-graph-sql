# Memory Graph SQL with Enhanced Semantic Layer

A sophisticated implementation of MCP (Model Context Protocol) that introduces a powerful semantic layer for enhanced graph relationships and validations. While MCP provides the foundation for entity-relation management, our semantic layer adds rich type hierarchies, intelligent relation validation, and semantic inference capabilities.

## Key Features

### Advanced Semantic Layer

What sets this implementation apart is its sophisticated semantic layer that provides:

- **Rich Type Hierarchies**
  - Multi-level type inheritance with IS_A, CAN_BE, and IMPLEMENTS relationships
  - Attribute-based type validation
  - Configurable inheritance rules

- **Intelligent Relation Validation**
  - Context-aware relationship validation
  - Cardinality enforcement
  - Custom constraint evaluation
  - Real-time semantic validation

- **Semantic Inference Engine**
  - Pattern-based relationship inference
  - Confidence scoring for inferred relations
  - Transitive relation calculation
  - Context-aware inference rules

### Standard MCP Features

- Entity Management
- Observation Tracking
- Relation Management
- Basic CRUD Operations

## Architecture

```
mcp_server/
├── semantic/
│   ├── type_system.py      # Type hierarchy and validation
│   ├── relations.py        # Semantic relation management
│   ├── inference.py        # Inference engine
│   └── validation.py       # Validation system
├── core/
│   ├── models.py           # Database models
│   ├── database.py         # Database connection
│   └── schemas.py          # Pydantic schemas
└── api/
    ├── routes/             # API endpoints
    └── dependencies.py      # API dependencies
```

## Semantic Layer Examples

### Type Hierarchy Definition
```python
# Define sophisticated type hierarchies
type_system.add_hierarchy({
    'parent': 'Plugin',
    'child': 'VideoPlugin',
    'inheritance': 'IS_A',
    'attributes': {
        'stream_capability': {'type': 'boolean', 'required': True},
        'protocols': {'type': 'array', 'items': 'string'}
    }
})
```

### Semantic Relation Validation
```python
# Define semantically validated relations
semantic.add_relation_rule({
    'from_type': 'VideoPlugin',
    'relation': 'IMPLEMENTS',
    'to_type': 'StreamInterface',
    'cardinality': 'ONE_TO_MANY',
    'constraints': {
        'required_attributes': ['stream_protocol'],
        'validation_mode': 'strict'
    }
})
```

### Inference Rule Definition
```python
# Create sophisticated inference rules
inference.add_rule({
    'name': 'stream_capability',
    'pattern': {
        'type': 'VideoPlugin',
        'attributes': {'has_streaming': True}
    },
    'inference': 'CAN_STREAM',
    'confidence_threshold': 0.95
})
```

## Setup

1. Clone the repository:
```bash
git clone https://github.com/DMontgomery40/memory-graph-sql.git
cd memory-graph-sql
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database:
```python
from database import init_db
init_db()
```

4. Run the server:
```bash
uvicorn main:app --reload
```

## Documentation

Comprehensive documentation is available at [https://dmontgomery40.github.io/memory-graph-sql/](https://dmontgomery40.github.io/memory-graph-sql/)

Key documentation sections:
- [Semantic Layer Architecture](docs/semantic-layer.md)
- [API Reference](docs/api-reference.md)
- [Best Practices](docs/best-practices.md)

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
