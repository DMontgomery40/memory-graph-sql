import sqlite3
from typing import Dict, Any, Optional
import json
import re
from datetime import datetime

class MemoryGraph:
    def __init__(self, db_path: str = ':memory:'):
        self.conn = sqlite3.connect(db_path)
        self.setup_database()
        self.initialize_patterns()
    
    def setup_database(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS patterns (
            id TEXT PRIMARY KEY,
            type TEXT,
            pattern_data TEXT,
            confidence REAL
        )''')
        self.conn.commit()
    
    def initialize_patterns(self):
        patterns = [
            {
                "id": "document_pattern",
                "type": "Document",
                "pattern_data": {
                    "attribute_patterns": {
                        "title": {"type": "string", "required": True, "keywords": ["report", "doc", "specification"]},
                        "format": {"type": "string", "values": ["pdf", "doc", "txt"]}
                    }
                },
                "confidence": 0.8
            }
        ]
        
        cursor = self.conn.cursor()
        for p in patterns:
            cursor.execute(
                "INSERT OR REPLACE INTO patterns (id, type, pattern_data, confidence) VALUES (?, ?, ?, ?)",
                (p["id"], p["type"], json.dumps(p["pattern_data"]), p["confidence"])
            )
        self.conn.commit()
    
    def infer_type(self, doc_id: str, attributes: Dict[str, Any]) -> Dict[str, Any]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT type, pattern_data, confidence FROM patterns")
        patterns = cursor.fetchall()
        
        scores = {}
        for pattern_type, pattern_data, confidence in patterns:
            pattern = json.loads(pattern_data)
            match_score = self._match_pattern({"id": doc_id, "attributes": attributes}, pattern)
            if match_score > 0:
                scores[pattern_type] = match_score * confidence
        
        return {
            "inferred_types": scores,
            "best_match": max(scores.items(), key=lambda x: x[1])[0] if scores else None,
            "confidence": max(scores.values()) if scores else 0
        }
    
    def add_pattern(self, pattern_id: str, pattern_type: str, pattern_data: Dict[str, Any], confidence: float = 0.7) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO patterns (id, type, pattern_data, confidence) VALUES (?, ?, ?, ?)",
            (pattern_id, pattern_type, json.dumps(pattern_data), confidence)
        )
        self.conn.commit()
    
    def get_patterns(self) -> list:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, type, pattern_data, confidence FROM patterns")
        patterns = cursor.fetchall()
        
        return [{
            "id": p[0],
            "type": p[1],
            "pattern_data": json.loads(p[2]),
            "confidence": p[3]
        } for p in patterns]
    
    def _match_pattern(self, doc: Dict[str, Any], pattern: Dict[str, Any]) -> float:
        attributes = doc["attributes"]
        attr_patterns = pattern["attribute_patterns"]
        
        matches = 0
        total_weight = 0
        
        for attr_name, attr_pattern in attr_patterns.items():
            weight = 2 if attr_pattern.get("required", False) else 1
            total_weight += weight
            
            if attr_name not in attributes:
                if attr_pattern.get("required", False):
                    return 0.0
                continue
            
            attr_value = attributes[attr_name]
            match_score = self._match_value(attr_value, attr_pattern)
            matches += match_score * weight
        
        return matches / total_weight if total_weight > 0 else 0.0
    
    def _match_value(self, value: Any, pattern: Dict[str, Any]) -> float:
        if pattern["type"] == "string" and isinstance(value, str):
            score = 1.0
            
            if "values" in pattern and value not in pattern["values"]:
                score *= 0.5
            
            if "pattern" in pattern and not re.match(pattern["pattern"], value):
                score *= 0.5
            
            if "keywords" in pattern and any(kw in value.lower() for kw in pattern["keywords"]):
                score *= 1.2
            
            return min(score, 1.0)
        
        return 0.0

# Global instance for Claude Desktop
_memory_graph = MemoryGraph()

# MCP Function Implementations
def infer_type(id: str, attributes: Dict[str, Any]) -> Dict[str, Any]:
    return _memory_graph.infer_type(id, attributes)

def add_pattern(id: str, type: str, pattern_data: Dict[str, Any], confidence: Optional[float] = 0.7) -> Dict[str, Any]:
    _memory_graph.add_pattern(id, type, pattern_data, confidence)
    return {"status": "success"}

def get_patterns() -> Dict[str, Any]:
    patterns = _memory_graph.get_patterns()
    return {"patterns": patterns}