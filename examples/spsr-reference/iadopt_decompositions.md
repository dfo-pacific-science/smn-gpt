# I-ADOPT Decompositions for SPSR Measurement Columns

This document provides I-ADOPT-style decompositions for all measurement columns in the SPSR data dictionary, following the I-ADOPT framework for observable properties (property/entity/constraints) plus an optional procedure/method link (`method_iri`).

## I-ADOPT Framework Overview

The I-ADOPT framework decomposes observable properties into:
- **property_iri**: What is being measured (e.g., count, rate, proportion)
- **entity_iri**: What object/phenomenon is being observed (e.g., salmon stock, conservation unit)
- **constraint_iri**: Constraints that narrow the observation (e.g., age class, location, time)

SDP also allows an optional procedure/method link:
- **method_iri**: Procedure/method IRI (aligned to SOSA `sosa:Procedure`, where SOSA is the W3C/OGC observations vocabulary). Optional; rarely specified in SPSR.

Constraints are semicolon-separated when multiple apply (e.g., age AND location).

---

## Pattern 1: Age-Stratified Catch by Location

**Pattern:** `{LOCATION}_AGE_{N}` where location is MAINSTEM, OCEAN, or TERMINAL

**Example:** MAINSTEM_AGE_3 = "Number of fish caught in mainstem at age 3"

**I-ADOPT Decomposition:**
```csv
unit_iri: http://qudt.org/vocab/unit/NUM
term_iri: http://rs.tdwg.org/dwc/terms/individualCount
term_type: owl_object_property
property_iri: http://purl.obolibrary.org/obo/PATO_0000070
entity_iri: https://w3id.org/gcdfo/salmon#Stock
constraint_iri: [age_3_IRI];[mainstem_location_IRI]
method_iri: (blank)
```

**Applies to Columns:**
- smu_timeseries: MAINSTEM_AGE_1 through MAINSTEM_AGE_7, OCEAN_AGE_1 through OCEAN_AGE_7, TERMINAL_AGE_1 through TERMINAL_AGE_7
- cu_year: MAINSTEM_AGE_1 through MAINSTEM_AGE_7, OCEAN_AGE_1 through OCEAN_AGE_7, TERMINAL_AGE_1 through TERMINAL_AGE_7
- pfma_timeseries: MAINSTEM_AGE_1 through MAINSTEM_AGE_7, OCEAN_AGE_1 through OCEAN_AGE_7, TERMINAL_AGE_1 through TERMINAL_AGE_7

**Total: 63 columns** (3 locations × 7 ages × 3 tables)

**Note:** Age and location constraints need to be formalized in the ontology. Proposed constraint IRIs:
- Age: `https://w3id.org/gcdfo/salmon#Age1` through `https://w3id.org/gcdfo/salmon#Age7`
- Location: `https://w3id.org/gcdfo/salmon#MainstemLocation`, `https://w3id.org/gcdfo/salmon#OceanLocation`, `https://w3id.org/gcdfo/salmon#TerminalLocation`

---

## Pattern 2: Age-Stratified Spawners

**Pattern:** `SPAWNERS_AGE_{N}`

**Example:** SPAWNERS_AGE_3 = "Number of age 3 spawners"

**I-ADOPT Decomposition:**
```csv
unit_iri: http://qudt.org/vocab/unit/NUM
term_iri: http://rs.tdwg.org/dwc/terms/individualCount
term_type: owl_object_property
property_iri: http://purl.obolibrary.org/obo/PATO_0000070
entity_iri: https://w3id.org/gcdfo/salmon#Stock
constraint_iri: [age_3_IRI];[spawner_lifestage_IRI]
method_iri: (blank)
```

**Applies to Columns:**
- smu_timeseries: SPAWNERS_AGE_1 through SPAWNERS_AGE_7
- cu_year: SPAWNERS_AGE_1 through SPAWNERS_AGE_7
- pop_year: SPAWNERS_AGE_1 through SPAWNERS_AGE_7
- indicator_year: SPAWNERS_AGE_1 through SPAWNERS_AGE_7

**Total: 28 columns** (7 ages × 4 tables)

**Note:** Spawner life stage constraint needs formalization: `https://w3id.org/gcdfo/salmon#SpawnerLifeStage`

---

## Pattern 3: Age-Stratified Total Catch

**Pattern:** `CATCH_AGE_{N}` or `TOTAL_AGE_{N}_CATCH`

**Example:** CATCH_AGE_3 = "Total number of age 3 catch per year"

**I-ADOPT Decomposition:**
```csv
unit_iri: http://qudt.org/vocab/unit/NUM
term_iri: (blank - needs new term)
term_type: skos_concept
property_iri: http://purl.obolibrary.org/obo/PATO_0000070
entity_iri: https://w3id.org/gcdfo/salmon#Stock
constraint_iri: [age_3_IRI]
method_iri: (blank)
```

**Applies to Columns:**
- smu_timeseries: CATCH_AGE_1 through CATCH_AGE_7
- cu_year: CATCH_AGE_1 through CATCH_AGE_7
- pfma_timeseries: CATCH_AGE_1 through CATCH_AGE_7

**Total: 21 columns** (7 ages × 3 tables)

---

## Pattern 4: Age-Stratified Run Size

**Pattern:** `RUN_AGE_{N}`

**Example:** RUN_AGE_3 = "Number of salmon returning at age 3"

**I-ADOPT Decomposition:**
```csv
unit_iri: http://qudt.org/vocab/unit/NUM
term_iri: (blank - needs new term)
term_type: skos_concept
property_iri: http://purl.obolibrary.org/obo/PATO_0000070
entity_iri: https://w3id.org/gcdfo/salmon#Stock
constraint_iri: [age_3_IRI];[returning_lifestage_IRI]
method_iri: (blank)
```

**Applies to Columns:**
- smu_timeseries: RUN_AGE_1 through RUN_AGE_7

**Total: 7 columns**

**Note:** Returning/migrating life stage constraint needs formalization: `https://w3id.org/gcdfo/salmon#ReturningAdultLifeStage`

---

## Pattern 5: Total Counts (No Age Stratification)

**Pattern:** `TOTAL_{QUANTITY}` or `{QUANTITY}_CATCH`

**Examples:**
- TOTAL_SPAWNERS = "Total number of spawners for the year"
- TOTAL_CATCH = "Total harvest including commercial, recreational, and First Nations fisheries"
- TOTAL_RUN = "Number of salmon returning to a given system in a given year"

**I-ADOPT Decomposition:**
```csv
unit_iri: http://qudt.org/vocab/unit/NUM
term_iri: http://rs.tdwg.org/dwc/terms/individualCount (if applicable)
term_type: owl_object_property or skos_concept
property_iri: http://purl.obolibrary.org/obo/PATO_0000070
entity_iri: https://w3id.org/gcdfo/salmon#Stock (or ConservationUnit, or dwc:Organism for populations)
constraint_iri: varies by column type
method_iri: (blank)
```

**Applies to Columns:**
- TOTAL_SPAWNERS (smu_timeseries, cu_year, pop_year, indicator_year) - 4 columns
- TOTAL_CATCH (smu_timeseries, cu_year) - 2 columns
- TOTAL_RUN (smu_timeseries, cu_year) - 2 columns
- TOTAL_OCEAN_RUN (smu_timeseries) - 1 column
- TOTAL_TERMINAL_RUN (smu_timeseries) - 1 column
- MAINSTEM_CATCH (smu_timeseries) - 1 column
- OCEAN_CATCH (smu_timeseries) - 1 column
- TERMINAL_CATCH (smu_timeseries) - 1 column
- RECRUITS (smu_timeseries, cu_year, indicator_year) - 3 columns

**Total: 16 columns**

---

## Pattern 6: Mortality Rates

**Pattern:** `{LOCATION}_MORTALITY_RATE` or `TOTAL_MORTALITY_RATE` or `IN_RIVER_MORTALITY_RATE`

**Examples:**
- MAINSTEM_MORTALITY_RATE = "Proportion of fish that die while migrating through the mainstem"
- OCEAN_MORTALITY_RATE = "Proportion of fish that die while at sea"
- TERMINAL_MORTALITY_RATE = "Proportion of fish that die in terminal area before spawning"

**I-ADOPT Decomposition:**
```csv
unit_iri: http://qudt.org/vocab/unit/UNITLESS
term_iri: (blank - needs new term per location)
term_type: skos_concept
property_iri: (blank - needs mortality rate property IRI)
entity_iri: https://w3id.org/gcdfo/salmon#Stock
constraint_iri: [location_constraint_IRI] or [phase_constraint_IRI]
method_iri: (blank)
```

**Applies to Columns:**
- MAINSTEM_MORTALITY_RATE (smu_timeseries, cu_year) - 2 columns
- OCEAN_MORTALITY_RATE (smu_timeseries, cu_year) - 2 columns
- TERMINAL_MORTALITY_RATE (smu_timeseries, cu_year) - 2 columns
- IN_RIVER_MORTALITY_RATE (smu_timeseries) - 1 column
- TOTAL_MORTALITY_RATE (smu_timeseries, cu_year) - 2 columns

**Total: 9 columns**

**Constraint IRIs needed:**
- `https://w3id.org/gcdfo/salmon#MainstemPhase`
- `https://w3id.org/gcdfo/salmon#OceanPhase`
- `https://w3id.org/gcdfo/salmon#TerminalPhase`
- `https://w3id.org/gcdfo/salmon#InRiverPhase`

---

## Pattern 7: Exploitation Rates

**Pattern:** `{SCOPE}_EXPLOITATION_RATE`

**Examples:**
- OCEAN_EXPLOITATION_RATE = "Total exploitation rate in the ocean area"
- TOTAL_EXPLOITATION_RATE = "Proportion of fish population harvested by all fisheries"
- ER = "Estimated annual calendar year exploitation rate at CU or PFMA scale"

**I-ADOPT Decomposition:**
```csv
unit_iri: http://qudt.org/vocab/unit/UNITLESS
term_iri: https://w3id.org/gcdfo/salmon#ExploitationRate or #TotalExploitationRate
term_type: owl_class
property_iri: http://purl.obolibrary.org/obo/NCIT_C25337 (rate)
entity_iri: https://w3id.org/gcdfo/salmon#Stock
constraint_iri: [location_or_scope_constraint_IRI]
method_iri: (blank)
```

**Applies to Columns:**
- OCEAN_EXPLOITATION_RATE (smu_timeseries) - 1 column
- TOTAL_EXPLOITATION_RATE (smu_timeseries, cu_year, indicator_year) - 3 columns
- ER (pfma_timeseries) - 1 column

**Total: 5 columns**

**Note:** Existing ontology terms:
- `https://w3id.org/gcdfo/salmon#ExploitationRate`
- `https://w3id.org/gcdfo/salmon#TotalExploitationRate`

---

## Pattern 8: Reference Points and Benchmarks

**Pattern:** `{ACRONYM}` where acronym is LRP, USR, TR, RR, LOWER_WSP_BENCHMARK, UPPER_WSP_BENCHMARK, UPPER_MANAGEMENT_LEVEL, LOWER_MANAGEMENT_LEVEL

**Examples:**
- LRP = "Limit Reference Point: stock status below which serious harm may be incurred"
- USR = "Upper Stock Reference: threshold for progressive reduction of fishing mortality"
- LOWER_WSP_BENCHMARK = "Wild Salmon Policy lower biological benchmark"

**I-ADOPT Decomposition:**
```csv
unit_iri: http://qudt.org/vocab/unit/NUM (for abundance) or UNITLESS (for rates)
term_iri: varies (LimitReferencePoint, UpperStockReferencePoint, MetricBenchmark, ReferencePoint)
term_type: owl_class
property_iri: http://purl.obolibrary.org/obo/PATO_0000070 (abundance) or rate property
entity_iri: https://w3id.org/gcdfo/salmon#Stock or #ConservationUnit
constraint_iri: [management_framework_constraint_IRI]
method_iri: (blank)
```

**Applies to Columns:**
- LRP (smu, cu) - 2 columns
- USR (smu, cu) - 2 columns
- TR (smu, cu) - 2 columns
- RR (smu, cu) - 2 columns
- LOWER_WSP_BENCHMARK (cu) - 1 column
- UPPER_WSP_BENCHMARK (cu) - 1 column
- UPPER_MANAGEMENT_LEVEL (pfma_metadata) - 1 column
- LOWER_MANAGEMENT_LEVEL (pfma_metadata) - 1 column

**Total: 12 columns**

**Existing ontology terms:**
- `https://w3id.org/gcdfo/salmon#LimitReferencePoint`
- `https://w3id.org/gcdfo/salmon#UpperStockReferencePoint`
- `https://w3id.org/gcdfo/salmon#ReferencePoint`
- `https://w3id.org/gcdfo/salmon#MetricBenchmark`

---

## Pattern 9: Proportion/Index Measurements

**Pattern:** Special ratio or index columns

**Examples:**
- pHOS = "Proportion of hatchery-origin spawners"
- MARINE_SURVIVAL_INDEX = "Survival rate of fish during ocean time"
- EXPANSION_FACTOR = "Tool to estimate total run size from observed catch"

### pHOS (Proportion Hatchery-Origin Spawners)

**I-ADOPT Decomposition:**
```csv
unit_iri: http://qudt.org/vocab/unit/UNITLESS
term_iri: (blank - needs new term)
term_type: skos_concept
property_iri: http://purl.obolibrary.org/obo/NCIT_C25337 (proportion)
entity_iri: http://rs.tdwg.org/dwc/terms/Organism
constraint_iri: [spawner_lifestage_IRI];[hatchery_origin_IRI]
method_iri: (blank)
```

**Applies to:** pop_year.pHOS - 1 column

### MARINE_SURVIVAL_INDEX

**I-ADOPT Decomposition:**
```csv
unit_iri: http://qudt.org/vocab/unit/UNITLESS
term_iri: (blank - needs new term: Marine Survival Rate)
term_type: skos_concept
property_iri: http://purl.obolibrary.org/obo/NCIT_C25337 (rate/survival rate)
entity_iri: http://rs.tdwg.org/dwc/terms/Organism
constraint_iri: [juvenile_lifestage_IRI];[marine_phase_IRI]
method_iri: (blank)
```

**Applies to:** pop_year.MARINE_SURVIVAL_INDEX, indicator_year.MARINE_SURVIVAL_INDEX - 2 columns

### EXPANSION_FACTOR

**I-ADOPT Decomposition:**
```csv
unit_iri: http://qudt.org/vocab/unit/UNITLESS
term_iri: (blank - needs new term: Run Reconstruction Expansion Factor)
term_type: skos_concept
property_iri: (blank - scalar multiplier property)
entity_iri: https://w3id.org/gcdfo/salmon#Stock
constraint_iri: [run_reconstruction_method_IRI]
method_iri: (blank)
```

**Applies to:** pop_year.EXPANSION_FACTOR - 1 column

**Total for Pattern 9: 4 columns**

---

## Summary Statistics

**Total Measurement Columns: 167**

Breakdown by pattern:
1. Age-Stratified Catch by Location: 63 columns
2. Age-Stratified Spawners: 28 columns
3. Age-Stratified Total Catch: 21 columns
4. Age-Stratified Run Size: 7 columns
5. Total Counts (no age): 16 columns
6. Mortality Rates: 9 columns
7. Exploitation Rates: 5 columns
8. Reference Points and Benchmarks: 12 columns
9. Proportion/Index Measurements: 4 columns
10. Other temporal/identifier columns: ~35 columns (not measurements)

**Total Columns in Dictionary: ~202 columns** (167 measurements + 35 identifiers/attributes/temporal)

---

## Required Ontology Additions

To fully support I-ADOPT decomposition for SPSR measurements, the following terms need to be added to the DFO Salmon Ontology:

### Age Constraints (7 terms)
- `https://w3id.org/gcdfo/salmon#Age1` through `https://w3id.org/gcdfo/salmon#Age7`

### Location Constraints (3 terms)
- `https://w3id.org/gcdfo/salmon#MainstemLocation`
- `https://w3id.org/gcdfo/salmon#OceanLocation`
- `https://w3id.org/gcdfo/salmon#TerminalLocation`

### Life Stage Constraints (3 terms)
- `https://w3id.org/gcdfo/salmon#SpawnerLifeStage`
- `https://w3id.org/gcdfo/salmon#ReturningAdultLifeStage`
- `https://w3id.org/gcdfo/salmon#JuvenileLifeStage`

### Phase/Process Constraints (5 terms)
- `https://w3id.org/gcdfo/salmon#MainstemPhase`
- `https://w3id.org/gcdfo/salmon#OceanPhase`
- `https://w3id.org/gcdfo/salmon#TerminalPhase`
- `https://w3id.org/gcdfo/salmon#InRiverPhase`
- `https://w3id.org/gcdfo/salmon#MarinePhase`

### Origin Constraints (1 term)
- `https://w3id.org/gcdfo/salmon#HatcheryOrigin`

### Observable Properties (11 terms)
See gpt_proposed_terms.csv for full list including:
- Age-Location-Stratified Catch
- Marine Survival Rate
- Proportion Hatchery-Origin Spawners
- Mainstem Mortality Rate
- Ocean Mortality Rate
- Terminal Mortality Rate
- In-River Mortality Rate
- Run Reconstruction Expansion Factor
- Return Year
- Gilbert-Rich Age Convention
- European Age Convention

---

## Usage in SDP Validation

When validating SPSR data against this dictionary:

1. **Check measurement columns have unit_iri**: All measurement columns must have a unit_iri (either `http://qudt.org/vocab/unit/NUM` for counts or `http://qudt.org/vocab/unit/UNITLESS` for ratios)

2. **Check I-ADOPT completeness for measurements**: All measurement columns should have at minimum:
   - property_iri
   - entity_iri
   - constraint_iri (if the measurement is stratified or scoped)

3. **Validate constraint syntax**: Multiple constraints must be semicolon-separated (e.g., `age_3_IRI;mainstem_location_IRI`)

4. **Check term_iri mapping**: Where existing ontology terms exist (e.g., dwc:individualCount, salmon:ExploitationRate), they should be used. Blank term_iri indicates a proposed new term is needed.

---

## References

- I-ADOPT Framework: https://i-adopt.github.io/
- DFO Salmon Ontology: https://github.com/dfo-pacific-science/dfo-salmon-ontology
- QUDT Units: http://qudt.org/vocab/unit/
- Darwin Core: http://rs.tdwg.org/dwc/terms/
- OBO Foundry (PATO, NCIT): http://www.obofoundry.org/
