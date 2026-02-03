# Entrypoints (What Is Actually Used?)

Purpose: keep a short map of what starts the system and where to edit.

Entrypoint means the file you should open first for a given task.

## Canonical entrypoints
Canonical means the single official source.
- SYSTEM-PROMPT.md: the core system prompt (a system prompt is the top-level instruction set for the model).
- skills/*/<skill-folder>.md: task-specific instructions selected by the router, and a router is a rule for choosing the right skill file.
- schema/glossary.md: the shared field glossary, and a glossary is a list of field definitions.
- docs/vocabulary.md: vocabulary/ontology guidance for SDP semantics fields.
- SPECIFICATION.md: the normative spec, and normative means it defines what is valid.
- examples/canonical-basic/* and examples/canonical-semantics/*: reference SDPs (with and without semantics) used for retrieval and validation.

## Vocabulary source
- dfo-salmon.ttl: schema-only vocabulary file (a schema is a list of fields and rules), not data.

## Output contract
- CSV only (CSV is a comma-separated text table).
- codes.csv required only when categorical columns exist (a categorical column stores codes or labels from a fixed list).

## Validator and helpers
- Preferred (R/metasalmon, source of truth):
  - Load ontology: `metasalmon::fetch_salmon_ontology()` (content-negotiated TTL/OWL, cached)
  - Validate semantics + gaps: `metasalmon::validate_semantics(column_dictionary)` (reports missing term/property/unit/entity IRIs)
- Python fallback: `python -m salmonpy.scripts.validate_sdp --dataset dataset.csv --tables tables.csv --dictionary column_dictionary.csv [--codes codes.csv] [--require-semantics]`
- New term helper: `python -m salmonpy.scripts.draft_new_term --label "<label>" --definition "<definition>" --term-type skos_concept --parent-iri <iri>`
- Vocabulary/config preload: `docs/vocabulary.md`, `config/entity_defaults.csv`, `config/vocab_priority.md`
