<!-- FICTIONAL EXAMPLE DATA. Not a real person. Saved by tests/prompt-runs/run_prompts.py -->
# Prompt run: Find gaps in my central file, on haiku

- Prompt file: `prompts/05-find-gaps.txt`
- Date: 2026-10-01. Model alias `haiku`, which ran as `claude-haiku-4-5-20251001` (Claude Code can add a small helper model call of its own).
- Turns: 1. Cost: $0.05 (the simulated user's calls are not included).
- Grade: see `GRADES.md`.

## Conversation

### User

[the prompt below, with attached files: ARCHITECTURE.md, section 'What the validator checks', fixtures/gappy-profile.yaml]

I'm attaching the 'What the validator checks' section of ARCHITECTURE.md and my career-profile.yaml. The validator checks shape and consistency, not truth, so find what it cannot catch. Read my whole file the way a skeptical hiring manager and a careful editor would: look for places where the file claims more than its own evidence shows, says something that conflicts with another part of the file, or would make a posting score in a misleading way. Check every section, not only skills. For each weak spot, give the exact YAML path, quote the part that worries you, say why it matters for scoring, and give one question you would ask me to fix it. Do not fill any gap yourself, and do not report a problem you cannot point to in the file. A good answer names only things that are really in the file and gives a YAML path for each one.

### Model

# Gaps a careful reader should find

I'm finding five real problems, each grounded in what's actually written:

---

## 1. **Contradictory requirement in tech-writing lane**

**YAML path:** `lanes[1].requirements[1]`

**Quote:** 
```yaml
- id: owns_pipeline
  label: "🛠️ Owns the docs build"
  severity: strong
  why: "The point of the role is building, not only writing."
```

**Why it matters for scoring:** The lane itself is described as *"Roles writing and editing technical content,"* yet it requires—at strong severity—that the role be about *building, not only writing.* A scoring system will penalize pure writing roles that don't own docs infrastructure, even though they fit the lane's stated purpose. This contradicts what the lane claims to target.

**Question:** For roles that focus primarily on writing and editing content, do you really need them to own the docs build, or should that be a strong requirement only for the docs-platform lane?

---

## 2. **High skill score with thin, unchecked evidence**

**YAML path:** `skills[1]` (docs_ci)

**Quote:**
```yaml
- id: docs_ci
  label: Docs build and CI checks
  self_score: 5
  ...
  evidence_ids: [ev-placeholder-docs-ci]
```

**Evidence details:** This single evidence spans only **2023-05 to 2023-06** (two months), sourced from an **unchecked interview**, with no document link or secondary verification.

**Why it matters for scoring:** A score of 5 (expert) typically signals deep, demonstrated mastery. Two months of work mentioned in an interview is insufficient to support expert-level scoring in most hiring contexts. A hiring manager would reasonably expect multiple projects, production evidence, or a documented body of work.

**Question:** Beyond that 2023 project, what other docs build or CI systems have you set up or maintained?

---

## 3. **Authorship mischaracterization inflates platform claims**

**YAML path:** `evidence[1].authorship`

**Quote:**
```yaml
- id: ev-placeholder-docs-ci
  claim: "Set up a build check that blocks a docs change with a broken link."
  authorship: WROTE
  source: {type: interview, ...}
```

**Why it matters for scoring:** Setting up a CI/build-check system is platform or infrastructure work, not writing. Marking it as "WROTE" implies authorship of written content, not implementation of technical systems. This conflates different skill domains and makes Robin's platform engineering background appear stronger than a technical writer setting up CI tooling might justify.

**Question:** Did you write the code or configuration that implements this check, or did you spec/design it and have an engineer implement it?

---

## 4. **Writing sample does not match evidence**

**YAML path:** `writing_samples[0]`

**Quote:**
```yaml
- id: ws-api-guide
  title: "API getting-started guide"
  link: "https://example.com/fictional/getting-started"
  evidence_id: ev-northwind-api-rebuild
```

**The evidence (ev-northwind-api-rebuild) claims:** *"Moved the API reference from hand-edited pages to pages generated from the API spec."*

**Why it matters for scoring:** The sample title promises a guide (writing), but the evidence describes tooling and automation (not writing). A hiring manager clicking the link expects to see Robin's writing work, not an automation project. This mismatch makes the portfolio appear misleading.

**Question:** Did you write the API getting-started guide yourself, or is the link actually to the auto-generated reference documentation?

---

## 5. **Platform engineer role aspiration vs. actual titles**

**YAML path:** `person.target_roles[1]` + `employers[*].title`

**Quote:**
```yaml
target_roles: [Senior Technical Writer, "Docs Platform Engineer"]
```
vs. actual titles:
```yaml
employers:
  - title: "Technical Writer"      # 2017–2021
  - title: "Senior Technical Writer"  # 2022–present
```

**Why it matters for scoring:** Robin targets "Docs Platform Engineer" but has held only writer titles. While the evidence suggests platform work within those roles, the lack of an actual platform engineer title—combined with scores of 5 in docs_ci—could read as role inflation. A hiring manager evaluating for a platform engineer role might ask whether Robin has been trusted with that title, or only did platform tasks as a side project.

**Question:** Have you held any position officially titled "Platform Engineer," "Infrastructure Engineer," or "Systems Engineer," or has your platform work all occurred within technical writing roles?
