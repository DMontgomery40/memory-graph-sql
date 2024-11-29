---
title: Semantic Layer
layout: default
nav_order: 6
---

# Semantic Layer

## Overview

The semantic layer in Memory Graph SQL provides enhanced meaning and structure to the relationships between entities. It enables validation of relationships, type hierarchies, and semantic constraints.

## Features

### Type Hierarchy
- Defines valid entity types and their relationships
- Enforces type constraints on relations
- Validates entity type assignments

### Relation Types
- Implements - For plugin implementation relationships
- Contains - For hierarchical relationships
- References - For loose coupling between entities
- Depends - For dependency relationships

### Semantic Validation
- Validates relation types between entity types
- Ensures data integrity through semantic rules
- Prevents invalid relationships

## Examples

### Type Hierarchy Definition
```sql
CREATE TABLE type_hierarchy (
    parent_type TEXT NOT NULL,
    child_type TEXT NOT NULL,
    PRIMARY KEY (parent_type, child_type)
);
```

### Valid Relations
```sql
CREATE TABLE valid_relations (
    from_type TEXT NOT NULL,
    relation_type TEXT NOT NULL,
    to_type TEXT NOT NULL,
    PRIMARY KEY (from_type, relation_type, to_type)
);
```