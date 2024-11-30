# Memory Graph MCP Tool

A semantic pattern matching and type inference tool that implements the Model Context Protocol (MCP).

## Installation

1. Install the package:
```bash
pip install -r requirements.txt
```

2. Start the MCP server:
```bash
python mcp_server.py
```

The server will start and register itself with Claude Desktop.

## Usage in Claude

Once the server is running, you can use the tool in Claude Desktop with these commands:

1. Infer type for a document:
```json
{
    "command": "infer_type",
    "parameters": {
        "id": "doc1",
        "attributes": {
            "title": "Project Report",
            "format": "pdf"
        }
    }
}
```

2. Add a new pattern:
```json
{
    "command": "add_pattern",
    "parameters": {
        "id": "pdf_doc",
        "type": "Document",
        "pattern_data": {
            "attribute_patterns": {
                "title": {"type": "string", "required": true},
                "format": {"type": "string", "values": ["pdf"]}
            }
        },
        "confidence": 0.8
    }
}
```

3. Get all patterns:
```json
{
    "command": "get_patterns",
    "parameters": {}
}
```

## Tool Commands

1. `infer_type`: Analyzes a document and returns matching patterns with confidence scores
2. `add_pattern`: Adds a new pattern for matching
3. `get_patterns`: Lists all available patterns

## Development

This tool uses the Model Context Protocol to integrate with Claude Desktop. See the [MCP documentation](https://github.com/modelcontextprotocol/docs) for more details.