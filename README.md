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

## Usage

1. First create the base tables:
```sql
sqlite3 memory_graph.db < schema.sql
```

2. Then add the semantic layer:
```sql
sqlite3 memory_graph.db < semantic_layer.sql
```

## Example Queries

### Get all implementations with their interfaces:
```sql
WITH RECURSIVE interface_hierarchy AS (
    SELECT 
        e1.name as implementation,
        e2.name as interface,
        1 as level
    FROM relations r
    JOIN entities e1 ON e1.id = r.from_entity_id
    JOIN entities e2 ON e2.id = r.to_entity_id
    JOIN relation_types rt ON rt.relation_name = r.relation_type
    WHERE rt.semantic_category = 'inheritance'
)
SELECT * FROM interface_hierarchy;
```

### Validate relationships:
```sql
SELECT 
    e1.name as from_entity,
    e1.entity_type as from_type,
    r.relation_type,
    e2.name as to_entity,
    e2.entity_type as to_type,
    CASE 
        WHEN vtr.id IS NULL THEN 'Invalid'
        ELSE 'Valid'
    END as validity
FROM relations r
JOIN entities e1 ON e1.id = r.from_entity_id
JOIN entities e2 ON e2.id = r.to_entity_id
LEFT JOIN valid_type_relations vtr ON 
    vtr.from_type = e1.entity_type AND
    vtr.relation_type = r.relation_type AND
    vtr.to_type = e2.entity_type;
```