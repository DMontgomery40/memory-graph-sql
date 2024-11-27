-- Example queries for memory graph database

-- 1. Get full implementation hierarchy
WITH RECURSIVE interface_hierarchy AS (
    SELECT 
        e1.name as implementation,
        e2.name as interface,
        1 as level,
        e1.name || ' -> ' || e2.name as path
    FROM relations r
    JOIN entities e1 ON e1.id = r.from_entity_id
    JOIN entities e2 ON e2.id = r.to_entity_id
    JOIN relation_types rt ON rt.relation_name = r.relation_type
    WHERE rt.semantic_category = 'inheritance'
    
    UNION ALL
    
    SELECT
        ih.implementation,
        e2.name,
        ih.level + 1,
        ih.path || ' -> ' || e2.name
    FROM interface_hierarchy ih
    JOIN relations r ON r.from_entity_id = (
        SELECT id FROM entities WHERE name = ih.interface
    )
    JOIN entities e2 ON e2.id = r.to_entity_id
    JOIN relation_types rt ON rt.relation_name = r.relation_type
    WHERE rt.semantic_category = 'inheritance'
    AND ih.level < 5
)
SELECT * FROM interface_hierarchy;

-- 2. Validate relationships
SELECT 
    e1.name as from_entity,
    e1.entity_type as from_type,
    r.relation_type,
    e2.name as to_entity,
    e2.entity_type as to_type,
    CASE 
        WHEN vtr.id IS NULL THEN 'Invalid'
        ELSE 'Valid'
    END as validity
FROM relations r
JOIN entities e1 ON e1.id = r.from_entity_id
JOIN entities e2 ON e2.id = r.to_entity_id
LEFT JOIN valid_type_relations vtr ON 
    vtr.from_type = e1.entity_type AND
    vtr.relation_type = r.relation_type AND
    vtr.to_type = e2.entity_type;

-- 3. Find all implementations of a specific interface
SELECT 
    e1.name as implementation,
    e1.entity_type as impl_type,
    r.relation_type,
    e2.name as interface
FROM relations r
JOIN entities e1 ON e1.id = r.from_entity_id
JOIN entities e2 ON e2.id = r.to_entity_id
WHERE e2.name = 'VideoCamera'
AND r.relation_type = 'implements';