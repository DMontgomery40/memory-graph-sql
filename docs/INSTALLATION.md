# Installation Guide

## Prerequisites

- Python 3.7 or higher
- pip package manager
- Git (optional)

## Installation Steps

### 1. Get the Code

```bash
# Clone the repository
git clone https://github.com/DMontgomery40/memory-graph-sql.git
cd memory-graph-sql

# Switch to MCP integration branch
git checkout mcp-integration
```

Or download the ZIP file from GitHub.

### 2. Install Dependencies

```bash
# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 3. Configuration

The tool uses a SQLite database by default. No additional configuration is needed for basic usage.

### 4. Start the MCP Server

```bash
python mcp_server.py
```

The server will start and register itself with Claude Desktop.

## Verification

### 1. Test Connection

In Claude Desktop, try a simple command:

```python
result = await memory_graph.handle_request({
    'command': 'get_patterns',
    'parameters': {}
})
print(result)
```

### 2. Run Tests

```bash
python -m unittest discover tests
```

## Troubleshooting

### Common Issues

1. **Server Won't Start**
   - Check Python version
   - Verify all dependencies are installed
   - Check port availability

2. **Database Errors**
   - Verify write permissions in the directory
   - Check SQLite installation

3. **Pattern Matching Issues**
   - Verify pattern format
   - Check confidence thresholds
   - Review pattern definitions

### Logging

The server logs to stdout by default. For more detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Updates

```bash
# Pull latest changes
git pull

# Update dependencies
pip install -r requirements.txt --upgrade
```

## Security Notes

1. The server runs locally by default
2. Database is file-based and requires appropriate permissions
3. No authentication is required for local usage
