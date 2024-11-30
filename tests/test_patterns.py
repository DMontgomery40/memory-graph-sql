import unittest
from src.semantic_core import SemanticCore
from datetime import datetime

class TestPatterns(unittest.TestCase):
    def setUp(self):
        self.semantic_core = SemanticCore()
        self.test_patterns = [
            {
                "id": "test_doc",
                "type": "TestDocument",
                "pattern_data": {
                    "attribute_patterns": {
                        "title": {
                            "type": "string",
                            "required": True,
                            "keywords": ["test", "sample"]
                        },
                        "format": {
                            "type": "string",
                            "values": ["pdf", "doc"]
                        }
                    }
                },
                "confidence": 0.8
            }
        ]
        
        for pattern in self.test_patterns:
            self.semantic_core.add_pattern(
                pattern["id"],
                pattern["type"],
                pattern["pattern_data"],
                pattern["confidence"]
            )
    
    def test_keyword_matching(self):
        doc = {
            "id": "doc1",
            "attributes": {
                "title": "Test Document Sample",
                "format": "pdf"
            }
        }
        
        result = self.semantic_core.infer_types(doc)
        self.assertIn("TestDocument", result)
        self.assertGreaterEqual(result["TestDocument"], 0.8)
    
    def test_value_matching(self):
        doc = {
            "id": "doc2",
            "attributes": {
                "title": "Test Document",
                "format": "invalid"
            }
        }
        
        result = self.semantic_core.infer_types(doc)
        self.assertTrue(
            result.get("TestDocument", 0) < 0.8,
            "Document with invalid format should have lower confidence"
        )
    
    def test_required_attributes(self):
        doc = {
            "id": "doc3",
            "attributes": {
                "format": "pdf"
            }
        }
        
        result = self.semantic_core.infer_types(doc)
        self.assertNotIn(
            "TestDocument", result,
            "Document missing required title should not match"
        )

if __name__ == '__main__':
    unittest.main()