# models.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class RelationType(Base):
    __tablename__ = 'relation_types'
    id = Column(Integer, primary_key=True, index=True)
    relation_name = Column(String, unique=True, nullable=False)
    semantic_category = Column(String, nullable=False)
    description = Column(Text)
    inverse_relation = Column(Integer, ForeignKey('relation_types.id'))
    transitive = Column(Boolean, default=False)
    symmetric = Column(Boolean, default=False)
    directional = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
    updated_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")

    inverse = relationship("RelationType", remote_side=[id])

class EntityTypeHierarchy(Base):
    __tablename__ = 'entity_type_hierarchy'
    id = Column(Integer, primary_key=True, index=True)
    parent_type = Column(String, nullable=False)
    child_type = Column(String, nullable=False)
    hierarchy_level = Column(Integer, nullable=False)

class ValidTypeRelation(Base):
    __tablename__ = 'valid_type_relations'
    id = Column(Integer, primary_key=True, index=True)
    from_type = Column(String, nullable=False)
    relation_type = Column(Integer, ForeignKey('relation_types.id'), nullable=False)
    to_type = Column(String, nullable=False)

    relation = relationship("RelationType")

class Entity(Base):
    __tablename__ = 'entities'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    entity_type = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
    updated_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")

    attributes = relationship("EntityAttribute", back_populates="entity")
    observations = relationship("Observation", back_populates="entity")
    relations_from = relationship("Relation", back_populates="from_entity", foreign_keys='Relation.from_entity_id')
    relations_to = relationship("Relation", back_populates="to_entity", foreign_keys='Relation.to_entity_id')

class Observation(Base):
    __tablename__ = 'observations'
    id = Column(Integer, primary_key=True, index=True)
    entity_id = Column(Integer, ForeignKey('entities.id'), nullable=False)
    relation_id = Column(Integer, ForeignKey('relations.id'), nullable=True)
    observation = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")

    entity = relationship("Entity", back_populates="observations")
    relation = relationship("Relation")

class Relation(Base):
    __tablename__ = 'relations'
    id = Column(Integer, primary_key=True, index=True)
    from_entity_id = Column(Integer, ForeignKey('entities.id'), nullable=False)
    to_entity_id = Column(Integer, ForeignKey('entities.id'), nullable=False)
    relation_type = Column(Integer, ForeignKey('relation_types.id'), nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")

    from_entity = relationship("Entity", foreign_keys=[from_entity_id], back_populates="relations_from")
    to_entity = relationship("Entity", foreign_keys=[to_entity_id], back_populates="relations_to")
    relation_type_obj = relationship("RelationType")

class EntityAttribute(Base):
    __tablename__ = 'entity_attributes'
    id = Column(Integer, primary_key=True, index=True)
    entity_id = Column(Integer, ForeignKey('entities.id'), nullable=False)
    attribute_key = Column(String, nullable=False)
    attribute_value = Column(String)

    entity = relationship("Entity", back_populates="attributes")
