# SDP Schema Glossary (Shared)

SPECIFICATION.md is normative (normative means it defines what is valid). This glossary keeps field names and meanings aligned across prompts and docs.

## Files
- dataset.csv: dataset-level metadata (metadata means data about the data, like names and descriptions), one row per dataset.
- tables.csv: table-level metadata, one row per data file.
- column_dictionary.csv: column-level metadata, one row per column.
- codes.csv: code list metadata; required only when categorical columns exist (a categorical column stores codes or labels from a fixed list).

## Core identifiers
- dataset_id: stable identifier used to join rows across metadata files; prefer a DOI (Digital Object Identifier, a persistent identifier for a dataset or publication) when available.
- table_id: short table identifier; use snake_case (snake_case means lowercase words separated by underscores).
- column_name: exact column name in the data file, case sensitive.

## tables.csv fields
- file_name: relative path to the data file, no ../.
- table_label: human-readable label.
- description: what each row represents.
- observation_unit: the thing each row is about.
- observation_unit_iri: IRI (a web-style identifier for a concept) for the observation unit.
- primary_key: comma-separated column names that uniquely identify a row.

## column_dictionary.csv fields
- column_role: one of identifier, attribute, temporal, categorical, measurement.
- value_type: one of integer, number, string, boolean, date, datetime.
- term_iri: IRI for the meaning of the column; for measurement columns use a SKOS concept, and SKOS is a standard for controlled vocabularies. Required when column_role is measurement.
- term_type: one of:
  - skos_concept: a controlled vocabulary concept in SKOS, and SKOS is a standard for controlled vocabularies.
  - owl_class: a class in OWL, and OWL is a formal language for machine-readable models of concepts and relationships.
  - owl_object_property: a relationship in OWL between two things.
- unit_iri: IRI for the unit. Required when column_role is measurement.
- property_iri: I-ADOPT property IRI; I-ADOPT is a standard for describing variables by parts like property and entity. Required when column_role is measurement.
- entity_iri: I-ADOPT entity IRI. Required when column_role is measurement.
- constraint_iri: I-ADOPT constraint IRI; multiple values separated by `;`. Optional.
- method_iri: procedure/method IRI (aligns to SOSA `sosa:Procedure`; SOSA is the W3C/OGC observations vocabulary). Optional; fill when known. Not an I-ADOPT role.

## codes.csv fields
- code_value: stored code value in the data.
- code_label: human-readable label for the code.
- code_description: longer description of the code meaning.
- vocabulary_iri: IRI for the code system.
- term_iri: IRI for the specific code meaning.
- term_type: see term_type above.
- skos:notation: a code string attached to a SKOS concept; if term_iri points to a DFO SKOS concept with skos:notation, set code_value to that notation.

## gpt_proposed_terms.csv fields
- term_label: short name for a proposed term.
- term_definition: plain-language definition.
- definition_source_url: link to the definition source.
- term_type: see term_type above.
- suggested_parent_iri: IRI for the closest parent term.
- suggested_relationships: broader/narrower/related or OWL relationships.
- notes: extra context or constraints.
