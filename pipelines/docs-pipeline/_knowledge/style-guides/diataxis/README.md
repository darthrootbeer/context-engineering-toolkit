# Diataxis Documentation Framework

Diataxis organizes technical documentation around four distinct user needs. Each type serves a different purpose and must remain structurally distinct.

Source: <https://diataxis.fr/>

## Four Documentation Types

| Type | Orientation | Purpose |
|------|-------------|---------|
| **Tutorial** | Learning + Doing | Teach skills through guided, hands-on instruction |
| **How-to guide** | Working + Doing | Goal-driven directions for accomplishing real-world work |
| **Reference** | Working + Thinking | Accurate, complete technical facts for quick lookup |
| **Explanation** | Learning + Thinking | Context, background, and reasoning behind concepts |

## Classification Decision Tree

1. Is the user **learning** or **working**? Learning = Tutorial or Explanation. Working = How-to or Reference.
2. Is the user **doing** or **thinking**? Doing + Learning = Tutorial. Thinking + Learning = Explanation. Doing + Working = How-to. Thinking + Working = Reference.
3. Validate: content stays within the chosen type's boundaries.

## Boundary Integrity

Maintain strict separation between types. Common violations:

- **Tutorial → How-to**: Skipping explanations, assuming knowledge, prioritizing efficiency over learning
- **How-to → Explanation**: Adding conceptual content beyond task context
- **How-to → Tutorial**: Teaching basics instead of assuming competence
- **Reference → How-to**: Including procedural steps or setup instructions
- **Reference → Explanation**: Explaining design decisions or reasoning
- **Explanation → How-to**: Prescribing specific actions

## The Product Guide Sets

Every multi-doc guide includes a **guide set overview** (not a Diataxis type) as the entry point, plus the relevant typed docs:

1. **Guide set overview** (`index.md`). Navigation layer: scope, audience, prerequisites, links to all docs.
2. **Explanation**. Conceptual background.
3. **How-to**. Step-by-step implementation.
4. **Reference**. Complete specifications.
5. **Tutorial** (optional). Hands-on learning.

See `style-guide_guide-set-overview.md` for full rules on writing the overview.

## Style Guides

- **style-guide_guide-set-overview.md** - Entry point that sits above a guide set: scope, audience, prerequisites, and links to all docs. Not a Diataxis type — the navigation layer.
- **style-guide_diataxis-type_tutorials.md** - Learning-oriented guides for building competence through practice
- **style-guide_diataxis-type_how-to-guides.md** - Task-oriented directions for solving real-world problems
- **style-guide_diataxis-type_reference.md** - Information-oriented technical specifications for quick lookup
- **style-guide_diataxis-type_explanation.md** - Understanding-oriented content explaining why and how things work
- **style-guide_read-next.md** - Cross-cutting standard: every article ends with a Read next section linking to 3–6 related docs with one-sentence descriptions

## Slash Commands

### Audit Command

- **/audit-diataxis [file-path]** - Analyze existing documentation to identify content types, detect boundary violations, and recommend restructuring into proper Diataxis categories

### Format Application Commands

- **/apply-diataxis-overview-format [file-path]** - Create or reformat a guide set overview document: scope, audience, prerequisites, and linked doc list
- **/apply-diataxis-tutorial-format [file-path]** - Transform content into hands-on learning tutorial with clear outcomes, prerequisites, and step-by-step guidance for beginners
- **/apply-diataxis-how-to-format [file-path]** - Convert content into goal-oriented instructions for competent users solving specific real-world problems
- **/apply-diataxis-reference-format [file-path]** - Restructure content into exhaustive technical specifications with neutral tone and complete parameter documentation
- **/apply-diataxis-explanation-format [file-path]** - Reformat content to explain concepts, rationale, and design decisions without prescribing actions
