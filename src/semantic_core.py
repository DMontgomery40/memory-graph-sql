from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import sqlite3
import json
import re
from datetime import datetime

class SemanticCore:
    def __init__(self):
        self.conn = sqlite3.connect("semantic.db")
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
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS semantic_metadata (
            entity_id TEXT PRIMARY KEY,
            inferred_types TEXT,
            attribute_patterns TEXT,
            last_updated TEXT
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
            },
            {
                "id": "user_pattern",
                "type": "User",
                "pattern_data": {
                    "attribute_patterns": {
                        "name": {"type": "string", "required": True},
                        "email": {"type": "string", "required": True, "pattern": r"^[^@]+@[^@]+\.[^@]+$"}
                    }
                },
                "confidence": 0.9
            }
        ]
        
        cursor = self.conn.cursor()
        for p in patterns:
            cursor.execute(
                "INSERT OR REPLACE INTO patterns (id, type, pattern_data, confidence) VALUES (?, ?, ?, ?)",
                (p["id"], p["type"], json.dumps(p["pattern_data"]), p["confidence"])
            )
        self.conn.commit()

    def infer_types(self, entity: Dict[str, Any]) -> Dict[str, float]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT type, pattern_data, confidence FROM patterns")
        patterns = cursor.fetchall()
        
        scores = {}
        for pattern_type, pattern_data, confidence in patterns:
            pattern = json.loads(pattern_data)
            match_score = self._match_pattern(entity, pattern)
            if match_score > 0:
                scores[pattern_type] = match_score * confidence
        
        if entity.get("id"):
            self._store_inference(entity["id"], scores)
        
        return scores
    
    def _match_pattern(self, entity: Dict[str, Any], pattern: Dict[str, Any]) -> float:
        attributes = entity.get("attributes", {})
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
    
    def _store_inference(self, entity_id: str, scores: Dict[str, float]):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO semantic_metadata (entity_id, inferred_types, last_updated) VALUES (?, ?, ?)",
            (entity_id, json.dumps(scores), datetime.now().isoformat())
        )
        self.conn.commit()