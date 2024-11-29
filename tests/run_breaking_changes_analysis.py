# run_breaking_changes_analysis.py

from agents.breaking_changes_check import AgentBreakingChangesCheck

def main():
    agent = AgentBreakingChangesCheck()
    
    # Read current files
    try:
        with open('../semantic_layer.sql', 'r') as f:
            current_schema = f.read()
            
        with open('../main.py', 'r') as f:
            current_api = f.read()
            
        with open('../models.py', 'r') as f:
            current_models = f.read()
    except FileNotFoundError as e:
        print(f"Error reading current files: {e}")
        return
    
    # Define proposed changes
    proposed_schema = '''-- Enhanced schema with semantic capabilities
    CREATE TABLE IF NOT EXISTS semantic_rules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rule_name TEXT NOT NULL,
        pattern JSONB NOT NULL,
        actions JSONB NOT NULL,
        priority INTEGER DEFAULT 0,
        context JSONB
    );

    ALTER TABLE relation_types 
    ADD COLUMN confidence_score FLOAT CHECK(confidence_score BETWEEN 0 AND 1),
    ADD COLUMN semantic_context JSONB,
    ADD COLUMN validation_rules JSONB;
    '''
    
    proposed_models = '''from sqlalchemy import Column, Integer, String, Float, JSON
    class SemanticRule(Base):
        __tablename__ = 'semantic_rules'
        id = Column(Integer, primary_key=True, index=True)
        rule_name = Column(String, nullable=False)
        pattern = Column(JSON, nullable=False)
        actions = Column(JSON, nullable=False)
        priority = Column(Integer, default=0)
        context = Column(JSON)
    '''
    
    # Run analysis
    schema_changes = agent.check_schema_changes(current_schema, proposed_schema)
    api_changes = agent.check_api_changes(current_api, '''async def enhanced_api():
        pass''')
    model_changes = agent.check_model_changes(current_models, proposed_models)
    
    # Generate report
    agent.breaking_changes.extend(schema_changes)
    agent.breaking_changes.extend(api_changes)
    agent.breaking_changes.extend(model_changes)
    
    report = agent.generate_report()
    
    # Write report to file
    with open('breaking_changes_report.md', 'w') as f:
        f.write(report)
    
    print("Breaking changes analysis complete. See breaking_changes_report.md for details.")

if __name__ == '__main__':
    main()