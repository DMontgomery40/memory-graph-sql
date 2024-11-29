-- Migration: Enhance Semantic Layer
-- Version: 001
-- Description: Adds enhanced semantic capabilities with backward compatibility

-- Start transaction
BEGIN;

-- 1. Create backup of relation_types table
CREATE TABLE relation_types_backup AS SELECT * FROM relation_types;

-- 2. Add new columns to relation_types with safe defaults
ALTER TABLE relation_types
ADD COLUMN confidence_score FLOAT DEFAULT 1.0 CHECK(confidence_score BETWEEN 0 AND 1),
ADD COLUMN semantic_context TEXT DEFAULT '{}',
ADD COLUMN validation_rules TEXT DEFAULT '{}';

-- 3. Create new semantic tables with versioning support
CREATE TABLE semantic_rules_v1 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_name TEXT NOT NULL,
    pattern TEXT NOT NULL, -- Store as JSON string for SQLite compatibility
    actions TEXT NOT NULL, -- Store as JSON string
    priority INTEGER DEFAULT 0,
    context TEXT, -- Store as JSON string
    version INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE semantic_properties_v1 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    relation_id INTEGER NOT NULL,
    property_key TEXT NOT NULL,
    property_value TEXT,
    confidence FLOAT DEFAULT 1.0 CHECK(confidence BETWEEN 0 AND 1),
    context TEXT, -- Store as JSON string
    version INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (relation_id) REFERENCES relations(id)
);

-- 4. Create compatibility views
CREATE VIEW semantic_rules AS 
    SELECT id, rule_name, pattern, actions, priority, context 
    FROM semantic_rules_v1
    WHERE version = (
        SELECT MAX(version) 
        FROM semantic_rules_v1 sr2 
        WHERE sr2.rule_name = semantic_rules_v1.rule_name
    );

CREATE VIEW semantic_properties AS
    SELECT id, relation_id, property_key, property_value, confidence, context
    FROM semantic_properties_v1
    WHERE version = (
        SELECT MAX(version) 
        FROM semantic_properties_v1 sp2
        WHERE sp2.relation_id = semantic_properties_v1.relation_id
        AND sp2.property_key = semantic_properties_v1.property_key
    );

-- 5. Create indexes for performance
CREATE INDEX idx_semantic_rules_name ON semantic_rules_v1(rule_name);
CREATE INDEX idx_semantic_rules_priority ON semantic_rules_v1(priority);
CREATE INDEX idx_semantic_properties_relation ON semantic_properties_v1(relation_id);
CREATE INDEX idx_semantic_properties_key ON semantic_properties_v1(property_key);

-- 6. Create triggers for automatic versioning
CREATE TRIGGER trg_semantic_rules_version
BEFORE INSERT ON semantic_rules_v1
FOR EACH ROW
BEGIN
    SELECT COALESCE(MAX(version) + 1, 1)
    INTO NEW.version
    FROM semantic_rules_v1
    WHERE rule_name = NEW.rule_name;
END;

CREATE TRIGGER trg_semantic_properties_version
BEFORE INSERT ON semantic_properties_v1
FOR EACH ROW
BEGIN
    SELECT COALESCE(MAX(version) + 1, 1)
    INTO NEW.version
    FROM semantic_properties_v1
    WHERE relation_id = NEW.relation_id
    AND property_key = NEW.property_key;
END;

-- 7. Commit transaction
COMMIT;
