# smn-gpt

`smn-gpt` is a lightweight orchestration layer for salmon data standardization.

It provides a **system prompt**, a **set of reusable skills**, and a **small library of examples/guides** for connecting:

- the [`metasalmon`](https://github.com/dfo-pacific-science/metasalmon) R package
- the [Salmon Data Package specification](https://github.com/dfo-pacific-science/smn-data-pkg)
- the [DFO Salmon Ontology](https://github.com/dfo-pacific-science/dfo-salmon-ontology)
- the shared Salmon Domain Ontology (`smn`)

The point of this repo is not to replace those upstream projects. The point is to make them work together well in an LLM-assisted workflow for salmon biologists, analysts, and data stewards.

## What this repo is for

This repository is a good place to keep the **assistant-facing layer** of the salmon data standardization workflow:

- the core system prompt that defines the assistant's role and output contract
- skills that break recurring tasks into usable patterns
- examples that show what good Salmon Data Package outputs and ontology-aligned mappings look like
- supporting guidance for tidy data, naming, and issue drafting

In other words:

- `metasalmon` does the **deterministic package work**
- the SDP specification defines the **package contract**
- the ontologies define the **semantic targets**
- `smn-gpt` provides the **conversational glue** between them

## Why this layer matters

The package/spec/ontology stack is strong, but users still hit messy judgment calls:

- “What should this column mean?”
- “Is this a measurement, an attribute, or a code list?”
- “Is there already a good ontology term for this?”
- “Is this a real ontology gap, or just a bad local label?”
- “How do I get from raw data to a reviewable package without drowning in metadata?”

That is where an LLM can help — as long as it is tightly constrained by the package specification, ontology guidance, and example outputs.

This repo is the place for that constraint layer.

## Core design stance

The intended design stance for `smn-gpt` is:

- **package-first** rather than ontology-first
- **CSV-first** for standard package outputs
- **human review in the loop** for ambiguous semantics
- **ontology-aware** but not ontology-theatre
- **deterministic where possible** by leaning on `metasalmon`
- **proposal-oriented** rather than silently inventing semantics

The LLM should help users move faster, but it should not become a second unofficial source of truth.

## The two recommended user paths

### 1) MetaSalmon-assisted package workflow (preferred)

This is the preferred path for most real work.

1. The user starts in `metasalmon`.
2. They run `create_sdp()` to generate a review-ready package.
3. They review the output in Excel or R:
   - `metadata/dataset.csv`
   - `metadata/tables.csv`
   - `metadata/column_dictionary.csv`
   - `metadata/codes.csv` (if present)
   - `semantic_suggestions.csv` (if present)
   - `README-review.txt`
4. They bring that package, or selected metadata plus a data sample, into SMN-GPT.
5. SMN-GPT helps with:
   - semantic sanity checks
   - ambiguity triage
   - ontology gap detection
   - proposed term drafting
   - GitHub-ready ontology issue text

This path keeps the package structure anchored in the current R package workflow and uses the assistant mainly for the fuzzy parts.

Relevant `metasalmon` functions include:

- `create_sdp()`
- `infer_dictionary()`
- `suggest_semantics()`
- `apply_semantic_suggestions()`
- `validate_dictionary()`
- `validate_semantics()`
- `detect_semantic_term_gaps()`
- `render_ontology_term_request()`
- `submit_term_request_issues()`

### 2) One-shot dataset standardization workflow

This is the faster, more conversational path.

1. A user uploads a representative dataset sample plus any codebook/method notes.
2. SMN-GPT creates a **minimal first pass** only:
   - `dataset.csv`
   - `tables.csv`
   - `column_dictionary.csv`
   - `codes.csv` when needed
   - `gpt_proposed_terms.csv` when genuine gaps appear
   - explicit assumptions / ambiguities
3. The user reviews and corrects the first pass.
4. SMN-GPT then supports a refinement loop for:
   - better labels and descriptions
   - better ontology mappings
   - better code lists
   - gap triage and issue drafting

This path is useful when someone does **not** start in R, but the deliverable should still converge toward a proper Salmon Data Package workflow rather than an ad hoc one-off artifact.

## How this repo connects the ecosystem

| Component | Role |
| --- | --- |
| `metasalmon` | Deterministic R package for creating, reading, validating, and enriching Salmon Data Packages |
| `smn-data-pkg` | Normative Salmon Data Package specification |
| DFO Salmon Ontology (`gcdfo`) | DFO-specific semantic layer |
| Salmon Domain Ontology (`smn`) | Shared cross-context semantic layer |
| `smn-gpt` | Prompt/skills/examples layer that helps users move between raw data, packages, and ontology-aligned semantics |

## What belongs in this repo

This repo is a good home for:

- the canonical Custom GPT deployment bundle in `custom-gpt-pack/`
- reusable working-repo skill files in `skills/`
- worked package examples in `examples/`
- concise reference docs like:
  - `schema/glossary.md`
  - `naming_conventions.md`
  - `tidy_data_guide.md`
- guidance for drafting ontology term requests
- example outputs that help keep assistant behavior grounded

This repo is **not** the canonical home for:

- the Salmon Data Package specification itself
- the `metasalmon` implementation
- the DFO Salmon Ontology source files
- the Salmon Domain Ontology source files
- production secrets, auth config, or deployment-specific infrastructure state

Those should remain upstream and authoritative in their own repositories.

## Repository contents

### Core assistant assets

- `custom-gpt-pack/` — the canonical offline ChatGPT Custom GPT deployment bundle, including the prompt, numbered knowledge-base files, and upload instructions
- `skills/` — modular working-repo skills for local/dev agent use
- `examples/` — worked examples of package outputs and semantic patterns

### Current example folders

- `examples/canonical-basic/` — minimal package-style example without deep semantics
- `examples/canonical-semantics/` — package example with ontology-aligned fields
- `examples/spsr-reference/` — richer reference material for SPSR-style workflows and issue drafting

### Supporting guides

- `schema/glossary.md` — shared glossary for SDP field meanings
- `naming_conventions.md` — naming rules for data elements and ontology alignment
- `tidy_data_guide.md` — guidance for structuring data into tidy, analysis-ready, ontology-aware forms
- `dependencies.md` — notes on how this repo depends on related projects

## Canonical Custom GPT knowledge-base folder

The canonical upload folder for the ChatGPT Custom GPT knowledge base is:

- `custom-gpt-pack/`

That folder is meant to solve the exact problem you spotted: the numbered knowledge-base files were effectively split across repos, with many of the missing numbered files living in `smn-data-gpt/custom-gpt-packs/` rather than in `smn-gpt` itself.

Use `custom-gpt-pack/README.md` as the upload instructions.

Operationally:

- upload the **20 numbered files** in `custom-gpt-pack/`
- do not rely on the repo root as the upload source
- treat `custom-gpt-pack/` as the deployment-ready knowledge bundle for the current Custom GPT
- treat the root `skills/` folder as the **working-repo / online-or-local-tooling layer**, not as the upload pack
- use `skills/README.md` for the split between offline upload-pack skills and local/dev skills

## Example of the intended connection pattern

A healthy workflow looks like this:

```r
library(metasalmon)
library(readr)

sample_path <- system.file("extdata", "nuseds-fraser-coho-sample.csv", package = "metasalmon")
df <- read_csv(sample_path, show_col_types = FALSE)

pkg_path <- create_sdp(
  df,
  dataset_id = "fraser-coho-2024",
  table_id = "escapement",
  overwrite = TRUE
)
```

Then the user asks the assistant to help with review questions such as:

- Which semantic suggestions look solid vs shaky?
- Which measurement columns still need better `property_iri` / `entity_iri` choices?
- Which fields are true ontology gaps?
- Which proposed terms should become GitHub issues?

That is the sweet spot for this repo.

## Current deployment status

At the moment, this repository is being used to support a deployment on **Brett Johnson's personal paid ChatGPT Custom GPT**.

That is a useful proving ground, but it should not be the end state.

## Future production direction

This repo should eventually be put into production using **DFO infrastructure**.

That future production version should aim for:

- DFO-controlled hosting and governance
- DFO-managed authentication and access patterns
- clearer operational ownership
- stable knowledge synchronization from upstream repositories
- auditable prompt/skill/version changes
- a safer path for institutional use with real datasets and documentation workflows

The materials in this repo should therefore stay as **deployment-portable assets**:

- prompt
- skills
- examples
- reference guidance

That way the same logic can support:

- a ChatGPT Custom GPT today
- an API-backed assistant tomorrow
- a DFO-hosted interface later

## Recommended next steps for the repo

To make this repository more production-ready over time:

1. Keep the prompt and skills aligned with the latest `metasalmon` API, especially the `create_sdp()`-centered workflow.
2. Prefer package-first and CSV-first guidance by default.
3. Treat ontology issue drafting as a downstream review step, not the starting point.
4. Add lightweight checks for dead file references in prompt/skill documents.
5. Keep examples current so they remain usable as grounding material.
6. Separate deployment-specific concerns from reusable assistant assets.

## Summary

`smn-gpt` should be understood as a **good mechanism for connecting**:

- the `metasalmon` R package
- the Salmon Data Package specification
- the DFO Salmon Ontology
- the Salmon Domain Ontology

through a curated combination of:

- system prompt
- reusable skills
- worked examples
- domain-specific guidance

Used well, it can make salmon data standardization faster, more consistent, and easier for real users — while still keeping the package specification and ontology repositories as the actual sources of truth.
