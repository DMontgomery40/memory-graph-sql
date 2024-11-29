-- schema.sql
-- Base Schema for Memory Graph
-- Generated on 2024-11-29

-- Enable Foreign Key Constraints
PRAGMA foreign_keys = ON;

-- ===========================
-- Entities Table
-- ===========================
CREATE TABLE IF NOT EXISTS entities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    entity_type TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===========================
-- Observations Table
-- ===========================
CREATE TABLE IF NOT EXISTS observations (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    entity_id INTEGER NOT NULL,
    relation_id INTEGER, -- Optional: Link to a specific relation
    observation TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (entity_id) REFERENCES entities(id),
    FOREIGN KEY (relation_id) REFERENCES relations(id)
);

-- ===========================
-- Relations Table
-- ===========================
CREATE TABLE IF NOT EXISTS relations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_entity_id INTEGER NOT NULL,
    to_entity_id INTEGER NOT NULL, 
    relation_type INTEGER NOT NULL, -- References relation_types(id)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (from_entity_id) REFERENCES entities(id),
    FOREIGN KEY (to_entity_id) REFERENCES entities(id),
    FOREIGN KEY (relation_type) REFERENCES relation_types(id)
);

-- ===========================
-- Indexes for Base Schema
-- ===========================
CREATE INDEX IF NOT EXISTS idx_entities_name ON entities(name);
CREATE INDEX IF NOT EXISTS idx_observations_entity_id ON observations(entity_id);
CREATE INDEX IF NOT EXISTS idx_observations_relation_id ON observations(relation_id);
CREATE INDEX IF NOT EXISTS idx_relations_from_to ON relations(from_entity_id, to_entity_id);
