# Skills Guide

This consolidated guide covers all workflows for creating and enriching Salmon Data Packages (SDPs).

---

## 1. Data Package Generation

Use this when the user wants to create or update SDP metadata files.

### References
- `02-SPECIFICATION.md` is normative (defines what is valid)
- `03-GLOSSARY.md` is the shared field glossary
- `05-VOCABULARY-GUIDE.md` for ontology selection
- `20-metasalmon-workflow.md` for the preferred MetaSalmon/metasalmon package-first workflow

### Data Minimization
Request only what's needed:
- 50-500 representative rows per table
- Column names and type hints
- Codebooks or methods documents
- dataset_id, license, and contact details if missing

### Steps
1. If the user already has a MetaSalmon/metasalmon package, review that package first instead of rebuilding it from scratch (see `20-metasalmon-workflow.md`).
2. Confirm dataset_id (the join key across metadata files)
3. Build dataset.csv with required fields
4. Build tables.csv:
   - Use table_id in snake_case
   - file_name should be relative path without `../`
   - observation_unit is the thing each row is about
5. Build column_dictionary.csv:
   - Set column_role and value_type from the data
   - For measurement columns, include term_iri, unit_iri, property_iri, and entity_iri
   - For vocabulary selection, follow `05-VOCABULARY-GUIDE.md`
6. If categorical columns exist, build codes.csv

### Column Role Decision Guide
- **identifier**: primary/foreign keys (e.g., SMU_ID, CU_ID, POP_ID)
- **temporal**: dates, datetimes, year columns
- **categorical**: fixed lists or code tables (<~50 values)
- **attribute**: free text, names, labels, descriptors
- **measurement**: numeric observed/computed values with units

### Value Type Guide
- **integer**: whole-number counts, ages, years as YYYY
- **number**: decimals (rates, proportions, continuous measurements)
- **string**: text, identifiers, categorical codes
- **boolean**: true/false only
- **date**: ISO dates (YYYY-MM-DD)
- **datetime**: ISO datetimes (YYYY-MM-DDTHH:MM:SSZ)

### When to Use codes.csv
- Use when column_role = categorical AND values are from a fixed list AND labels/definitions or IRIs are useful
- Prefer codes.csv when codes map to ontology IRIs
- If >~50 distinct values, note the external vocabulary instead

### Response Template (Ordered Outputs)
1. dataset.csv
2. tables.csv
3. column_dictionary.csv
4. codes.csv (only when categorical columns exist)
5. gpt_proposed_terms.csv (if new terms needed)

---

## 2. Ontology Term Mapping

Use this when the user wants IRIs for columns or codes.

### Key Principles
- **Never invent IRIs** - if unknown, leave blank and propose new term
- **Avoid punning** - don't reuse same IRI as both OWL class and SKOS concept
- Look up terms in bundled vocabulary CSVs:
  - `19-salmon-domain-terms.csv` for shared Salmon Domain Ontology terms
  - `07-dfo-salmon-terms.csv` for DFO Salmon Ontology terms
  - `08-qudt-units.csv` for unit IRIs
  - `09-qudt-quantity-kinds.csv` for property IRIs
  - `10-dwc-terms.csv` for Darwin Core terms

### SKOS vs OWL Decision Rule
- **SKOS concepts**: controlled vocabularies and compound variables
- **OWL classes**: types used as classes in data (StockManagementUnit, ConservationUnit)
- **OWL object properties**: relationships between entities

Decision tree:
- Categorical code list → SKOS scheme + codes.csv
- Measurement or variable → SKOS variable concept + I-ADOPT fields
- Class or type label → OWL class
- Otherwise → leave term_iri blank and propose new term

### Measurement Columns and I-ADOPT Parts
For measurement columns, include:
- **term_iri**: The variable concept (e.g., escapement measurement)
- **unit_iri**: The unit (look up in `08-qudt-units.csv`)
- **property_iri**: The quantity kind (look up in `09-qudt-quantity-kinds.csv`)
- **entity_iri**: The thing being measured (look up in `07-dfo-salmon-terms.csv`)
- **constraint_iri**: Optional facets (age, location, season); use `;` for multiple
- **method_iri**: Optional procedure/method IRI

### I-ADOPT Worked Examples

**Age-stratified catch (MAINSTEM_AGE_3)**
- term_iri: http://rs.tdwg.org/dwc/terms/individualCount
- unit_iri: http://qudt.org/vocab/unit/NUM
- property_iri: http://qudt.org/vocab/quantitykind/Count
- entity_iri: https://w3id.org/gcdfo/salmon#StockManagementUnit
- constraint_iri: `<age_3_IRI>;<mainstem_location_IRI>`

**Exploitation rate (TOTAL_EXPLOITATION_RATE)**
- term_iri: https://w3id.org/gcdfo/salmon#TotalExploitationRate
- unit_iri: http://qudt.org/vocab/unit/UNITLESS
- property_iri: http://qudt.org/vocab/quantitykind/DimensionlessRatio
- entity_iri: https://w3id.org/gcdfo/salmon#StockManagementUnit

**Escapement count (ESCAPEMENT_COUNT)**
- term_iri: https://w3id.org/gcdfo/salmon#EscapementMeasurement
- unit_iri: http://qudt.org/vocab/unit/NUM
- property_iri: http://qudt.org/vocab/quantitykind/Count
- entity_iri: https://w3id.org/gcdfo/salmon#Stock

### Codes and skos:notation
If term_iri points to a SKOS concept with skos:notation, set code_value to that notation.

### Missing Terms
If no term exists in bundled vocabularies:
1. Leave term_iri blank
2. Add row to gpt_proposed_terms.csv
3. See `17-github-issue-templates.md` for issue template format

---

## 3. Ontology Term Creation

Use this when no existing term fits and a new term is needed.

### gpt_proposed_terms.csv Schema

**Required fields:**
- term_label: short human-readable name
- term_definition: plain-language definition
- term_type: skos_concept | owl_class | owl_object_property
- suggested_parent_iri: IRI for the closest parent concept

**Optional fields:**
- definition_source_url: link to definition source
- suggested_relationships: comma-separated broader/narrower/related
- notes: extra context or constraints

### Term Types
- **skos_concept**: controlled vocabulary concept
- **owl_class**: a class (e.g., StockManagementUnit)
- **owl_object_property**: a relationship between entities

### Term Request Workflow
1. Add rows to gpt_proposed_terms.csv
2. See `17-github-issue-templates.md` for issue format
3. Provide a definition source (where the wording came from)

### Batch Submission Guidance
- **Individual issues**: terms requiring distinct review
- **Grouped issues**: related terms sharing same pattern and parent
- Recommended groupings:
  - Temporal conventions (year types)
  - Mortality rates (in-river, mainstem, ocean, terminal)
  - Age conventions (Gilbert-Rich, European)
  - Reference points (LRP, USR, benchmarks)

---

## 4. Ontology Helpers

Use this for validation and gap detection.

### Post-Generation Validation Checklist

**Measurement column completeness:**
- [ ] All measurement columns have unit_iri populated
- [ ] All measurement columns have property_iri populated
- [ ] All measurement columns have entity_iri populated
- [ ] term_iri is populated OR documented in gpt_proposed_terms.csv

**Constraint handling:**
- [ ] Multiple constraints use `;` separator
- [ ] All placeholder IRIs documented in gpt_proposed_terms.csv
- [ ] Constraint patterns consistent across similar columns

**Categorical column coverage:**
- [ ] All categorical columns have entries in codes.csv
- [ ] codes.csv includes term_iri where mappings exist
- [ ] code_value matches actual data values

**Term type consistency:**
- [ ] term_type matches source of term_iri
- [ ] No punning (same IRI as both owl_class and skos_concept)

**Cross-file integrity:**
- [ ] All table_id values in column_dictionary.csv exist in tables.csv
- [ ] All dataset_id values match across all files
- [ ] Primary keys in tables.csv exist as columns in column_dictionary.csv

**Entity selection consistency:**
- [ ] SMU-level tables use entity_iri = `https://w3id.org/gcdfo/salmon#StockManagementUnit`
- [ ] CU-level tables use entity_iri = `https://w3id.org/gcdfo/salmon#ConservationUnit`
- [ ] Population-level tables use entity_iri = `https://w3id.org/gcdfo/salmon#Stock`
- [ ] Individual fish observations use entity_iri = `http://rs.tdwg.org/dwc/terms/Organism`
- [ ] User confirmed entity selections via pattern-based workflow

### Entity Selection by Table Context

| Table Prefix | Default Entity | IRI |
|--------------|----------------|-----|
| `smu_*` | StockManagementUnit | `https://w3id.org/gcdfo/salmon#StockManagementUnit` |
| `cu_*` | ConservationUnit | `https://w3id.org/gcdfo/salmon#ConservationUnit` |
| `pop_*` | Stock (fallback) | `https://w3id.org/gcdfo/salmon#Stock` |
| `indicator_*` | Stock (fallback) | `https://w3id.org/gcdfo/salmon#Stock` |
| `pfma_*` | Stock | `https://w3id.org/gcdfo/salmon#Stock` |

**Override rules:**
- Column contains `CU_` in non-cu_* table → use ConservationUnit
- Column contains `SMU_` in non-smu_* table → use StockManagementUnit
- Column describes individual fish (LENGTH, WEIGHT) → use `dwc:Organism`
- Column describes spawning adults → use Stock plus spawner constraint

### Property Selection by Unit

| Unit Pattern | Default Property IRI |
|--------------|----------------------|
| NUM, count, individuals | `http://qudt.org/vocab/quantitykind/Count` |
| UNITLESS, ratio, proportion | `http://qudt.org/vocab/quantitykind/DimensionlessRatio` |
| cm, mm, m | `http://qudt.org/vocab/quantitykind/Length` |
| g, kg | `http://qudt.org/vocab/quantitykind/Mass` |

---

## 5. Vocabulary Lookup Guidance

Since this environment cannot make API calls to external vocabularies, use the bundled CSV files to look up terms.

### Available Vocabulary Files

| File | Contents | Use For |
|------|----------|---------|
| `07-dfo-salmon-terms.csv` | DFO Salmon Ontology terms | entity_iri, salmon-specific concepts |
| `08-qudt-units.csv` | Common QUDT units | unit_iri |
| `09-qudt-quantity-kinds.csv` | QUDT quantity kinds | property_iri |
| `10-dwc-terms.csv` | Darwin Core terms | occurrence, event, location fields |
| `11-ontology-preferences.csv` | Role-based vocabulary priorities | choosing between sources |
| `12-iadopt-terminologies.csv` | I-ADOPT vocabulary catalog | term ranking hints |

### Lookup Workflow

1. Identify what you need (unit, property, entity, etc.)
2. Search the appropriate bundled CSV by label or definition
3. Use the IRI from the matching row
4. If no match found, leave blank and propose new term

### When Bundled Vocabularies Don't Have a Match

1. Check if a close match exists (broader or related term)
2. If semantically correct, use the broader term
3. If no suitable match:
   - Leave the IRI field blank
   - Add entry to gpt_proposed_terms.csv
   - Document the gap

---

## Response Template

For any SDP generation task, always return outputs in this order:

1. **dataset.csv** - Dataset metadata (1 row)
2. **tables.csv** - Table metadata (1 row per table)
3. **column_dictionary.csv** - Column definitions
4. **codes.csv** - Code lists (only if categorical columns exist)
5. **gpt_proposed_terms.csv** - New term proposals (if needed)
6. **questions** - Clarification questions (only if required)

Keep outputs deterministic and pasteable.
