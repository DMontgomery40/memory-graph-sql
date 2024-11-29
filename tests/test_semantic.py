import httpx
import asyncio
from typing import Dict, Any
import json

async def test_semantic_layer():
    """Test the semantic layer with real examples."""
    async with httpx.AsyncClient() as client:
        print("\nTesting Semantic Layer Functionality")
        print("===================================")
        
        # Test document inference
        doc = {
            "id": "doc1",
            "attributes": {
                "title": "Project Specification Document",
                "format": "pdf"
            }
        }
        
        print("\n1. Testing Document Inference:")
        print("Input:", json.dumps(doc, indent=2))
        response = await client.post("http://localhost:8000/infer", json=doc)
        print("Response:", json.dumps(response.json(), indent=2))
        
        # Test user inference
        user = {
            "id": "user1",
            "attributes": {
                "name": "John Smith",
                "email": "john@example.com"
            }
        }
        
        print("\n2. Testing User Inference:")
        print("Input:", json.dumps(user, indent=2))
        response = await client.post("http://localhost:8000/infer", json=user)
        print("Response:", json.dumps(response.json(), indent=2))
        
        # Test ambiguous entity
        ambiguous = {
            "id": "amb1",
            "attributes": {
                "title": "User Profile Document",
                "name": "John Smith"
            }
        }
        
        print("\n3. Testing Ambiguous Entity:")
        print("Input:", json.dumps(ambiguous, indent=2))
        response = await client.post("http://localhost:8000/infer", json=ambiguous)
        print("Response:", json.dumps(response.json(), indent=2))
        
        # Get patterns
        print("\n4. Retrieving Patterns:")
        response = await client.get("http://localhost:8000/patterns")
        print("Patterns:", json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    asyncio.run(test_semantic_layer())