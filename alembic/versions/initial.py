"""Initial migration

Revision ID: initial
Revises: 
Create Date: 2024-11-29
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

revision = 'initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create semantic_metadata table
    op.create_table(
        'semantic_metadata',
        sa.Column('entity_id', sa.String(), nullable=False),
        sa.Column('inferred_types', sqlite.JSON(), nullable=True),
        sa.Column('derived_attributes', sqlite.JSON(), nullable=True),
        sa.Column('type_hierarchy', sqlite.JSON(), nullable=True),
        sa.Column('relationship_patterns', sqlite.JSON(), nullable=True),
        sa.Column('suggested_relations', sqlite.JSON(), nullable=True),
        sa.Column('last_updated', sa.DateTime(), nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.Column('provenance', sqlite.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('entity_id')
    )
    
    # Create semantic_patterns table
    op.create_table(
        'semantic_patterns',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('pattern_type', sa.String(), nullable=True),
        sa.Column('pattern_data', sqlite.JSON(), nullable=True),
        sa.Column('confidence', sa.Float(), nullable=True),
        sa.Column('examples', sqlite.JSON(), nullable=True),
        sa.Column('last_applied', sa.DateTime(), nullable=True),
        sa.Column('success_rate', sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('semantic_patterns')
    op.drop_table('semantic_metadata')
