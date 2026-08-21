# Diátaxis Reference Formatting Rules

## Definition

Accurate, complete technical specifications users consult during work. Describes what something IS, not how to use it.

**Use when**: User needs specifications, parameter lists, return values, error codes ("What are X's parameters?")
**Don't use**: Learning (→Tutorial), problem-solving (→How-to), concepts (→Explanation)

## Core Rules

- Information-oriented, not task-oriented. Facts, not instructions.
- Structured for lookup, not sequential reading. Scannable, searchable, consistent.
- Exhaustive and accurate. Document ALL parameters/values/errors/constraints.
- Austere and factual. No opinions, advice, explanations, or procedures.

## Structure

### Title

Pattern: "[Object/Feature] Reference" or object name ("API Reference", "Error Codes")
Avoid: "How to use...", "Understanding...", "Getting started..."

### Organization

- Alphabetical order (functions, methods, parameters)
- Logical grouping (related items together)
- Hierarchical (parent/child relationships)
- Consistent ordering within entries

### Required Entry Components

1. Name/identifier (exact as in code)
2. Signature/syntax (precise format)
3. Description (neutral, factual, 1 line)
4. Parameters/arguments (ALL, with types and constraints)
5. Return values (exact format, all possible values)
6. Examples (minimal, syntax-only)
7. Related items (cross-references)

## Content Templates

**API Endpoint**: Title `## POST /v1/merchants` → Description (1 line) → **Request** (headers, body params table) → **Response** (success code + object, error codes) → **Example** (minimal curl/code)

**Function/Method**: Title `## calculateTotal()` → Description → **Syntax** (signature) → **Parameters** (table or inline: name, type, required, description+constraints+defaults) → **Returns** (type + description) → **Throws** (error types + conditions) → **Example**

**Configuration**: Title `## timeout` → Description → Type | Default | Range | Env var (inline format)

**Error Code**: Title `## E_CODE_NAME` → Code | HTTP | Category → Description → Causes (list) → Resolution (list) → Related codes

**Object/Model**: Title `## Merchant Object` → Description → **Attributes** table (attribute, type, description+constraints) → **Example** (JSON)

**Enumeration**: Title `## Status` → Table (value, description) → Type | Used in (inline)

## Writing Style

**Voice**: Third person, neutral, present tense. Technical precision over readability. No imperative/opinions/recommendations.

- ✅ "Returns Merchant object" ❌ "This will return..."
- ✅ "Throws TypeError if not array" ❌ "Make sure items is an array"

**Requirements**: Exhaustive (ALL params/values/errors/constraints), Precise (exact types/constraints/defaults), Consistent (format/ordering/terminology)

- Type: `timeout` (number, optional): Integer 1000-300000. Default: 30000
- Constraint: Max 255 chars. Pattern: ^[A-Za-z0-9_-]+$

## Content Boundaries

**Include**: Complete specs (all params/values/errors/constraints), exact syntax/signatures/types, required vs optional, defaults, minimal syntax examples
**Exclude**: Instructions ("First, do X..."), explanations (why/how internally), advice ("We recommend..."), tutorials, problem-solving

- ❌ "To authenticate, first obtain API key, then include in header" → ✅ "Authentication requires Bearer token in Authorization header"
- ❌ "We use idempotency keys to prevent duplicate charges" → ✅ "Idempotency-Key (string, optional): Prevents duplicates. Max 255 chars. 24hr cache"

## Formatting

**Tables**: Use for params/fields/options/errors. Format: `| Parameter | Type | Required | Description |` with constraints inline
**Code**: Specify language, exact syntax, minimal code, no explanatory comments
**Types**: `string` `number` `boolean` `Array<string>` `Object` `{key: value}` `string | number` `Promise<Type>`
**Cross-refs**: `See [Object](#object)` `Related: [GET /endpoint](#endpoint)`

## Quality Checklist

- All parameters/fields/values/constraints/defaults/errors documented
- Types correct, syntax matches implementation, examples tested
- Consistent format, logical organization, scannable
- No instructions/explanations/tutorials/advice
- Neutral, third person, factual

## Common Mistakes

- ❌ "To create a merchant, send POST..." → ✅ "POST /v1/merchants creates merchant"
- ❌ "Webhooks work by sending HTTP..." → ✅ "Webhook endpoints receive POST requests"
- ❌ Document only "important" params → ✅ Document ALL params
- ❌ "String. Keep it short." → ✅ "String. Max 255 chars. Pattern: ^[A-Za-z0-9_-]+$"
- ❌ "We recommend async/await" → ✅ "Returns Promise<Merchant>"

## Template

```markdown
## [Name]

[One-sentence description]

### Syntax: `[exact]`

### Parameters: | name | type | req | description+constraints+default |

### Returns: **[type]**: description

### Errors: | code | condition |

### Example: [minimal code]

### Related: [items]
```

## Maintenance

Update with product changes. Prefer code generation. Version docs, archive old. Test examples, validate implementation.
