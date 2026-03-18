# GitHub Issue Templates for DFO Salmon Ontology

When proposing new terms or changes to the DFO Salmon Ontology, use these templates to create GitHub issues.

**Tracker URL**: https://github.com/dfo-pacific-science/dfo-salmon-ontology/issues

---

## 1. New Term Request

Use this template when no existing term fits and you need to propose a new concept.

**Issue URL**: https://github.com/dfo-pacific-science/dfo-salmon-ontology/issues/new?template=new-term-request.md

### Template

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

### Filled Example (Marine Survival Rate)

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

* **Definition source (required):** DFO Pacific Region salmon assessment documentation

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

---

## 2. Missing Superclass (Parent) Request

Use this template when an existing term needs a new parent class added.

**Issue URL**: https://github.com/dfo-pacific-science/dfo-salmon-ontology/issues/new?template=missing-superclass.md

### Template

```markdown
---
name: Missing superclass
about: Request a new superclass (parent) to be added to an existing GCDFO term
title: 'Missing parent: [Term IRI and label]'
labels: missing parentage
assignees: ''
---

* DFO term IRI and label for which you are requesting a new superclass:

* New superclass suggested:

* Reference(s):
```

### Filled Example

```markdown
---
name: Missing superclass
about: Request a new superclass (parent) to be added to an existing GCDFO term
title: 'Missing parent: https://w3id.org/gcdfo/salmon#EscapementMeasurement'
labels: missing parentage
assignees: ''
---

* DFO term IRI and label for which you are requesting a new superclass:
  https://w3id.org/gcdfo/salmon#EscapementMeasurement (Escapement Measurement)

* New superclass suggested:
  iao:0000109 (Measurement Datum) from the Information Artifact Ontology

* Reference(s):
  IAO documentation: http://purl.obolibrary.org/obo/iao.owl
```

---

## 3. Term Definition Update

Use this template to suggest an improved or corrected definition for an existing term.

**Issue URL**: https://github.com/dfo-pacific-science/dfo-salmon-ontology/issues/new?template=term-definition-update.md

### Template

```markdown
---
name: Term definition update
about: Suggest an alternative definition for an existing GCDFO term
title: 'Update definition: [Term IRI and label]'
labels: textual definition
assignees: ''
---

* GCDFO term IRI and label for which you are requesting a definition update:

* New proposed definition:

* Definition source:

* Additional information/rationale for change in definition:
```

### Filled Example

```markdown
---
name: Term definition update
about: Suggest an alternative definition for an existing GCDFO term
title: 'Update definition: https://w3id.org/gcdfo/salmon#ConservationUnit'
labels: textual definition
assignees: ''
---

* GCDFO term IRI and label for which you are requesting a definition update:
  https://w3id.org/gcdfo/salmon#ConservationUnit (Conservation Unit)

* New proposed definition:
  A group of wild salmon sufficiently isolated from other groups that, if extirpated, is very unlikely to recolonize naturally within an acceptable timeframe, as defined under Canada's Wild Salmon Policy.

* Definition source:
  DFO Wild Salmon Policy (2005)

* Additional information/rationale for change in definition:
  Added "wild salmon" and "Canada's Wild Salmon Policy" for specificity.
```

---

## 4. Term Obsoletion (Deprecation) Request

Use this template to request that a term be deprecated/obsoleted.

**Issue URL**: https://github.com/dfo-pacific-science/dfo-salmon-ontology/issues/new?template=term-obsoletion.md

### Template

```markdown
---
name: Term obsoletion
about: Request a DFO Salmon Term to be deprecated
title: 'Obsolete term: [Term IRI and label]'
labels: obsoletion
assignees: ''
---

Please provide as much information as you can:

* DFO term IRI and and label:
* Reason for deprecation (put an X in the appropriate box):
[ ] The reason for obsoletion is that the term is not clearly defined and usage has been inconsistent.
[ ] The reason for obsoletion is that more specific terms were created.
[ ] The reason for obsoletion is that this term was an unnecessary grouping term.
[ ] The reason for obsoletion is that the meaning of the term is ambiguous.

* "Replace by" term (ID and label):
- If all annotations can safely be moved to that term

* "Consider" term(s) (ID and label)
- Suggestions for reannotating
- Are there annotations to this term?
- Are there mappings and cross-references to this term?
- Any other information
```

---

## Batch Submission Guidance

### When to Submit Individual Issues
- Terms requiring distinct review or discussion
- Terms with complex parent relationships
- Terms where definition source is uncertain

### When to Group Related Terms
Group into a single issue when terms share the same pattern and parent:
- **Temporal conventions**: brood year, catch year, return year
- **Mortality rates**: in-river mortality, mainstem mortality, ocean mortality, terminal mortality
- **Age conventions**: Gilbert-Rich age notation, European age notation
- **Reference points**: LRP, USR, various benchmarks

### Grouped Issue Example

```markdown
---
name: New term request
title: 'New term request: Mortality rate variants (batch)'
labels: new term request
---

Requesting a set of related mortality rate terms that share the same parent and structure.

**Parent for all**: https://w3id.org/gcdfo/salmon#MortalityRate

| Term Label | Definition | Constraint |
|------------|------------|------------|
| In-river Mortality Rate | Proportion of fish that die in freshwater during upstream migration | freshwater_location |
| Mainstem Mortality Rate | Proportion of fish that die in mainstem river reaches | mainstem_location |
| Ocean Mortality Rate | Proportion of fish that die during ocean residence | ocean_phase |
| Terminal Mortality Rate | Proportion of fish that die in terminal fishing areas | terminal_area |

**Definition source**: DFO Pacific Region salmon assessment terminology

**I-ADOPT decomposition** (common to all):
- property_iri: http://qudt.org/vocab/quantitykind/DimensionlessRatio
- entity_iri: https://w3id.org/gcdfo/salmon#Stock
- unit_iri: http://qudt.org/vocab/unit/UNITLESS
```

---

## Mapping gpt_proposed_terms.csv to Issues

When you have a `gpt_proposed_terms.csv` file, convert each row to an issue:

| CSV Column | Issue Field |
|------------|-------------|
| term_label | Suggested term label |
| term_definition | Definition |
| definition_source_url | Definition source |
| suggested_parent_iri | Parent term(s) |
| suggested_relationships | Synonyms / Cross-references |
| notes | Any other information |
| term_type | Determines if OWL class or SKOS concept (note in "other information") |
