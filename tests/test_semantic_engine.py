import pytest
from semantic.engine import SemanticEngine
from semantic.models import SemanticMetadata, SemanticPattern

@pytest.fixture
def sample_entity():
    return {
        "id": "test1",
        "type": "Document",
        "attributes": {
            "title": "Test Document",
            "size": 1000,
            "format": "pdf"
        }
    }

@pytest.fixture
def sample_pattern():
    return {
        "type": "type_inference",
        "match_rules": [
            {
                "type": "attribute_exists",
                "attribute": "format"
            },
            {
                "type": "attribute_type",
                "attribute": "size",
                "value_type": int
            }
        ],
        "confidence": 0.9
    }

async def test_pattern_matching(engine, sample_entity, sample_pattern):
    assert engine._matches_pattern(sample_entity, sample_pattern) == True

async def test_metadata_creation(engine, sample_entity):
    metadata = await engine._get_metadata(sample_entity['id'])
    assert metadata is not None
    assert metadata.entity_id == sample_entity['id']

async def test_entity_enrichment(engine, sample_entity):
    enriched = await engine.enrich_entity(sample_entity)
    assert 'semantic' in enriched
    assert 'inferred_types' in enriched['semantic']