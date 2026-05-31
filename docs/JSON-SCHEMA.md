# Template JSON Schemas

This document defines machine-verifiable contracts for all template placeholders.

## What is a JSON Schema?

A JSON Schema defines the structure, types, and constraints of data. In AIOA, every template placeholder must have a schema so agents can validate input before filling in templates.

## Template Schemas

### constitution-template-aioa.md

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["project_name", "project_description", "principles"],
  "properties": {
    "project_name": {
      "type": "string",
      "minLength": 1,
      "maxLength": 100,
      "description": "Name of the project"
    },
    "project_description": {
      "type": "string",
      "minLength": 10,
      "maxLength": 500,
      "description": "Brief description of the project"
    },
    "principles": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["id", "name", "description"],
        "properties": {
          "id": { "type": "string", "pattern": "^P[0-9]+$" },
          "name": { "type": "string", "minLength": 1 },
          "description": { "type": "string", "minLength": 10 }
        }
      }
    }
  }
}
```

### spec-template-aioa.md

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["feature_name", "description", "principle_analysis"],
  "properties": {
    "feature_name": {
      "type": "string",
      "minLength": 1,
      "maxLength": 100
    },
    "description": {
      "type": "string",
      "minLength": 20,
      "maxLength": 2000
    },
    "principle_analysis": {
      "type": "object",
      "required": ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9", "P10"],
      "properties": {
        "P1": { "type": "string", "minLength": 10 },
        "P2": { "type": "string", "minLength": 10 },
        "P3": { "type": "string", "minLength": 10 },
        "P4": { "type": "string", "minLength": 10 },
        "P5": { "type": "string", "minLength": 10 },
        "P6": { "type": "string", "minLength": 10 },
        "P7": { "type": "string", "minLength": 10 },
        "P8": { "type": "string", "minLength": 10 },
        "P9": { "type": "string", "minLength": 10 },
        "P10": { "type": "string", "minLength": 10 }
      }
    }
  }
}
```

### plan-template-aioa.md

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["plan_name", "description", "steps", "adrs"],
  "properties": {
    "plan_name": {
      "type": "string",
      "minLength": 1,
      "maxLength": 100
    },
    "description": {
      "type": "string",
      "minLength": 20,
      "maxLength": 2000
    },
    "steps": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["name", "description", "files_affected"],
        "properties": {
          "name": { "type": "string", "minLength": 1 },
          "description": { "type": "string", "minLength": 10 },
          "files_affected": { "type": "array", "items": { "type": "string" } }
        }
      }
    },
    "adrs": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["title", "principle", "decision", "rationale"],
        "properties": {
          "title": { "type": "string", "minLength": 1 },
          "principle": { "type": "string", "pattern": "^P[0-9]+$" },
          "decision": { "type": "string", "minLength": 10 },
          "rationale": { "type": "string", "minLength": 10 }
        }
      }
    }
  }
}
```

### tasks-template-aioa.md

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["tasks"],
  "properties": {
    "tasks": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["id", "name", "description", "context_budget", "files"],
        "properties": {
          "id": { "type": "string", "pattern": "^T[0-9]+$" },
          "name": { "type": "string", "minLength": 1 },
          "description": { "type": "string", "minLength": 10 },
          "context_budget": {
            "type": "object",
            "required": ["max_files", "max_tokens"],
            "properties": {
              "max_files": { "type": "integer", "minimum": 1, "maximum": 20 },
              "max_tokens": { "type": "integer", "minimum": 500, "maximum": 10000 }
            }
          },
          "files": { "type": "array", "items": { "type": "string" } }
        }
      }
    }
  }
}
```
