---
title: API Examples
layout: default
nav_order: 8
---

# API Examples

## Working with Entities

### Create Multiple Entities
```python
import requests

def create_entities(entities):
    url = 'http://localhost:8000/entities/batch'
    response = requests.post(url, json={'entities': entities})
    return response.json()

# Example usage
entities = [
    {'name': 'CameraPlugin', 'entity_type': 'Plugin'},
    {'name': 'VideoStream', 'entity_type': 'Interface'}
]
result = create_entities(entities)
```

### Query Entities with Filtering
```python
def query_entities(entity_type=None, name_pattern=None):
    url = 'http://localhost:8000/entities/'
    params = {}
    if entity_type:
        params['type'] = entity_type
    if name_pattern:
        params['name'] = name_pattern
    response = requests.get(url, params=params)
    return response.json()
```

## Managing Relations

### Create Complex Relations
```python
def create_relation_chain(entities):
    url = 'http://localhost:8000/relations/chain'
    response = requests.post(url, json={'entities': entities})
    return response.json()

# Example usage
chain = [
    {'name': 'UIComponent', 'relation': 'contains'},
    {'name': 'Button', 'relation': 'implements'},
    {'name': 'ClickHandler', 'relation': 'uses'}
]
result = create_relation_chain(chain)
```