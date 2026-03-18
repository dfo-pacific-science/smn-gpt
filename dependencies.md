# Cross-repo Dependencies

## At-a-glance graph (source → depends on)

- `smn-data-pkg` → canonical Salmon Data Package specification consumed by `metasalmon`, `salmonpy`, and `smn-gpt`.
- `dfo-salmon-ontology` → ontology term source for `metasalmon`, `salmonpy`, and `smn-gpt`.
- `salmon-domain-ontology` → shared `smn:` term source used by `smn-gpt` Custom GPT packs and cross-context semantic guidance.
- `metasalmon` ↔ `salmonpy` → Python mirror relationship; function/API changes should stay aligned.
- `smn-gpt` → assistant/prompt/skills/deployment layer connecting `metasalmon`, the SDP spec, and ontology assets.
- `smn-data-gpt` → **legacy source of migrated Custom GPT pack assets only**; no longer the preferred home for active `smn-gpt` deployment materials.
- `data-stewardship-unit` → **historical/optional only** for this stack right now; term-table sync should be ignored unless that integration is revived.

## Current reality checks

- `dfo-pacific-science/salmonpy` now exists as the DFO Pacific Science org copy.
- Local sibling clone now exists at `../salmonpy`, which matches the `metasalmon` parity-work expectation.
- The canonical ChatGPT Custom GPT upload bundle now lives in `custom-gpt-pack/`.
- Do **not** assume DSU term-table sync is part of the active dependency path for `smn-gpt` right now.
- For ontology term lookup/discovery, prefer the ontology’s WIDOCO/content-negotiation terms and the curated extracted CSVs used in the upload pack.

## Per-repo notes and manual prompts

### smn-data-pkg

- Canonical Salmon Data Package spec.
- Upstream source of truth for the SDP contract consumed by `metasalmon`, `salmonpy`, and `smn-gpt`.
- **Manual prompts when spec changes:**
  - update `metasalmon` schemas/validation and examples
  - update `salmonpy` schemas/validation and examples
  - refresh `custom-gpt-pack/02-SPECIFICATION.md`
  - refresh any examples or guidance in `smn-gpt` that assume older file layouts or field rules

### metasalmon

- Canonical R package workflow for package-first Salmon Data Package creation and semantic review.
- Uses the SDP spec plus ontology/vocabulary guidance.
- The `metasalmon` vignette `gpt-collaboration.Rmd` still treats `smn-gpt` as the assistant-facing guidance layer, so drift here matters.
- The `metasalmon` repo's `AGENTS.md` expects sibling parity work against `../salmonpy`.
- **Manual prompts when metasalmon changes:**
  - port equivalent changes to `salmonpy`
  - re-run parity checks where relevant
  - update `custom-gpt-pack/20-metasalmon-workflow.md`
  - update any `smn-gpt` prompt/skill text that references older APIs or older workflow assumptions

### salmonpy

- Python mirror of `metasalmon`.
- DFO org copy: `https://github.com/dfo-pacific-science/salmonpy`
- Legacy/personal source repo still exists at `https://github.com/Br-Johnson/salmonpy`; use the DFO org repo for ongoing institutional coordination.
- Local sibling checkout path: `../salmonpy`
- **Manual prompts when salmonpy changes:**
  - keep parity notes aligned with `metasalmon`
  - update `smn-gpt` guidance if Python helper names, CLI entrypoints, or workflow steps change
  - prefer pointing users to current package-first workflows rather than stale Python helper examples embedded in old skill docs

### dfo-salmon-ontology

- Upstream source for DFO-specific ontology terms (`gcdfo:`).
- `smn-gpt` should treat ontology term access as coming from the ontology itself (including WIDOCO/content negotiation) plus curated extracted CSVs for Custom GPT upload packs.
- **Current non-dependency:** DSU term-table sync is not required for `smn-gpt` right now.
- **Manual prompts when ontology changes:**
  - refresh any curated extracted term CSVs used by `custom-gpt-pack/07-dfo-salmon-terms.csv`
  - refresh issue-template guidance if tracker flows change
  - update vocabulary guidance when `gcdfo:` vs `smn:` boundaries change

### salmon-domain-ontology

- Shared `smn:` term source for cross-context salmon-domain semantics.
- Primary impact on `smn-gpt` is the shared-layer lookup pack used for Custom GPT knowledge uploads.
- **Manual prompts when ontology changes:**
  - refresh `custom-gpt-pack/19-salmon-domain-terms.csv`
  - update vocabulary guidance where shared-layer precedence or namespace normalization changes

### smn-gpt

- Assistant/prompt/skills layer, not the canonical home of the spec or the ontologies.
- The canonical ChatGPT Custom GPT knowledge-base folder is now:
  - `custom-gpt-pack/`
- Numbered upload files were migrated from `smn-data-gpt/custom-gpt-packs/*` and should now be maintained here.
- Root repo docs may still exist for human-oriented working notes, but deployment-ready knowledge uploads should come from `custom-gpt-pack/`.
- Root `skills/` files are the working-repo/local-agent layer; `custom-gpt-pack/04-SKILLS-GUIDE.md` and `custom-gpt-pack/06-I-ADOPT-PATTERNS.md` are the offline deployment-safe skill equivalents.
- **Manual prompts when upstreams change:**
  - if the SDP spec changes, refresh `custom-gpt-pack/02-SPECIFICATION.md`
  - if `metasalmon` workflow changes, refresh `custom-gpt-pack/20-metasalmon-workflow.md` and any prompt/skill files that encode the flow
  - if ontology terms change, refresh `07-dfo-salmon-terms.csv` and/or `19-salmon-domain-terms.csv`
  - if issue template or validation expectations change, refresh `17-github-issue-templates.md` and `18-validation-checklist.md`
  - avoid relying on stale assumptions about root-level copies of spec/TTL/docs that are not actually present in the repo

### smn-data-gpt

- Historical/legacy repo that previously held a number of the numbered Custom GPT pack files.
- It was the source for migrated assets now staged in `custom-gpt-pack/`.
- **Operational rule:** future `smn-gpt` Custom GPT pack maintenance should happen in `smn-gpt`, not be split across both repos.

### data-stewardship-unit

- Treat as historical/optional for this dependency map right now.
- The previously documented ontology-term-table sync path should be ignored unless DSU becomes an active downstream again.
- Do not model `smn-gpt` maintenance as depending on DSU term tables.

## Practical maintenance checklist

When something changes upstream, ask:

1. Did the SDP contract change?
   - Update `metasalmon`, `salmonpy`, and `custom-gpt-pack/02-SPECIFICATION.md`.
2. Did the package-first workflow change?
   - Update `custom-gpt-pack/20-metasalmon-workflow.md` and any prompt/skill guidance.
3. Did ontology terms or ontology boundaries change?
   - Refresh `07-dfo-salmon-terms.csv`, `19-salmon-domain-terms.csv`, and vocabulary guidance.
4. Did the Custom GPT upload contract change?
   - Update the numbered files in `custom-gpt-pack/` and its `README.md`.
5. Is a dependency only historical noise now?
   - Remove or downgrade it rather than keeping drift-prone pseudo-dependencies alive.
