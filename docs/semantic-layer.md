---
title: Semantic Layer
layout: default
nav_order: 2
---

# Semantic Layer Architecture

## Core Concepts

The semantic layer is the distinguishing feature of this Memory Graph SQL implementation. It provides a sophisticated system for understanding and enforcing relationships between entities, going beyond simple graph connections to enable rich semantic validation and inference.

### Key Components

#### 1. Type System
```sql
CREATE TABLE type_hierarchy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_type TEXT NOT NULL,
    child_type TEXT NOT NULL,
    inheritance_type TEXT CHECK(inheritance_type IN ('IS_A', 'CAN_BE', 'IMPLEMENTS')) NOT NULL,
    metadata JSONB,
    UNIQUE(parent_type, child_type)
);

CREATE TABLE type_attributes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_name TEXT NOT NULL,
    attribute_name TEXT NOT NULL,
    attribute_type TEXT NOT NULL,
    is_required BOOLEAN DEFAULT false,
    validation_rules JSONB,
    UNIQUE(type_name, attribute_name)
);
```

#### 2. Semantic Relations
```sql
CREATE TABLE semantic_relations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_type TEXT NOT NULL,
    relation_type TEXT NOT NULL,
    to_type TEXT NOT NULL,
    cardinality TEXT CHECK(cardinality IN ('ONE_TO_ONE', 'ONE_TO_MANY', 'MANY_TO_ONE', 'MANY_TO_MANY')),
    constraints JSONB,
    inference_rules JSONB,
    UNIQUE(from_type, relation_type, to_type)
);
```

#### 3. Inference Engine
```sql
CREATE TABLE inference_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_name TEXT NOT NULL,
    pattern JSONB NOT NULL,  -- Describes the pattern to match
    inference TEXT NOT NULL, -- The relation or attribute to infer
    confidence FLOAT CHECK(confidence BETWEEN 0 AND 1),
    metadata JSONB
);
```

## Semantic Validation System

### Type Validation
```python
def validate_type_assignment(entity_type, attributes):
    # Check if type exists and validate all required attributes
    required_attrs = db.query(type_attributes)\
        .filter_by(type_name=entity_type, is_required=True)\
        .all()
    
    for attr in required_attrs:
        if attr.attribute_name not in attributes:
            raise ValidationError(f"Missing required attribute: {attr.attribute_name}")
        
        # Validate attribute value against rules
        validate_attribute(
            attributes[attr.attribute_name],
            attr.attribute_type,
            attr.validation_rules
        )
```

### Relation Validation
```python
def validate_relation(from_entity, relation_type, to_entity):
    # Get semantic relation rules
    rules = db.query(semantic_relations)\
        .filter_by(
            from_type=from_entity.type,
            relation_type=relation_type,
            to_type=to_entity.type
        ).first()
    
    if not rules:
        # Check type hierarchy for valid inheritance-based relations
        if not is_valid_through_hierarchy(from_entity.type, relation_type, to_entity.type):
            raise ValidationError("Invalid relation between types")
    
    # Check cardinality constraints
    validate_cardinality(from_entity, relation_type, to_entity, rules.cardinality)
    
    # Apply custom constraints
    apply_relation_constraints(from_entity, to_entity, rules.constraints)
```

## Inference Capabilities

### Pattern-Based Inference
```python
def infer_relations(entity):
    # Find applicable inference rules
    rules = db.query(inference_rules)\
        .filter(match_pattern(inference_rules.pattern, entity))\
        .all()
    
    inferred_relations = []
    for rule in rules:
        # Apply inference rule and calculate confidence
        inference = apply_inference_rule(rule, entity)
        if inference.confidence >= CONFIDENCE_THRESHOLD:
            inferred_relations.append(inference)
    
    return inferred_relations
```

### Semantic Propagation
```python
def propagate_semantics(entity, relation):
    # Identify semantic implications
    implications = db.query(semantic_implications)\
        .filter_by(source_relation=relation.type)\
        .all()
    
    for implication in implications:
        # Calculate transitive relations
        transitive_relations = calculate_transitive_relations(
            entity,
            implication.pattern,
            implication.depth_limit
        )
        
        # Apply semantic rules to transitive relations
        apply_semantic_rules(transitive_relations, implication.rules)
```

## Advanced Features

### Context-Aware Validation
```python
def validate_in_context(entity, context):
    # Get context-specific validation rules
    context_rules = db.query(context_validation_rules)\
        .filter_by(context_type=context.type)\
        .all()
    
    for rule in context_rules:
        # Apply contextual validation
        validate_contextual_rule(entity, rule, context)
```

### Semantic Query Enhancement
```python
def enhance_query(base_query, semantic_context):
    # Analyze query semantics
    semantic_patterns = analyze_query_semantics(base_query)
    
    # Enhance query with semantic understanding
    enhanced_query = apply_semantic_patterns(
        base_query,
        semantic_patterns,
        semantic_context
    )
    
    return enhanced_query
```

## Best Practices

### 1. Type Hierarchy Design
- Use specific, well-defined types
- Implement clear inheritance patterns
- Document type relationships

### 2. Relation Definition
- Define clear cardinality rules
- Implement comprehensive validation
- Use semantic constraints effectively

### 3. Inference Rule Creation
- Set appropriate confidence thresholds
- Define clear inference patterns
- Document rule implications

### 4. Performance Optimization
- Index frequently queried semantic patterns
- Cache common inference results
- Optimize validation checks

## Usage Examples

### Define Complex Type Hierarchies
```python
# Define a plugin type hierarchy
db.add_type_hierarchy(
    parent_type='Plugin',
    child_type='VideoPlugin',
    inheritance_type='IS_A',
    metadata={
        'capabilities': ['streaming', 'recording'],
        'validation_level': 'strict'
    }
)
```

### Create Semantic Relations
```python
# Define a semantic relation with constraints
db.add_semantic_relation(
    from_type='VideoPlugin',
    relation_type='IMPLEMENTS',
    to_type='StreamInterface',
    cardinality='ONE_TO_MANY',
    constraints={
        'requires_attributes': ['stream_protocol', 'max_resolution'],
        'validate_method': 'strict'
    }
)
```

### Apply Inference Rules
```python
# Create an inference rule
db.add_inference_rule(
    rule_name='stream_capability_inference',
    pattern={
        'type': 'VideoPlugin',
        'attributes': {
            'has_streaming': True
        }
    },
    inference='CAN_STREAM',
    confidence=0.95,
    metadata={
        'description': 'Infers streaming capability from plugin attributes',
        'author': 'system'
    }
)
```