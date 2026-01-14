# Tidy Data Guide for DFO Salmon Data

*Practical conventions for transforming messy salmon datasets into analysis‑ready, ontology‑aware, FAIR-compliant structures*

---

## 1. Purpose

This guide defines how salmon datasets should be structured for:
- **Data analysis** (R/Tidyverse, Python/pandas)
- **Interoperability** (Darwin Core, schema.org, DwC-Event)
- **Ontology integration** (DFO Salmon Ontology measurement patterns)
- **Controlled vocabulary alignment** (SKOS concept schemes)
- **Metadata publication** (Open Government of Canada)

The goal is to give biologists and analysts simple, predictable rules for cleaning, validating, joining, transforming, and publishing salmon data.

This complements the DSU’s **Naming Conventions** and **Ontology Conventions**.

---

## 2. Core Principles

### 2.1 Wickham’s Tidy Data Rules
Data must follow the three canonical rules:

1. **Each variable is a column.**
2. **Each observation is a row.**
3. **Each observational unit type is its own table.**

These rules eliminate ambiguity, allow automatic validation, and enable GPT-driven transformations.

### 2.2 No Embedded Semantics in Columns
Column names may **not** encode:
- Age classes (e.g., `Age_5`)
- Locations (e.g., `Ocean`, `Terminal`)
- Methods (e.g., `Sonar`, `Visual`)
- Seasons or strata (`Early`, `Late`)
- Statistical treatments (`LogitSmooth`)

Instead, each becomes a **column** or maps to a **controlled vocabulary**.

### 2.3 Alignment with the DFO Salmon Ontology
- Measurements follow the ontology’s `Measurement` pattern.
- Classifications map to SKOS concept schemes.
- Units may be linked via QUDT IRIs when appropriate.
- Observational events map to Darwin Core `dwc:Event`.

### 2.4 Reproducibility and Validation
Tidy data allows:
- SHACL validation
- Version-controlled data dictionaries
- Automated quality checks
- Consistent metadata generation

---

## 3. Recommended Table Types

### 3.1 CU–Year Index Table (SPSR-like)
One row per **CU–Year** (or one row per **CU–Year × stratum** in long form).

Columns represent:
- Identifiers: `cu_id`, `cu_year_id`, `year`
- Abundance metrics: `spawner_count_total`, `run_size_total`, `catch_count_total`
- Rates: `exploitation_rate_total`, `mortality_rate` (if rates vary by stratum/location, add a stratum column rather than encoding `_ocean`/`_terminal` in the metric name)
- Age-specific counts (long form preferred):
  - `age`
  - `spawner_count` or `catch_count`
- Metadata: `method_analysis`, `method_collection`, `estimate_type_code`

This is the **primary tidy dataset** for many salmon workflows.

### 3.2 Survey Event Table
If survey events are being retained:
- `survey_event_id`
- `cu_id`
- `survey_event_date`
- `enumeration_method_code`
- Spatial metadata (waterbody, reach, etc.)
- Observation-level detail (counts, efficiency estimates)

Maps to **Darwin Core Event + Measurement**.

### 3.3 Controlled Vocabulary Reference Tables
In SDP packages, `codes.csv` is the canonical (single source of truth) reference table for controlled vocabularies: it defines allowed code values plus labels/descriptions and (optionally) ontology IRIs.

In data tables:
- Store the value in a single `*_code` column.
- Join to `codes.csv` when you need human-readable labels or IRIs.

Optional (derived for convenience/export; must match `codes.csv` when present):
- `*_label`
- `*_iri`

Examples:
- Enumeration Method Scheme
- Estimate Type Scheme
- Life History Type Scheme

### 3.4 Spatial Lookup Tables
For CU, SMU, or stream reach definitions.

---

## 4. Wide vs Long Format

### 4.1 Use Long Format for:
- **Age classes**: preferred for most analysis and ontology alignment.
- **Life-stage counts**.
- **Method-stratified counts**.
- **Temporal measurements** (daily, weekly, survey-by-survey).

Example (wide legacy → long tidy):

Wide legacy:
```
SPAWNERS_AGE_3, SPAWNERS_AGE_4, SPAWNERS_AGE_5
```

Long tidy:
```
age, spawner_count
3,   120
4,   430
5,   210
```

### 4.2 Use Wide Format Sparingly
Wide format is acceptable for **operational schemas** like SPSR where interpretation is straightforward and columns are stable.

However, wide format should **always** be normalized to tidy format before analysis.

---

## 5. Identifier Conventions

### 5.1 Required Keys
Every tidy table must include:

- `cu_id` — authoritative CU identifier
- `year` — observation year (calendar or brood)
- `cu_year_id` — surrogate key for CU–Year combos

### 5.2 Survey Event IDs
Survey data must include:
- `survey_event_id` — unique ID per event
- `survey_event_date` — ISO 8601 date

### 5.3 Avoid Composite Keys
Names like `CUYEAR2022` must be avoided.

Use separate fields, then a surrogate key if needed.

---

## 6. Controlled Vocabulary Columns

### 6.1 Code + Lookup Pattern
Store a controlled vocabulary value once (as a code) and keep labels/IRIs in a canonical lookup table (in SDP, `codes.csv`).

```
<name>_code
```

Example:
```
estimate_type_code = "2"
```

Then, when needed, derive convenience columns by joining to the lookup table (these should match `codes.csv` when present):

```
estimate_type_label = "Type‑2, True Abundance"
estimate_type_iri = "https://w3id.org/gcdfo/salmon#Type2"
```

This is fully compatible with:
- Ontology reasoning
- R Tidyverse filtering/grouping
- JSON-LD metadata
- SHACL validation

---

## 7. Units and Measurement Standards

### 7.1 Units Must Be Explicit
Do not encode units in column names.

Bad:
- `mortality_rate_pct`

Good:
- `mortality_rate`
- `mortality_rate_unit = "percent"`
- `mortality_rate_unit_iri = "http://qudt.org/vocab/unit#Percent"`

### 7.2 Ontology Integration
Measurements correspond to ontology `Measurement` classes.

Store:
- Value: `<metric>_value`
- Unit: `<metric>_unit`
- IRI: `<metric>_unit_iri`

---

## 8. Temporal Variables

### 8.1 Standard Columns
- `year`
- `brood_year`
- `calendar_year`
- `season`
- `survey_event_date`

Use ISO formats:
- Dates: `YYYY‑MM‑DD`
- Years: `YYYY`
- Year types: use CV codes

---

## 9. Spatial Variables

Spatial data must:
- Use authoritative names for CUs, SMUs, watersheds.
- Include clear identifiers: `cu_id`, `smu_id`, etc.
- Avoid ambiguous natural language strings.

Where possible, link spatial codes to resolvable IRIs.

---

## 10. Tidy Data Pipelines

Recommended tidy operations in R:

- `rename()` using naming conventions
- `pivot_longer()` for age, stratum, or method dimensions (especially when inherited legacy wide columns encode them)
- `left_join()` with controlled vocabulary tables
- `mutate()` to add IRI columns
- `validate_*()` (SHACL or custom functions) for QC

Example transformation:

```
library(dplyr)
library(tidyr)

data_long <- spsr_raw %>%
  rename_with(tolower) %>%
  pivot_longer(
    cols = matches("^spawners_age_\\d+$"),
    names_to = "age",
    names_pattern = "^spawners_age_(\\d+)$",
    values_to = "spawner_count"
  ) %>%
  mutate(age = as.integer(age))
```

---

## 11. Publication to Open Government

Tidy data enables:
- Simple JSON-LD transformation
- Cleaner metadata mapping (keywords, temporal/spatial coverage)
- Transparent lineage and versioning

### Best Practices
- Keep identifiers stable across releases.
- Provide a full data dictionary with `name`, `definition`, `iri`.
- Ensure code lists are included or linked.

---

## 12. Summary Cheat Sheet

### ALWAYS
- Use lower_snake_case
- Keep each variable atomic
- Store controlled vocabularies using `code`, `label`, `iri`
- Use long format for age, method, or strata
- Use ISO dates
- Keep units explicit and separate

### NEVER
- Encode age, location, or method in a single wide column name
- Mix units in one column
- Embed metadata inside variable names
- Use ambiguous labels

---

If you'd like, I can create:
- A **wide_to_long_recipes.md** cheat sheet
- A **data_dictionary_template.md** for consistent documentation
- A **metadata_mapping_open_gov.md** guide for JSON-LD publication
