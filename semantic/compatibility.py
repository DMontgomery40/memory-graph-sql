# compatibility.py
from typing import Any, Dict, Optional, List
from sqlalchemy import text
from sqlalchemy.orm import Session
import json

class SemanticCompatibilityLayer:
    """Provides backward compatibility for semantic layer enhancements."""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def convert_old_relation(self, relation: Dict[str, Any]) -> Dict[str, Any]:
        """Convert old relation format to new format with semantic properties."""
        new_relation = relation.copy()
        
        # Add default semantic properties if not present
        if 'confidence_score' not in new_relation:
            new_relation['confidence_score'] = 1.0
        
        if 'semantic_context' not in new_relation:
            new_relation['semantic_context'] = json.dumps({})
            
        if 'validation_rules' not in new_relation:
            new_relation['validation_rules'] = json.dumps({
                'type': 'basic',
                'rules': []
            })
        
        return new_relation
    
    async def migrate_relation_type(self, relation_type_id: int) -> None:
        """Migrate existing relation type to new schema."""
        query = text("""
            SELECT * FROM relation_types_backup 
            WHERE id = :relation_type_id
        """)
        
        result = await self.db.execute(query, {'relation_type_id': relation_type_id})
        old_relation_type = result.first()
        
        if old_relation_type:
            # Create semantic properties for existing relation type
            await self.db.execute(text("""
                INSERT INTO semantic_properties_v1 (
                    relation_id, 
                    property_key, 
                    property_value, 
                    confidence,
                    context
                ) VALUES (
                    :relation_id,
                    'legacy_type',
                    :semantic_category,
                    1.0,
                    :context
                )
            """), {
                'relation_id': old_relation_type.id,
                'semantic_category': old_relation_type.semantic_category,
                'context': json.dumps({'migrated_from': 'legacy_schema'})
            })
    
    async def create_compatibility_view(self) -> None:
        """Create a view that provides legacy-compatible interface."""
        await self.db.execute(text("""
            CREATE VIEW IF NOT EXISTS legacy_relations AS
            SELECT 
                r.id,
                r.relation_name,
                r.semantic_category,
                r.description,
                r.inverse_relation,
                r.transitive,
                r.symmetric,
                r.directional,
                r.created_at,
                r.updated_at
            FROM relation_types r
        """))
    
    async def validate_semantic_rules(self, rules: List[Dict[str, Any]]) -> List[str]:
        """Validate semantic rules against both old and new schemas."""
        violations = []
        
        for rule in rules:
            # Check legacy constraints
            if not self._validate_legacy_constraints(rule):
                violations.append(
                    f"Rule {rule.get('name')} violates legacy constraints"
                )
            
            # Check new semantic constraints
            if not await self._validate_semantic_constraints(rule):
                violations.append(
                    f"Rule {rule.get('name')} violates semantic constraints"
                )
        
        return violations
    
    def _validate_legacy_constraints(self, rule: Dict[str, Any]) -> bool:
        """Validate rule against legacy constraints."""
        required_fields = ['relation_name', 'semantic_category']
        return all(field in rule for field in required_fields)
    
    async def _validate_semantic_constraints(self, rule: Dict[str, Any]) -> bool:
        """Validate rule against new semantic constraints."""
        try:
            pattern = json.loads(rule.get('pattern', '{}'))
            actions = json.loads(rule.get('actions', '{}'))
            
            # Validate pattern structure
            if not isinstance(pattern, dict) or 'type' not in pattern:
                return False
                
            # Validate actions
            if not isinstance(actions, list):
                return False
                
            return True
        except json.JSONDecodeError:
            return False
    
    async def create_semantic_indexes(self) -> None:
        """Create indexes for semantic queries."""
        await self.db.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_semantic_rules_pattern 
            ON semantic_rules_v1((json_extract(pattern, '$.type')));
            
            CREATE INDEX IF NOT EXISTS idx_semantic_properties_confidence
            ON semantic_properties_v1(confidence);
        """))

    async def get_legacy_format(self, entity_id: int) -> Dict[str, Any]:
        """Get entity in legacy format for backward compatibility."""
        query = text("""
            SELECT e.*, json_group_array(
                json_object(
                    'key', sp.property_key,
                    'value', sp.property_value
                )
            ) as properties
            FROM entities e
            LEFT JOIN semantic_properties_v1 sp ON sp.relation_id = e.id
            WHERE e.id = :entity_id
            GROUP BY e.id
        """)
        
        result = await self.db.execute(query, {'entity_id': entity_id})
        row = result.first()
        
        if not row:
            return {}
            
        entity = dict(row)
        try:
            properties = json.loads(entity.pop('properties'))
            # Convert new format properties to legacy format
            entity.update({
                prop['key']: prop['value'] 
                for prop in properties 
                if prop['key'] in ['semantic_category', 'description']
            })
        except json.JSONDecodeError:
            pass
            
        return entity