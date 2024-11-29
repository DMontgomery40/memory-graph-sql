from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime
from semantic_core import SemanticCore

app = FastAPI()

# Initialize core
semantic_core = SemanticCore()

# API Models
class Entity(BaseModel):
    id: str
    attributes: Dict[str, Any]

@app.post("/infer")
async def infer_types(entity: Entity):
    try:
        scores = semantic_core.infer_types(entity.dict())
        return {
            "entity_id": entity.id,
            "inferred_types": scores,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/patterns")
async def get_patterns():
    cursor = semantic_core.conn.cursor()
    cursor.execute("SELECT id, type, pattern_data, confidence FROM patterns")
    patterns = cursor.fetchall()
    
    return [{
        "id": p[0],
        "type": p[1],
        "pattern_data": json.loads(p[2]),
        "confidence": p[3]
    } for p in patterns]