# Root skills vs Custom GPT upload-pack skills

This directory is the **working-repo skills layer**.

It is **not** the canonical ChatGPT Custom GPT upload pack.

## Which version is for what?

### Use `custom-gpt-pack/` for the Custom GPT knowledge base

If you are uploading files into ChatGPT Custom GPT knowledge, use:

- `custom-gpt-pack/01-SYSTEM-PROMPT.md`
- `custom-gpt-pack/04-SKILLS-GUIDE.md`
- `custom-gpt-pack/06-I-ADOPT-PATTERNS.md`
- the rest of the numbered files in `custom-gpt-pack/`

That bundle is designed for an **offline / no-code / no-network** Custom GPT setup.

It assumes:

- no live API access
- no local R session
- no local Python execution
- bundled CSV lookups instead of runtime ontology calls

### Use `skills/` for local or development-time agent work

The files in this `skills/` directory are modular working docs for repo-local use.

They may assume some combination of:

- a local checkout of this repo
- a local R environment with `metasalmon`
- a local Python environment with `salmonpy`
- local helper scripts in this repo
- live network/API access where the skill explicitly says so

These root skills are useful for:

- OpenClaw / local agent work
- repo development
- updating examples, prompts, and helper scripts
- documenting richer workflows than the tighter upload pack can carry cleanly

## Practical rule

- **Custom GPT deployment** → use `custom-gpt-pack/`
- **Local/dev/online agent work** → use `skills/`

## Current intent

The root skills have been kept as modular working files, while the upload pack has been kept as the consolidated offline deployment bundle.

That means some overlap is intentional:

- `custom-gpt-pack/04-SKILLS-GUIDE.md` and `custom-gpt-pack/06-I-ADOPT-PATTERNS.md` are the deployment-safe consolidated versions
- the root `skills/*/*.md` files are the more detailed working-repo versions

## Environment assumptions by root skill

| Skill | Typical assumptions |
| --- | --- |
| `data-package-generation` | local repo context; may reference `salmonpy`/validation helpers |
| `metasalmon-usage` | local R environment with `metasalmon`; may reference live term-search workflows |
| `i-adopt-decomposition` | mainly conceptual, but still part of the working-repo layer |
| `ontology-helpers` | local Python and repo helper scripts |
| `ontology-term-creation` | repo docs + ontology tracker workflow |
| `ontology-term-mapping` | may use local docs plus live/shared ontology guidance |

## Maintenance rule

When the offline upload-pack workflow changes, update:

- `custom-gpt-pack/01-SYSTEM-PROMPT.md`
- `custom-gpt-pack/04-SKILLS-GUIDE.md`
- `custom-gpt-pack/06-I-ADOPT-PATTERNS.md`

When the local/dev/online workflow changes, update the relevant files in `skills/`.
