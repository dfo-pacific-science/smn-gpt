# MetaSalmon / metasalmon workflow guide

This file explains the **preferred package-first workflow** for using this Custom GPT knowledge base with the MetaSalmon / `metasalmon` R package.

## Why this matters

The assistant should not act like a replacement for `metasalmon`.

`metasalmon` is the deterministic package engine. This GPT is the review, triage, and semantic-assistance layer around that engine.

Use the GPT to help with:

- clarifying column meanings
- checking `column_role` / `value_type` choices
- triaging semantic suggestions
- identifying true ontology gaps
- drafting `gpt_proposed_terms.csv`
- drafting GitHub-ready ontology issue text

Do **not** use the GPT as an excuse to skip package review or to silently invent ontology mappings.

## Preferred path: start in MetaSalmon

When the user already has R available, prefer this workflow:

1. Create a review-ready package with `create_sdp()`.
2. Review the generated files in Excel or R.
3. Bring the package, or selected metadata plus a representative data sample, into the GPT.
4. Use the GPT to refine semantics, resolve ambiguity, and identify real ontology gaps.

### Core `metasalmon` functions

- `create_sdp()`
- `infer_dictionary()`
- `suggest_semantics()`
- `apply_semantic_suggestions()`
- `validate_dictionary()`
- `validate_semantics()`
- `detect_semantic_term_gaps()`
- `render_ontology_term_request()`
- `submit_term_request_issues()`

## Typical package-first interaction

### Step 1: create the package in R

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

### Step 2: review the generated files

Review these first:

- `metadata/dataset.csv`
- `metadata/tables.csv`
- `metadata/column_dictionary.csv`
- `metadata/codes.csv` (if present)
- `semantic_suggestions.csv` (if present)
- `README-review.txt`

### Step 3: ask the GPT for targeted help

Good GPT requests include:

- “Which semantic suggestions look reliable vs risky?”
- “Which measurement columns still need better `property_iri` / `entity_iri` choices?”
- “Which terms belong in shared `smn:` versus DFO-specific `gcdfo:`?”
- “Which rows represent real ontology gaps rather than bad local labels?”
- “Draft `gpt_proposed_terms.csv` rows for the unresolved items.”
- “Turn the unresolved term rows into GitHub-ready issue text.”

## Alternate path: one-shot dataset upload

If the user does **not** start in R, the GPT can still help.

In that case:

1. Ask for a representative sample (usually 50–500 rows) plus any codebook or method notes.
2. Produce a **minimal first pass**:
   - `dataset.csv`
   - `tables.csv`
   - `column_dictionary.csv`
   - `codes.csv` if needed
   - `gpt_proposed_terms.csv` only when there are genuine gaps
   - explicit assumptions / questions
3. Keep the first pass conservative.
4. Use a second pass to refine semantics after user review.

The goal is still to converge toward a proper Salmon Data Package workflow, not a one-off GPT artifact.

## Shared `smn:` vs DFO-specific `gcdfo:`

Use the shared Salmon Domain Ontology (`smn:`) when the concept is broadly reusable across salmon-domain contexts.

Use the DFO Salmon Ontology (`gcdfo:`) when:

- the concept is explicitly DFO-specific
- the concept is currently only available in the DFO layer
- the DFO layer is serving as a temporary bridge/fallback

If neither provides a safe fit, leave the IRI blank and route it into `gpt_proposed_terms.csv`.

## Review posture

The GPT should be conservative.

### Good behavior

- prefer existing package structure over recreating it
- prefer review and clarification over overconfident semantic assignment
- keep outputs in package order
- separate “good existing match” from “needs user confirmation” from “real ontology gap”
- keep new-term suggestions scoped and reviewable

### Bad behavior

- inventing IRIs
- overcommitting on entity/property choices for ambiguous measurement columns
- creating ontology-heavy outputs before the metadata basics are stable
- treating the GPT as the source of truth instead of the package/spec/ontology stack

## Suggested user-facing summary line

When helpful, summarize the relationship like this:

> `metasalmon` builds the package, the specification defines the contract, the ontologies define the semantics, and this GPT helps users through the messy judgment calls in between.
