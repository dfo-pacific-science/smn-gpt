# DFO Salmon Data & Metadata Naming Conventions

*A cross‑domain convention for databases, tidy data, controlled vocabularies, and ontology alignment*

---

## 1. Purpose

This document defines a unified naming system used across the **DFO Salmon Ontology**, data dictionaries, SPSR‑like operational datasets, tidy analysis workflows, and metadata publication. It harmonizes:

- **ISO 11179** rules for data element naming
- **Darwin Core (DwC)** term patterns for interoperability
- **R Tidyverse** conventions for analysis-ready data
- **CONVENTIONS.md** ontology patterns (PascalCase classes, camelCase properties)

These conventions ensure that:
- Each concept has one clear name.
- Names are readable by biologists and predictable for machines.
- Datasets map cleanly into the ontology and controlled vocabularies.
- GPT-based tooling can reliably standardize legacy salmon datasets.

---

## 2. Core Principles

### 2.1 ISO 11179
Names must be:

- **Unique** — one concept → one name.
- **Atomic** — no compound meaning hiding in one element.
- **Consistent** — repeated concepts share structure.
- **Semantically transparent** — meaning is obvious.

### 2.2 Darwin Core Alignment
Darwin Core provides stable, predictable “shapes” for describing events, occurrences, measurements, metadata, and identifiers. Our conventions:
- Preserve DwC naming patterns where possible.
- Provide direct mappings for interoperability.
- Ensure that long-term salmon datasets can be shared using DwC or DwC-Event packages.

### 2.3 Tidyverse Alignment
Names must:
- Be in **lower_snake_case** for analysis.
- Avoid camelCase, dots, or spaces.
- Keep variables atomic.
- Do not encode analytic dimensions (age, location/stratum, method) in new tidy column names; represent them as separate columns or code lists.

### 2.4 Ontology Alignment (CONVENTIONS.md)
- **OWL Classes** → `PascalCase`
- **Properties** → `lowerCamelCase`
- **SKOS Concepts** → `PascalCase`
- Data fields → snake_case paired with optional `_iri` columns for mapping

---

## 3. Naming Rules Overview

### 3.1 Allowed Characters
- Only letters, numbers, and `_`
- No hyphens, dots, or spaces
- ASCII only

### 3.2 Structural Pattern
Every data element name follows:

```
<object_class>_<property>_<qualifier(s)>
```

Examples:
- `spawner_count_total`
- `catch_count_ocean`
- `run_size_terminal`
- `exploitation_rate_total`
- `spawner_count_age_5`

---

## 4. Object Classes

Object classes represent the entity being described. The following list is stable:

**Biological entities:**
- `spawner`
- `recruit`
- `run`
- `catch`
- `mortality`

**Spatial/fishery strata:**
- `ocean`
- `terminal`
- `mainstem`

**Metadata identifiers:**
- `cu`
- `smu`
- `survey_event`
- `project`
- `method`

**Examples:**
- `cu_id`
- `run_size_total`
- `catch_count_total`

---

## 5. Properties

Properties describe the characteristic being measured.

### 5.1 Common Properties
- `id` — unique identifier
- `count` — integer abundance
- `size` — total abundance/biomass/run size
- `rate` — proportion (0–1 or %)
- `code` — controlled vocabulary code
- `label` — human-readable text
- `type` — categorical classification
- `method` — enumeration/estimation method

### 5.2 Examples
- `spawner_count_total`
- `mortality_rate`
- `catch_count_total`

---

## 6. Qualifiers (dimensions) — don’t embed in tidy names

Qualifiers like age, location/stratum, and method are usually analytic dimensions. In new tidy tables, represent them as separate columns or code lists rather than encoding them in a metric name.

- **Age:** `age` (integer)
- **Location/stratum:** `stratum_code` (optionally `stratum_label`, `stratum_iri`)
- **Method:** `method_code` (optionally `method_label`, `method_iri`)

If you inherit legacy/wide columns that encode these dimensions, treat the suffixes as parseable hints and pivot/decompose into tidy columns.

Examples (legacy → tidy decomposition):
- `catch_count_ocean_age_3` → metric: `catch_count`; `stratum_code = ocean`; `age = 3`
- `mortality_rate_mainstem` → metric: `mortality_rate`; `stratum_code = mainstem`

---

## 7. Age-class handling (legacy wide → tidy long)

Legacy wide datasets often encode age in the column name (e.g., `SPAWNERS_AGE_5` or `spawner_count_age_5`). For new tidy datasets, keep the metric name age-agnostic (e.g., `spawner_count`) and store age in an `age` column.

Example:
- Legacy columns: `spawner_count_age_4`, `spawner_count_age_5`
- Tidy long columns: `age`, `spawner_count`

---

## 8. Controlled Vocabulary Mapping

For any field derived from a controlled vocabulary (SKOS Concept Scheme), keep the code value in the data table and treat `codes.csv` as the canonical lookup for labels/definitions/IRIs.

In data tables (canonical):
```
<concept>_code
```

Optional (derived for convenience/export; must match `codes.csv` when present):
```
<concept>_label
<concept>_iri
```

Example:
- Data table: `estimate_type_code = "2"`
- `codes.csv`: code lookup provides `code_label` and optional `term_iri` for that code value
- Optional derived columns: `estimate_type_label`, `estimate_type_iri`

---

## 9. Identifiers

Identifiers must be atomic and stable. Recommended:

- `cu_id`
- `cu_year_id`
- `smu_id`
- `survey_event_id`

Never concatenate elements:

Bad:
```
CUYEAR2023
```

Good:
```
cu_id
year
cu_year_id
```

---

## 10. Alignment With Darwin Core

### 10.1 Equivalent Patterns

| Darwin Core Term | Our Convention |
|------------------|----------------|
| `eventID` | `survey_event_id` |
| `eventDate` | `survey_event_date` |
| `measurementType` | `<metric>_label` |
| `measurementValue` | `<metric>_value` |
| `measurementUnit` | `<metric>_unit` or `<metric>_unit_iri` |

DwC terms themselves remain camelCase for external publication; internal and tidy use snake_case.

---

## 11. Alignment with the DFO Salmon Ontology

### 11.1 Mapping Data → Ontology

- Field names use **snake_case**.
- Ontology classes are **PascalCase**.
- Ontology properties are **lowerCamelCase**.
- Controlled vocabulary concepts have resolvable IRIs.

### 11.2 Example Mapping
Data field (canonical code value):
```
estimate_type_code = "2"
```

Then use a controlled vocabulary lookup (in SDP packages, `codes.csv`) to map the code to an ontology IRI when needed (optional derived field):
```
estimate_type_iri = "https://w3id.org/gcdfo/salmon#Type2"
```
Ontology:
```
:Type2 a skos:Concept ;
  skos:prefLabel "Type-2, True Abundance, Medium Resolution" .
```

This guarantees semantic clarity and validation.

---

## 12. Modernization of Legacy SPSR Fields

Legacy fields like:
```
MAINSTEM_AGE_1
SPAWNERS_AGE_5
TOTAL_OCEAN_RUN
```
Should be decomposed into:

- A base metric name (e.g., `catch_count`, `spawner_count`, `run_size`)
- One or more dimension columns (e.g., `age`, `stratum_code`)

Examples (decomposition targets):
- `SPAWNERS_AGE_5` → `spawner_count` with `age = 5`
- `TOTAL_OCEAN_RUN` → `run_size` with `stratum_code = ocean` (and `aggregation = total` if you need to represent “total” explicitly)
- `MAINSTEM_AGE_1` is ambiguous without context; resolve the base metric first, then represent `stratum_code = mainstem` and `age = 1`

---

## 13. Tidyverse Conventions

All analysis-ready datasets must:

- Use **lower_snake_case**.
- Avoid embedded units in names (e.g., `_pct`, `_num`).
- Store units in metadata or separate fields.
- Keep each variable atomic.
- Use long format for age, location, and method when appropriate.

### Example: Wide → Long
Wide legacy:
```
SPAWNERS_AGE_4, SPAWNERS_AGE_5
```
Long tidy:
```
age, spawner_count
```

---

## 14. Summary Cheatsheet

### ALWAYS
- `lower_snake_case` for data
- `PascalCase` for ontology classes
- `lowerCamelCase` for ontology properties
- `*_code` columns for vocabularies + `codes.csv` as the canonical lookup (derive `*_label`/`*_iri` only when needed)
- Keep variables atomic and unambiguous

### NEVER
- Hide compound meaning in a single name
- Mix cases or punctuation
- Embed Dewey-decimal-style logic in names
- Reuse codes or abbreviations

### Example Gold-Standard Record
```
cu_id = "20-001"
year = 2023
stratum_code = "ocean"
spawner_count_total = 15320
catch_count = 5321
exploitation_rate_total = 0.32
estimate_type_code = "2"
```

---

If you'd like, I can also produce a companion **data_dictionary_template.md** or a **translation map** that converts SPSR → standardized → ontology-aligned names.
