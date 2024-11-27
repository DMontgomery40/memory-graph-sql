-- Semantic layer for memory graph
CREATE TABLE relation_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    relation_name TEXT NOT NULL UNIQUE,
    semantic_category TEXT NOT NULL,
    description TEXT,
    inverse_relation TEXT,
    transitive BOOLEAN DEFAULT FALSE,
    symmetric BOOLEAN DEFAULT FALSE
);

-- Define known relation types
INSERT INTO relation_types (relation_name, semantic_category, description, transitive) VALUES
('implements', 'inheritance', 'Indicates interface implementation', TRUE),
('extends', 'inheritance', 'Indicates class inheritance', TRUE),
('uses', 'dependency', 'Indicates usage dependency', FALSE),
('provides', 'composition', 'Indicates provided functionality', FALSE),
('configures', 'configuration', 'Indicates configuration relationship', FALSE),
('complementsWith', 'integration', 'Indicates complementary functionality', TRUE);

-- Entity type hierarchy
CREATE TABLE entity_type_hierarchy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_type TEXT NOT NULL,
    child_type TEXT NOT NULL,
    hierarchy_level INTEGER,
    UNIQUE(parent_type, child_type)
);

-- Define type hierarchy
INSERT INTO entity_type_hierarchy (parent_type, child_type, hierarchy_level) VALUES
('BaseClass', 'Class', 1),
('Interface', 'CoreConcept', 1),
('Implementation', 'CorePattern', 2),
('Pattern', 'CorePattern', 1);

-- Valid relationships between types 
CREATE TABLE valid_type_relations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_type TEXT NOT NULL,
    relation_type TEXT NOT NULL,
    to_type TEXT NOT NULL,
    UNIQUE(from_type, relation_type, to_type)
);

-- Define valid relationships
INSERT INTO valid_type_relations (from_type, relation_type, to_type) VALUES
('Implementation', 'implements', 'Interface'),
('Class', 'extends', 'BaseClass'),
('Implementation', 'uses', 'Protocol'),
('Class', 'provides', 'Feature'),
('Implementation', 'configures', 'Configuration');