-- example_queries.sql
-- Example Queries for Memory Graph with Enhanced Semantic Layer
-- Generated on 2024-11-29

-- ===========================
-- 1. Get Full Implementation Hierarchy with Depth and Path
-- ===========================
WITH RECURSIVE interface_hierarchy AS (
    SELECT 
        e1.id AS implementation_id,
        e1.name AS implementation,
        e2.id AS interface_id,
        e2.name AS interface,
        1 AS level,
        e1.name || ' -> ' || e2.name AS path
    FROM relations r
    JOIN entities e1 ON e1.id = r.from_entity_id
    JOIN entities e2 ON e2.id = r.to_entity_id
    JOIN relation_types rt ON rt.id = r.relation_type
    WHERE rt.semantic_category = 'inheritance'
    
    UNION ALL
    
    SELECT
        ih.implementation_id,
        ih.implementation,
        e2.id,
        e2.name,
        ih.level + 1,
        ih.path || ' -> ' || e2.name
    FROM interface_hierarchy ih
    JOIN relations r ON r.from_entity_id = ih.interface_id
    JOIN entities e2 ON e2.id = r.to_entity_id
    JOIN relation_types rt ON rt.id = r.relation_type
    WHERE rt.semantic_category = 'inheritance'
    AND ih.level < 10
)
SELECT * FROM interface_hierarchy;

-- ===========================
-- 2. Validate Relationships with Enhanced Details
-- ===========================
SELECT 
    e1.name AS from_entity,
    e1.entity_type AS from_type,
    rt.relation_name AS relation_type,
    e2.name AS to_entity,
    e2.entity_type AS to_type,
    CASE 
        WHEN vtr.id IS NULL THEN 'Invalid'
        ELSE 'Valid'
    END AS validity,
    vtr.id AS valid_relation_id
FROM relations r
JOIN entities e1 ON e1.id = r.from_entity_id
JOIN entities e2 ON e2.id = r.to_entity_id
JOIN relation_types rt ON rt.id = r.relation_type
LEFT JOIN valid_type_relations vtr ON 
    vtr.from_type = e1.entity_type AND
    vtr.relation_type = rt.id AND
    vtr.to_type = e2.entity_type;

-- ===========================
-- 3. Find All Implementations of a Specific Interface with Attributes
-- ===========================
SELECT 
    e1.name AS implementation,
    e1.entity_type AS impl_type,
    rt.relation_name AS relation_type,
    e2.name AS interface,
    ea.attribute_key,
    ea.attribute_value
FROM relations r
JOIN entities e1 ON e1.id = r.from_entity_id
JOIN entities e2 ON e2.id = r.to_entity_id
JOIN relation_types rt ON rt.id = r.relation_type
LEFT JOIN entity_attributes ea ON ea.entity_id = e1.id
WHERE e2.name = 'VideoCamera'
AND rt.relation_name = 'implements';

-- ===========================
-- 4. Insert a New Valid Relation (Example)
-- ===========================
INSERT INTO relations (from_entity_id, to_entity_id, relation_type)
SELECT 
    (SELECT id FROM entities WHERE name = 'NewImplementation'),
    (SELECT id FROM entities WHERE name = 'NewInterface'),
    (SELECT id FROM relation_types WHERE relation_name = 'implements')
WHERE EXISTS (
    SELECT 1 FROM valid_type_relations
    WHERE from_type = 'Implementation'
    AND relation_type = (SELECT id FROM relation_types WHERE relation_name = 'implements')
    AND to_type = 'Interface'
);

-- ===========================
-- 5. Attempt to Insert an Invalid Relation (Should Fail)
-- ===========================
INSERT INTO relations (from_entity_id, to_entity_id, relation_type)
SELECT 
    (SELECT id FROM entities WHERE name = 'Hikvision'),
    (SELECT id FROM entities WHERE name = 'Intercom'),
    (SELECT id FROM relation_types WHERE relation_name = 'invalid_relation')
WHERE EXISTS (
    SELECT 1 FROM valid_type_relations
    WHERE from_type = 'Plugin'
    AND relation_type = (SELECT id FROM relation_types WHERE relation_name = 'invalid_relation')
    AND to_type = 'Interface'
);

-- ===========================
-- 6. List All Relations of a Specific Semantic Category
-- ===========================
SELECT 
    r.id,
    e1.name AS from_entity,
    rt.relation_name,
    e2.name AS to_entity,
    rt.semantic_category
FROM relations r
JOIN entities e1 ON e1.id = r.from_entity_id
JOIN entities e2 ON e2.id = r.to_entity_id
JOIN relation_types rt ON rt.id = r.relation_type
WHERE rt.semantic_category = 'inheritance';
