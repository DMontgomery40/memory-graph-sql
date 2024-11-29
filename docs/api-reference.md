---
title: API Reference
layout: default
nav_order: 3
---

# API Reference

## Endpoints Overview

### Entity Management

#### Create an Entity
- **Endpoint**: `POST /entities/`
- **Description**: Creates a new entity in the system
- **Request Body**:
  ```json
  {
    "name": "Hikvision",
    "entity_type": "Plugin"
  }
  ```

#### Get Entities
- **Endpoint**: `GET /entities/`
- **Description**: Retrieves all entities

### Observation Management

#### Create an Observation
- **Endpoint**: `POST /observations/`
- **Description**: Creates a new observation for an entity
- **Request Body**:
  ```json
  {
    "entity_id": 1,
    "relation_id": 2,
    "observation": "Supports cameras and NVRs"
  }
  ```