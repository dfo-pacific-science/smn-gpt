---
name: ontology-helpers
description: Helper scripts and guidance for ontology term mapping: detecting missing IRIs, drafting issue URLs, and checking categorical codes.
---

# Ontology Helpers

Use this skill when:
- You need to find missing semantics in column_dictionary/codes (measurement or categorical columns).
- You need to draft a GitHub issue URL or Markdown for new terms.
- You want to check categorical columns for codes coverage.

## Scripts (run from repo root)
- Detect missing IRIs and draft gpt_proposed_terms skeleton:
  `python smn-gpt/skills/ontology-helpers/scripts/detect_missing_iris.py --dictionary path/to/column_dictionary.csv --output gpt_proposed_terms.csv`
- Draft new-term issue Markdown/URL:
  `python smn-gpt/skills/ontology-helpers/scripts/draft_issue_url.py --label "escapement count" --definition "Count..." --term-type skos_concept --parent-iri <iri>`
- Check categorical codes coverage:
  `python smn-gpt/skills/ontology-helpers/scripts/check_codes_vs_dictionary.py --dictionary column_dictionary.csv --codes codes.csv`

## When to run
- After drafting/receiving column_dictionary.csv (with or without codes.csv) to find gaps.
- Before proposing new terms to populate gpt_proposed_terms.csv and craft issue text.
- Before final delivery to ensure categorical columns align with codes.csv.

## Output rules
- Keep SDP output order: dataset.csv, tables.csv, column_dictionary.csv, codes.csv.
- Never invent IRIs; leave blank and propose new terms via the issue helper if needed.

## Post-generation validation checklist

Run through this checklist after generating column_dictionary.csv and before delivering to the user:

### Measurement column completeness
- [ ] All `column_role=measurement` columns have `unit_iri` populated
- [ ] All `column_role=measurement` columns have `property_iri` populated
- [ ] All `column_role=measurement` columns have `entity_iri` populated
- [ ] `term_iri` is populated OR documented in gpt_proposed_terms.csv

### Constraint handling
- [ ] Multiple constraints use `;` separator (e.g., `<age_3_IRI>;<mainstem_location_IRI>`)
- [ ] All placeholder IRIs (e.g., `<age_3_IRI>`) are documented in gpt_proposed_terms.csv or `skills/i-adopt-decomposition/i-adopt-decomposition.md`
- [ ] Constraint patterns are consistent across similar columns (e.g., all age-stratified columns follow same pattern)

### Categorical column coverage
- [ ] All `column_role=categorical` columns have entries in codes.csv
- [ ] codes.csv includes `term_iri` where ontology mappings exist
- [ ] codes.csv `code_value` matches actual data values

### Term type consistency
- [ ] `term_type` matches the source of `term_iri`:
  - `skos_concept` for SKOS vocabularies and compound variables
  - `owl_class` for OWL classes (StockManagementUnit, ConservationUnit, Population, etc.)
  - `owl_object_property` for OWL properties
- [ ] No punning (same IRI used as both owl_class and skos_concept)

### Cross-file integrity
- [ ] All `table_id` values in column_dictionary.csv exist in tables.csv
- [ ] All `dataset_id` values match across all files
- [ ] Primary keys listed in tables.csv exist as columns in column_dictionary.csv

### Entity selection consistency
- [ ] SMU-level tables use `entity_iri = https://w3id.org/gcdfo/salmon#StockManagementUnit`
- [ ] CU-level tables use `entity_iri = https://w3id.org/gcdfo/salmon#ConservationUnit`
- [ ] Population-level tables use `entity_iri = https://w3id.org/gcdfo/salmon#Stock` (until a population class exists in `dfo-salmon.ttl`)
- [ ] Individual fish observations use `entity_iri = http://rs.tdwg.org/dwc/terms/Organism`
- [ ] User confirmed entity selections via pattern-based confirmation workflow (see i-adopt-decomposition.md)

### Proposed terms documentation
- [ ] gpt_proposed_terms.csv includes all terms where `term_iri` was left blank
- [ ] Each proposed term has: term_label, term_definition, term_type, suggested_parent_iri
- [ ] definition_source_url is provided where available (not fabricated)

---

## Entity Selection Rules (Detailed)

Entity selection is critical for I-ADOPT decomposition. Use these rules to determine the correct `entity_iri`.

### Table context defaults

| Table Prefix | Default Entity | IRI | Rationale |
|--------------|----------------|-----|-----------|
| `smu_*` | StockManagementUnit | `https://w3id.org/gcdfo/salmon#StockManagementUnit` | Stock Management Unit data describes SMU-level aggregations |
| `cu_*` | ConservationUnit | `https://w3id.org/gcdfo/salmon#ConservationUnit` | Conservation Unit data describes CU-level metrics |
| `pop_*` | Stock (fallback) | `https://w3id.org/gcdfo/salmon#Stock` | Use until a population class exists in `dfo-salmon.ttl` |
| `indicator_*` | Stock (fallback) | `https://w3id.org/gcdfo/salmon#Stock` | Use until a population class exists in `dfo-salmon.ttl` |
| `pfma_*` | Stock (catch constrained by area) | `https://w3id.org/gcdfo/salmon#Stock` | Prefer a PFMA constraint concept; propose a class if needed |

### Column name overrides

Even within a table, column names may indicate a different entity:

| Column Pattern | Override Entity | Example |
|----------------|-----------------|---------|
| Contains `CU_` | ConservationUnit | `CU_ABUNDANCE` in smu_timeseries |
| Contains `SMU_` | StockManagementUnit | `SMU_TOTAL` in cu_year |
| Contains `INDIVIDUAL` or describes single fish | dwc:Organism | `INDIVIDUAL_LENGTH` |
| Contains `SPAWNER` as subject (not modifier) | Stock (+ spawner constraint) | `SPAWNER_BIOMASS` (entity defaults to stock; constrain to spawners/lifestage) |
| Contains `CATCH` as subject | Stock (+ catch/harvest constraint) | `CATCH_COUNT` (entity defaults to stock; constrain to catch context) |
| Contains `HABITAT` or `REACH` | Ask user (often ENVO) | `REACH_COVERAGE` |

### Decision tree for entity selection

```
1. Is the column about individual fish observations?
   YES → entity = dwc:Organism
   NO → continue

2. Does the column name explicitly reference CU?
   YES → entity = ConservationUnit
   NO → continue

3. Does the column measure spawning adults specifically?
   YES → entity = gcdfo:Stock (and add a spawner/lifestage constraint)
   NO → continue

4. Does the column measure catch events?
   YES → entity = gcdfo:Stock (and add a catch/harvest constraint)
   NO → continue

5. Use table context default (see table above)
```

### Ambiguous cases requiring user confirmation

Always ask the user when:
- Column name suggests one entity but table context suggests another
- Reference points (LRP, USR) appear in multiple table types
- Survival/mortality metrics (could be SMU/CU/Stock or individual fish)
- Benchmark columns (could be SMU-level, CU-level, or Stock-level)

See **i-adopt-decomposition.md → User Confirmation Workflow** for the pattern-based approach to resolving ambiguities.

---

## Property Selection Rules (Detailed)

### Unit-to-property mapping

| Unit Pattern | Default Property | Property IRI |
|--------------|------------------|--------------|
| NUM, count, individuals | count | `http://qudt.org/vocab/quantitykind/Count` |
| UNITLESS, ratio, proportion | ratio/proportion | `http://qudt.org/vocab/quantitykind/DimensionlessRatio` |
| cm, mm, m | length | `http://qudt.org/vocab/quantitykind/Length` |
| g, kg | mass | `http://qudt.org/vocab/quantitykind/Mass` |
| per day, per hour | rate-like (non-unitless) | *(pick closest QUDT quantity kind or propose a term)* |

### Column name-to-property mapping

| Column Contains | Property | Notes |
|-----------------|----------|-------|
| `_RATE`, `MORTALITY`, `EXPLOITATION`, `SURVIVAL` | rate | Even if units not specified |
| `_COUNT`, `TOTAL_`, `SPAWNERS`, `RECRUITS` | count | Abundance measurements |
| `_INDEX` | ratio or rate | Depends on definition |
| `LRP`, `USR`, `BENCHMARK`, `REFERENCE` | threshold | Reference point values |
| `LENGTH`, `FORK_LENGTH` | length | Physical measurement |
| `WEIGHT`, `BIOMASS`, `MASS` | mass | Physical measurement |
| `PROPORTION`, `PERCENT`, `FRACTION`, `pHOS` | proportion | Part-of-whole ratios |

### Ambiguous property cases

Ask user when:
- `_INDEX` columns could be rate or scalar
- `EXPANSION_FACTOR` could be scalar or method parameter
- `ADJUSTED_` prefix could change property interpretation
