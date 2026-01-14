---
name: ontology-term-creation
description: Draft new term requests and gpt_proposed_terms.csv rows when no existing term fits.
---

# Ontology term creation

Use this skill when no existing term fits and a new term is needed for the ontology, and an ontology is a formal model of concepts and relationships.

## Guardrails
- Never invent IRIs (an IRI is a web-style identifier for a concept).
- Avoid punning: punning means reusing the same IRI as both an OWL class and a SKOS concept.
- Vocabulary/ontology guidance for SDP semantics lives in `docs/vocabulary.md`.

## gpt_proposed_terms.csv schema
Required fields:
- term_label (short human-readable name)
- term_definition (plain-language definition)
- term_type (see below)
- suggested_parent_iri (IRI for the closest parent concept)
Optional fields:
- definition_source_url (link to the source of the definition)
- suggested_relationships (comma-separated list of broader/narrower/related or OWL relationships)
- notes (extra context or constraints)

Term types:
- skos_concept: a controlled vocabulary concept in SKOS, and SKOS is a standard for controlled vocabularies.
- owl_class: a class in OWL, and OWL is a formal language for machine-readable models of concepts and relationships.
- owl_object_property: a relationship in OWL between two things.

## Response template (ordered outputs)
Keep outputs deterministic (deterministic means the same input yields the same output) and ordered:
1) dataset.csv
2) tables.csv
3) column_dictionary.csv
4) codes.csv (include only when categorical columns exist)
Then provide gpt_proposed_terms.csv and the drafted issue text.

## Term request workflow
1) Add rows to gpt_proposed_terms.csv with the fields above.
2) Draft the term request using the public DFO Salmon Ontology tracker:
   https://github.com/dfo-pacific-science/dfo-salmon-ontology/issues/new?template=new-term-request.md
3) Provide a definition source; a definition source is where the wording came from.

## GitHub issue template format

The DFO Salmon Ontology uses this issue template for new term requests. Copy and fill in this format when submitting:

```markdown
---
name: New term request
about: Request new term to be added in GC DFO Salmon ontology
title: 'New term request: [Term label]'
labels: new term request
assignees: ''
---

Please provide as much information as you can:

* **Suggested term label (required):**

* **Definition (required):**

* **Definition source (required):**

* **Parent term(s):**

* **Children terms** (if applicable; should any existing terms be moved underneath this new proposed term?):

* **Synonyms** (please specify, EXACT, BROAD, NARROW or RELATED):

* **Cross-references:**

* **Any other information:**
```

### Filled example (Marine Survival Rate)

```markdown
---
name: New term request
about: Request new term to be added in GC DFO Salmon ontology
title: 'New term request: Marine Survival Rate'
labels: new term request
assignees: ''
---

Please provide as much information as you can:

* **Suggested term label (required):** Marine Survival Rate

* **Definition (required):** Proportion of juvenile salmon that survive their ocean residence period and return as adults.

* **Definition source (required):** https://www.dfo-mpo.gc.ca/science/

* **Parent term(s):** https://w3id.org/gcdfo/salmon#TargetOrLimitRateOrAbundance

* **Children terms** (if applicable): None

* **Synonyms** (please specify, EXACT, BROAD, NARROW or RELATED):
  - RELATED: ocean survival
  - BROAD: survival rate

* **Cross-references:** Used in SPSR data dictionary for MARINE_SURVIVAL_INDEX column

* **Any other information:**
I-ADOPT decomposition for this variable:
- property_iri: http://qudt.org/vocab/quantitykind/DimensionlessRatio
- entity_iri: https://w3id.org/gcdfo/salmon#Stock
- constraint_iri: [marine_phase_constraint_IRI]
```

### Batch submission guidance

- **Individual issues**: Submit terms individually when each requires distinct review or discussion.
- **Grouped issues**: Group related terms (e.g., all mortality rate variants) into a single issue when they share the same pattern and parent.
- **Recommended groupings**:
  - Temporal conventions (year types)
  - Mortality rates (in-river, mainstem, ocean, terminal)
  - Age conventions (Gilbert-Rich, European)
  - Reference points (LRP, USR, benchmarks)

## Helper script (optional)
- CLI template helper: `python -m salmonpy.scripts.draft_new_term --label "<label>" --definition "<definition>" --term-type skos_concept --parent-iri <parent_iri>`
- Output is Markdown you can paste into the issue template; keep keys and secrets out of chat.

## salmonpy helper (Python)
Use salmonpy to keep proposed terms aligned with the dictionary:
```python
import pandas as pd
from salmonpy import infer_dictionary, validate_dictionary

df = pd.DataFrame({"new_measurement": [1.0, 2.5]})
dict_df = infer_dictionary(df, dataset_id="demo", table_id="observations")
dict_df.loc[dict_df["column_name"] == "new_measurement", "column_role"] = "measurement"
validate_dictionary(dict_df)
# Add proposed terms for the measurement parts in gpt_proposed_terms.csv
```
