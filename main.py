from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List, Any

from mcp.operations import MCPOperations
from semantic.operations import SemanticOperations
from semantic.type_system import TypeSystem
from core.database import get_db_session

app = FastAPI(title="MCP-Compliant Semantic Graph Server")

# Dependency injection
async def get_semantic_operations(
    db: AsyncSession = Depends(get_db_session),
    type_system: TypeSystem = Depends(get_type_system)
) -> SemanticOperations:
    return SemanticOperations(db, type_system)

# Core MCP endpoints
@app.post("/entities")
async def create_entities(
    request: Dict[str, Any],
    ops: SemanticOperations = Depends(get_semantic_operations)
) -> Dict[str, Any]:
    """Standard MCP entity creation endpoint."""
    return await ops.create_entities(request["entities"])

@app.post("/relations")
async def create_relations(
    request: Dict[str, Any],
    ops: SemanticOperations = Depends(get_semantic_operations)
) -> Dict[str, Any]:
    """Standard MCP relation creation endpoint."""
    return await ops.create_relations(request["relations"])

# Semantic extension endpoints
@app.post("/semantic/validate")
async def validate_semantic(
    request: Dict[str, Any],
    ops: SemanticOperations = Depends(get_semantic_operations)
) -> Dict[str, Any]:
    """Optional semantic validation endpoint."""
    return await ops.semantic_validate_entity(request["entity"])

# Error handling
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Standard error response format."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
                "type": "mcp_error"
            }
        }
    )