from typing import Dict, Any, List

class BasePattern:
    """Base class for semantic patterns."""
    
    def __init__(self, confidence: float = 1.0):
        self.confidence = confidence
        self.examples: List[Dict[str, Any]] = []
        
    def matches(self, entity: Dict[str, Any]) -> bool:
        raise NotImplementedError
        
    def add_example(self, entity: Dict[str, Any]) -> None:
        self.examples.append(entity)
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "confidence": self.confidence,
            "examples": self.examples
        }