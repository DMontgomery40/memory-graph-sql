# database.py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./memory_graph.db")

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    with engine.connect() as connection:
        with open("semantic_layer.sql", "r") as f:
            semantic_sql = f.read()
            connection.execute(text(semantic_sql))
        with open("schema.sql", "r") as f:
            schema_sql = f.read()
            connection.execute(text(schema_sql))
