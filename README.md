# Memory Graph SQL Implementation

This repository contains a SQL implementation of a memory graph data model with semantic layer support.

## Structure

### Base Schema (`schema.sql`)
- Entities table
- Observations table
- Relations table

### Semantic Layer (`semantic_layer.sql`)
- Relation types with semantic categories
- Entity type hierarchy
- Valid relationship constraints

## Files
- `schema.sql`: Base tables and data model
- `semantic_layer.sql`: Semantic relationships and type system
- `example_queries.sql`: Sample queries demonstrating usage

## Setup

```bash
# Create database and base schema
sqlite3 memory_graph.db < schema.sql

# Add semantic layer
sqlite3 memory_graph.db < semantic_layer.sql
```

## Key Features

1. Base Schema
   - Entity management
   - Observation tracking
   - Relationship mapping

2. Semantic Layer
   - Relationship type classification
   - Type hierarchy management
   - Relationship validation

3. Advanced Queries
   - Inheritance hierarchy traversal
   - Implementation validation
   - Type consistency checking