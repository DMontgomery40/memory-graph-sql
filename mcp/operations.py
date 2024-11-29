from typing import Dict, List, Any, Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

class MCPOperations:
    """Core MCP operations implementation."""
    
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def create_entities(self, entities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Standard MCP entity creation."""
        try:
            # Core MCP validation
            self._validate_entities(entities)
            
            created_entities = []
            for entity in entities:
                db_entity = await self._create_entity(entity)
                created_entities.append(db_entity)
                
            return {"status": "success", "entities": created_entities}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def create_relations(self, relations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Standard MCP relation creation."""
        try:
            # Core MCP validation
            self._validate_relations(relations)
            
            created_relations = []
            for relation in relations:
                db_relation = await self._create_relation(relation)
                created_relations.append(db_relation)
                
            return {"status": "success", "relations": created_relations}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))