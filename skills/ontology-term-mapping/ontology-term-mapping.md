---
name: ontology-term-mapping
description: Map SDP columns and codes to ontology terms using DFO Salmon Ontology and I-ADOPT.
---

# Ontology term mapping

Use this skill when the user wants IRIs for columns or codes, and you need to map them to ontology terms (an ontology is a formal model of concepts and relationships).

## References
- dfo-salmon.ttl is a schema-only vocabulary file (a schema is a list of fields and rules, and a vocabulary file is a list of terms), not data.
- schema/glossary.md is the shared field glossary (a glossary is a list of field definitions used to keep wording consistent).
- SPECIFICATION.md is normative (normative means it defines what is valid).
- docs/vocabulary.md is the canonical vocabulary/ontology guidance for SDP semantics fields.
- Canonical semantics example lives in `examples/canonical-semantics/`.
- Helper scripts: see `skills/ontology-helpers/scripts/` for gap detection and issue drafting.

## Guardrails
- Never invent IRIs (an IRI is a web-style identifier for a concept).
- Avoid punning: punning means reusing the same IRI as both an OWL class and a SKOS concept.

## SKOS vs OWL decision rule
SKOS is a standard for controlled vocabularies; OWL is a formal language for machine-readable models of concepts and relationships.
- Use SKOS concepts for controlled vocabularies and compound variables.
- Use OWL classes or OWL object properties only when the column represents a type or relationship used as a class or property in data.
- If unsure, leave term_iri blank and add gpt_proposed_terms.csv.

Decision tree (short):
- Categorical code list -> SKOS scheme + codes.csv
- Measurement or variable -> SKOS variable concept + I-ADOPT fields (if no suitable variable concept exists yet, use a well-known external term as a temporary fallback and propose a `gcdfo:` variable concept)
- Class or type label -> OWL class
- Otherwise -> leave term_iri blank and propose a new term

## Response template (ordered outputs)
When you return SDP metadata, keep outputs deterministic (deterministic means the same input yields the same output) and ordered:
1) dataset.csv
2) tables.csv
3) column_dictionary.csv
4) codes.csv (include only when categorical columns exist)
Place any notes or gpt_proposed_terms.csv after these blocks.

## Measurement columns and I-ADOPT parts (plus procedure/method)
A measurement column is a column whose values are observed or computed quantities.
I-ADOPT is a standard for describing variables by parts like property and entity.
For measurement columns, include term_iri, unit_iri, property_iri, entity_iri; constraint_iri is optional; method_iri is an optional procedure/method link (aligned to SOSA `sosa:Procedure`, where SOSA is the W3C/OGC observations vocabulary) and is not an I-ADOPT role.
Do not include OWL examples for I-ADOPT decomposition; keep decomposition in fields only.

## I-ADOPT patterns for salmon metrics (worked examples)
- Age-stratified catch in mainstem (e.g., MAINSTEM_AGE_3 = number of fish caught in mainstem at age 3)
  - term_iri: http://rs.tdwg.org/dwc/terms/individualCount (Darwin Core property; use as generic fallback when no salmon-specific variable exists)
  - unit_iri: http://qudt.org/vocab/unit/NUM
  - property_iri: http://qudt.org/vocab/quantitykind/Count
  - entity_iri: https://w3id.org/gcdfo/salmon#StockManagementUnit
  - constraint_iri: <age_3_IRI>;<mainstem_location_IRI> (use `;` to separate multiple constraints)
  - method_iri: <procedure_or_method_IRI_if_applicable>
- Location-stratified catch (ocean) (e.g., OCEAN_CATCH_TOTAL)
  - term_iri: http://rs.tdwg.org/dwc/terms/individualCount
  - unit_iri: http://qudt.org/vocab/unit/NUM
  - property_iri: http://qudt.org/vocab/quantitykind/Count
  - entity_iri: https://w3id.org/gcdfo/salmon#ConservationUnit
  - constraint_iri: <ocean_area_IRI>
- Exploitation rate (TOTAL_EXPLOITATION_RATE = proportion harvested)
  - term_iri: https://w3id.org/gcdfo/salmon#TotalExploitationRate
  - unit_iri: http://qudt.org/vocab/unit/UNITLESS
  - property_iri: http://qudt.org/vocab/quantitykind/DimensionlessRatio
  - entity_iri: https://w3id.org/gcdfo/salmon#StockManagementUnit
  - constraint_iri: <fishing_mortality_IRI>
- Spawner abundance (ESCAPEMENT_COUNT)
  - term_iri: https://w3id.org/gcdfo/salmon#EscapementMeasurement
  - unit_iri: http://qudt.org/vocab/unit/NUM
  - property_iri: http://qudt.org/vocab/quantitykind/Count
  - entity_iri: https://w3id.org/gcdfo/salmon#Stock
  - constraint_iri: <river_system_IRI>
- Length at age (LENGTH_AGE_3)
  - term_iri: http://purl.obolibrary.org/obo/CMO_0000013 (length)
  - unit_iri: http://qudt.org/vocab/unit/CentiM
  - property_iri: http://qudt.org/vocab/quantitykind/Length
  - entity_iri: http://rs.tdwg.org/dwc/terms/Organism
  - constraint_iri: <age_3_IRI>

Tips from I-ADOPT:
- Identify components: Property, Object of Interest, Matrix (if embedded), Context objects, Constraints.
- Use units to infer property when uncertain (unit → property lookup).
- If relevant, capture procedure/method explicitly in `method_iri` (aligned to SOSA `sosa:Procedure`).
- Keep constraints explicit; use `;` to separate multiple constraints.

## Codes and skos:notation
skos:notation is a code string attached to a SKOS concept.
If term_iri points to a DFO SKOS concept with skos:notation, set code_value to that notation.

## Missing terms
If no term exists, add a row to gpt_proposed_terms.csv and draft a term request using the public tracker:
https://github.com/dfo-pacific-science/dfo-salmon-ontology/issues/new?template=new-term-request.md
Use that tracker for other ontology issues too (it is the canonical public log for the DFO Salmon Ontology).

## API key setup for BioPortal (only if you need BioPortal results)
- Get a key: https://bioportal.bioontology.org/register
- Shell (bash/zsh): `export BIOPORTAL_APIKEY=your_key_here` (persist by adding that line to `~/.zshrc` or `~/.bashrc`)
- R session: add `BIOPORTAL_APIKEY=your_key_here` to `~/.Renviron`, then `readRenviron("~/.Renviron")`
- Python session: `import os; os.environ["BIOPORTAL_APIKEY"] = "your_key_here"`
- Caching (optional): set `SALMONPY_CACHE=1` or `METASALMON_CACHE=1` to cache term search results by query+role locally.
Never paste keys into chat; keep them in your environment.

## Complementary R tools
When the user has R available, suggest these metasalmon functions:
- `find_terms()`: searches OLS, NVS, and BioPortal for matching IRIs
- `suggest_semantics()`: provides role-aware I-ADOPT suggestions using the bundled terminology catalogue
These provide deterministic, reproducible suggestions that complement GPT-assisted mapping.

## Quick R workflow (minimal toolchain)
1) Fetch ontology (cached): `path <- system('Rscript skills/ontology-helpers/scripts/r/fetch_dfo_salmon_ttl.R', intern=TRUE)`
2) Load configs: `entity_defaults <- read.csv('config/entity_defaults.csv'); vocab_priority <- readLines('config/vocab_priority.md')`
3) Suggest + validate: `source('skills/ontology-helpers/scripts/r/validate_semantics.R')` (runs metasalmon::validate_dictionary; emits gpt_proposed_terms.csv for missing term_iri)
4) Keep skills thin: add reusable helpers to metasalmon; call them here rather than re-implementing.

## GitHub issue template (clean Markdown)
```
## Summary
<goal>

## Tasks
- [ ] <task>
- [ ] <task>

Base branch: `main`
```

## salmonpy helper (Python)
Use salmonpy (Python mirror of metasalmon) for deterministic term suggestions:
```python
import pandas as pd
from salmonpy import infer_dictionary, suggest_semantics, find_terms

df = pd.DataFrame({"count": [1, 2]})
dict_df = infer_dictionary(df, dataset_id="demo", table_id="observations")
dict_df.loc[dict_df["column_name"] == "count", "column_role"] = "measurement"

# Targeted lookup
find_terms("escapement count", role="variable", sources=("ols", "nvs")).head(3)

# Role-aware suggestions per measurement column
dict_with_suggestions = suggest_semantics(df, dict_df, sources=("ols", "nvs"))
dict_with_suggestions.attrs.get("semantic_suggestions")
```
