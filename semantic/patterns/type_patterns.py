from typing import Dict, Any
from . import BasePattern

class DocumentPattern(BasePattern):
    """Pattern for identifying document entities."""
    
    def matches(self, entity: Dict[str, Any]) -> bool:
        attributes = entity.get("attributes", {})
        
        # Check for document-like attributes
        has_title = "title" in attributes
        has_format = "format" in attributes
        has_size = isinstance(attributes.get("size"), (int, float))
        
        if has_title and (has_format or has_size):
            return True
            
        return False
        
class UserPattern(BasePattern):
    """Pattern for identifying user entities."""
    
    def matches(self, entity: Dict[str, Any]) -> bool:
        attributes = entity.get("attributes", {})
        
        # Check for user-like attributes
        has_name = "name" in attributes
        has_email = "email" in attributes
        has_role = "role" in attributes
        
        if has_name and (has_email or has_role):
            return True
            
        return False