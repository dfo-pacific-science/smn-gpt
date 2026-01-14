---
name: data-package-generation
description: Generate SDP metadata CSVs from user data with CSV-only outputs and dataset_id.
---

# Data package generation

Use this skill when the user wants to create or update SDP metadata files, where an SDP (Salmon Data Package) is a small folder of CSV metadata files plus data files, and metadata means data about the data, like names and descriptions.

## References

- SPECIFICATION.md is normative (normative means it defines what is valid).
- schema/glossary.md is the shared field glossary (a glossary is a list of field definitions used to keep wording consistent).
- Canonical examples: `examples/canonical-basic/` (no semantics) and `examples/canonical-semantics/` (with IRIs and codes); see examples/README.md for workflows.

## Data minimization

Data minimization means ask for the smallest amount of data needed.
Request:

- 50-500 representative rows per table
- column names and type hints
- codebooks or methods documents
- dataset_id, license, and contact details if missing
- Start with a small sub-sample of metadata/dictionary rows to confirm patterns before delivering full files.

## Steps

1. Confirm dataset_id (dataset_id is the join key across metadata files).
2. Build dataset.csv with required fields; ask only for missing required fields.
3. Build tables.csv:
   - Use table_id in snake_case (snake_case means lowercase words separated by underscores).
   - file_name should be a relative path without ../.
   - observation_unit is the thing each row is about.
4. Build column_dictionary.csv:
   - Set column_role and value_type from the data.
   - For measurement columns, include term_iri, unit_iri, property_iri, and entity_iri; I-ADOPT is a standard for describing variables by parts like property and entity.
   - For vocabulary/ontology selection (term_iri, property_iri, entity_iri, etc), follow `docs/vocabulary.md`.
5. If categorical columns exist (a categorical column stores codes or labels from a fixed list), build codes.csv.

## Response template (ordered outputs)

Always answer in this order to keep outputs deterministic (deterministic means the same input yields the same output):

1. dataset.csv
2. tables.csv
3. column_dictionary.csv
4. codes.csv (include only when categorical columns exist)
   Keep any notes or questions after these CSV blocks.

## Output contract

CSV only; CSV is a comma-separated text table.
Required outputs: dataset.csv, tables.csv, column_dictionary.csv.
Required when categorical columns exist: codes.csv.
Optional outputs: gpt_proposed_terms.csv and questions (questions only when needed to avoid wrong assumptions).

## Scale guidance (large dictionaries)
- Always start with a small representative subset to confirm patterns and assumptions.
- If <50 columns: return complete column_dictionary.csv.
- If 50-150 columns: return complete column_dictionary.csv with a short summary note.
- If >150 columns: return complete dataset.csv and tables.csv; for column_dictionary.csv show one full representative table and 5-10 rows per remaining table to demonstrate the pattern, then offer to generate the full file as a follow-up deliverable.
- codes.csv: return complete file (categorical values are usually manageable).

## Column role decision guide
- identifier: primary/foreign keys (e.g., SMU_ID, CU_ID, POP_ID, YEAR if used as key), unique sample/observation IDs.
- temporal: dates, datetimes, year columns.
- categorical: fixed lists or code tables (<~50 values), status/quality/method codes; if values come from a fixed list, mark categorical and consider codes.csv.
- attribute: free text, names, labels, descriptors that are not keys and not quantitative.
- measurement: numeric observed/computed values with units or I-ADOPT decomposition (counts, rates, indices, reference points).

## Value type guide
- integer: whole-number counts, ages, years stored as YYYY, ordinal codes (1/2/3/4/U).
- number: decimals (rates, proportions, ratios, continuous measurements).
- string: text, identifiers, categorical codes, free-text descriptions.
- boolean: true/false only (use sparingly; often categorical with codes.csv is clearer).
- date: ISO dates (YYYY-MM-DD); use integer for year-only columns stored as ints.
- datetime: ISO datetimes (YYYY-MM-DDTHH:MM:SSZ).

## When to use codes.csv
- Use codes.csv when column_role = categorical AND values are from a fixed list AND labels/definitions or IRIs are useful.
- Prefer codes.csv when codes map to ontology IRIs or need human-readable labels.
- If values are free text, skip codes.csv and keep column_role = attribute.
- If >~50 distinct values, include a note pointing to the external vocabulary instead of enumerating all codes.
- Species codes are often well-known; still use codes.csv if you need NCBITaxon IRIs.

## Automating large conversions (Python)
Use scripting to avoid manual errors when source dictionaries are wide:
```python
import pandas as pd

dd = pd.read_csv("SPSR-Data-Dictionary_verbose.csv")
long_df = dd.rename(columns={
    "File Name": "table_id",
    "Variable Name": "column_name",
    "Label": "column_label",
    "Variable Definition": "column_description",
    "Units": "unit_label",
    "Variable Type": "value_type"
})
long_df["dataset_id"] = "spsr-data-dictionary"

def infer_role(row):
    name = row["column_name"].upper()
    if any(k in name for k in ["_ID", "ID_", "KEY"]):
        return "identifier"
    if "YEAR" in name or "DATE" in name or "TIME" in name:
        return "temporal"
    if row.get("unit_label") and str(row["unit_label"]).strip().upper() not in ("", "NA"):
        return "measurement"
    if row.get("value_type", "").lower() in ("varchar", "char"):
        return "attribute"
    return "categorical"

long_df["column_role"] = long_df.apply(infer_role, axis=1)
long_df.to_csv("column_dictionary_skeleton.csv", index=False)
```

## Final checks
- Run validator (Python): `python -m salmonpy.scripts.validate_sdp --dataset dataset.csv --tables tables.csv --dictionary column_dictionary.csv [--codes codes.csv] [--require-semantics]`
- Ensure outputs stay ordered: dataset.csv, tables.csv, column_dictionary.csv, then codes.csv (if categorical columns exist).

## salmonpy helper (Python)

Use salmonpy (Python mirror of metasalmon) for deterministic scaffolding:

```python
import pandas as pd
from salmonpy import infer_dictionary, validate_dictionary, create_salmon_datapackage

df = pd.DataFrame({"species": ["Coho", "Chinook"], "count": [100, 200]})
dict_df = infer_dictionary(df, dataset_id="demo", table_id="observations")
dict_df.loc[dict_df["column_name"] == "count", "column_role"] = "measurement"
validate_dictionary(dict_df)

dataset_meta = pd.DataFrame({"dataset_id": ["demo"], "title": ["Demo"], "description": ["Demo dataset"]})
table_meta = pd.DataFrame({"dataset_id": ["demo"], "table_id": ["observations"], "file_name": ["observations.csv"], "table_label": ["Observations"]})
create_salmon_datapackage({"observations": df}, dataset_meta, table_meta, dict_df, path="out", overwrite=True)
```
