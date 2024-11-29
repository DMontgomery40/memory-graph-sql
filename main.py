# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
import models
from models import Base, Entity, Observation, Relation, RelationType, ValidTypeRelation, EntityTypeHierarchy, EntityAttribute
from typing import List, Optional
import uvicorn

app = FastAPI(title="MCP Server with Semantic Layer")

# Initialize the database and create tables
init_db()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic Models
class EntityCreate(BaseModel):
    name: str
    entity_type: str

class EntityOut(BaseModel):
    id: int
    name: str
    entity_type: str

    class Config:
        orm_mode = True

class ObservationCreate(BaseModel):
    entity_id: int
    relation_id: Optional[int] = None
    observation: str

class ObservationOut(BaseModel):
    id: int
    entity_id: int
    relation_id: Optional[int]
    observation: str

    class Config:
        orm_mode = True

class RelationCreate(BaseModel):
    from_entity_id: int
    to_entity_id: int
    relation_type: str  # relation_name

class RelationOut(BaseModel):
    id: int
    from_entity_id: int
    to_entity_id: int
    relation_type: str

    class Config:
        orm_mode = True

class InsightCreate(BaseModel):
    insight: str

# API Endpoints

@app.post("/entities/", response_model=EntityOut)
def create_entity(entity: EntityCreate, db: Session = next(get_db())):
    db_entity = db.query(Entity).filter(Entity.name == entity.name).first()
    if db_entity:
        raise HTTPException(status_code=400, detail="Entity already exists")
    new_entity = Entity(name=entity.name, entity_type=entity.entity_type)
    db.add(new_entity)
    db.commit()
    db.refresh(new_entity)
    return new_entity

@app.get("/entities/", response_model=List[EntityOut])
def read_entities(skip: int = 0, limit: int = 100, db: Session = next(get_db())):
    entities = db.query(Entity).offset(skip).limit(limit).all()
    return entities

@app.post("/observations/", response_model=ObservationOut)
def create_observation(observation: ObservationCreate, db: Session = next(get_db())):
    db_entity = db.query(Entity).filter(Entity.id == observation.entity_id).first()
    if not db_entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    if observation.relation_id:
        db_relation = db.query(Relation).filter(Relation.id == observation.relation_id).first()
        if not db_relation:
            raise HTTPException(status_code=404, detail="Relation not found")
    new_observation = Observation(
        entity_id=observation.entity_id,
        relation_id=observation.relation_id,
        observation=observation.observation
    )
    db.add(new_observation)
    db.commit()
    db.refresh(new_observation)
    return new_observation

@app.get("/observations/", response_model=List[ObservationOut])
def read_observations(skip: int = 0, limit: int = 100, db: Session = next(get_db())):
    observations = db.query(Observation).offset(skip).limit(limit).all()
    return observations

@app.post("/relations/", response_model=RelationOut)
def create_relation(relation: RelationCreate, db: Session = next(get_db())):
    from_entity = db.query(Entity).filter(Entity.id == relation.from_entity_id).first()
    to_entity = db.query(Entity).filter(Entity.id == relation.to_entity_id).first()
    if not from_entity or not to_entity:
        raise HTTPException(status_code=404, detail="From or To entity not found")
    
    # Get relation_type id
    relation_type = db.query(RelationType).filter(RelationType.relation_name == relation.relation_type).first()
    if not relation_type:
        raise HTTPException(status_code=404, detail="Relation type not found")
    
    # Validate the relation based on semantic constraints
    valid_relation = db.query(ValidTypeRelation).filter(
        ValidTypeRelation.from_type == from_entity.entity_type,
        ValidTypeRelation.relation_type == relation_type.id,
        ValidTypeRelation.to_type == to_entity.entity_type
    ).first()
    
    if not valid_relation:
        raise HTTPException(status_code=400, detail="Invalid relationship based on semantic constraints")
    
    new_relation = Relation(
        from_entity_id=relation.from_entity_id,
        to_entity_id=relation.to_entity_id,
        relation_type=relation_type.id
    )
    db.add(new_relation)
    db.commit()
    db.refresh(new_relation)
    return RelationOut(
        id=new_relation.id,
        from_entity_id=new_relation.from_entity_id,
        to_entity_id=new_relation.to_entity_id,
        relation_type=relation_type.relation_name
    )

@app.get("/relations/", response_model=List[RelationOut])
def read_relations(skip: int = 0, limit: int = 100, db: Session = next(get_db())):
    relations = db.query(Relation).offset(skip).limit(limit).all()
    result = []
    for rel in relations:
        relation_type = db.query(RelationType).filter(RelationType.id == rel.relation_type).first()
        result.append(RelationOut(
            id=rel.id,
            from_entity_id=rel.from_entity_id,
            to_entity_id=rel.to_entity_id,
            relation_type=relation_type.relation_name if relation_type else "Unknown"
        ))
    return result

@app.post("/insights/", response_model=dict)
def append_insight(insight: InsightCreate, db: Session = next(get_db())):
    # Here, you can define how to handle insights.
    # For demonstration, we'll store insights as observations linked to a special entity.
    special_entity = db.query(Entity).filter(Entity.name == "Insights").first()
    if not special_entity:
        special_entity = Entity(name="Insights", entity_type="System")
        db.add(special_entity)
        db.commit()
        db.refresh(special_entity)
    
    new_observation = Observation(
        entity_id=special_entity.id,
        observation=insight.insight
    )
    db.add(new_observation)
    db.commit()
    return {"message": "Insight added successfully."}

@app.get("/hierarchy/", response_model=List[dict])
def get_full_implementation_hierarchy(db: Session = next(get_db())):
    query = """
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
    """
    result = db.execute(text(query)).fetchall()
    hierarchy = []
    for row in result:
        hierarchy.append({
            "implementation_id": row.implementation_id,
            "implementation": row.implementation,
            "interface_id": row.interface_id,
            "interface": row.interface,
            "level": row.level,
            "path": row.path
        })
    return hierarchy

@app.get("/validate_relations/", response_model=List[dict])
def validate_relations(db: Session = next(get_db())):
    query = """
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
    """
    result = db.execute(text(query)).fetchall()
    validation = []
    for row in result:
        validation.append({
            "from_entity": row.from_entity,
            "from_type": row.from_type,
            "relation_type": row.relation_type,
            "to_entity": row.to_entity,
            "to_type": row.to_type,
            "validity": row.validity,
            "valid_relation_id": row.valid_relation_id
        })
    return validation

@app.get("/find_implementations/{interface_name}", response_model=List[dict])
def find_implementations(interface_name: str, db: Session = next(get_db())):
    query = """
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
    WHERE e2.name = :interface_name
    AND rt.relation_name = 'implements';
    """
    result = db.execute(text(query), {"interface_name": interface_name}).fetchall()
    implementations = []
    for row in result:
        implementations.append({
            "implementation": row.implementation,
            "impl_type": row.impl_type,
            "relation_type": row.relation_type,
            "interface": row.interface,
            "attribute_key": row.attribute_key,
            "attribute_value": row.attribute_value
        })
    return implementations

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
