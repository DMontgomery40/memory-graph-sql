class TypeSystem:
    """Semantic type system implementation."""
    
    def __init__(self):
        self.type_hierarchies = {}
        self.validation_rules = {}

    async def enhance_entity(self, entity: Dict[str, Any]) -> None:
        """Add semantic information to entity."""
        if not entity.get("type"):
            return
            
        type_info = self.type_hierarchies.get(entity["type"])
        if type_info:
            entity["semantic"] = {
                "type_hierarchy": type_info.get("hierarchy", []),
                "attributes": type_info.get("attributes", {})
            }

    async def validate_entity(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        """Perform semantic validation."""
        warnings = []
        suggestions = []
        
        if entity.get("type") in self.validation_rules:
            rule = self.validation_rules[entity["type"]]
            if not rule.validate(entity):
                warnings.append(f"Entity does not meet semantic requirements for type {entity['type']}")
                suggestions.append(rule.get_suggestion(entity))
        
        return {
            "valid": True,  # Always valid for MCP compliance
            "warnings": warnings,
            "suggestions": suggestions
        }