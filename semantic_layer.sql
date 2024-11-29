-- semantic_layer.sql
-- Enhanced Semantic Layer for Memory Graph
-- Generated on 2024-11-29

-- Enable Foreign Key Constraints
PRAGMA foreign_keys = ON;

-- ===========================
-- Relation Types Table
-- ===========================
CREATE TABLE IF NOT EXISTS relation_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    relation_name TEXT NOT NULL UNIQUE,
    semantic_category TEXT NOT NULL,
    description TEXT,
    inverse_relation INTEGER REFERENCES relation_types(id),
    transitive BOOLEAN DEFAULT FALSE,
    symmetric BOOLEAN DEFAULT FALSE,
    directional BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert Known Relation Types
INSERT OR IGNORE INTO relation_types (relation_name, semantic_category, description, transitive, symmetric, directional) VALUES
('implements', 'inheritance', 'Indicates interface implementation', TRUE, FALSE, TRUE),
('extends', 'inheritance', 'Indicates class inheritance', TRUE, FALSE, TRUE),
('uses', 'dependency', 'Indicates usage dependency', FALSE, FALSE, TRUE),
('provides', 'composition', 'Indicates provided functionality', FALSE, FALSE, TRUE),
('configures', 'configuration', 'Indicates configuration relationship', FALSE, FALSE, TRUE),
('complementsWith', 'integration', 'Indicates complementary functionality', TRUE, TRUE, FALSE);

-- ===========================
-- Entity Type Hierarchy Table
-- ===========================
CREATE TABLE IF NOT EXISTS entity_type_hierarchy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_type TEXT NOT NULL,
    child_type TEXT NOT NULL,
    hierarchy_level INTEGER NOT NULL,
    UNIQUE(parent_type, child_type),
    CHECK (hierarchy_level > 0)
);

-- Insert Entity Type Hierarchy
INSERT OR IGNORE INTO entity_type_hierarchy (parent_type, child_type, hierarchy_level) VALUES
('BaseClass', 'Class', 1),
('Interface', 'CoreConcept', 1),
('Implementation', 'CorePattern', 2),
('Pattern', 'CorePattern', 1);

-- ===========================
-- Valid Type Relations Table
-- ===========================
CREATE TABLE IF NOT EXISTS valid_type_relations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_type TEXT NOT NULL,
    relation_type INTEGER NOT NULL, -- References relation_types(id)
    to_type TEXT NOT NULL,
    UNIQUE(from_type, relation_type, to_type),
    FOREIGN KEY (relation_type) REFERENCES relation_types(id)
);

-- Insert Valid Type Relations
INSERT OR IGNORE INTO valid_type_relations (from_type, relation_type, to_type) VALUES
('Implementation', (SELECT id FROM relation_types WHERE relation_name = 'implements'), 'Interface'),
('Class', (SELECT id FROM relation_types WHERE relation_name = 'extends'), 'BaseClass'),
('Implementation', (SELECT id FROM relation_types WHERE relation_name = 'uses'), 'Protocol'),
('Class', (SELECT id FROM relation_types WHERE relation_name = 'provides'), 'Feature'),
('Implementation', (SELECT id FROM relation_types WHERE relation_name = 'configures'), 'Configuration');

-- ===========================
-- Entity Attributes Table
-- ===========================
CREATE TABLE IF NOT EXISTS entity_attributes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id INTEGER NOT NULL,
    attribute_key TEXT NOT NULL,
    attribute_value TEXT,
    FOREIGN KEY (entity_id) REFERENCES entities(id),
    UNIQUE(entity_id, attribute_key)
);

-- ===========================
-- Audit Tables for Change Tracking
-- ===========================
CREATE TABLE IF NOT EXISTS entity_audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id INTEGER NOT NULL,
    action TEXT NOT NULL, -- 'INSERT', 'UPDATE', 'DELETE'
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    changed_by TEXT,
    FOREIGN KEY (entity_id) REFERENCES entities(id)
);

CREATE TABLE IF NOT EXISTS relations_audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    relation_id INTEGER NOT NULL,
    action TEXT NOT NULL, -- 'INSERT', 'UPDATE', 'DELETE'
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    changed_by TEXT,
    FOREIGN KEY (relation_id) REFERENCES relations(id)
);

-- ===========================
-- Triggers for Automatic Audit Logging
-- ===========================

-- Trigger for Entities Table
CREATE TRIGGER IF NOT EXISTS trg_entities_audit
AFTER INSERT OR UPDATE OR DELETE ON entities
FOR EACH ROW
BEGIN
    INSERT INTO entity_audit (entity_id, action, changed_by)
    VALUES (
        COALESCE(NEW.id, OLD.id),
        CASE 
            WHEN (NEW.id IS NOT NULL AND OLD.id IS NULL) THEN 'INSERT'
            WHEN (NEW.id IS NOT NULL AND OLD.id IS NOT NULL) THEN 'UPDATE'
            WHEN (NEW.id IS NULL AND OLD.id IS NOT NULL) THEN 'DELETE'
        END,
        'system' -- Replace with dynamic user identifier if available
    );
END;

-- Trigger for Relations Table
CREATE TRIGGER IF NOT EXISTS trg_relations_audit
AFTER INSERT OR UPDATE OR DELETE ON relations
FOR EACH ROW
BEGIN
    INSERT INTO relations_audit (relation_id, action, changed_by)
    VALUES (
        COALESCE(NEW.id, OLD.id),
        CASE 
            WHEN (NEW.id IS NOT NULL AND OLD.id IS NULL) THEN 'INSERT'
            WHEN (NEW.id IS NOT NULL AND OLD.id IS NOT NULL) THEN 'UPDATE'
            WHEN (NEW.id IS NULL AND OLD.id IS NOT NULL) THEN 'DELETE'
        END,
        'system' -- Replace with dynamic user identifier if available
    );
END;

-- ===========================
-- Indexes for Semantic Tables
-- ===========================
CREATE INDEX IF NOT EXISTS idx_relation_types_category ON relation_types(semantic_category);
CREATE INDEX IF NOT EXISTS idx_entity_type_hierarchy_parent ON entity_type_hierarchy(parent_type);
CREATE INDEX IF NOT EXISTS idx_entity_type_hierarchy_child ON entity_type_hierarchy(child_type);
CREATE INDEX IF NOT EXISTS idx_valid_type_relations_from_type ON valid_type_relations(from_type);
CREATE INDEX IF NOT EXISTS idx_valid_type_relations_to_type ON valid_type_relations(to_type);
