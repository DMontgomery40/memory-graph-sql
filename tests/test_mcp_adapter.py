import unittest
import asyncio
from src.mcp_adapter import MemoryGraphMCP
from mcp_core import MCPRequest

class TestMemoryGraphMCP(unittest.TestCase):
    def setUp(self):
        self.memory_graph = MemoryGraphMCP(':memory:')

    def test_infer_types(self):
        request = MCPRequest(
            command='infer',
            parameters={
                'id': 'doc1',
                'attributes': {
                    'title': 'Project Report',
                    'format': 'pdf'
                }
            }
        )

        async def run_test():
            response = await self.memory_graph.handle_request(request)
            self.assertEqual(response.status, 'success')
            self.assertIn('Document', response.data)

        asyncio.run(run_test())

    def test_add_pattern(self):
        request = MCPRequest(
            command='add_pattern',
            parameters={
                'id': 'test_pattern',
                'type': 'TestDoc',
                'pattern_data': {
                    'attribute_patterns': {
                        'title': {'type': 'string', 'required': True},
                        'format': {'type': 'string', 'values': ['test']}
                    }
                },
                'confidence': 0.8
            }
        )

        async def run_test():
            response = await self.memory_graph.handle_request(request)
            self.assertEqual(response.status, 'success')

        asyncio.run(run_test())

    def test_get_patterns(self):
        request = MCPRequest(
            command='get_patterns',
            parameters={}
        )

        async def run_test():
            response = await self.memory_graph.handle_request(request)
            self.assertEqual(response.status, 'success')
            self.assertIsInstance(response.data, list)

        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()