from typing import Dict, Any
from mcp_core import MCPTool, MCPRequest, MCPResponse
from semantic_core import SemanticCore

class MemoryGraphMCP(MCPTool):
    def __init__(self, db_path: str = "semantic.db"):
        super().__init__()
        self.semantic_core = SemanticCore()

    async def handle_request(self, request: MCPRequest) -> MCPResponse:
        command = request.command
        params = request.parameters

        try:
            if command == 'infer':
                result = self.semantic_core.infer_types(params)
                return MCPResponse(status='success', data=result)
            
            elif command == 'add_pattern':
                pattern_id = params.get('id')
                if not pattern_id:
                    return MCPResponse(status='error', message='Pattern ID is required')
                
                cursor = self.semantic_core.conn.cursor()
                cursor.execute(
                    'INSERT OR REPLACE INTO patterns (id, type, pattern_data, confidence) VALUES (?, ?, ?, ?)',
                    (pattern_id, params.get('type'), str(params.get('pattern_data')), params.get('confidence', 0.7))
                )
                self.semantic_core.conn.commit()
                return MCPResponse(status='success')
            
            elif command == 'get_patterns':
                cursor = self.semantic_core.conn.cursor()
                cursor.execute('SELECT id, type, pattern_data, confidence FROM patterns')
                patterns = cursor.fetchall()
                return MCPResponse(
                    status='success',
                    data=[{
                        'id': p[0],
                        'type': p[1],
                        'pattern_data': p[2],
                        'confidence': p[3]
                    } for p in patterns]
                )
            
            else:
                return MCPResponse(
                    status='error',
                    message=f'Unknown command: {command}'
                )

        except Exception as e:
            return MCPResponse(
                status='error',
                message=str(e)
            )
