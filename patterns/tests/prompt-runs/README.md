# Saved prompt runs for the pattern docs

These are the answers behind the "How these prompts were checked" paragraph at the end of each doc in `patterns/`.

**How they were produced.** On 2026-10-01 each of the nine "Prompt for your AI model" prompts was run through the Claude Code command line (`claude -p`, version 2.1.287) with no tools, no project instructions and automatic memory turned off, once on `sonnet` and once on `haiku`. The doc's text was pasted where the prompt says `[PASTE FILE]`, and the other bracketed inputs were replaced with made-up samples. Each saved file shows the prompt that was sent, then the answer. The script that does this is `../run_prompts.py`. It needs the `claude` tool, so the normal test suite does not run it.

**How they were graded.** A Claude model (Sonnet 5.5, working under my direction) read each answer against that prompt's own "A good answer ..." sentence, which was written before the run. One run per prompt per model, so a Pass here means "this run met the sentence", not "this prompt always does". I have not re-read every answer myself.

File names are `<doc>-<teach|review|adapt>-<model>.md`.

| Doc and prompt | Sonnet | Haiku |
|---|---|---|
| block-and-tell-hooks, understand and teach | Pass | Pass |
| block-and-tell-hooks, review against your setup | Pass | Partial. It said the exit-code claims did not need checking for my tool, which the prompt asks it to question. |
| block-and-tell-hooks, adapt and test | Pass | Partial. The settings entry has the right shape and watches both Edit and Write. The guard only matches the relative path `migrations/*`, so an absolute file path would slip past it. |
| rules-index-architecture, understand and teach | Pass | Pass |
| rules-index-architecture, review against your setup | Pass | Partial. It flagged one claim to check and no others, and gave a made-up saving of "15 to 20 percent". |
| rules-index-architecture, adapt and test | Pass | Partial. It proposed splitting a file of about 15 lines without saying the doc's "when not to" section applies, and its before and after measurements did not cover the same files. |
| typed-memory-system, understand and teach | Pass | Partial. It never explained why compaction keeps topic files. |
| typed-memory-system, review against your setup | Pass | Partial. It listed gaps it could not see from a file listing (frontmatter, index grouping). |
| typed-memory-system, adapt and test | Pass | Partial. The size script uses a variable it never sets, and its test expects exit code 1 from a branch that exits 0. |

Sonnet met the sentence on all nine. Haiku met it on two and only partly on seven. Those Haiku misses are the reason the docs say "check what it gives you" and do not say the prompts are reliable on a small model.

## What the first attempt taught

- **A first set of 18 runs was thrown away.** The runs picked up Claude Code's automatic memory instructions: one Sonnet answer tried to call a file tool and returned nothing usable, and a Haiku answer put a scratch path in its script. I turned automatic memory off (`CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`) and ran all 18 again. Only the second set is saved.
- **The hook registration.** Before the settings example was added to `block-and-tell-hooks.md`, a reviewer's Haiku run of the "adapt and test" prompt invented the registration (`"matcher": ["Edit"]` with an `"event"` key, which is not Claude Code's shape) and guarded only `Edit`. After the example was added, both models in these saved runs wrote the correct shape and watched both `Edit` and `Write`.
