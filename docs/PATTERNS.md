# Pattern Definition Guide

## Pattern Structure

Patterns are defined using a flexible schema that supports various matching rules:

```json
{
    "id": "pattern_identifier",
    "type": "document_type",
    "pattern_data": {
        "attribute_patterns": {
            "attribute_name": {
                "type": "data_type",
                "required": boolean,
                "values": ["allowed", "values"],
                "keywords": ["matching", "keywords"],
                "pattern": "regex_pattern"
            }
        }
    },
    "confidence": 0.7
}
```

## Matching Rules

### 1. Type Matching
- `type`: Specifies the expected data type (string, integer, array, etc.)
- Example:
```json
{
    "type": "string"
}
```

### 2. Value Matching
- `values`: List of allowed values
- Example:
```json
{
    "values": ["pdf", "doc", "docx"]
}
```

### 3. Keyword Matching
- `keywords`: List of keywords to match within string values
- Example:
```json
{
    "keywords": ["report", "analysis", "study"]
}
```

### 4. Pattern Matching
- `pattern`: Regular expression pattern
- Example:
```json
{
    "pattern": "^[A-Z][a-z]+\s+Report$"
}
```

## Example Patterns

### 1. Financial Report
```json
{
    "id": "financial_report",
    "type": "FinancialDocument",
    "pattern_data": {
        "attribute_patterns": {
            "title": {
                "type": "string",
                "required": true,
                "keywords": ["financial", "quarterly", "annual", "report"],
                "pattern": "^[QQ1234]\d\s+\d{4}.*Report$"
            },
            "format": {
                "type": "string",
                "required": true,
                "values": ["pdf", "xlsx"]
            },
            "fiscal_year": {
                "type": "integer",
                "required": true
            }
        }
    },
    "confidence": 0.9
}
```

### 2. User Profile
```json
{
    "id": "user_profile",
    "type": "UserDocument",
    "pattern_data": {
        "attribute_patterns": {
            "name": {
                "type": "string",
                "required": true
            },
            "email": {
                "type": "string",
                "required": true,
                "pattern": "^[^@]+@[^@]+\.[^@]+$"
            },
            "age": {
                "type": "integer",
                "required": false
            }
        }
    },
    "confidence": 0.8
}
```

## Best Practices

1. **Pattern Names**
   - Use descriptive, unique identifiers
   - Follow a consistent naming convention

2. **Confidence Scores**
   - Use higher confidence for strict patterns
   - Use lower confidence for flexible patterns
   - Typical range: 0.7 - 0.95

3. **Required Attributes**
   - Mark critical attributes as required
   - Keep required attributes minimal

4. **Keyword Selection**
   - Choose distinctive keywords
   - Include common variations
   - Consider domain-specific terminology

5. **Regular Expressions**
   - Keep patterns simple and maintainable
   - Test patterns thoroughly
   - Document complex patterns

6. **Value Lists**
   - Keep lists current and comprehensive
   - Document any special values
   - Consider case sensitivity
