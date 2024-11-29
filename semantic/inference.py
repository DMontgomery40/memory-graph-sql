# inference.py
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass
from sqlalchemy import text
from sqlalchemy.orm import Session
import json

@dataclass
class InferenceResult:
    inferred_relations: List[Dict[str, Any]]
    confidence_scores: Dict[str, float]
    supporting_evidence: Dict[str, List[str]]
    inference_path: List[str]

class SemanticInferenceEngine:
    """Advanced semantic inference engine with pattern matching and confidence scoring."""
    
    def __init__(self, db: Session):
        self.db = db
        self.confidence_threshold = 0.7  # Minimum confidence for inference
        
    async def infer_relations(
        self,
        entity: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> InferenceResult:
        """Infer semantic relations for an entity using available context."""
        inferred = []
        confidence_scores = {}
        evidence = {}
        inference_path = []
        
        # 1. Get applicable inference rules
        rules = await self._get_inference_rules(entity['entity_type'])
        
        # 2. Apply each rule and collect results
        for rule in rules:
            pattern = json.loads(rule['pattern'])
            if self._matches_inference_pattern(entity, pattern, context):
                inference_result = await self._apply_inference_rule(
                    rule,
                    entity,
                    context
                )
                
                if inference_result:
                    inferred.extend(inference_result.inferred_relations)
                    confidence_scores.update(inference_result.confidence_scores)
                    evidence.update(inference_result.supporting_evidence)
                    inference_path.extend(inference_result.inference_path)
        
        # 3. Validate and deduplicate inferences
        final_inferences = await self._validate_and_deduplicate(
            inferred,
            confidence_scores,
            evidence
        )
        
        return InferenceResult(
            inferred_relations=final_inferences,
            confidence_scores=confidence_scores,
            supporting_evidence=evidence,
            inference_path=inference_path
        )
    
    async def _get_inference_rules(self, entity_type: str) -> List[Dict[str, Any]]:
        """Get applicable inference rules for an entity type."""
        query = text("""
        WITH RECURSIVE type_hierarchy AS (
            -- Base case: direct type
            SELECT parent_type, child_type, 1 as depth
            FROM entity_type_hierarchy
            WHERE child_type = :entity_type
            
            UNION ALL
            
            -- Recursive case: traverse up the hierarchy
            SELECT h.parent_type, h.child_type, th.depth + 1
            FROM entity_type_hierarchy h
            JOIN type_hierarchy th ON h.child_type = th.parent_type
            WHERE th.depth < 5  -- Limit recursion depth
        )
        SELECT DISTINCT r.*
        FROM semantic_rules r
        JOIN type_hierarchy th ON json_extract(r.pattern, '$.target_type') = th.parent_type
        ORDER BY r.priority DESC
        """)
        
        result = await self.db.execute(query, {'entity_type': entity_type})
        return result.fetchall()
    
    def _matches_inference_pattern(self, 
        entity: Dict[str, Any],
        pattern: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Check if an entity matches an inference pattern."""
        # Check basic type matching
        if 'type' in pattern and pattern['type'] != entity.get('entity_type'):
            return False
            
        # Check property constraints
        if 'properties' in pattern:
            for prop, constraint in pattern['properties'].items():
                if not self._check_property_constraint(entity, prop, constraint):
                    return False
                    
        # Check contextual constraints
        if context and 'context' in pattern:
            for ctx_key, ctx_pattern in pattern['context'].items():
                if not self._check_context_constraint(context, ctx_key, ctx_pattern):
                    return False
                    
        return True
    
    def _check_property_constraint(self,
        entity: Dict[str, Any],
        property_name: str,
        constraint: Any
    ) -> bool:
        """Check if an entity property satisfies a constraint."""
        if property_name not in entity:
            return False
            
        value = entity[property_name]
        
        if isinstance(constraint, dict):
            operator = constraint.get('operator', '==')
            target = constraint.get('value')
            
            if operator == '==':
                return value == target
            elif operator == '!=':
                return value != target
            elif operator == '>':
                return value > target
            elif operator == '<':
                return value < target
            elif operator == 'in':
                return value in target
            elif operator == 'contains':
                return target in value
        else:
            return value == constraint
    
    async def _apply_inference_rule(self,
        rule: Dict[str, Any],
        entity: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Optional[InferenceResult]:
        """Apply an inference rule to generate new relations."""
        actions = json.loads(rule['actions'])
        inferred_relations = []
        confidence_scores = {}
        evidence = {}
        inference_path = [rule['rule_name']]
        
        for action in actions:
            action_type = action['type']
            
            if action_type == 'infer_relation':
                relation = await self._infer_relation(entity, action, context)
                if relation:
                    relation_id = f"{relation['from_id']}-{relation['type']}-{relation['to_id']}"
                    inferred_relations.append(relation)
                    confidence_scores[relation_id] = self._calculate_confidence(action, context)
                    evidence[relation_id] = self._collect_evidence(action, entity, context)
                    
            elif action_type == 'infer_property':
                property_result = await self._infer_property(entity, action, context)
                if property_result:
                    inferred_relations.append({
                        'type': 'property',
                        'entity_id': entity['id'],
                        'property': property_result
                    })
        
        if inferred_relations:
            return InferenceResult(
                inferred_relations=inferred_relations,
                confidence_scores=confidence_scores,
                supporting_evidence=evidence,
                inference_path=inference_path
            )
        return None
    
    def _calculate_confidence(self,
        action: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> float:
        """Calculate confidence score for an inference."""
        base_confidence = action.get('confidence', 0.8)
        
        # Adjust confidence based on context
        if context:
            # Evidence strength adjustment
            evidence_factor = len(context.get('supporting_evidence', [])) * 0.1
            base_confidence = min(1.0, base_confidence + evidence_factor)
            
            # Consistency adjustment
            if 'contradicting_evidence' in context:
                contradiction_factor = len(context['contradicting_evidence']) * 0.2
                base_confidence = max(0.0, base_confidence - contradiction_factor)
        
        return base_confidence
    
    def _collect_evidence(self,
        action: Dict[str, Any],
        entity: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """Collect supporting evidence for an inference."""
        evidence = []
        
        # Add direct property evidence
        for property_name in action.get('evidence_properties', []):
            if property_name in entity:
                evidence.append(f"Property: {property_name}={entity[property_name]}")
        
        # Add contextual evidence
        if context:
            for ctx_type in action.get('evidence_context', []):
                if ctx_type in context:
                    evidence.append(f"Context: {ctx_type} present")
        
        return evidence
    
    async def _validate_and_deduplicate(self,
        inferred: List[Dict[str, Any]],
        confidence_scores: Dict[str, float],
        evidence: Dict[str, List[str]]
    ) -> List[Dict[str, Any]]:
        """Validate and deduplicate inferred relations."""
        validated = []
        seen = set()
        
        for relation in inferred:
            relation_id = f"{relation['from_id']}-{relation['type']}-{relation['to_id']}"
            
            # Skip if already seen with higher confidence
            if relation_id in seen:
                continue
            
            # Validate confidence threshold
            if confidence_scores.get(relation_id, 0) < self.confidence_threshold:
                continue
            
            # Add supporting evidence to relation
            relation['evidence'] = evidence.get(relation_id, [])
            relation['confidence'] = confidence_scores.get(relation_id, 0)
            
            validated.append(relation)
            seen.add(relation_id)
        
        return validated