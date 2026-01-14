---
name: metasalmon-usage
description: Guide users through the metasalmon R package workflows for SDP.
---

# metasalmon usage

Use this skill when the user asks how to read, validate, or build SDP metadata with metasalmon, where an SDP (Salmon Data Package) is a small folder of CSV metadata files plus data files, and metadata means data about the data, like names and descriptions.

## References
- SPECIFICATION.md is normative (normative means it defines what is valid).
- schema/glossary.md is the shared field glossary (a glossary is a list of field definitions used to keep wording consistent).
- A vignette is a tutorial document bundled with an R package; R is a statistical programming language.

## Suggested reading order
1) metasalmon/vignettes/how-it-fits-together.Rmd (How it Fits Together)
2) metasalmon/vignettes/metasalmon.Rmd (Biologist Quickstart)
3) metasalmon/vignettes/functions-workflow.Rmd (R Workflow and Validation)
4) metasalmon/vignettes/semantic-enrichment.Rmd (Semantic Enrichment)
5) metasalmon/vignettes/gpt-collaboration.Rmd (AI Assistance)

## Workflow guidance
- Keep metadata CSVs aligned to schema/glossary.md.
- Validate required fields before adding semantics.
- Use codes.csv only when categorical columns exist.

## Response template (ordered outputs)
When producing SDP metadata, keep outputs deterministic (deterministic means the same input yields the same output):
1) dataset.csv
2) tables.csv
3) column_dictionary.csv
4) codes.csv (include only when categorical columns exist)
Place any notes or gpt_proposed_terms.csv after these blocks.

## Key functions for ontology lookup
- `find_terms()`: search OLS, NVS, BioPortal for IRIs by keyword
- `suggest_semantics()`: get role-aware I-ADOPT suggestions for measurement columns
See semantic-enrichment.Rmd for usage examples.

## Caching and API keys
- Optional cache: set `METASALMON_CACHE=1` (R) or `SALMONPY_CACHE=1` (Python) to cache term search results by query+role locally.
- BioPortal: set `BIOPORTAL_APIKEY` in your environment (do not paste keys into chat). Get a key at https://bioportal.bioontology.org/register.

## salmonpy helper (Python mirror of metasalmon)
Use salmonpy for deterministic, code-based workflows when Python is preferred:
```python
import pandas as pd
from salmonpy import (
    infer_dictionary,
    validate_dictionary,
    suggest_semantics,
    create_salmon_datapackage,
    read_salmon_datapackage,
)

df = pd.DataFrame({"species": ["Coho", "Chinook"], "count": [10, 20]})
dict_df = infer_dictionary(df, dataset_id="demo", table_id="observations")
dict_df.loc[dict_df["column_name"] == "count", "column_role"] = "measurement"
dict_df = suggest_semantics(df, dict_df)  # access suggestions via dict_df.attrs["semantic_suggestions"]
validate_dictionary(dict_df)
```
