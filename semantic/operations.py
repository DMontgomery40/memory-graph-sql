class SemanticOperations(MCPOperations):
    """Semantic layer extending core MCP operations."""
    
    def __init__(self, db_session: AsyncSession, type_system: 'TypeSystem'):
        super().__init__(db_session)
        self.type_system = type_system

    async def create_entities(self, entities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Enhanced entity creation with semantic validation."""
        # First perform core MCP operation
        result = await super().create_entities(entities)
        
        # Then enhance with semantic information (non-blocking)
        try:
            for entity in result["entities"]:
                await self.type_system.enhance_entity(entity)
        except Exception as e:
            # Log but don't block operation
            logger.warning(f"Semantic enhancement failed: {e}")
            
        return result

    async def semantic_validate_entity(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        """Additional semantic validation (non-blocking)."""
        try:
            validation_result = await self.type_system.validate_entity(entity)
            return {
                "valid": validation_result["valid"],
                "warnings": validation_result.get("warnings", []),
                "suggestions": validation_result.get("suggestions", [])
            }
        except Exception as e:
            return {
                "valid": True,  # Non-blocking
                "warnings": [str(e)],
                "suggestions": []
            }