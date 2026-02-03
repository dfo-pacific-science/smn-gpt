# Vocabulary and ontology guidance (SDP semantics)

This repo treats `https://w3id.org/gcdfo/salmon` (DFO Salmon Ontology; prefix `gcdfo:`) as the canonical namespace for salmon-domain semantics, and uses external vocabularies for interoperability and I-ADOPT decompositions.

Key idea: **canonical identity** lives in `gcdfo:` when the concept is salmon-specific; **external IRIs** are used for alignment, decomposition parts, or broadly reusable concepts.

Definitions used below:

- **Primary source**: the external IRI is treated as canonical for the concept (we do not mint a new `gcdfo:` term for it).
- **Alignment**: `gcdfo:` is canonical, and we link external IRIs with mapping predicates (usually `skos:exactMatch` / `skos:closeMatch`).

Prefix shorthands used in this doc (expand to full HTTP IRIs in data files):

- `gcdfo:` → `https://w3id.org/gcdfo/salmon#`
- `dwc:` → `http://rs.tdwg.org/dwc/terms/`
- `dwciri:` → `http://rs.tdwg.org/dwc/iri/` (RDF usage when the object is an IRI)

## Rules of thumb

- **Check `gcdfo:` first**; reuse an existing term when it fits.
- **Prefer well-governed external vocabularies** when the concept is cross-domain and widely standardized.
- **NEVER invent IRIs**; if you can’t find a suitable term, leave it blank and add `gpt_proposed_terms.csv`.

## Recommended sources by SDP field

### `term_iri` (measurement columns)

Preferred order:

1. `gcdfo:` **SKOS variable concept** (compound metric/variable) when available (aligns with `CONVENTIONS.md` “variables as SKOS concepts” guidance).
2. External **variable/observable** vocabularies when the concept is genuinely cross-domain (examples from the I-ADOPT catalogue: CF Standard Names, BODC P01, CMO, ICES parameters).
3. As a last resort, a Darwin Core term IRI (e.g., `http://rs.tdwg.org/dwc/terms/individualCount`) only when the column is intended to be *the Darwin Core property* (typical in DwC Archives and `dwc:MeasurementOrFact`, i.e., “a measurement row with `dwc:measurementType` / `dwc:measurementValue` / `dwc:measurementUnit`”). In this case you are pointing at an `rdf:Property`, not a variable concept.

If you use a non-`gcdfo:` `term_iri` for a salmon-specific variable, add a proposed `gcdfo:` variable concept:

- If the external identifier is a concept/variable IRI, align later with `skos:exactMatch` / `skos:closeMatch`.
- If the external identifier is an RDF property (e.g., a Darwin Core `dwc:` term), treat it as a predicate-level mapping (not `skos:*Match`) and plan to replace `term_iri` with the `gcdfo:` variable concept when available.

### `property_iri` (I-ADOPT property)

Preferred order:

1. `gcdfo:` term (when a salmon-specific observable/property exists).
2. QUDT quantity kinds (`http://qudt.org/vocab/quantitykind/`).
3. PATO qualities (`http://purl.obolibrary.org/obo/PATO_`).
4. Other I-ADOPT-catalogued property vocabularies (for example: SVO, SWEET, ECSO).

### `unit_iri`

- Use **QUDT units** (`http://qudt.org/vocab/unit/`) consistently, even if the unit was discovered via another catalogue.

### `entity_iri` (I-ADOPT object of interest)

Preferred order:

1. `gcdfo:` OWL class (salmon management/assessment entities).
2. Darwin Core classes for general scaffolding (`dwc:Organism`, `dwc:Event`, `dwc:MaterialEntity`).
3. ENVO classes for environmental entities when needed.

### `constraint_iri` (I-ADOPT constraints)

Preferred order:

1. `gcdfo:` SKOS constraint concept (life stage, origin, year-basis, spatial/fishery strata).
2. External constraint vocabularies that match the domain (commonly ENVO; CF where appropriate).
3. **AGROVOC** SKOS concepts for broad fisheries/agriculture concepts (reasonable as a lightweight fallback; can be primary for broad, non-salmon-specific constraints; prefer `gcdfo:` for salmon-specific constraints and align to AGROVOC when helpful).
4. **Wikidata** only as an alignment target (crosswalk/reconciliation), not a primary constraint vocabulary.

### `method_iri` (procedure/method; SOSA-aligned)

I-ADOPT does not model methods/procedures. Use `method_iri` to record the procedure/method IRI for how a measurement was produced (aligns to SOSA `sosa:Procedure`, where SOSA is the W3C/OGC observations vocabulary).

Preferred order:

1. `gcdfo:` procedure/method concept (SKOS) when available.
2. External method vocabularies (for example, NERC NVS method collections or OBI) when you need community identifiers.
3. Otherwise propose a new `gcdfo:` procedure/method concept.

## Notes on specific resources

### Darwin Core

Darwin Core (http://rs.tdwg.org/dwc/terms/) is best treated as an **interoperability scaffold** for observation/event/organism modeling and for naming widely-shared metadata fields. Many DwC terms are RDF properties; use them when you actually mean a DwC property (for example, `dwc:eventDate`). In RDF, the Darwin Core RDF Guide distinguishes `dwc:` terms (generally literal objects) from `dwciri:` terms (use when the object is an IRI, e.g., controlled-vocabulary values for `measurementType` / `measurementUnit` / `lifeStage`).

### AGROVOC

AGROVOC is a multilingual controlled vocabulary maintained by FAO (“a multilingual and controlled vocabulary… a relevant Linked Open Data set…”: https://aims.fao.org/agrovoc). It is strong for general fisheries/agriculture concepts and indexing, but it is not optimized for precise observable-property decomposition; use it mainly for code lists and alignments.

### Wikidata

Wikidata data is CC0 (“All structured data… is made available under… CC0”: https://www.wikidata.org/wiki/Wikidata:Licensing). It has broad coverage but community-edited modeling; prefer authoritative domain identifiers (for example, GBIF Backbone for taxa) and use Wikidata primarily for crosswalks.

### Why the I-ADOPT catalogue omits some vocabularies

The I-ADOPT Catalogue of Terminologies (https://i-adopt.github.io/terminologies/) is curated and non-exhaustive; it is designed to list terminologies that can help fill I-ADOPT roles. Absence (for example: AGROVOC, Darwin Core, Wikidata) is typically scope/curation, not a prohibition; missing resources can be proposed upstream via https://github.com/i-adopt/terminologies.

---

## Top-Down Ontology Alignment Strategy

This section describes how to align `gcdfo:` (DFO Salmon Ontology) with established upper-level and domain ontologies. The alignment follows a **top-down approach**: we identify the most general ontological commitments first (BFO/IAO), then progressively specialize through observation/provenance patterns (SOSA/PROV), variable decomposition (I-ADOPT), and finally biodiversity interoperability (Darwin Core).

### Alignment Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│  BFO (Basic Formal Ontology) - Top-Level Ontology          │
│    └── IAO (Information Artifact Ontology)                  │
│          └── PROV-O (Provenance Ontology)                   │
│                └── SOSA/SSN (Observations & Sensors)        │
│                      └── I-ADOPT (Variable Decomposition)   │
│                            └── Darwin Core (Biodiversity)   │
│                                  └── gcdfo: (Salmon Domain) │
└─────────────────────────────────────────────────────────────┘
```

### BFO (Basic Formal Ontology)

**Namespace:** `http://purl.obolibrary.org/obo/BFO_`
**Purpose:** Provides the foundational ontological distinctions for all domain classes.

BFO is an ISO/IEC standard (ISO/IEC 21838-2:2021) top-level ontology that distinguishes:
- **Continuants** (entities that persist through time): Independent continuants (organisms, material entities) vs. dependent continuants (qualities, roles, functions)
- **Occurrents** (entities that unfold in time): Processes, temporal regions

**Alignment guidance for `gcdfo:`:**

| gcdfo: Class Type | BFO Alignment | Example |
|-------------------|---------------|---------|
| Physical entities (salmon, samples) | `BFO:0000040` (material entity) | `gcdfo:SalmonSpecimen rdfs:subClassOf BFO:0000040` |
| Qualities/properties | `BFO:0000019` (quality) | `gcdfo:ForkLength rdfs:subClassOf BFO:0000019` |
| Roles | `BFO:0000023` (role) | `gcdfo:BreederRole rdfs:subClassOf BFO:0000023` |
| Processes/activities | `BFO:0000015` (process) | `gcdfo:SpawningEvent rdfs:subClassOf BFO:0000015` |
| Temporal regions | `BFO:0000008` (temporal region) | Return year spans |

**When to use BFO alignment:**
- Creating new OWL classes that need rigorous ontological grounding
- Ensuring interoperability with OBO Foundry ontologies (ENVO, OBI, etc.)
- When reasoning over fundamental entity types is required

**References:**
- [BFO Official Site](https://basic-formal-ontology.org/)
- [OBO Foundry BFO](https://obofoundry.org/ontology/bfo.html)
- [BFO ISO Standard](https://www.iso.org/standard/74572.html)

### IAO (Information Artifact Ontology)

**Namespace:** `http://purl.obolibrary.org/obo/IAO_`
**Purpose:** Models information entities, data items, and their relationships to what they are about.

IAO extends BFO to handle information artifacts—entities whose function is to bear information quality. Key classes include:

| IAO Class | IRI | Use Case |
|-----------|-----|----------|
| `information content entity` | `IAO:0000030` | Parent class for all data/information |
| `data item` | `IAO:0000027` | Truthful statements about something |
| `measurement datum` | `IAO:0000109` | Results of measurements |
| `specification` | `IAO:0000104` | Protocols, methods |
| `document` | `IAO:0000310` | Reports, publications |

**Key property:** `IAO:0000136` (`is about`) – relates an information entity to what it describes.

**Alignment guidance for `gcdfo:`:**

```turtle
# A salmon assessment data item
gcdfo:EscapementEstimate rdfs:subClassOf IAO:0000027 ;
    IAO:0000136 gcdfo:SalmonPopulation .  # is about the population

# A sampling protocol specification
gcdfo:MarkRecaptureProtocol rdfs:subClassOf IAO:0000104 .
```

**When to use IAO alignment:**
- Modeling datasets, data items, or measurement results as first-class entities
- Distinguishing between the measured property (quality) and the recorded datum (information)
- Linking data to what it is about (especially for provenance)

**References:**
- [IAO GitHub](https://github.com/information-artifact-ontology/IAO)
- [OBO Foundry IAO](https://obofoundry.org/ontology/iao.html)

### PROV-O (Provenance Ontology)

**Namespace:** `http://www.w3.org/ns/prov#`
**Purpose:** Models provenance—how entities came to be, who/what was responsible, and what activities produced them.

PROV-O provides a W3C-standard vocabulary for provenance tracking:

| PROV Class | Description | gcdfo: Mapping |
|------------|-------------|----------------|
| `prov:Entity` | Things with provenance | Data products, samples, assessments |
| `prov:Activity` | Actions that transform/generate entities | Sampling events, observations, analyses |
| `prov:Agent` | Actors responsible for activities | Organizations, sensors, software |

**Key properties:**
- `prov:wasGeneratedBy` – Entity → Activity
- `prov:wasAttributedTo` – Entity → Agent
- `prov:used` – Activity → Entity
- `prov:wasAssociatedWith` – Activity → Agent
- `prov:wasDerivedFrom` – Entity → Entity

**PROV-SOSA Alignment (W3C standard):**

The W3C provides an official alignment between SOSA and PROV-O:

```turtle
# From W3C sosa-prov-mapping.ttl
sosa:Observation rdfs:subClassOf prov:Activity .
sosa:Sensor rdfs:subClassOf prov:Agent .
sosa:Sample rdfs:subClassOf prov:Entity .
sosa:Result rdfs:subClassOf prov:Entity .
sosa:resultTime rdfs:subPropertyOf prov:endedAtTime .
sosa:usedProcedure rdfs:subPropertyOf prov:hadPlan .
```

**Guidance for `gcdfo:`:**

```turtle
# An escapement survey is both a SOSA Sampling and a PROV Activity
gcdfo:EscapementSurvey rdfs:subClassOf sosa:Sampling , prov:Activity .

# The DFO agency as an agent
gcdfo:DFO rdf:type prov:Organization ;
    prov:actedOnBehalfOf gcdfo:GovernmentOfCanada .

# Derived data products
gcdfo:EscapementEstimate2024 prov:wasDerivedFrom gcdfo:RawCountData2024 ;
    prov:wasGeneratedBy gcdfo:MarkRecaptureAnalysis2024 ;
    prov:wasAttributedTo gcdfo:DFOStockAssessment .
```

**When to use PROV-O:**
- Tracking data lineage and derivation chains
- Attributing data products to responsible agents
- Documenting analytical workflows

**References:**
- [PROV-O W3C Recommendation](https://www.w3.org/TR/prov-o/)
- [SOSA-PROV Mapping](https://github.com/w3c/sdw/blob/gh-pages/ssn/rdf/sosa-prov-mapping.ttl)
- [PROV-to-BFO Mappings](https://github.com/BFO-Mappings/PROV-to-BFO)

### SOSA/SSN (Sensor, Observation, Sample, Actuator)

**Namespaces:**
- SOSA (lightweight core): `http://www.w3.org/ns/sosa/`
- SSN (full): `http://www.w3.org/ns/ssn/`

**Purpose:** Models observations, sampling, sensors, and the properties being observed.

SOSA/SSN is a W3C/OGC standard that provides the core observation pattern:

```
┌─────────────┐     observes      ┌───────────────────┐
│   Sensor    │──────────────────▶│ ObservableProperty │
└─────────────┘                   └───────────────────┘
       │                                    │
       │ madeObservation           isPropertyOf
       ▼                                    ▼
┌─────────────┐  hasFeatureOfInterest ┌───────────────────┐
│ Observation │──────────────────────▶│ FeatureOfInterest │
└─────────────┘                       └───────────────────┘
       │
       │ hasResult
       ▼
┌─────────────┐
│   Result    │
└─────────────┘
```

**Key SOSA classes for salmon data:**

| SOSA Class | Description | gcdfo: Example |
|------------|-------------|----------------|
| `sosa:Observation` | Act of observing a property | Count of fish at weir |
| `sosa:Sampling` | Act of creating/transforming samples | Collecting scale samples |
| `sosa:Sample` | Representative subset | Scale sample, tissue sample |
| `sosa:Sensor` | Device/agent making observations | Weir counter, human observer |
| `sosa:Procedure` | Method/protocol followed | Mark-recapture protocol |
| `sosa:FeatureOfInterest` | Entity being observed | Salmon population, river reach |
| `sosa:ObservableProperty` | Quality being measured | Abundance, fork length |
| `sosa:Result` | Outcome of observation | Count value with uncertainty |

**Key SOSA properties:**

| Property | Domain | Range | Use |
|----------|--------|-------|-----|
| `sosa:hasFeatureOfInterest` | Observation/Sampling | FeatureOfInterest | What was observed |
| `sosa:observedProperty` | Observation | ObservableProperty | What property was measured |
| `sosa:hasResult` | Observation | Result | The measurement outcome |
| `sosa:usedProcedure` | Observation | Procedure | Method used |
| `sosa:madeBySensor` | Observation | Sensor | What made the observation |
| `sosa:phenomenonTime` | Observation | time:TemporalEntity | When the property applied |
| `sosa:resultTime` | Observation | xsd:dateTime | When observation completed |
| `sosa:isSampleOf` | Sample | FeatureOfInterest | What the sample represents |

**Example alignment for salmon escapement:**

```turtle
@prefix gcdfo: <https://w3id.org/gcdfo/salmon#> .
@prefix sosa: <http://www.w3.org/ns/sosa/> .
@prefix qudt: <http://qudt.org/vocab/unit/> .

# The escapement count observation
gcdfo:escapement_count_2024_001 a sosa:Observation ;
    sosa:hasFeatureOfInterest gcdfo:FraserRiverSockeye ;
    sosa:observedProperty gcdfo:Escapement ;
    sosa:usedProcedure gcdfo:WeirCountProtocol ;
    sosa:madeBySensor gcdfo:HellsGateWeir ;
    sosa:phenomenonTime "2024-08-15"^^xsd:date ;
    sosa:hasResult [
        a sosa:Result ;
        qudt:numericValue 125000 ;
        qudt:unit qudt:NUM
    ] .

# A scale sample
gcdfo:scale_sample_001 a sosa:Sample ;
    sosa:isSampleOf gcdfo:FraserRiverSockeye ;
    sosa:isResultOf gcdfo:sampling_event_001 .
```

**When to use SOSA/SSN:**
- Modeling any measurement, observation, or count
- Representing sampling activities and sample provenance
- Linking observations to methods/protocols
- Distinguishing phenomenon time (when property applied) from result time (when recorded)

**References:**
- [SOSA/SSN W3C Recommendation](https://www.w3.org/TR/vocab-ssn/)
- [SOSA Namespace](http://www.w3.org/ns/sosa/)

### I-ADOPT (InteroperAble Descriptions of Observable Property Terminology)

**Namespace:** `https://w3id.org/iadopt/ont/`
**Purpose:** Decomposes complex variable descriptions into reusable components.

I-ADOPT provides a framework endorsed by the Research Data Alliance (RDA) for describing observable properties in a structured, machine-interpretable way. It addresses the challenge of harmonizing variable names across scientific domains.

**Core I-ADOPT Components:**

| Component | Class IRI | Description | Example |
|-----------|-----------|-------------|---------|
| **Variable** | `iop:Variable` | The complete observable property | "sockeye salmon wild adult escapement" |
| **Property** | `iop:Property` | The characteristic being measured | "count", "abundance", "length" |
| **ObjectOfInterest** | `iop:ObjectOfInterest` | Primary entity being observed | "sockeye salmon", "spawning population" |
| **ContextObject** | `iop:ContextObject` | Additional contextual entity | "Fraser River", "spawning grounds" |
| **Matrix** | `iop:Matrix` | Medium or environment | "freshwater", "marine environment" |
| **Constraint** | `iop:Constraint` | Limits scope of observation | "wild origin", "adult life stage", "2024 return year" |

**I-ADOPT Properties:**

| Property | Description |
|----------|-------------|
| `iop:hasProperty` | Links Variable to the Property being measured |
| `iop:hasObjectOfInterest` | Links Variable to primary entity |
| `iop:hasContextObject` | Links Variable to contextual entities |
| `iop:hasMatrix` | Links Variable to environmental medium |
| `iop:hasConstraint` | Links Variable to scope-limiting constraints |

**Example decomposition for salmon variable:**

Note: the GCDFO constraint IRIs in this example may not exist in the currently published ontology. Treat them as **proposed** constraints unless you can verify them in the ontology you loaded (for example via `metasalmon::fetch_salmon_ontology()` + term search). If a constraint IRI is missing, leave it blank in SDP metadata and propose it via `gpt_proposed_terms.csv`.

```turtle
@prefix gcdfo: <https://w3id.org/gcdfo/salmon#> .
@prefix iop: <https://w3id.org/iadopt/ont/> .
@prefix qudt: <http://qudt.org/vocab/quantitykind/> .

# The compound variable concept
gcdfo:WildAdultSockeyeEscapement a iop:Variable , skos:Concept ;
    rdfs:label "Wild adult sockeye salmon escapement"@en ;
    iop:hasProperty qudt:Count ;
    iop:hasObjectOfInterest gcdfo:SockeyeSalmon ;
    iop:hasConstraint gcdfo:NaturalOrigin ,
                      gcdfo:AdultLifeStage ,
                      gcdfo:EscapementContext .

# Constraints as SKOS concepts
gcdfo:NaturalOrigin a iop:Constraint , skos:Concept ;
    rdfs:label "Natural-origin"@en ;
    skos:definition "Fish that originated from natural spawning (not hatchery-origin)."@en .

gcdfo:AdultLifeStage a iop:Constraint , skos:Concept ;
    rdfs:label "Adult life stage"@en ;
    skos:broader gcdfo:LifeStage .
```

**Integration with SOSA:**

I-ADOPT Variables can be used as `sosa:ObservableProperty` values:

```turtle
gcdfo:escapement_obs_001 a sosa:Observation ;
    sosa:observedProperty gcdfo:WildAdultSockeyeEscapement ;  # I-ADOPT Variable
    sosa:hasFeatureOfInterest gcdfo:FraserRiverPopulation ;
    sosa:hasResult [ qudt:numericValue 125000 ] .
```

**Variable Set Extension (2023):**

The I-ADOPT framework was extended in 2023 to support aggregation of variables using coarser concepts for dataset discovery:

```turtle
gcdfo:SalmonAbundanceVariableSet a iop:VariableSet ;
    rdfs:label "Salmon abundance variables"@en ;
    iop:includesVariable gcdfo:WildAdultSockeyeEscapement ,
                         gcdfo:TotalSockeyeReturn ,
                         gcdfo:HatcheryContribution .
```

**When to use I-ADOPT:**
- Defining compound measurement variables with multiple constraints
- Enabling cross-dataset variable harmonization
- Creating machine-interpretable variable descriptions
- Populating SDP `property_iri`, `entity_iri`, `constraint_iri` columns (and optionally `method_iri` for procedure/method)

**References:**
- [I-ADOPT WG](https://i-adopt.github.io/)
- [I-ADOPT Ontology](https://i-adopt.github.io/ontology/index-en.html)
- [I-ADOPT Recommendations (Zenodo)](https://zenodo.org/records/6520132)
- [RDA I-ADOPT GitHub](https://github.com/i-adopt)

### Darwin Core and the Darwin Core Data Package

**Namespaces:**
- `dwc:` → `http://rs.tdwg.org/dwc/terms/`
- `dwciri:` → `http://rs.tdwg.org/dwc/iri/`

**Purpose:** Standard vocabulary for biodiversity data exchange, with new `dwc:Assertion` pattern for flexible measurements.

#### Darwin Core Classes

Darwin Core provides core classes for biodiversity information:

| Class | Description | Salmon Use Case |
|-------|-------------|-----------------|
| `dwc:Event` | Action at a location/time | Survey event, sampling trip |
| `dwc:Occurrence` | Evidence of organism presence | Fish observation, catch record |
| `dwc:Organism` | Particular organism or group | Individual salmon, cohort |
| `dwc:MaterialEntity` | Physical object | Scale sample, tissue sample |
| `dwc:Taxon` | Taxonomic concept | *Oncorhynchus nerka* |
| `dwc:Location` | Spatial region | Fraser River, spawning grounds |

#### Darwin Core Data Package (DwC-DP) and Assertions

The **Darwin Core Data Package** (currently in public review, 2025) introduces a flexible relational model that moves beyond the star-schema limitations of Darwin Core Archives. A key innovation is the **`dwc:Assertion`** class, which generalizes `dwc:MeasurementOrFact`.

**Assertion Types in DwC-DP:**

| Assertion Type | Description | Example |
|----------------|-------------|---------|
| `event-assertion` | Assertion about a `dwc:Event` | Water temperature at sampling event |
| `occurrence-assertion` | Assertion about a `dwc:Occurrence` | Fork length of observed fish |
| `material-assertion` | Assertion about a `dwc:MaterialEntity` | Weight of tissue sample |
| `organism-assertion` | Assertion about a `dwc:Organism` | Age determined from scale |
| `taxon-assertion` | Assertion about a `dwc:Taxon` | Conservation status |

**Key Assertion Properties:**

| Property | Description |
|----------|-------------|
| `dwc:assertionID` | Unique identifier for the assertion |
| `dwc:assertionType` | Category of the assertion (literal) |
| `dwciri:assertionTypeIRI` | Controlled vocabulary IRI for assertion type |
| `dwc:assertionValue` | Non-numeric value |
| `dwc:assertionValueNumeric` | Numeric value |
| `dwc:assertionUnit` | Unit (literal) |
| `dwciri:assertionUnitIRI` | Unit IRI (use QUDT) |
| `dwc:assertionBy` | Agent(s) making the assertion |
| `dwc:assertionMadeDate` | When assertion was made |
| `dwc:assertionEffectiveDate` | When assertion state was in effect |
| `dwc:assertionProtocols` | Protocol(s) used |
| `dwciri:assertionProtocolID` | Protocol IRI |

**Example event-assertion for salmon survey:**

```json
{
  "eventID": "survey_fraser_2024_001",
  "assertionID": "assertion_001",
  "assertionType": "water temperature",
  "assertionTypeIRI": "http://qudt.org/vocab/quantitykind/Temperature",
  "assertionValueNumeric": 12.5,
  "assertionUnit": "°C",
  "assertionUnitIRI": "http://qudt.org/vocab/unit/DEG_C",
  "assertionMadeDate": "2024-08-15",
  "assertionBy": "DFO Stock Assessment",
  "assertionProtocols": "Standard water quality measurement protocol"
}
```

#### Mapping gcdfo: to Darwin Core

**Class Alignments:**

```turtle
# Event-type data
gcdfo:SurveyEvent rdfs:subClassOf dwc:Event .
gcdfo:SamplingTrip rdfs:subClassOf dwc:Event .

# Occurrence data
gcdfo:FishObservation rdfs:subClassOf dwc:Occurrence .

# Material samples
gcdfo:ScaleSample rdfs:subClassOf dwc:MaterialEntity .
gcdfo:TissueSample rdfs:subClassOf dwc:MaterialEntity .
```

**Property Mappings:**

| gcdfo: Property | dwc: Equivalent | Notes |
|-----------------|-----------------|-------|
| `gcdfo:eventDate` | `dwc:eventDate` | Use dwc: directly |
| `gcdfo:locationID` | `dwc:locationID` | Use dwc: directly |
| `gcdfo:waterTemperature` | via `event-assertion` | Use assertionTypeIRI |
| `gcdfo:forkLength` | via `occurrence-assertion` | Use assertionTypeIRI |
| `gcdfo:ageFromScale` | via `organism-assertion` | Use assertionTypeIRI |

#### Using Assertions with I-ADOPT Variables

The `dwciri:assertionTypeIRI` can point to I-ADOPT-decomposed variable concepts:

```json
{
  "eventID": "survey_001",
  "assertionID": "escapement_est_001",
  "assertionType": "wild adult sockeye escapement",
  "assertionTypeIRI": "https://w3id.org/gcdfo/salmon#WildAdultSockeyeEscapement",
  "assertionValueNumeric": 125000,
  "assertionUnit": "individuals",
  "assertionUnitIRI": "http://qudt.org/vocab/unit/NUM"
}
```

This creates a link from Darwin Core's assertion pattern to the full I-ADOPT decomposition.

#### SOSA-Darwin Core Integration

Darwin Core classes can serve as SOSA Features of Interest:

```turtle
gcdfo:count_obs_001 a sosa:Observation ;
    sosa:hasFeatureOfInterest [
        a dwc:Event ;
        dwc:eventID "survey_fraser_2024_001" ;
        dwc:eventDate "2024-08-15" ;
        dwc:locationID "fraser_hells_gate"
    ] ;
    sosa:observedProperty gcdfo:WildAdultSockeyeEscapement ;
    sosa:hasResult [ qudt:numericValue 125000 ] .
```

**When to use Darwin Core:**
- Publishing biodiversity data to GBIF or other aggregators
- Modeling event-based sampling data
- Recording measurements about organisms, events, or materials
- Interoperability with the biodiversity informatics community

**References:**
- [Darwin Core Standard](https://www.tdwg.org/standards/dwc/)
- [Darwin Core Data Package Review](https://www.tdwg.org/news/2025/public-review-of-conceptual-model-and-dp-guide-for-darwin-core/)
- [DwC-DP Quick Reference](https://gbif.github.io/dwc-dp/qrg/)
- [DwC-DP GitHub](https://github.com/gbif/dwc-dp)

### Putting It All Together: Alignment Patterns

#### Pattern 1: Observation with Full Provenance

```turtle
@prefix gcdfo: <https://w3id.org/gcdfo/salmon#> .
@prefix sosa: <http://www.w3.org/ns/sosa/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix iop: <https://w3id.org/iadopt/ont/> .
@prefix dwc: <http://rs.tdwg.org/dwc/terms/> .

# The observation (SOSA + PROV)
gcdfo:obs_001 a sosa:Observation , prov:Activity ;
    rdfs:label "Fraser River sockeye escapement count 2024" ;

    # SOSA pattern
    sosa:hasFeatureOfInterest gcdfo:FraserRiverSockeyePopulation ;
    sosa:observedProperty gcdfo:WildAdultSockeyeEscapement ;  # I-ADOPT Variable
    sosa:usedProcedure gcdfo:WeirCountProtocol ;
    sosa:madeBySensor gcdfo:HellsGateWeir ;
    sosa:phenomenonTime "2024-08-15"^^xsd:date ;
    sosa:hasResult gcdfo:result_001 ;

    # PROV pattern
    prov:wasAssociatedWith gcdfo:DFOStockAssessment ;
    prov:used gcdfo:RawCountData2024 .

# The result (IAO alignment)
gcdfo:result_001 a sosa:Result , IAO:0000109 ;  # measurement datum
    qudt:numericValue 125000 ;
    qudt:unit qudt:NUM ;
    IAO:0000136 gcdfo:FraserRiverSockeyePopulation .  # is about
```

#### Pattern 2: Sample with Darwin Core Interoperability

```turtle
# A scale sample as both SOSA Sample and DwC MaterialEntity
gcdfo:scale_sample_001 a sosa:Sample , dwc:MaterialEntity ;
    sosa:isSampleOf gcdfo:FraserRiverSockeyePopulation ;
    sosa:isResultOf gcdfo:sampling_001 ;
    dwc:materialEntityID "GCDFO:SCALE:2024:001" ;
    dwc:preparations "dried scale" .

# The sampling event
gcdfo:sampling_001 a sosa:Sampling , dwc:Event , prov:Activity ;
    sosa:hasFeatureOfInterest gcdfo:FraserRiverSockeyePopulation ;
    sosa:hasResult gcdfo:scale_sample_001 ;
    dwc:eventID "GCDFO:EVENT:2024:001" ;
    dwc:eventDate "2024-08-15" ;
    prov:wasAssociatedWith gcdfo:DFOFieldTeam .
```

#### Pattern 3: I-ADOPT Variable with Full Decomposition

```turtle
# Complete variable definition
gcdfo:WildAdultSockeyeEscapement a iop:Variable , skos:Concept ;
    rdfs:label "Wild adult sockeye salmon escapement count"@en ;
    skos:definition "The count of wild-origin adult sockeye salmon that have successfully migrated to spawning grounds"@en ;

    # I-ADOPT decomposition
    iop:hasProperty qudt:Count ;
    iop:hasObjectOfInterest gcdfo:SockeyeSalmon ;
    iop:hasConstraint gcdfo:NaturalOrigin ,
                      gcdfo:AdultLifeStage ,
                      gcdfo:EscapementContext ;

    # External alignments
    skos:exactMatch <http://vocab.nerc.ac.uk/collection/P01/current/...> ;  # If available
    skos:closeMatch <http://aims.fao.org/aos/agrovoc/c_...> .  # AGROVOC alignment
```

### Decision Guide: Which Ontology to Use When

| Question | Primary Ontology | Secondary |
|----------|------------------|-----------|
| "What kind of thing is this?" | BFO | - |
| "Is this information or physical?" | IAO | BFO |
| "Who/what produced this data?" | PROV-O | - |
| "How was this measured?" | SOSA/SSN | PROV-O |
| "What property was measured?" | I-ADOPT | SOSA |
| "How do I publish to GBIF?" | Darwin Core | SOSA |
| "What constraints apply?" | I-ADOPT | gcdfo: SKOS |

### Namespace Summary

```turtle
@prefix bfo:    <http://purl.obolibrary.org/obo/BFO_> .
@prefix iao:    <http://purl.obolibrary.org/obo/IAO_> .
@prefix prov:   <http://www.w3.org/ns/prov#> .
@prefix sosa:   <http://www.w3.org/ns/sosa/> .
@prefix ssn:    <http://www.w3.org/ns/ssn/> .
@prefix iop:    <https://w3id.org/iadopt/ont/> .
@prefix dwc:    <http://rs.tdwg.org/dwc/terms/> .
@prefix dwciri: <http://rs.tdwg.org/dwc/iri/> .
@prefix qudt:   <http://qudt.org/vocab/unit/> .
@prefix gcdfo:  <https://w3id.org/gcdfo/salmon#> .
```
