# Salmon Data Package Specification

**Version**: sdp-0.1.0  
**Author**: Brett Johnson, Data Stewardship Unit (DFO Pacific Region Science Branch)

## Scope

This specification defines the required files and CSV schemas (a schema is the list of columns and rules for a file) for a Salmon Data Package (SDP). It is the only normative (rules that define validity) document for SDP validity.

## Package layout

A valid SDP package contains:

- `dataset.csv` - dataset-level metadata.
- `tables.csv` - table-level metadata.
- `column_dictionary.csv` - column-level metadata.
- `codes.csv` - controlled code lists (a controlled vocabulary is a defined list of allowed values) when categorical columns exist.
- One or more data files referenced from `tables.csv` (usually under `data/`).

Optional:

- `datapackage.json` - a JSON (a text format for structured data) descriptor used by external tooling (see `docs/implementation-guide.md`).

## CSV format rules

- Files are CSV (a text file where each row is a line and columns are separated by commas).
- Encoding is UTF-8 (a standard text encoding).
- The first row is a header row with column names.
- Fields containing commas, quotes, or newlines must be wrapped in double quotes; embedded quotes are doubled.
- Line endings may be LF or CRLF.
- Required fields must be non-empty.
- Optional columns may be omitted or left blank.
- Boolean fields use `TRUE` or `FALSE` (uppercase).
- Identifier matching is case-sensitive.

## Identifier rules

Identifiers are `dataset_id`, `table_id`, and `column_name`.

- `dataset_id` is an opaque identifier used to join across metadata files. It must be unique within the package. Prefer a DOI (Digital Object Identifier, a persistent identifier for a dataset or publication) when available; otherwise use a stable local identifier.
- `table_id` and `column_name` are constrained for tool-friendly joins:
  - Allowed characters: letters, numbers, and underscore.
  - Start with a letter or underscore.
  - `table_id` must be unique within a `dataset_id`.
  - `column_name` must be unique within a `table_id`.

## Data types

Value types used in `column_dictionary.csv`:

- `integer`: whole numbers only.
- `number`: numeric values with optional decimals.
- `string`: any text.
- `boolean`: `TRUE` or `FALSE` in metadata.
- `date`: ISO 8601 date (a standard date format) as `YYYY-MM-DD` or a year as `YYYY`.
- `datetime`: ISO 8601 datetime as `YYYY-MM-DDTHH:MM:SSZ` or with a timezone offset.

## `dataset.csv` schema

One row per dataset.

### Required columns

| Column | Type | Description |
| --- | --- | --- |
| dataset_id | string | Stable identifier used to join to other metadata files. Prefer a DOI (Digital Object Identifier, a persistent identifier for a dataset or publication) when available. |
| title | string | Human-readable dataset title. |
| description | string | Short description of the dataset contents and purpose. |
| creator | string | Name(s) of primary creator(s) or project. |
| contact_name | string | Primary contact person. |
| contact_email | string | Contact email address. |
| license | string | License name or URL (for example, `CC-BY-4.0`). |

### Optional columns

| Column | Type | Description |
| --- | --- | --- |
| temporal_start | date | Start date or year covered by the dataset. |
| temporal_end | date | End date or year covered by the dataset. |
| spatial_extent | string | Textual description of spatial coverage. |
| dataset_type | string | High-level dataset type. |
| source_citation | string | Citation for reports or publications. |
| provenance_note | string | Narrative about data lineage. |
| created | datetime | Timestamp when the dataset was created. |
| modified | datetime | Timestamp when the dataset was last modified. |
| spec_version | string | SDP specification version (for example, `sdp-0.1.0`). |

## `tables.csv` schema

One row per table in the package.

### Required columns

| Column | Type | Description |
| --- | --- | --- |
| dataset_id | string | References `dataset_id` in `dataset.csv`. |
| table_id | string | Short ID for the table. |
| file_name | string | Relative path to the data file (must not use `../`). |
| table_label | string | Human-readable label for the table. |
| description | string | Description of what each row represents. |

### Optional columns

| Column | Type | Description |
| --- | --- | --- |
| observation_unit | string | Human-readable label for the observation unit (the thing each row is about). |
| observation_unit_iri | string | IRI (a web identifier that points to a concept on the internet) for the observation unit class. |
| primary_key | string | Comma-separated list of column names forming a primary key (a column or set of columns that uniquely identifies each row), no spaces. |

## `column_dictionary.csv` schema

One row per column in each table.

### Required columns

| Column | Type | Description |
| --- | --- | --- |
| dataset_id | string | References `dataset_id` in `dataset.csv`. |
| table_id | string | References `table_id` in `tables.csv`. |
| column_name | string | Exact column name in the data file (case-sensitive). |
| column_label | string | Human-readable label. |
| column_description | string | Clear definition of the column's meaning. |
| column_role | string | One of `identifier`, `attribute`, `temporal`, `categorical`, `measurement`. |
| value_type | string | One of `integer`, `number`, `string`, `boolean`, `date`, `datetime`. |

### Optional columns

| Column | Type | Description |
| --- | --- | --- |
| required | boolean | `TRUE` if the column is required for each row, otherwise `FALSE` or blank. |
| unit_label | string | Human-readable unit label. |
| unit_iri | string | IRI for the unit. Required for measurement columns. |
| term_iri | string | IRI for the term that represents what the column measures or represents. Required for measurement columns. Use a SKOS concept (a controlled vocabulary term) for compound variables. |
| term_type | string | Type of term: `owl_class` (an ontology class, where an ontology is a formal model of concepts and relations, defined in OWL, the Web Ontology Language), `owl_object_property` (an ontology relationship in OWL), or `skos_concept` (a controlled vocabulary term in SKOS, a W3C standard for controlled vocabularies). |
| property_iri | string | I-ADOPT property IRI (I-ADOPT is a standard for describing variables by parts like property and entity). Required for measurement columns. |
| entity_iri | string | I-ADOPT entity IRI (what the measurement is about). Required for measurement columns. |
| constraint_iri | string | I-ADOPT constraint IRI(s). Optional; separate multiple IRIs with `;`. |
| method_iri | string | Procedure/method IRI (aligns to SOSA `sosa:Procedure`; SOSA is the W3C/OGC observations vocabulary). Optional; fill when known. Not an I-ADOPT role. |

### Measurement column requirements

A measurement column (a column whose values are the observed or computed quantity) must include:

- `unit_iri`
- `term_iri`
- `property_iri`
- `entity_iri`

`constraint_iri` and `method_iri` are optional.

## `codes.csv` schema

One row per allowed code value in a categorical column. Required only when categorical columns exist.

### Required columns

| Column | Type | Description |
| --- | --- | --- |
| dataset_id | string | References `dataset_id` in `dataset.csv`. |
| table_id | string | References `table_id` in `tables.csv`. |
| column_name | string | Column name in the data file that uses this code. |
| code_value | string | Stored value in the data. Required unless `vocabulary_iri` is provided. |

### Optional columns

| Column | Type | Description |
| --- | --- | --- |
| code_label | string | Human-readable label corresponding to the code. |
| code_description | string | Longer description of what the code means. |
| vocabulary_iri | string | IRI for the controlled vocabulary system (the system that defines valid values). |
| term_iri | string | IRI for the specific term that `code_value` represents. Recommended for machine-readable integration. |
| term_type | string | Type of term (for example, `skos_concept` or `owl_class`). |

### Codes rules

- `code_value` is required unless `vocabulary_iri` is provided.
- If `code_value` is present, providing `term_iri` is strongly recommended for machine-readable integration.
- Treat `codes.csv` as canonical (single source of truth) for code meaning (labels/descriptions) and optional code-level IRIs. In data files, prefer storing only the code value and join to `codes.csv` when you need labels/IRIs; avoid duplicating `*_label` / `*_iri` columns unless generating a derived export.
- If no categorical columns exist, `codes.csv` may be omitted.

## Versioning and extensions

- Add new optional columns in a backwards-compatible way; tools must ignore unknown columns.
- Breaking changes to required columns or semantics should bump the major version.

## Non-normative guides

These documents provide guidance and implementation detail but do not change validity rules:

- `docs/quickstart.md`
- `docs/implementation-guide.md`
- `docs/i-adopt-integration-guide.md`
- `docs/sdp-profile-schema-guide.md`
