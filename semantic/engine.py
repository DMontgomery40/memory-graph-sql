from typing import Dict, List, Any, Optional, Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from collections import defaultdict
import numpy as np
from .models import SemanticMetadata, SemanticPattern
import datetime

class SemanticEngine:
    def _matches_pattern(self, entity: Dict[str, Any], pattern: Dict[str, Any]) -> bool:
        """Check if an entity matches a semantic pattern."""
        if not pattern.get('match_rules'):
            return False
            
        for rule in pattern['match_rules']:
            rule_type = rule.get('type')
            if rule_type == 'attribute_exists':
                if rule['attribute'] not in entity.get('attributes', {}):
                    return False
            elif rule_type == 'attribute_value':
                attr_value = entity.get('attributes', {}).get(rule['attribute'])
                if attr_value != rule['value']:
                    return False
            elif rule_type == 'attribute_type':
                attr_value = entity.get('attributes', {}).get(rule['attribute'])
                if not isinstance(attr_value, rule['value_type']):
                    return False
                    
        return True

    async def _get_patterns(self, pattern_type: str) -> List[Dict[str, Any]]:
        """Retrieve patterns of a specific type from the database."""
        query = select(SemanticPattern).where(SemanticPattern.pattern_type == pattern_type)
        result = await self.session.execute(query)
        patterns = result.scalars().all()
        
        return [{
            'id': pattern.id,
            'pattern_type': pattern.pattern_type,
            'pattern_data': pattern.pattern_data,
            'confidence': pattern.confidence,
            'success_rate': pattern.success_rate,
            'last_applied': pattern.last_applied
        } for pattern in patterns]

    async def _store_pattern(self, pattern_data: Dict[str, Any]) -> None:
        """Store a new pattern in the database."""
        pattern = SemanticPattern(
            id=f"{pattern_data['type']}_{datetime.datetime.utcnow().timestamp()}",
            pattern_type=pattern_data['type'],
            pattern_data=pattern_data,
            confidence=pattern_data.get('confidence', 1.0),
            examples=pattern_data.get('examples', []),
            last_applied=datetime.datetime.utcnow(),
            success_rate=1.0  # Initial success rate
        )
        self.session.add(pattern)
        await self.session.commit()

    def _get_enrichment_basis(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        """Get the basis for semantic enrichment decisions."""
        return {
            'attributes_analyzed': list(entity.get('attributes', {}).keys()),
            'existing_relations': entity.get('relations', []),
            'entity_type': entity.get('type'),
            'timestamp': datetime.datetime.utcnow().isoformat()
        }

    async def _get_metadata(self, entity_id: str) -> SemanticMetadata:
        """Get or create semantic metadata for an entity."""
        query = select(SemanticMetadata).where(SemanticMetadata.entity_id == entity_id)
        result = await self.session.execute(query)
        metadata = result.scalars().first()
        
        if not metadata:
            metadata = SemanticMetadata(entity_id=entity_id)
            self.session.add(metadata)
            await self.session.commit()
            
        return metadata

    def _enhance_entity_with_metadata(self, entity: Dict[str, Any], metadata: SemanticMetadata) -> Dict[str, Any]:
        """Enhance an entity with its semantic metadata."""
        enhanced = entity.copy()
        enhanced['semantic'] = {
            'inferred_types': metadata.inferred_types,
            'derived_attributes': metadata.derived_attributes,
            'type_hierarchy': metadata.type_hierarchy,
            'suggested_relations': metadata.suggested_relations,
            'confidence_score': metadata.confidence_score,
            'last_updated': metadata.last_updated.isoformat(),
            'provenance': metadata.provenance
        }
        return enhanced