-- SQL Schema and data for Memory Graph
-- Generated 2024-11-27

-- Create tables
CREATE TABLE IF NOT EXISTS entities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    entity_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS observations (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    entity_id INTEGER NOT NULL,
    observation TEXT NOT NULL,
    FOREIGN KEY (entity_id) REFERENCES entities(id)
);

CREATE TABLE IF NOT EXISTS relations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_entity_id INTEGER NOT NULL,
    to_entity_id INTEGER NOT NULL, 
    relation_type TEXT NOT NULL,
    FOREIGN KEY (from_entity_id) REFERENCES entities(id),
    FOREIGN KEY (to_entity_id) REFERENCES entities(id)
);

-- Begin transaction for better performance
BEGIN TRANSACTION;

-- Insert all entities
INSERT INTO entities (name, entity_type) VALUES 
('Hikvision', 'Plugin'),
('VideoCamera', 'Interface'),
('Intercom', 'Interface'),
('ObjectDetector', 'Interface'),
('RTSP', 'Protocol'),
('HikvisionCamera', 'Class'),
('RtspProvider', 'Class'),
('MotionSensor', 'Interface');

-- Insert sample observations
INSERT INTO observations (entity_id, observation) VALUES
((SELECT id FROM entities WHERE name = 'Hikvision'), 'Supports cameras and NVRs'),
((SELECT id FROM entities WHERE name = 'Hikvision'), 'Implements VideoCamera interfaces'),
((SELECT id FROM entities WHERE name = 'VideoCamera'), 'Core interface for video streaming capabilities');

-- Insert sample relations
INSERT INTO relations (from_entity_id, to_entity_id, relation_type) VALUES
((SELECT id FROM entities WHERE name = 'Hikvision'), 
 (SELECT id FROM entities WHERE name = 'VideoCamera'),
 'implements');

-- Commit transaction
COMMIT;

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_entities_name ON entities(name);
CREATE INDEX IF NOT EXISTS idx_observations_entity_id ON observations(entity_id);
CREATE INDEX IF NOT EXISTS idx_relations_from_to ON relations(from_entity_id, to_entity_id);