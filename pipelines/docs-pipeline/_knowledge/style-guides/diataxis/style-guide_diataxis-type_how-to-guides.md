# Diátaxis How-to Guide Rules

Provide practical directions to help competent users accomplish specific real-world goals.

## Classification

**Use how-to when:** User understands basics and needs to do something specific, has concrete goal/problem, needs efficiency not learning

**Do NOT use how-to for:** Learning product (→Tutorial), looking up specs (→Reference), understanding concepts (→Explanation)

## Core Principles

- **Goal-oriented**: Solve problems, not teach skills
- **Assumes competence**: User knows basics, terminology, can follow technical directions
- **Real-world focus**: Address actual use cases, not theoretical
- **Action-focused**: Get to point quickly, minimal exposition

## Structure Requirements

### Title Format

Pattern: "How to [accomplish goal]" or "[Action] [object]"

✅ "How to configure SSO authentication", "Deploy to production", "Troubleshoot connection errors"
❌ "Understanding authentication" (Explanation), "Your first deployment" (Tutorial), "API reference" (Reference)

### Opening Section

**Must include:**

1. **Problem/goal** (1-2 sentences): What this solves or accomplishes
2. **Prerequisites**: Required knowledge, setup, access (brief, not tutorial)
3. **When to use** (optional): Conditions, trade-offs

**Must NOT include:** Teaching content, foundational concepts, detailed background/theory, learning exercises

**Example:**

```markdown
# Configure SAML SSO Authentication

Integrate SAML 2.0 single sign-on for enterprise customers.

## Prerequisites

- Admin access to The Product dashboard
- SAML metadata from identity provider

## When to use this

Use when you need multiple identity providers or enterprise security compliance.
For OAuth 2.0, see [How to configure OAuth authentication].
```

### Step-by-Step Instructions

**Structure:** (1) Action statement: imperative verb, specific, concise; (2) Technical details: code/commands/configs as needed; (3) Result/validation: only if critical; (4) Variations: alternatives/conditional paths if applicable

**Key differences from tutorials:** Less "why", more flexibility, offer options, assume user can adapt

### Options and Variations

Present multiple approaches when tools/technologies, environments, or organizational constraints differ.

```markdown
## Choose deployment method

### Option A: Docker

Best for: Containerized environments
[Steps]

### Option B: Traditional

Best for: Direct control
[Steps]
```

### Troubleshooting

Include when common problems predictable, errors have specific solutions, or users frequently stuck.

```markdown
## Troubleshooting

### Error: "Invalid SAML response"

**Cause**: Clock skew between IdP and The Product servers
**Solution**: Ensure NTP configured. Max clock skew: 60 seconds.
```

### Conclusion

**Include:** Confirmation of accomplishment, links to related how-tos/reference/explanations
**Exclude:** Teaching recaps, congratulations, extensive next steps

## Writing Style Rules

### Voice and Tone

Professional, direct, actionable. Second person ("you") but less hand-holding than tutorials. Imperative mood. Respectful of user's time.

✅ "Configure the endpoint URL in your IdP settings" / "Use `--force` flag to override settings"
❌ "Now you're going to configure the endpoint URL! This is an exciting step..." / "You can use the force flag (don't worry, this is safe!)"

### Language Specificity

Be precise not exhaustive. Use professional vocabulary. Be concise.

✅ "Set `timeout` parameter to 30" / "Run deployment script"
❌ "Set timeout parameter (which controls wait time) to 30 (seconds)" / "Now that you understand deployments, run script"

### Instruction Formatting

Numbered lists for sequential steps; bullets for non-sequential items; ### for major sections, #### for subsections; code blocks with language; bold for UI (**Save**); inline code for technical terms (`timeout`)

## Content Boundaries

**DO Include:** Specific steps, code/commands/configs, technical details, options/alternatives, troubleshooting, brief "why" if affects decisions, warnings, shortcuts

**Do NOT Include:** Foundational concepts (→Explanations), detailed how-things-work (→Explanations), learning exercises (→Tutorials), comprehensive parameters (→Reference), complete API specs (→Reference), architecture deep-dives (→Explanations), hand-holding (→Tutorial)

## Warnings and Cautions

Include for data loss risk, security implications, production impact, irreversible actions. Place **before** relevant step.

Severity levels: **Note** (informational), **Important** (affects behavior), **Warning** (potential problems), **Danger** (serious consequences)

## Quality Checklist

- [ ] Addresses specific goal, title states what's accomplished, assumes competence
- [ ] Prerequisites brief, steps clear/actionable, options provided where helpful
- [ ] No tutorial teaching/explanations/comprehensive reference (link to other doc types instead)
- [ ] Gets to point quickly, all code tested, professional tone

## Common Mistakes

- **Becomes Tutorial**: Remove pedagogical content, assume competence
- **Becomes Reference**: Show only what's needed, link to full reference
- **Becomes Explanation**: Remove concept explanations, link to explanation docs
- **Too vague**: Provide concrete steps with specific commands/code
- **Only one path**: Acknowledge alternatives, link to variations
- **Missing prerequisites/validation**: State clearly, include verification steps

## Template

```markdown
# [Action] [Object] / How to [Accomplish Goal]

[1-2 sentence description of what this guide accomplishes]

## Prerequisites

- [Required knowledge/skill]
- [Required setup/configuration]
- [Required access/permission]

## When to use this

[Optional: conditions, trade-offs, when to use alternatives]

---

## Steps

### 1. [Action]

[Instructions]

[Code/command]

[Validation or expected result - optional]

### 2. [Action]

[Continue pattern]

---

## Troubleshooting

### [Common Problem]

**Cause**: [Why this happens]

**Solution**: [How to fix it]

---

## Related guides

- [Link to related how-to]
- [Link to alternative approach]

## Reference

- [Link to API reference]
- [Link to configuration reference]

## Further reading

- [Link to explanation doc]
```
