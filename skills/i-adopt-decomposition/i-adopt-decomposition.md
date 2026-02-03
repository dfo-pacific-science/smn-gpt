---
name: i-adopt-decomposition
description: Guidance and scripts for decomposing measurement columns using I-ADOPT patterns for salmon datasets.
---

# I-ADOPT Decomposition

Use this skill when decomposing measurement columns into I-ADOPT parts (property, entity, matrix/context, constraints) plus an optional procedure/method link (`method_iri`, aligned to SOSA `sosa:Procedure`, where SOSA is the W3C/OGC observations vocabulary).

## Process (detailed, self contained)
1) Understand the variable
- What does it measure/represent? Quantitative or qualitative?
- What units or value formats? (units hint at property)
- How was it produced? (procedure/method, survey, model, gear)
- What population and segment? (age, brood year, run timing, location, fishery)

2) Identify I-ADOPT components
- Property: characteristic/quantity kind (often infer from units).
- Object of Interest: entity whose property is observed (StockManagementUnit, ConservationUnit, Population, Spawner, Fish, HabitatReach).
- Matrix: embedding entity (e.g., WaterBody for concentrations) — optional.
- Context objects: other involved entities (gear, site, life stage).
- Constraints: facets narrowing scope (age, location, season, sex, fishery); keep atomic; separate multiples with `;`.
- Procedure/method: how value obtained (survey, model, genetic assignment, gear); capture in `method_iri` as a procedure/method IRI (not an I-ADOPT role).

3) Map to IRIs (preferred vocabularies)
- Salmon-specific: DFO Salmon Ontology (`https://w3id.org/gcdfo/salmon#`).
- Counts: DwC `individualCount`.
- Quantity kinds: NCIT (e.g., count, rate, proportion), QUDT for units.
- Taxa: NCBITaxon (species/stage).
- If missing, leave blank and stage a new term request (ontology-helpers + ontology-term-creation skill).

4) Populate column_dictionary
- Fill: term_iri, unit_iri, property_iri, entity_iri, constraint_iri, method_iri (procedure/method IRI).
- Treat `method_iri` as a procedure/method IRI (aligned to SOSA `sosa:Procedure`), not an I-ADOPT role.
- Keep constraints atomic; join multiples with `;` in `constraint_iri`.
- For categorical codes, use `codes.csv` with IRIs/labels.

5) Sanity checks (before finalizing)
- Property aligns with unit (rate ↔ UNITLESS, length ↔ cm, mass ↔ g, count ↔ NUM).
- Entity matches the thing measured (Spawner vs StockManagementUnit vs ConservationUnit vs Population).
- Constraints cover every qualifier in the column name/definition (age, area, gear, brood vs return).
- Procedure/method recorded when known; blank is acceptable but note if model-based.

6) If no suitable term
- Leave unknown IRIs blank; add to `gpt_proposed_terms.csv` and launch a new-term issue via ontology-helpers script.

---

## User Confirmation Workflow (REQUIRED for measurement columns)

**Critical**: Entity and property selection are the highest-stakes semantic decisions. Do NOT silently assume these values for measurement columns. Follow this pattern-based confirmation workflow.

### Overview

Instead of confirming each column individually (which doesn't scale), confirm by **pattern**:
1. Group measurement columns by naming convention
2. Propose entity/property/constraints for each pattern
3. Get user approval on patterns (not individual columns)
4. Handle ambiguities and edge cases explicitly

### Step 1: Pattern Discovery

After reading the source dictionary, identify distinct measurement patterns:

```
I identified [N] measurement patterns across [M] columns. Please review:

| # | Pattern Name | Example Columns | Count | Proposed Entity | Proposed Property | Proposed Constraints |
|---|--------------|-----------------|-------|-----------------|-------------------|---------------------|
| 1 | Age-location catch | MAINSTEM_AGE_1..7, OCEAN_AGE_1..7 | 63 | [context] | count (PATO) | age_class; location |
| 2 | Age-stratified spawners | SPAWNERS_AGE_1..7 | 28 | [context] | count (PATO) | age_class; spawner_lifestage |
| 3 | Mortality rates | MAINSTEM_MORTALITY_RATE, OCEAN_MORTALITY_RATE | 9 | [context] | rate (NCIT) | location_or_phase |
| 4 | Total counts | TOTAL_SPAWNERS, TOTAL_CATCH, TOTAL_RUN | 16 | [context] | count (PATO) | [varies by column] |
| 5 | Reference points | LRP, USR, TR, RR | 12 | [context] | threshold (NCIT) | management_framework |
| 6 | Exploitation rates | TOTAL_EXPLOITATION_RATE, OCEAN_EXPLOITATION_RATE | 5 | [context] | rate (NCIT) | scope |
| 7 | Proportion metrics | pHOS | 2 | Population | proportion (NCIT) | origin |
| 8 | Survival indices | MARINE_SURVIVAL_INDEX | 2 | [context] | rate (NCIT) | marine_phase |
| 9 | Expansion factors | EXPANSION_FACTOR | 1 | Population | scalar | [none] |

**Notes:**
- `[context]` means entity depends on table: StockManagementUnit for smu_*, ConservationUnit for cu_*, Population for pop_*
- Pattern #5 (Reference points): Entity depends on table context (StockManagementUnit for smu_*, ConservationUnit for cu_*)

Reply with:
- "approve all" to accept all patterns
- Pattern numbers to modify (e.g., "2: entity=Spawner")
- "explain #N" for more detail on a pattern
```

### Step 2: Ambiguity Resolution

For patterns where entity or property has multiple valid interpretations, explicitly flag and ask:

```
⚠️ Pattern #5 (Reference Points) requires clarification:

The LRP, USR, TR columns could have different entities depending on context:

| Option | Entity | Rationale |
|--------|--------|-----------|
| A | StockManagementUnit | These are SMU-level reference points from smu_* tables |
| B | ConservationUnit | These are CU-level benchmarks from cu_* tables |
| C | Context-dependent | Use StockManagementUnit for smu_*, ConservationUnit for cu_*, Population for pop_* |

**Recommendation**: Option C (context-dependent) based on table naming patterns.

Choose: [A] [B] [C] [D: Other - please specify]
```

### Step 3: Edge Case Review

For columns that don't fit any recognized pattern, present individually:

```
These [N] columns don't match known patterns and need individual review:

| # | Column | Table | Best Guess | Confidence | Alternative Interpretation |
|---|--------|-------|------------|------------|---------------------------|
| 1 | EXPANSION_FACTOR | pop_year | entity=Population, property=scalar | Low | Could be method parameter, not measurement |
| 2 | pHOS | pop_year | entity=Population, property=proportion | Medium | Could use entity=Spawner |
| 3 | RECRUITS_PER_SPAWNER | cu_year | entity=ConservationUnit, property=ratio | Medium | Correct based on cu_* table context |

For each, reply with:
- "accept N" to use my guess
- "N: entity=X, property=Y" to override
- "skip N" to exclude from column_dictionary measurements
```

### Step 4: Apply Approved Patterns

Only after user confirms patterns and resolves ambiguities:
1. Generate full column_dictionary.csv applying approved patterns
2. Use approved entity/property for all columns matching each pattern
3. Document any remaining uncertainties in notes

---

## Confidence Thresholds

Use these thresholds to decide when to proceed vs. when to ask:

### High Confidence (proceed without asking)
- Column name exactly matches a worked example (e.g., TOTAL_EXPLOITATION_RATE)
- Pattern is unambiguous AND table context confirms entity choice
- Unit clearly indicates property (e.g., UNITLESS → rate, NUM → count)

### Medium Confidence (note in output, batch for review)
- Pattern matches but entity has 2 valid options based on context
- Column name follows a pattern but with variation (e.g., ADJUSTED_TOTAL_SPAWNERS)
- Property is clear but constraint interpretation varies

### Low Confidence (must ask before proceeding)
- Novel column name that doesn't match any pattern
- Ambiguous units (e.g., could be count or index)
- Table context conflicts with column name implications
- Multiple valid entity AND property interpretations

**Rule**: If >20% of measurement columns are Low Confidence, stop and ask user to provide additional context before proceeding.

---

## Approval Shorthand Syntax

Users can respond efficiently using these shortcuts:

| Command | Meaning |
|---------|---------|
| `approve all` | Accept all proposed patterns as-is |
| `approve 1-5, 7` | Accept patterns 1-5 and 7; review pattern 6 |
| `2: entity=Spawner` | Override pattern 2's entity to Spawner |
| `2: property=ratio` | Override pattern 2's property to ratio |
| `5: context` | Use context-dependent entity for pattern 5 |
| `reject 4` | Remove pattern 4 from auto-generation; handle manually later |
| `explain 3` | Provide more detail on pattern 3 before deciding |
| `split 4` | Break pattern 4 into sub-patterns for finer control |

**Batch override syntax:**
```
approve 1-3, 6-9
4: entity=ConservationUnit
5: context
reject 10
```

---

## Entity Selection by Table Context

When entity is ambiguous, use table naming conventions as the default:

| Table Prefix | Default Entity | IRI |
|--------------|----------------|-----|
| `smu_*` | StockManagementUnit | `https://w3id.org/gcdfo/salmon#StockManagementUnit` |
| `cu_*` | ConservationUnit | `https://w3id.org/gcdfo/salmon#ConservationUnit` |
| `pop_*` | Stock (fallback) | `https://w3id.org/gcdfo/salmon#Stock` |
| `indicator_*` | Stock (fallback) | `https://w3id.org/gcdfo/salmon#Stock` |
| `pfma_*` | Stock (catch constrained by area) | `https://w3id.org/gcdfo/salmon#Stock` |

**Override rules:**
- If column name contains `CU_` in a non-cu_* table → use ConservationUnit
- If column name contains `SMU_` in a non-smu_* table → use StockManagementUnit
- If column describes individual fish (LENGTH, WEIGHT) → use `dwc:Organism`
- If column describes spawning adults specifically → use `gcdfo:Stock` plus a spawner/lifestage constraint (or propose a spawner class/concept)
- If unsure → ask user explicitly

---

## Salmon patterns (quick cheatsheet)
- Age/location-stratified counts: property=count; entity=[table context: SMU/CU/Stock]; unit=NUM; constraints=age class; location.
- Rates (exploitation/survival/mortality): property=rate; unit=UNITLESS; entity=[table context]; constraint=process or fishery segment.
- Reference points (LRP/USR): property=benchmark/reference point; entity=[table context]; constraint=metric (e.g., spawning abundance).
- Length/weight: property=length or mass; unit=cm or g; entity=dwc:Organism; constraint=age class if present.

## Property IRI conventions (vocabulary preferences)

See `docs/vocabulary.md` for the canonical ordering. For quick work, these defaults cover most SDP measurement columns:

### Counts and abundance
- **Default**: QUDT Count (`http://qudt.org/vocab/quantitykind/Count`)
- **Alternative**: PATO count (`http://purl.obolibrary.org/obo/PATO_0000070`)

### Rates, proportions, and ratios
- **Default (unitless)**: QUDT DimensionlessRatio (`http://qudt.org/vocab/quantitykind/DimensionlessRatio`)
- **If not unitless**: use the closest QUDT quantity kind you can justify, or leave blank and propose a term.

### Lengths and masses
- **Length**: QUDT Length (`http://qudt.org/vocab/quantitykind/Length`) (alt: PATO length `http://purl.obolibrary.org/obo/PATO_0000122`)
- **Mass**: QUDT Mass (`http://qudt.org/vocab/quantitykind/Mass`)

### Thresholds and benchmarks
- **Reference points**: prefer `gcdfo:` reference point terms and use constraints to indicate the underlying metric (escapement, exploitation rate, etc.).

### Unit IRIs (QUDT preferred)
Always use QUDT for unit_iri:
- Counts: `http://qudt.org/vocab/unit/NUM` (dimensionless count)
- Unitless ratios: `http://qudt.org/vocab/unit/UNITLESS`
- Years: `http://qudt.org/vocab/unit/YR`
- Centimeters: `http://qudt.org/vocab/unit/CentiM`
- Grams: `http://qudt.org/vocab/unit/GM`
- Kilograms: `http://qudt.org/vocab/unit/KiloGM`

### Decision rule for property_iri
1. Follow `docs/vocabulary.md` (canonical ordering and role-specific guidance).
2. Prefer a `gcdfo:` term when a salmon-specific observable/property exists.
3. Otherwise use QUDT quantity kinds (`http://qudt.org/vocab/quantitykind/`).
4. Use PATO qualities when QUDT is not appropriate.
5. If no suitable term exists, leave blank and add to `gpt_proposed_terms.csv`.

## Decomposition hints (name-based heuristics)
- Names containing `AGE_` + number → constraint_iri = life-stage/age-class; property set by units (count/length/mass/rate).
- `EXPLOITATION`, `MORTALITY`, `SURVIVAL`, `RATE` → property_iri = `http://qudt.org/vocab/quantitykind/DimensionlessRatio`; unit_iri = UNITLESS; entity=[table context]; constraints note fishery or process.
- `CPUE`, `CUE`, `EFFORT` → property_iri = catch per effort; unit depends on gear; context includes gear and effort units.
- `LRP`, `USR`, `BENCHMARK` → property_iri = reference point/benchmark; constraint indicates underlying metric (e.g., spawning abundance).
- `HATCHERY`, `WILD`, `MARKED`, `UNMARKED` → constraint_iri for origin/mark-status.
- `OCEAN`, `TERMINAL`, `MAINSTEM`, `TRIBUTARY` → constraint_iri for location segment.
- `METHOD`, `MODEL`, `SURVEY` suffix → method_iri (procedure/method IRI); do not place in constraint unless it filters scope.

## Worked examples (expanded)
- Age/location catch (MAINSTEM_AGE_3 in smu_timeseries)
  - term_iri: http://rs.tdwg.org/dwc/terms/individualCount
  - unit_iri: http://qudt.org/vocab/unit/NUM
  - property_iri: http://qudt.org/vocab/quantitykind/Count
  - entity_iri: https://w3id.org/gcdfo/salmon#StockManagementUnit
  - constraint_iri: <age_3_IRI>;<mainstem_location_IRI>
  - method_iri: <procedure_or_method_IRI_if_applicable>
- Exploitation rate (TOTAL_EXPLOITATION_RATE in smu_timeseries)
  - term_iri: https://w3id.org/gcdfo/salmon#TotalExploitationRate
  - unit_iri: http://qudt.org/vocab/unit/UNITLESS
  - property_iri: http://qudt.org/vocab/quantitykind/DimensionlessRatio
  - entity_iri: https://w3id.org/gcdfo/salmon#StockManagementUnit
  - constraint_iri: <fishing_mortality_IRI>
- Escapement count (ESCAPEMENT_COUNT)
  - term_iri: https://w3id.org/gcdfo/salmon#EscapementMeasurement
  - unit_iri: http://qudt.org/vocab/unit/NUM
  - property_iri: http://qudt.org/vocab/quantitykind/Count
  - entity_iri: https://w3id.org/gcdfo/salmon#Stock
  - constraint_iri: <river_system_IRI>
- Length at age (LENGTH_AGE_3)
  - term_iri: http://purl.obolibrary.org/obo/CMO_0000013
  - unit_iri: http://qudt.org/vocab/unit/CentiM
  - property_iri: http://qudt.org/vocab/quantitykind/Length
  - entity_iri: http://rs.tdwg.org/dwc/terms/Organism
  - constraint_iri: <age_3_IRI>
- Reference point (LRP in cu_year)
  - term_iri: https://w3id.org/gcdfo/salmon#LimitReferencePoint
  - unit_iri: http://qudt.org/vocab/unit/NUM
  - property_iri: http://qudt.org/vocab/quantitykind/Count
  - entity_iri: https://w3id.org/gcdfo/salmon#ConservationUnit
  - constraint_iri: <metric_iri_for_this_reference_point>

## Quick R patterning (dataset-agnostic)
```r
library(dplyr); library(readr); library(stringr)
entity_defaults <- read.csv("config/entity_defaults.csv")
cols <- read_csv("column_dictionary.csv", show_col_types = FALSE)
detect_phase <- function(u) paste(na.omit(c(
  if (str_starts(u, "OCEAN")) "<ocean_phase>",
  if (str_starts(u, "MAINSTEM")) "<mainstem_phase>",
  if (str_starts(u, "TERMINAL")) "<terminal_phase>"
)), collapse=";")
patterns <- cols %>%
  mutate(u = toupper(column_name),
         pattern = case_when(
           str_detect(u, "AGE_\\d+") & str_detect(u, "CATCH") ~ "age_location_catch",
           str_detect(u, "^CATCH_AGE_\\d+") ~ "age_catch",
           str_detect(u, "^SPAWNERS_AGE_\\d+") ~ "age_spawner",
           str_detect(u, "^RUN_AGE_\\d+") ~ "age_run",
           str_detect(u, "EXPLOITATION_RATE|^ER$") ~ "exploitation_rate",
           str_detect(u, "MORTALITY|SURVIVAL") ~ "mortality_survival",
           TRUE ~ "other"
         ),
         constraint_iri = str_c(
           ifelse(str_detect(u, "AGE_(\\d+)"),
                  str_replace(u, ".*AGE_(\\d+).*", "<age_\\1_constraint>"), NA_character_),
           detect_phase(u),
           ifelse(str_detect(u, "CATCH"), "<catch_context>", NA_character_),
           ifelse(str_detect(u, "RUN"), "<run_context>", NA_character_),
           sep=";"),
         constraint_iri = str_replace_all(constraint_iri, "(^;|;$|;;)", "")) %>%
  group_by(pattern) %>%
  summarise(count=n(), examples=str_c(head(column_name,3), collapse=", "))
print(patterns)
```
Use this to draft pattern tables quickly; keep constraint placeholders even when IRIs are unknown.

## Validation scripts
- Run ontology helper scripts when drafting semantics (see skills/ontology-helpers/scripts).
- Cross-check: every measurement has unit_iri + property_iri + entity_iri; constraints match qualifiers; new terms flagged; codes.csv used for categorical columns.

## Output rules
- Keep SDP output order: dataset.csv, tables.csv, column_dictionary.csv, codes.csv.
- If constraints >1, join with `;` in constraint_iri.

## Notes
- Data minimization applies to observation data only; metadata should be complete.
- Do not invent IRIs. If unknown, leave blank and propose new terms.
