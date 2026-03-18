# SDP Validation Checklist

Use this checklist to manually validate Salmon Data Package (SDP) files before delivery.

---

## 1. Dataset Metadata (dataset.csv)

- [ ] Exactly 1 row
- [ ] `dataset_id` is non-empty and uses snake_case
- [ ] `title` is present and descriptive
- [ ] `description` is present
- [ ] `license` is a valid license identifier (e.g., CC-BY-4.0)
- [ ] `contact_name` and `contact_email` are present

### Required Columns
```
dataset_id, title, description, license, contact_name, contact_email
```

---

## 2. Table Metadata (tables.csv)

- [ ] At least 1 row
- [ ] All `dataset_id` values match dataset.csv
- [ ] Each `table_id` is unique within the dataset
- [ ] `table_id` uses snake_case
- [ ] `file_name` is a relative path (no `../`)
- [ ] `observation_unit` describes what each row represents

### Required Columns
```
dataset_id, table_id, file_name, table_label, description, observation_unit
```

---

## 3. Column Dictionary (column_dictionary.csv)

### Basic Validation
- [ ] All `dataset_id` values match dataset.csv
- [ ] All `table_id` values exist in tables.csv
- [ ] No duplicate `column_name` within the same `table_id`
- [ ] `column_role` is one of: identifier, temporal, categorical, attribute, measurement
- [ ] `value_type` is one of: string, integer, number, boolean, date, datetime

### Required Columns
```
dataset_id, table_id, column_name, column_label, column_description, column_role, value_type
```

### Measurement Column Requirements
For all rows where `column_role = measurement`:
- [ ] `unit_iri` is populated (look up in `08-qudt-units.csv`)
- [ ] `property_iri` is populated (look up in `09-qudt-quantity-kinds.csv`)
- [ ] `entity_iri` is populated (look up in `07-dfo-salmon-terms.csv`)
- [ ] `term_iri` is populated OR documented in gpt_proposed_terms.csv

### Semantic IRI Validation
- [ ] All IRIs are valid URLs (start with `http://` or `https://`)
- [ ] IRIs match expected vocabulary patterns:
  - Units: `http://qudt.org/vocab/unit/...`
  - Quantity kinds: `http://qudt.org/vocab/quantitykind/...`
  - DFO terms: `https://w3id.org/gcdfo/salmon#...`
  - DwC terms: `http://rs.tdwg.org/dwc/terms/...`
- [ ] No invented/fabricated IRIs
- [ ] `term_type` matches source (skos_concept, owl_class, owl_object_property)

### Constraint Handling
- [ ] Multiple constraints use `;` separator
- [ ] Placeholder IRIs (e.g., `<age_3_IRI>`) are documented in gpt_proposed_terms.csv
- [ ] Constraint patterns are consistent across similar columns

---

## 4. Codes (codes.csv) - If Applicable

Only required when `column_role = categorical` columns exist.

### Basic Validation
- [ ] All `dataset_id` values match dataset.csv
- [ ] All `table_id` values exist in tables.csv
- [ ] All `column_name` values exist in column_dictionary.csv with `column_role = categorical`
- [ ] `code_value` matches actual data values
- [ ] `code_label` is human-readable

### Required Columns
```
dataset_id, table_id, column_name, code_value, code_label
```

### Optional Semantic Columns
- [ ] `term_iri` populated where ontology mappings exist
- [ ] IRIs are valid and from appropriate vocabularies

---

## 5. Cross-File Integrity

- [ ] All `dataset_id` values are identical across all files
- [ ] All `table_id` in column_dictionary.csv exist in tables.csv
- [ ] All `table_id` in codes.csv exist in tables.csv
- [ ] Primary keys listed in tables.csv exist as columns in column_dictionary.csv

---

## 6. Entity Selection Consistency

Check that entity_iri follows table context conventions:

| Table Prefix | Expected entity_iri |
|--------------|---------------------|
| `smu_*` | `https://w3id.org/gcdfo/salmon#StockManagementUnit` |
| `cu_*` | `https://w3id.org/gcdfo/salmon#ConservationUnit` |
| `pop_*` | `https://w3id.org/gcdfo/salmon#Stock` |
| Individual fish | `http://rs.tdwg.org/dwc/terms/Organism` |

- [ ] Entity selections are consistent within tables
- [ ] Overrides (e.g., CU_ column in smu_* table) are intentional

---

## 7. Term Type Consistency

- [ ] `term_type = skos_concept` for SKOS vocabularies and compound variables
- [ ] `term_type = owl_class` for OWL classes (StockManagementUnit, ConservationUnit, etc.)
- [ ] `term_type = owl_object_property` for OWL properties
- [ ] No punning (same IRI used as both owl_class and skos_concept)

---

## 8. Proposed Terms (gpt_proposed_terms.csv) - If Applicable

When term_iri was left blank due to missing vocabulary terms:

### Required Columns
```
term_label, term_definition, term_type, suggested_parent_iri
```

### Validation
- [ ] All terms where `term_iri` was blank have corresponding rows
- [ ] `term_label` is concise and descriptive
- [ ] `term_definition` is complete and not fabricated
- [ ] `definition_source_url` is provided where available (not fabricated)
- [ ] `term_type` is one of: skos_concept, owl_class, owl_object_property
- [ ] `suggested_parent_iri` is a valid IRI from the ontology

---

## 9. Common Issues to Check

### Missing Semantics
- [ ] No measurement columns missing unit_iri
- [ ] No measurement columns missing property_iri
- [ ] No measurement columns missing entity_iri

### Invalid Values
- [ ] No empty strings where values are required
- [ ] No placeholder text like "TBD", "TODO", "FIXME"
- [ ] No fabricated URLs or DOIs

### Format Issues
- [ ] CSV files are properly comma-separated
- [ ] No trailing commas
- [ ] Quoted strings where values contain commas
- [ ] UTF-8 encoding

---

## Quick Validation Summary

Before delivery, confirm:

1. **File count**: 3 required (dataset, tables, dictionary) + codes if categorical columns exist
2. **Row counts**: dataset=1, tables≥1, dictionary has all columns
3. **ID consistency**: dataset_id matches everywhere
4. **Measurement completeness**: All measurements have unit, property, entity IRIs
5. **No invented IRIs**: All IRIs from bundled vocabularies or marked as proposed
6. **Proposed terms documented**: Gaps captured in gpt_proposed_terms.csv
