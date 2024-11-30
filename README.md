# Memory Graph - Claude Desktop Tool

A semantic pattern matching and type inference tool for Claude Desktop.

## Installation

1. Copy `mcp_tool.py` and `claude_desktop.json` to your Claude Desktop tools directory
2. Add the tool configuration to your Claude Desktop tools registry

## Usage in Claude

```python
# Add a pattern
result = await memory_graph.add_pattern(
    id="pdf_report",
    type="Report",
    pattern_data={
        "attribute_patterns": {
            "title": {
                "type": "string",
                "required": True,
                "keywords": ["report", "analysis"]
            },
            "format": {
                "type": "string",
                "values": ["pdf"]
            }
        }
    },
    confidence=0.8
)

# Infer document type
result = await memory_graph.infer_type(
    id="doc1",
    attributes={
        "title": "Q4 Financial Analysis Report",
        "format": "pdf"
    }
)

# Get all patterns
patterns = await memory_graph.get_patterns()
```

## Features

- Pattern-based document type inference
- Configurable confidence scoring
- SQLite-based pattern storage
- Keyword and value matching
- Regular expression support