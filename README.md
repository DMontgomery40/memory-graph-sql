
# MCP Server with Enhanced Semantic Layer

This repository contains a robust **Model Context Protocol (MCP)** server implementation that incorporates an enhanced **Semantic Layer for Memory Graph**. The server is built using **FastAPI** and **SQLAlchemy**, providing RESTful API endpoints for managing entities, observations, relations, and insights with semantic validations.

## Project Structure

mcp_server/ ├── README.md ├── requirements.txt ├── main.py ├── models.py ├── database.py ├── semantic_layer.sql └── example_requests.py



### Files

- **schema.sql**: Base tables and data model for entities, observations, and relations.
- **semantic_layer.sql**: Enhanced semantic relationships, type hierarchy, and constraints.
- **database.py**: Database connection and initialization.
- **models.py**: SQLAlchemy ORM models for the database tables.
- **main.py**: FastAPI server with API endpoints.
- **requirements.txt**: Python dependencies.
- **example_requests.py**: Example Python scripts to interact with the MCP server.
- **README.md**: Project documentation.

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/mcp_server.git
cd mcp_server
2. Create a Virtual Environment
It's recommended to use a virtual environment to manage dependencies.


python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Dependencies
bash
Copy code
pip install -r requirements.txt
4. Initialize the Database
Ensure that semantic_layer.sql and schema.sql are in the project root directory.


python
>>> from database import init_db
>>> init_db()
>>> exit()
This will create a memory_graph.db SQLite database with the necessary tables and initial data.

5. Run the MCP Server
bash
Copy code
uvicorn main:app --reload
The server will start at http://127.0.0.1:8000.

API Endpoints
1. Create an Entity
Endpoint: POST /entities/

Request Body:

json
Copy code
{
  "name": "Hikvision",
  "entity_type": "Plugin"
}
Response:


{
  "id": 1,
  "name": "Hikvision",
  "entity_type": "Plugin"
}
2. Read Entities
Endpoint: GET /entities/

Response:


[
  {
    "id": 1,
    "name": "Hikvision",
    "entity_type": "Plugin"
  },
  ...
]
3. Create an Observation
Endpoint: POST /observations/

Request Body:


{
  "entity_id": 1,
  "relation_id": 2,
  "observation": "Supports cameras and NVRs"
}
Response:


{
  "id": 1,
  "entity_id": 1,
  "relation_id": 2,
  "observation": "Supports cameras and NVRs"
}
4. Create a Relation
Endpoint: POST /relations/

Request Body:


{
  "from_entity_id": 1,
  "to_entity_id": 2,
  "relation_type": "implements"
}
Response:


{
  "id": 1,
  "from_entity_id": 1,
  "to_entity_id": 2,
  "relation_type": "implements"
}
5. Append an Insight
Endpoint: POST /insights/

Request Body:


{
  "insight": "Hikvision implements multiple video camera interfaces, enhancing interoperability."
}
Response:


{
  "message": "Insight added successfully."
}
6. Get Full Implementation Hierarchy
Endpoint: GET /hierarchy/

Response:


[
  {
    "implementation_id": 1,
    "implementation": "Hikvision",
    "interface_id": 2,
    "interface": "VideoCamera",
    "level": 1,
    "path": "Hikvision -> VideoCamera"
  },
  ...
]
7. Validate Relationships
Endpoint: GET /validate_relations/

Response:

[
  {
    "from_entity": "Hikvision",
    "from_type": "Plugin",
    "relation_type": "implements",
    "to_entity": "VideoCamera",
    "to_type": "Interface",
    "validity": "Valid",
    "valid_relation_id": 1
  },
  ...
]
8. Find All Implementations of a Specific Interface
Endpoint: GET /find_implementations/{interface_name}

Example: /find_implementations/VideoCamera

Response:


[
  {
    "implementation": "Hikvision",
    "impl_type": "Plugin",
    "relation_type": "implements",
    "interface": "VideoCamera",
    "attribute_key": "supports",
    "attribute_value": "High-definition streaming"
  },
  ...
]
Example Requests
You can use the provided example_requests.py script to interact with the MCP server.

example_requests.py

# example_requests.py
import requests

BASE_URL = "http://127.0.0.1:8000"

def create_entity(name, entity_type):
    url = f"{BASE_URL}/entities/"
    payload = {"name": name, "entity_type": entity_type}
    response = requests.post(url, json=payload)
    print("Create Entity:", response.json())

def create_relation(from_id, to_id, relation_type):
    url = f"{BASE_URL}/relations/"
    payload = {"from_entity_id": from_id, "to_entity_id": to_id, "relation_type": relation_type}
    response = requests.post(url, json=payload)
    print("Create Relation:", response.json())

def append_insight(insight):
    url = f"{BASE_URL}/insights/"
    payload = {"insight": insight}
    response = requests.post(url, json=payload)
    print("Append Insight:", response.json())

def query_entities(entity_type):
    url = f"{BASE_URL}/entities/"
    response = requests.get(url, params={"entity_type": entity_type})
    print("Query Entities:", response.json())

if __name__ == "__main__":
    # Example usage
    create_entity("Hikvision", "Plugin")
    create_entity("VideoCamera", "Interface")
    create_relation(1, 2, "implements")
    append_insight("Hikvision implements multiple video camera interfaces, enhancing interoperability.")
Run the script:


python example_requests.py
Best Practices and Recommendations
1. Version Control and Migrations
Migration Tools: Utilize migration tools like Alembic for managing database schema changes over time. This ensures consistency across different environments and facilitates collaborative development.
2. Automated Testing
Testing Frameworks: Implement automated tests using frameworks like pytest to test your API endpoints, database interactions, and business logic. This helps catch issues early during development.
3. Documentation
API Documentation: FastAPI automatically generates interactive API documentation at /docs using Swagger UI and at /redoc using ReDoc. Utilize these tools to provide comprehensive API documentation.

Entity-Relationship Diagrams: Maintain ER diagrams to visualize the database schema, aiding in understanding and onboarding new developers.

4. Backup and Recovery
Regular Backups: Implement regular backups of your memory_graph.db SQLite database to prevent data loss.

Recovery Strategy: Establish a clear recovery strategy to restore the database from backups in case of failures.

5. Security
Authentication and Authorization: Implement authentication (e.g., OAuth2, JWT) and authorization to secure your API endpoints and protect sensitive data.

Input Validation: Ensure all inputs are validated to prevent SQL injection and other security vulnerabilities.

6. Performance Optimization
Indexing: Ensure that your database indexes are optimized for the most frequently queried columns to enhance query performance.

Caching: Implement caching strategies (e.g., using Redis) for frequently accessed data to reduce database load and improve response times.

7. Scalability
Database Choice: While SQLite is suitable for development and small-scale deployments, consider migrating to more robust databases like PostgreSQL for production environments to handle higher loads and concurrent access.

Asynchronous Operations: Utilize FastAPI's asynchronous capabilities to handle multiple requests efficiently.

Conclusion
By following this comprehensive setup, you now have a fully functional MCP Server with an enhanced Semantic Layer for Memory Graph. This server allows for sophisticated management and querying of entities, relationships, and insights with robust semantic validations. Adhering to best practices ensures that your server remains maintainable, secure, and scalable as your project grows.

Feel free to extend the server's functionality based on your specific requirements and integrate additional features as needed. If you encounter any issues or have further questions, don't hesitate to reach out!
