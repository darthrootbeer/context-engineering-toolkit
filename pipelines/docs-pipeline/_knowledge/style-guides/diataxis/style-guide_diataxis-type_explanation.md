# Diátaxis Explanation Rules

Clarify concepts and provide understanding. Answer "why" and "how it works," not "how to do it."

## Classification Criteria

**Use Explanation when:**

- User asks "Why does this work this way?"
- User needs conceptual understanding, design rationale, or context
- User needs to evaluate alternatives or understand trade-offs

**Do NOT use Explanation for:**

- Learning by doing → Tutorial
- Solving specific problems → How-to Guide
- Technical specifications → Reference

## Hard Structural Rules

### Title Format

Required patterns: "Understanding [concept]", "How [system] works", "[Concept] explained", "About [topic]", or direct concept name.

✅ "Understanding the order lifecycle", "How invoice matching works", "Authentication models explained"
❌ "How to implement webhooks" (How-to), "Create your first webhook" (Tutorial)

### Opening Section (Required)

1. **Context**: What problem domain, why it exists, where it fits
2. **Scope**: What's covered, boundaries, related topics

Keep to 2-3 paragraphs. Link to related Tutorial/How-to/Reference docs.

### Body Structure (Flexible)

Organize by: conceptual progression (simple→complex), thematic (by component/concern), or comparative (alternatives/trade-offs).

### Conclusion (Required)

Include: key insights summary, connections to practice, links to related docs.
Exclude: repetitive summaries, calls to action, instructions.

## Core Content Rules

### ✅ DO Include

- What things are and why they exist
- How systems work internally, component relationships
- Design rationale, regulatory requirements, industry standards
- Trade-offs, alternatives, when to use different strategies
- Opinions, best practices (with justification), architectural guidance

### ❌ Do NOT Include

- Step-by-step procedures or "First do X, then Y"
- Complete API documentation, parameter lists, exact return values
- Hands-on tutorials, practice examples, learning activities

### Boundary Examples

❌ Wrong (instructional): "To implement webhook handling, first create an endpoint that accepts POST requests. Then verify the signature..."

✅ Right (explanatory): "Webhook handling requires an endpoint and signature verification. The signature mechanism prevents attackers from sending fake events."

❌ Wrong (reference): "POST /v1/orders | Parameters: total (number, required)..."

✅ Right (explanatory): "Order totals are specified in smallest currency units (cents for USD) to avoid floating-point precision issues that could accumulate across invoices."

## Writing Style Rules

### Voice

- Third person or inclusive first person ("we")
- Thoughtful, reflective, conversational yet authoritative
- Can express opinions and perspective

✅ "This architecture reflects a trade-off between simplicity and flexibility"
✅ "We designed this because..."
❌ "Now you're going to learn about webhooks!" (tutorial-like)
❌ "Click the Settings button" (instructional)

### Language

- Be discursive: use analogies, explore tangents that illuminate, connect related concepts
- Be analytical: discuss reasons, compare alternatives, explain implications
- Use technical precision with plain language for concepts
- Define terms in context

### Explanation Techniques

**Analogies:**
"Idempotency keys are like package tracking numbers. They always refer to the same operation regardless of how many times submitted."

**Contrasts:**
"Unlike invoices that are paid after delivery, prepaid orders are always confirmed in real time because the payment has already cleared."

**Causation chains:**
"Tax rules require a signed total → mandates online validation → needs connectivity → affects offline-first architecture"

## Visual Elements

### Diagrams (Highly Valuable)

Use for: architecture, flows, state machines, concept maps, relationships, sequences.

### Code Examples (Minimal)

Show concepts only, not complete implementations. Illustrate principles, not prescribe solutions.

```python
def verify_signature(payload, signature, secret):
    expected = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)
```

"This pattern prevents timing attacks while validating authenticity."

### Tables (For Comparisons)

Use to contrast order types, payment terms, cancellation windows, etc.

## Common Mistakes

1. **Becomes How-to**: Provides instructions → Fix: Remove procedures, focus on concepts/rationale
2. **Becomes Reference**: Lists specs without context → Fix: Add interpretation, reasoning
3. **Too Abstract**: Pure theory disconnected from practice → Fix: Connect to practical implications
4. **Too Surface**: Doesn't deepen understanding → Fix: Go deeper into "why" and "how it works"
5. **Assumes Too Much**: Unexplained jargon → Fix: Define terms, build understanding progressively

## Domain and Compliance Context

### Tax and Shipping Rules

When explaining tax or shipping requirements:

- State regulatory mandates clearly (tax authority and regional rules)
- Explain why requirements exist (fraud prevention, customer protection, audit accountability)
- Connect regulations to technical implications (signed total → online validation → connectivity requirements)

### Taxable Item Verification

Explain the complexity of taxable item rules, variability across regions, and technical challenges in real-time verification.

### Real-time Confirmation

Contrast with the invoice-after-delivery model. Explain why prepaid orders require immediate confirmation.

## Template

```markdown
# Understanding [Concept] / How [System] Works

[Context: why this matters, problem domain]
[Scope: what's covered, boundaries]

## [Major concept]

[What it is, why it exists, how it works, why designed this way]

## [Another concept]

[Continue pattern]

## [Comparative/analytical section]

[Alternatives, trade-offs, implications]

## Key insights

[Summary and significance]

## Related topics

**How-to guides:** [practical implementation]
**Reference:** [technical specifications]
**Tutorials:** [hands-on learning]
**Further explanation:** [related explanatory content]
```

## Quality Checklist

- [ ] Clarifies why things are the way they are
- [ ] Explains how things work, provides useful mental models
- [ ] No step-by-step instructions, specs, or exercises
- [ ] Discusses alternatives, trade-offs, design decisions
- [ ] Concepts clearly explained with appropriate detail
- [ ] Helps readers make informed decisions
- [ ] Connects theory to practice

## Cross-references

Link to Tutorial (practice), How-to (implementation), Reference (specs), related Explanations (deeper context).

## Maintenance Triggers

Update when: architecture/concepts change, regulations/standards change, better mental models emerge, user questions reveal gaps, feedback indicates confusion.
