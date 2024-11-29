---
title: API Reference
layout: default
nav_order: 3
---

# API Reference

## Core Endpoints

### Entity Management

#### Create Entity
`POST /entities/`

Creates a new entity in the system.

**Request Body:**
```json
{
  "name": "string",
  "entity_type": "string"
}
```

**Response:**
```json
{
  "id": "integer",
  "name": "string",
  "entity_type": "string",
  "created_at": "datetime"
}
```

**Status Codes:**
- 201: Entity created successfully
- 400: Invalid input
- 409: Entity already exists

#### Get Entities
`GET /entities/`

Retrieves all entities matching the specified criteria.

**Query Parameters:**
- type (optional): Filter by entity type
- name (optional): Filter by name pattern
- limit (optional): Maximum number of results
- offset (optional): Pagination offset

**Response:**
```json
{
  "total": "integer",
  "items": [
    {
      "id": "integer",
      "name": "string",
      "entity_type": "string",
      "created_at": "datetime"
    }
  ]
}
```

### Relation Management

#### Create Relation
`POST /relations/`

Creates a new relation between entities.

**Request Body:**
```json
{
  "from_entity_id": "integer",
  "to_entity_id": "integer",
  "relation_type": "string"
}
```

**Response:**
```json
{
  "id": "integer",
  "from_entity_id": "integer",
  "to_entity_id": "integer",
  "relation_type": "string",
  "created_at": "datetime"
}
```

### Observation Management

#### Create Observation
`POST /observations/`

Creates a new observation for an entity.

**Request Body:**
```json
{
  "entity_id": "integer",
  "relation_id": "integer",
  "observation": "string"
}
```

**Response:**
```json
{
  "id": "integer",
  "entity_id": "integer",
  "relation_id": "integer",
  "observation": "string",
  "created_at": "datetime"
}
```

## Advanced Endpoints

### Batch Operations

#### Batch Create Entities
`POST /entities/batch`

Creates multiple entities in a single request.

**Request Body:**
```json
{
  "entities": [
    {
      "name": "string",
      "entity_type": "string"
    }
  ]
}
```

#### Batch Create Relations
`POST /relations/batch`

Creates multiple relations in a single request.

**Request Body:**
```json
{
  "relations": [
    {
      "from_entity_id": "integer",
      "to_entity_id": "integer",
      "relation_type": "string"
    }
  ]
}
```