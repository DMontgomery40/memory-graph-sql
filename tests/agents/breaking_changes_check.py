# breaking_changes_check.py

import ast
import difflib
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class BreakingChange:
    file: str
    change_type: str
    description: str
    severity: str
    mitigation: str

class AgentBreakingChangesCheck:
    def __init__(self):
        self.breaking_changes: List[BreakingChange] = []
        
    def check_schema_changes(self, old_schema: str, new_schema: str) -> List[BreakingChange]:
        """Analyze SQL schema changes for breaking changes."""
        changes = []
        
        # Parse table definitions
        old_tables = self._parse_sql_tables(old_schema)
        new_tables = self._parse_sql_tables(new_schema)
        
        # Check for table removals
        for table in old_tables:
            if table not in new_tables:
                changes.append(BreakingChange(
                    file='semantic_layer.sql',
                    change_type='table_removal',
                    description=f'Table {table} has been removed',
                    severity='HIGH',
                    mitigation='Add migration script to handle removed table'
                ))
        
        # Check for column changes
        for table in old_tables:
            if table in new_tables:
                old_cols = old_tables[table]
                new_cols = new_tables[table]
                
                for col in old_cols:
                    if col not in new_cols:
                        changes.append(BreakingChange(
                            file='semantic_layer.sql',
                            change_type='column_removal',
                            description=f'Column {col} removed from {table}',
                            severity='HIGH',
                            mitigation='Add migration script to handle removed column'
                        ))
                    elif old_cols[col] != new_cols[col]:
                        changes.append(BreakingChange(
                            file='semantic_layer.sql',
                            change_type='column_type_change',
                            description=f'Column {col} in {table} changed type',
                            severity='HIGH',
                            mitigation='Add data conversion in migration'
                        ))
        
        return changes

    def check_api_changes(self, old_code: str, new_code: str) -> List[BreakingChange]:
        """Analyze API changes for breaking changes."""
        changes = []
        
        old_tree = ast.parse(old_code)
        new_tree = ast.parse(new_code)
        
        old_endpoints = self._get_endpoints(old_tree)
        new_endpoints = self._get_endpoints(new_tree)
        
        # Check for removed or modified endpoints
        for path, methods in old_endpoints.items():
            if path not in new_endpoints:
                changes.append(BreakingChange(
                    file='main.py',
                    change_type='endpoint_removal',
                    description=f'Endpoint {path} has been removed',
                    severity='HIGH',
                    mitigation='Add endpoint compatibility layer'
                ))
            else:
                for method in methods:
                    if method not in new_endpoints[path]:
                        changes.append(BreakingChange(
                            file='main.py',
                            change_type='method_removal',
                            description=f'{method} method removed from {path}',
                            severity='HIGH',
                            mitigation='Add method compatibility layer'
                        ))
        
        return changes

    def check_model_changes(self, old_models: str, new_models: str) -> List[BreakingChange]:
        """Analyze model changes for breaking changes."""
        changes = []
        
        old_tree = ast.parse(old_models)
        new_tree = ast.parse(new_models)
        
        old_models = self._get_models(old_tree)
        new_models = self._get_models(new_tree)
        
        # Check for model changes
        for model in old_models:
            if model not in new_models:
                changes.append(BreakingChange(
                    file='models.py',
                    change_type='model_removal',
                    description=f'Model {model} has been removed',
                    severity='HIGH',
                    mitigation='Add model compatibility layer'
                ))
            else:
                old_attrs = old_models[model]
                new_attrs = new_models[model]
                
                for attr in old_attrs:
                    if attr not in new_attrs:
                        changes.append(BreakingChange(
                            file='models.py',
                            change_type='attribute_removal',
                            description=f'Attribute {attr} removed from {model}',
                            severity='HIGH',
                            mitigation='Add attribute compatibility layer'
                        ))
        
        return changes

    def check_semantic_changes(self, old_semantic: str, new_semantic: str) -> List[BreakingChange]:
        """Analyze semantic layer changes for breaking changes."""
        changes = []
        
        # Compare semantic rules
        old_rules = self._parse_semantic_rules(old_semantic)
        new_rules = self._parse_semantic_rules(new_semantic)
        
        for rule in old_rules:
            if rule not in new_rules:
                changes.append(BreakingChange(
                    file='semantic_layer.sql',
                    change_type='semantic_rule_removal',
                    description=f'Semantic rule {rule} has been removed',
                    severity='MEDIUM',
                    mitigation='Review semantic rule dependencies'
                ))
        
        return changes

    def _parse_sql_tables(self, sql: str) -> Dict[str, Dict[str, str]]:
        """Parse SQL schema into table definitions."""
        tables = {}
        current_table = None
        
        for line in sql.split('\n'):
            line = line.strip()
            if line.startswith('CREATE TABLE'):
                current_table = line.split()[2]
                tables[current_table] = {}
            elif current_table and line.startswith(('    ', '\t')) and ' ' in line:
                col_def = line.strip().split(' ', 1)
                if len(col_def) == 2:
                    col_name, col_type = col_def
                    tables[current_table][col_name] = col_type
        
        return tables

    def _get_endpoints(self, tree: ast.AST) -> Dict[str, List[str]]:
        """Extract FastAPI endpoints from AST."""
        endpoints = {}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Call):
                        if hasattr(decorator.func, 'attr') and decorator.func.attr in ['get', 'post', 'put', 'delete']:
                            method = decorator.func.attr.upper()
                            path = decorator.args[0].value if decorator.args else '/'
                            if path not in endpoints:
                                endpoints[path] = []
                            endpoints[path].append(method)
        
        return endpoints

    def _get_models(self, tree: ast.AST) -> Dict[str, List[str]]:
        """Extract SQLAlchemy models from AST."""
        models = {}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for base in node.bases:
                    if isinstance(base, ast.Name) and base.id == 'Base':
                        models[node.name] = []
                        for child in node.body:
                            if isinstance(child, ast.Assign):
                                for target in child.targets:
                                    if isinstance(target, ast.Name):
                                        models[node.name].append(target.id)
        
        return models

    def _parse_semantic_rules(self, sql: str) -> List[str]:
        """Extract semantic rules from SQL."""
        rules = []
        
        for line in sql.split('\n'):
            if 'INSERT INTO relation_types' in line:
                parts = line.split('VALUES')
                if len(parts) == 2:
                    rules.append(parts[1].strip())
        
        return rules

    def generate_report(self) -> str:
        """Generate a breaking changes report."""
        report = ["Breaking Changes Analysis Report\n"]
        
        if not self.breaking_changes:
            report.append("No breaking changes detected.")
            return '\n'.join(report)
        
        # Group changes by severity
        changes_by_severity = {}
        for change in self.breaking_changes:
            if change.severity not in changes_by_severity:
                changes_by_severity[change.severity] = []
            changes_by_severity[change.severity].append(change)
        
        # Report high severity changes first
        for severity in ['HIGH', 'MEDIUM', 'LOW']:
            if severity in changes_by_severity:
                report.append(f"\n{severity} Severity Changes:")
                for change in changes_by_severity[severity]:
                    report.append(f"\nFile: {change.file}")
                    report.append(f"Type: {change.change_type}")
                    report.append(f"Description: {change.description}")
                    report.append(f"Mitigation: {change.mitigation}\n")
        
        return '\n'.join(report)
