# GitHub Issue Templates for Proposed New Terms

Submit these terms to the DFO Salmon Ontology tracker at:
https://github.com/dfo-pacific-science/dfo-salmon-ontology/issues/new?template=new-term-request.md

---

## Issue 1: Return Year

**Term Label:** Return Year

**Term Definition:** The calendar year in which adult salmon return to their natal freshwater spawning habitat.

**Term Type:** owl_class

**Suggested Parent IRI:** https://w3id.org/gcdfo/salmon#YearBasis

**Definition Source:** https://www.pac.dfo-mpo.gc.ca/fm-gp/salmon-saumon/gloss-eng.html

**Suggested Relationships:** broader: YearBasis

**Notes:** Complements BroodYear and CatchYear as temporal reference frame. This term is needed to distinguish between the different year conventions used in salmon time series data (brood year, catch year, return year).

**Use Case:** Used in SPSR data dictionary to specify the temporal reference for smu_metadata.YEAR_TYPE, cu_metadata.YEAR_TYPE, pfma_metadata.YEAR_TYPE columns.

---

## Issue 2: Age-Location-Stratified Catch

**Term Label:** Age-Location-Stratified Catch

**Term Definition:** Number of individuals caught or observed in a specific age class at a specific spatial location (mainstem, ocean, or terminal).

**Term Type:** skos_concept

**Suggested Parent IRI:** http://rs.tdwg.org/dwc/terms/individualCount

**Definition Source:** New term for SPSR

**Suggested Relationships:** broader: individualCount; constraint: age class + spatial stratum

**Notes:** I-ADOPT decomposition requires constraint_iri for age and location. This covers the common MAINSTEM_AGE_X, OCEAN_AGE_X, TERMINAL_AGE_X column pattern in salmon stock assessment data.

**Use Case:** Used throughout SPSR data dictionary for columns like MAINSTEM_AGE_1 through MAINSTEM_AGE_7, OCEAN_AGE_1 through OCEAN_AGE_7, TERMINAL_AGE_1 through TERMINAL_AGE_7 across smu_timeseries, cu_year, and pfma_timeseries tables.

**I-ADOPT Decomposition:**
- property_iri: http://purl.obolibrary.org/obo/PATO_0000070 (count)
- entity_iri: https://w3id.org/gcdfo/salmon#Stock
- constraint_iri: [age_constraint_IRI];[location_constraint_IRI] (semicolon-separated)

---

## Issue 3: Marine Survival Rate

**Term Label:** Marine Survival Rate

**Term Definition:** Proportion of juvenile salmon that survive their ocean residence period and return as adults.

**Term Type:** skos_concept

**Suggested Parent IRI:** http://purl.obolibrary.org/obo/NCIT_C25337 (survival rate)

**Definition Source:** https://www.dfo-mpo.gc.ca/science/

**Suggested Relationships:** broader: survival rate; entity: juvenile salmon; phase: marine

**Notes:** Related to MARINE_SURVIVAL_INDEX column in pop_year and indicator_year tables. Often expressed as a percentage or ratio.

**Use Case:** Used in pop_year.MARINE_SURVIVAL_INDEX and indicator_year.MARINE_SURVIVAL_INDEX columns.

**I-ADOPT Decomposition:**
- property_iri: http://purl.obolibrary.org/obo/NCIT_C25337 (rate)
- entity_iri: https://w3id.org/gcdfo/salmon#Stock
- constraint_iri: [marine_phase_constraint_IRI]

---

## Issue 4: Proportion Hatchery-Origin Spawners (pHOS)

**Term Label:** Proportion Hatchery-Origin Spawners

**Term Definition:** The proportion of spawning adults in a population that originated from hatchery production rather than natural spawning.

**Term Type:** skos_concept

**Suggested Parent IRI:** http://purl.obolibrary.org/obo/NCIT_C25337 (proportion)

**Definition Source:** https://publications.gc.ca/site/eng/9.928944/publication.html (Genetically based targets for enhanced contributions to Canadian Pacific chinook salmon populations)

**Suggested Relationships:** property: proportion; entity: spawners; constraint: hatchery origin

**Notes:** Commonly abbreviated as pHOS. Important metric for managing the genetic impact of hatchery supplementation on wild salmon populations.

**Use Case:** Used in pop_year.pHOS column.

**I-ADOPT Decomposition:**
- property_iri: http://purl.obolibrary.org/obo/NCIT_C25337 (proportion)
- entity_iri: https://w3id.org/gcdfo/salmon#Stock
- constraint_iri: [hatchery_origin_constraint_IRI]

---

## Issue 5: In-River Mortality Rate

**Term Label:** In-River Mortality Rate

**Term Definition:** The proportion of a salmon population that dies during freshwater migration before reaching spawning grounds.

**Term Type:** skos_concept

**Definition Source:** New term for SPSR

**Suggested Relationships:** broader: mortality rate; entity: salmon; phase: freshwater migration; constraint: pre-spawning

**Notes:** Distinct from mainstem, terminal, and ocean mortality. Occurs during the entire river migration phase. Used in smu_timeseries.IN_RIVER_MORTALITY_RATE column (note: column label says "Total Mortality" but definition and context indicate in-river mortality).

**Use Case:** Used in smu_timeseries.IN_RIVER_MORTALITY_RATE column.

---

## Issue 6: Mainstem Mortality Rate

**Term Label:** Mainstem Mortality Rate

**Term Definition:** The proportion of fish that die while migrating through the mainstem river channel before reaching spawning grounds.

**Term Type:** skos_concept

**Definition Source:** New term for SPSR

**Suggested Relationships:** broader: mortality rate; entity: salmon; location: mainstem; phase: migration; constraint: pre-spawning

**Notes:** Specific to main river channel mortality. The mainstem is the primary, large river channel. This reduces the number of fish reaching spawning grounds.

**Use Case:** Used in smu_timeseries.MAINSTEM_MORTALITY_RATE, cu_year.MAINSTEM_MORTALITY_RATE columns.

---

## Issue 7: Ocean Mortality Rate

**Term Label:** Ocean Mortality Rate

**Term Definition:** The proportion of fish that die while at sea due to natural causes such as predation, disease, starvation, or unfavorable environmental conditions.

**Term Type:** skos_concept

**Definition Source:** New term for SPSR

**Suggested Relationships:** broader: mortality rate; entity: salmon; location: ocean; phase: marine residence

**Notes:** Covers natural mortality during ocean phase, excluding fishing mortality. Affects overall survival before fish return to rivers.

**Use Case:** Used in smu_timeseries.OCEAN_MORTALITY_RATE, cu_year.OCEAN_MORTALITY_RATE columns.

---

## Issue 8: Terminal Mortality Rate

**Term Label:** Terminal Mortality Rate

**Term Definition:** The proportion of fish that die in the terminal area near or at spawning grounds before they can spawn.

**Term Type:** skos_concept

**Definition Source:** New term for SPSR

**Suggested Relationships:** broader: mortality rate; entity: salmon; location: terminal area; phase: pre-spawning

**Notes:** Terminal areas are typically in rivers or estuaries near spawning grounds. This rate affects the spawning population and recruitment success, directly impacting the stock's ability to replenish.

**Use Case:** Used in smu_timeseries.TERMINAL_MORTALITY_RATE, cu_year.TERMINAL_MORTALITY_RATE columns.

---

## Issue 9: Run Reconstruction Expansion Factor

**Term Label:** Run Reconstruction Expansion Factor

**Term Definition:** A scalar multiplier used to scale observed catch numbers to estimate total run size in a fishery management area.

**Term Type:** skos_concept

**Definition Source:** New term for SPSR

**Notes:** Accounts for unobserved components of the population when estimating total run size from observed catches. Used in PFMA run reconstruction methods.

**Use Case:** Used in pop_year.EXPANSION_FACTOR column.

---

## Issue 10: Gilbert-Rich Age Convention

**Term Label:** Gilbert-Rich Age Convention

**Term Definition:** Age determination convention for Pacific salmon where age is expressed as European_age.Freshwater_age (e.g., 1.3 means 1 year in freshwater, 3 years total).

**Term Type:** owl_class

**Definition Source:** https://www.npafc.org/

**Suggested Relationships:** alternative: European Age Convention

**Notes:** Standard aging method for Pacific salmon used throughout North Pacific fisheries science.

**Use Case:** Used as a code value in smu_metadata.AGE_TYPE, cu_metadata.AGE_TYPE, pfma_metadata.AGE_TYPE, pop_metadata.AGE_TYPE, indicator_metadata.AGE_TYPE columns.

---

## Issue 11: European Age Convention

**Term Label:** European Age Convention

**Term Definition:** Age determination convention where age is total years since hatching.

**Term Type:** owl_class

**Definition Source:** https://www.npafc.org/

**Suggested Relationships:** alternative: Gilbert-Rich Age Convention

**Notes:** Simpler aging convention expressing total age without distinguishing freshwater vs. marine residence time.

**Use Case:** Used as a code value in smu_metadata.AGE_TYPE, cu_metadata.AGE_TYPE, pfma_metadata.AGE_TYPE, pop_metadata.AGE_TYPE, indicator_metadata.AGE_TYPE columns.

---

## Batch Submission Notes

These 11 terms can be submitted as individual issues or grouped thematically:

**Group 1: Temporal Conventions** (1 term)
- Return Year

**Group 2: Age-Location Stratification** (1 term)
- Age-Location-Stratified Catch

**Group 3: Survival and Hatchery Metrics** (2 terms)
- Marine Survival Rate
- Proportion Hatchery-Origin Spawners

**Group 4: Mortality Rates** (4 terms)
- In-River Mortality Rate
- Mainstem Mortality Rate
- Ocean Mortality Rate
- Terminal Mortality Rate

**Group 5: Run Reconstruction** (1 term)
- Run Reconstruction Expansion Factor

**Group 6: Age Conventions** (2 terms)
- Gilbert-Rich Age Convention
- European Age Convention

Submit to: https://github.com/dfo-pacific-science/dfo-salmon-ontology/issues
