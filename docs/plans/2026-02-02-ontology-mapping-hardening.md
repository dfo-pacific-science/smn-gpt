# ExecPlan: Semantics Hardening (R-first, smn-gpt-only) — 2026-02-02

## Purpose / Big Picture

Make ontology mapping repeatable and mostly autonomous with minimal tools (smn-gpt + metasalmon + internet), so any salmon dataset (scraped or user-supplied) can be semantically mapped and validated with minimal manual steps. Remove hard-coded heuristics, preserve constraints, and keep vocab/entity preferences synchronized with metasalmon and the DFO Salmon Ontology.

## Context & Constraints

- Minimal toolchain: smn-gpt repo, internet, metasalmon R package; assume salmonpy may be absent.
- Ontology source: https://dfo-pacific-science.github.io/dfo-salmon-ontology/ (content negotiation).
- Skills: prefer ~/.claude/skills; keep smn-gpt skills authoritative/editable.
- Datasets may be scraped or user-supplied; schema unknown a priori.
- Base branch defaults to `main` (confirm per repo).

## Plan of Work (what to edit/create)

1. **Config files (smn-gpt/config/)**
   - `entity_defaults.csv`: table prefix → default entity IRI (+ notes for overrides).
   - `vocab_priority.md`: ordered list (DFO Salmon → DwC → QUDT → NCIT → NCBITaxon → others) used by skills and R helper.
2. **Skill updates (smn-gpt/skills/)**
   - ontology-term-mapping: add R snippet loading vocab_priority + entity_defaults; show suggest_semantics call; show placeholder constraint IRIs; reference content-negotiated TTL fetch helper.
   - i-adopt-decomposition: add R snippet to build pattern table (grouping by regex for age/location/rate) and emit constraint placeholders when IRIs missing.
   - ontology-term-creation: add inline issue-text template for in-chat drafting (no local scripts).
   - ontology-helpers: add “no-python” R workflow for missing-IRI detection + validation loop using metasalmon::validate_dictionary; checklist for required fields and constraints.
3. **R helper scripts**
   - `skills/ontology-helpers/scripts/r/validate_semantics.R`: read column_dictionary (CSV or clipboard), run metasalmon::validate_dictionary and suggest_semantics, report missing term/property/unit/entity, emit skeleton gpt_proposed_terms.csv with constraint placeholders.
   - `skills/ontology-helpers/scripts/r/fetch_dfo_salmon_ttl.R`: fetch ontology via content negotiation from the GitHub Pages URL; save to temp path; return path/loaded graph.
4. **metasalmon enhancement**
   - Add an R helper function (e.g., `fetch_salmon_ontology()`) that calls the same content-negotiated URL, caches by ETag/Last-Modified, and returns a parsed ontology object (or file path).
   - Add an optional argument to `suggest_semantics()`/related helpers to accept custom vocab priority and entity defaults (read from config if provided).
5. **Operational guardrails (docs)**
   - Update SYSTEM-PROMPT.md (or relevant skill sections) to: always record constraint placeholders; run validation after every mapping pass; note ontology version/commit hash when fetched remotely.
6. **Testing/Validation**
   - R: run validate_semantics.R against a small sample dictionary to confirm missing-IRI report and proposed-terms output.
   - metasalmon: run existing tests or a focused script to ensure fetch helper works and suggestions still run.
7. **Docs & wiring**
   - Update `docs/entrypoints.md` (if present in smn-gpt) with new R helper locations.
   - Add usage examples in the relevant skill files.

## Concrete Steps (command-ready; run inside smn-gpt unless noted)

1. `cd ~/code/smn-gpt`
2. `mkdir -p config skills/ontology-helpers/scripts/r`
3. Create `config/entity_defaults.csv` with columns: table_prefix, entity_iri, notes.
4. Create `config/vocab_priority.md` listing vocab order + rationale.
5. Edit skill files as in Plan of Work step 2 (use apply_patch).
6. Add `validate_semantics.R`:
   - read column_dictionary (file or stdin/clipboard),
   - load entity_defaults + vocab_priority,
   - run metasalmon::suggest_semantics / validate_dictionary,
   - emit missing-IRI report and gpt_proposed_terms.csv.
7. Add `fetch_dfo_salmon_ttl.R`:
   - GET with `Accept: application/rdf+xml` (fallback turtle),
   - save to temp, return path; optionally parse with rdflib.
8. metasalmon: add/confirm built-in helpers (source of truth), then keep skill scripts thin:
   - `fetch_salmon_ontology()` with content negotiation + caching (ETag/Last-Modified).
   - Validation helper that ensures `required` column, reports missing term_iri instead of truncating, and can read optional `entity_defaults`/`vocab_priority`.
   - Allow suggest_semantics/validators to accept config-driven vocab/entity defaults.
   - Skills should call these metasalmon helpers rather than re-implement logic.
9. Update SYSTEM-PROMPT.md and skills with guardrails on constraint placeholders and per-pass validation.
10. Update `docs/entrypoints.md` (if applicable) to point to new R helpers.

## Risks & Mitigations

- **Ontology drift**: record fetched ontology URL + Date + ETag in outputs; prefer bundled TTL when available.
- **Constraint loss**: require placeholder constraint_iri strings when age/location parsed but IRI missing.
- **Permission limits**: metasalmon changes may need separate PR; scope accordingly.

## Progress Tracker (fill as work proceeds)

- [x] Config files added (`entity_defaults.csv`, `vocab_priority.md`)
- [x] Skill files updated (ontology-term-mapping, i-adopt-decomposition, ontology-helpers; ontology-term-creation unchanged)
- [x] R helpers added (`validate_semantics.R`, `fetch_dfo_salmon_ttl.R`)
- [ ] SYSTEM-PROMPT guardrails updated
 - [x] metasalmon helpers added (fetch_salmon_ontology, validate_semantics); tests pending
- [ ] entrypoints/docs updated

## New findings (generalized learnings)

- Add write safety in R helpers: verify expected headers/row counts before saving column_dictionary; abort on mismatch to avoid truncation.
- metasalmon validation requirements: ensure `required` column exists; report missing term_iri for measurements separately so runs don’t die mid-stream.
- Assume salmonpy may be absent; R helper must be first-class validator and work without data payloads.
- Pin known terms (e.g., ExploitationRate/TotalExploitationRate) to avoid re-proposing established concepts.
- Provide gh issue Markdown templates to prevent escaped-newline formatting problems.

## Validation & Acceptance

- R helper reports missing IRIs and generates gpt_proposed_terms.csv with constraint placeholders.
- Skill files contain R examples using vocab/entity configs and content-negotiated ontology fetch.
- Constraint placeholders present wherever qualifiers exist without IRIs.
- metasalmon helper (if added) fetches ontology successfully via content negotiation and does not break existing tests.

## Idempotence & Recovery

- Scripts read config files if present; safe to rerun.
- Remote fetch helper caches by ETag/Last-Modified when supported; falls back gracefully if offline.
- If metasalmon changes are deferred, smn-gpt instructions still provide the workflow using existing metasalmon APIs.
