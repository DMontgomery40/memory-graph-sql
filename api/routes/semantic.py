from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List, Any
from semantic.engine import SemanticEngine
from core.database import get_session
from pydantic import BaseModel

router = APIRouter(prefix="/semantic")

class EntityInput(BaseModel):
    id: str
    type: Optional[str] = None
    attributes: Dict[str, Any] = {}
    relations: List[Dict[str, Any]] = []

@router.post("/enrich")
async def enrich_entity(
    entity: EntityInput,
    session: AsyncSession = Depends(get_session)
) -> Dict[str, Any]:
    """Enrich an entity with semantic intelligence."""
    engine = SemanticEngine(session)
    return await engine.enrich_entity(entity.dict())

@router.post("/learn")
async def learn_patterns(
    entities: List[EntityInput],
    session: AsyncSession = Depends(get_session)
) -> Dict[str, str]:
    """Learn semantic patterns from a set of entities."""
    engine = SemanticEngine(session)
    await engine.learn_patterns([e.dict() for e in entities])
    return {"status": "Patterns learned successfully"}

@router.get("/patterns/{pattern_type}")
async def get_patterns(
    pattern_type: str,
    session: AsyncSession = Depends(get_session)
) -> Dict[str, Any]:
    """Get learned patterns of a specific type."""
    engine = SemanticEngine(session)
    patterns = await engine._get_patterns(pattern_type)
    return {
        "patterns": patterns,
        "total": len(patterns)
    }