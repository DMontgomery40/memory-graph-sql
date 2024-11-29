# validation.py
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass
from sqlalchemy import text
from sqlalchemy.orm import Session
import json

@dataclass
class ValidationResult:
    is_valid: bool
    violations: List[str]
    suggestions: List[str]
    confidence: float
    context: Dict[str, Any]

class SemanticValidator:
    """Enhanced semantic validation system with support for complex rules and context."""
    
    def __init__(self, db: Session):
        self.db = db
        
    async def validate_relation(
        self,
        from_entity: Dict[str, Any],
        to_entity: Dict[str, Any],
        relation_type: str,
        context: Optional[Dict[str, Any]] = None
    ) -> ValidationResult:
        """Validate a semantic relation with full context awareness."""
        violations = []
        suggestions = []
        confidence = 1.0
        validation_context = context or {}

        # 1. Type Hierarchy Validation
        type_valid, type_violations = await self._validate_type_hierarchy(
            from_entity['entity_type'],
            to_entity['entity_type'],
            relation_type
        )
        violations.extend(type_violations)

        # 2. Semantic Rules Validation
        rules_valid, rule_violations, rule_suggestions = await self._validate_semantic_rules(
            from_entity,
            to_entity,
            relation_type,
            validation_context
        )
        violations.extend(rule_violations)
        suggestions.extend(rule_suggestions)

        # 3. Constraint Validation
        constraints_valid, constraint_violations = await self._validate_constraints(
            from_entity,
            to_entity,
            relation_type,
            validation_context
        )
        violations.extend(constraint_violations)

        # 4. Context Validation
        context_valid, context_violations, context_confidence = await self._validate_context(
            validation_context
        )
        violations.extend(context_violations)
        confidence *= context_confidence

        # Overall validation result
        is_valid = type_valid and rules_valid and constraints_valid and context_valid

        return ValidationResult(
            is_valid=is_valid,
            violations=violations,
            suggestions=suggestions,
            confidence=confidence,
            context=validation_context
        )

    async def _validate_type_hierarchy(
        self,
        from_type: str,
        to_type: str,
        relation_type: str
    ) -> Tuple[bool, List[str]]:
        """Validate types against the semantic hierarchy."""
        query = text("""
        WITH RECURSIVE type_hierarchy_path AS (
            -- Base case: direct relationships
            SELECT 
                parent_type,
                child_type,
                1 as depth,
                child_type as path
            FROM entity_type_hierarchy
            WHERE child_type = :from_type OR child_type = :to_type

            UNION ALL

            -- Recursive case: traverse up the hierarchy
            SELECT 
                h.parent_type,
                h.child_type,
                thp.depth + 1,
                h.child_type || '>' || thp.path
            FROM entity_type_hierarchy h
            JOIN type_hierarchy_path thp ON h.child_type = thp.parent_type
            WHERE thp.depth < 10  -- Prevent infinite recursion
        )
        SELECT DISTINCT path, depth
        FROM type_hierarchy_path
        WHERE parent_type IN (
            SELECT from_type FROM valid_type_relations
            WHERE relation_type = :relation_type
        )
        """)

        result = await self.db.execute(
            query,
            {
                'from_type': from_type,
                'to_type': to_type,
                'relation_type': relation_type
            }
        )

        paths = result.fetchall()
        violations = []

        if not paths:
            violations.append(
                f"Invalid type hierarchy: {from_type} -> {relation_type} -> {to_type}"
            )
            return False, violations

        return True, violations

    async def _validate_semantic_rules(
        self,
        from_entity: Dict[str, Any],
        to_entity: Dict[str, Any],
        relation_type: str,
        context: Dict[str, Any]
    ) -> Tuple[bool, List[str], List[str]]:
        """Validate against defined semantic rules."""
        query = text("""
        SELECT rule_name, pattern, actions, priority
        FROM semantic_rules
        WHERE json_extract(pattern, '$.type') = :relation_type
        ORDER BY priority DESC
        """)

        result = await self.db.execute(query, {'relation_type': relation_type})
        rules = result.fetchall()

        violations = []
        suggestions = []
        is_valid = True

        for rule in rules:
            pattern = json.loads(rule.pattern)
            if self._matches_pattern(from_entity, to_entity, pattern, context):
                actions = json.loads(rule.actions)
                rule_valid, rule_violations, rule_suggestions = self._apply_rule_actions(
                    actions,
                    from_entity,
                    to_entity,
                    context
                )
                
                violations.extend(rule_violations)
                suggestions.extend(rule_suggestions)
                is_valid = is_valid and rule_valid

        return is_valid, violations, suggestions

    async def _validate_constraints(
        self,
        from_entity: Dict[str, Any],
        to_entity: Dict[str, Any],
        relation_type: str,
        context: Dict[str, Any]
    ) -> Tuple[bool, List[str]]:
        """Validate semantic constraints."""
        query = text("""
        SELECT rt.validation_rules
        FROM relation_types rt
        WHERE rt.relation_name = :relation_type
        """)

        result = await self.db.execute(query, {'relation_type': relation_type})
        validation_rules = result.fetchone()

        if not validation_rules or not validation_rules.validation_rules:
            return True, []

        rules = json.loads(validation_rules.validation_rules)
        violations = []

        for rule in rules:
            if not self._check_constraint(rule, from_entity, to_entity, context):
                violations.append(f"Constraint violation: {rule['description']}")

        return len(violations) == 0, violations

    async def _validate_context(
        self,
        context: Dict[str, Any]
    ) -> Tuple[bool, List[str], float]:
        """Validate and score the semantic context."""
        violations = []
        confidence = 1.0

        # Required context validations
        required_contexts = ['hierarchy', 'constraints', 'inference_rules']
        for req in required_contexts:
            if req not in context:
                violations.append(f"Missing required context: {req}")
                confidence *= 0.8

        # Context completeness check
        if 'hierarchy' in context:
            hierarchy_completeness = self._check_hierarchy_completeness(context['hierarchy'])
            confidence *= hierarchy_completeness

        # Context consistency check
        if len(context) > 0:
            consistency_score = self._check_context_consistency(context)
            confidence *= consistency_score

        is_valid = len(violations) == 0 and confidence > 0.5
        return is_valid, violations, confidence

    def _matches_pattern(self, from_entity: Dict[str, Any], to_entity: Dict[str, Any], 
                        pattern: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Check if entities match a semantic pattern."""
        # Basic property matching
        if 'properties' in pattern:
            for prop, value in pattern['properties'].items():
                if prop not in from_entity or from_entity[prop] != value:
                    return False

        # Relationship pattern matching
        if 'relationship' in pattern:
            rel_pattern = pattern['relationship']
            if 'cardinality' in rel_pattern:
                if not self._check_cardinality(from_entity, to_entity, rel_pattern['cardinality']):
                    return False

        # Context pattern matching
        if 'context' in pattern:
            for ctx_key, ctx_pattern in pattern['context'].items():
                if ctx_key not in context:
                    return False
                if not self._match_context_pattern(context[ctx_key], ctx_pattern):
                    return False

        return True

    def _apply_rule_actions(self, actions: List[Dict[str, Any]], from_entity: Dict[str, Any],
                           to_entity: Dict[str, Any], context: Dict[str, Any]) \
                           -> Tuple[bool, List[str], List[str]]:
        """Apply semantic rule actions and generate validation results."""
        violations = []
        suggestions = []
        is_valid = True

        for action in actions:
            action_type = action.get('type')
            if action_type == 'validate':
                valid, violation = self._validate_action(action, from_entity, to_entity, context)
                if not valid:
                    violations.append(violation)
                    is_valid = False
            elif action_type == 'suggest':
                suggestion = self._generate_suggestion(action, from_entity, to_entity, context)
                if suggestion:
                    suggestions.append(suggestion)

        return is_valid, violations, suggestions

    def _check_constraint(self, constraint: Dict[str, Any], from_entity: Dict[str, Any],
                         to_entity: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Check if a specific semantic constraint is satisfied."""
        constraint_type = constraint.get('type')
        
        if constraint_type == 'attribute':
            return self._check_attribute_constraint(constraint, from_entity, to_entity)
        elif constraint_type == 'cardinality':
            return self._check_cardinality_constraint(constraint, from_entity, to_entity)
        elif constraint_type == 'context':
            return self._check_context_constraint(constraint, context)
        
        return True

    def _check_hierarchy_completeness(self, hierarchy: Dict[str, Any]) -> float:
        """Check the completeness of type hierarchy information."""
        if not hierarchy:
            return 0.5

        completeness_score = 1.0
        required_fields = ['types', 'relationships']
        
        for field in required_fields:
            if field not in hierarchy:
                completeness_score *= 0.8

        if 'types' in hierarchy and len(hierarchy['types']) == 0:
            completeness_score *= 0.7

        return completeness_score

    def _check_context_consistency(self, context: Dict[str, Any]) -> float:
        """Check the internal consistency of semantic context."""
        consistency_score = 1.0

        # Check for conflicting rules
        if 'inference_rules' in context and 'constraints' in context:
            conflicts = self._find_rule_conflicts(
                context['inference_rules'],
                context['constraints']
            )
            consistency_score *= (1 - (len(conflicts) * 0.1))

        return max(0.1, consistency_score)  # Ensure minimum score of 0.1