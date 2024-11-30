from mcp.server import MCPServer
from semantic_core import SemanticCore
from typing import Dict, Any
import asyncio

class MemoryGraphTool:
    def __init__(self):
        self.semantic_core = SemanticCore()

    async def handle_request(self, command: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if command == 'infer_type':
                result = self.semantic_core.infer_types(parameters)
                return {
                    'status': 'success',
                    'data': result
                }
            elif command == 'add_pattern':
                self.semantic_core.add_pattern(
                    parameters['id'],
                    parameters['type'],
                    parameters['pattern_data'],
                    parameters.get('confidence', 0.7)
                )
                return {'status': 'success'}
            elif command == 'get_patterns':
                patterns = self.semantic_core.get_patterns()
                return {
                    'status': 'success',
                    'data': patterns
                }
            else:
                return {
                    'status': 'error',
                    'message': f'Unknown command: {command}'
                }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

async def main():
    # Initialize the tool
    tool = MemoryGraphTool()
    
    # Create MCP server with the tool
    server = MCPServer([
        {
            'name': 'memory_graph',
            'handler': tool.handle_request,
            'description': 'A semantic pattern matching and type inference tool',
            'commands': {
                'infer_type': {
                    'description': 'Infer types for a given document',
                    'parameters': {
                        'id': 'string',
                        'attributes': 'object'
                    }
                },
                'add_pattern': {
                    'description': 'Add a new pattern for matching',
                    'parameters': {
                        'id': 'string',
                        'type': 'string',
                        'pattern_data': 'object',
                        'confidence': 'number?'
                    }
                },
                'get_patterns': {
                    'description': 'Get all available patterns',
                    'parameters': {}
                }
            }
        }
    ])
    
    # Start the server
    await server.start()

if __name__ == '__main__':
    asyncio.run(main())
