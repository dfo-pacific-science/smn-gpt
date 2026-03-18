# I-ADOPT Decomposition Patterns

Use this guide when decomposing measurement columns into I-ADOPT parts (property, entity, matrix/context, constraints) plus an optional procedure/method link.

---

## Process Overview

### 1. Understand the Variable
- What does it measure/represent? Quantitative or qualitative?
- What units or value formats? (units hint at property)
- How was it produced? (procedure/method, survey, model, gear)
- What population and segment? (age, brood year, run timing, location, fishery)

### 2. Identify I-ADOPT Components
- **Property**: characteristic/quantity kind (often infer from units)
- **Object of Interest**: entity whose property is observed (StockManagementUnit, ConservationUnit, Stock, Spawner, Fish, HabitatReach)
- **Matrix**: embedding entity (e.g., WaterBody for concentrations) — optional
- **Context objects**: other involved entities (gear, site, life stage)
- **Constraints**: facets narrowing scope (age, location, season, sex, fishery); keep atomic; separate multiples with `;`
- **Procedure/method**: how value obtained (survey, model, genetic assignment, gear); capture in `method_iri`

### 3. Map to IRIs
Use bundled vocabulary files:
- **Salmon-specific**: Look up in `07-dfo-salmon-terms.csv`
- **Counts**: Darwin Core `individualCount` from `10-dwc-terms.csv`
- **Quantity kinds**: QUDT from `09-qudt-quantity-kinds.csv`
- **Units**: QUDT from `08-qudt-units.csv`
- **Taxa**: NCBITaxon (species/stage) - note in definition
- If missing, leave blank and stage a new term request

### 4. Populate column_dictionary
Fill: term_iri, unit_iri, property_iri, entity_iri, constraint_iri, method_iri
- Keep constraints atomic; join multiples with `;`
- For categorical codes, use `codes.csv` with IRIs/labels

### 5. Sanity Checks
- Property aligns with unit (rate ↔ UNITLESS, length ↔ cm, mass ↔ g, count ↔ NUM)
- Entity matches the thing measured (Spawner vs StockManagementUnit vs ConservationUnit vs Stock)
- Constraints cover every qualifier in the column name/definition
- Procedure/method recorded when known

### 6. If No Suitable Term
- Leave unknown IRIs blank
- Add to `gpt_proposed_terms.csv`
- See `17-github-issue-templates.md` for issue format

---

## User Confirmation Workflow (REQUIRED for measurement columns)

**Critical**: Entity and property selection are the highest-stakes semantic decisions. Do NOT silently assume these values. Follow this pattern-based confirmation workflow.

### Step 1: Pattern Discovery

After reading the source dictionary, identify distinct measurement patterns:

```
I identified [N] measurement patterns across [M] columns. Please review:

| # | Pattern Name | Example Columns | Count | Proposed Entity | Proposed Property | Proposed Constraints |
|---|--------------|-----------------|-------|-----------------|-------------------|---------------------|
| 1 | Age-location catch | MAINSTEM_AGE_1..7 | 63 | [context] | count | age_class; location |
| 2 | Mortality rates | MAINSTEM_MORTALITY_RATE | 9 | [context] | rate | location_or_phase |
| 3 | Reference points | LRP, USR, TR | 12 | [context] | threshold | management_framework |

**Notes:**
- `[context]` means entity depends on table: SMU for smu_*, CU for cu_*, Stock for pop_*

Reply with:
- "approve all" to accept all patterns
- Pattern numbers to modify (e.g., "2: entity=Spawner")
- "explain #N" for more detail
```

### Step 2: Ambiguity Resolution

For patterns where entity or property has multiple valid interpretations:

```
⚠️ Pattern #5 (Reference Points) requires clarification:

| Option | Entity | Rationale |
|--------|--------|-----------|
| A | StockManagementUnit | These are SMU-level reference points |
| B | ConservationUnit | These are CU-level benchmarks |
| C | Context-dependent | Use table prefix to determine |

**Recommendation**: Option C

Choose: [A] [B] [C] [D: Other]
```

### Step 3: Edge Case Review

For columns that don't fit patterns:

```
These [N] columns need individual review:

| # | Column | Table | Best Guess | Confidence | Alternative |
|---|--------|-------|------------|------------|-------------|
| 1 | EXPANSION_FACTOR | pop_year | entity=Stock, property=scalar | Low | Could be method parameter |
| 2 | pHOS | pop_year | entity=Stock, property=proportion | Medium | Could use entity=Spawner |

Reply with:
- "accept N" to use my guess
- "N: entity=X, property=Y" to override
- "skip N" to exclude
```

### Step 4: Apply Approved Patterns

Only after user confirms:
1. Generate full column_dictionary.csv
2. Use approved entity/property for all columns matching each pattern
3. Document remaining uncertainties in notes

---

## Confidence Thresholds

### High Confidence (proceed without asking)
- Column name exactly matches a worked example
- Pattern is unambiguous AND table context confirms entity
- Unit clearly indicates property

### Medium Confidence (note in output, batch for review)
- Pattern matches but entity has 2 valid options
- Column name follows pattern with variation
- Property is clear but constraint interpretation varies

### Low Confidence (must ask before proceeding)
- Novel column name
- Ambiguous units
- Table context conflicts with column name
- Multiple valid entity AND property interpretations

**Rule**: If >20% of measurement columns are Low Confidence, stop and ask for additional context.

---

## Approval Shorthand Syntax

| Command | Meaning |
|---------|---------|
| `approve all` | Accept all proposed patterns |
| `approve 1-5, 7` | Accept patterns 1-5 and 7 |
| `2: entity=Spawner` | Override pattern 2's entity |
| `2: property=ratio` | Override pattern 2's property |
| `5: context` | Use context-dependent entity |
| `reject 4` | Handle pattern 4 manually |
| `explain 3` | Get more detail on pattern 3 |
| `split 4` | Break pattern into sub-patterns |

---

## Entity Selection by Table Context

| Table Prefix | Default Entity | IRI |
|--------------|----------------|-----|
| `smu_*` | StockManagementUnit | `https://w3id.org/gcdfo/salmon#StockManagementUnit` |
| `cu_*` | ConservationUnit | `https://w3id.org/gcdfo/salmon#ConservationUnit` |
| `pop_*` | Stock (fallback) | `https://w3id.org/gcdfo/salmon#Stock` |
| `indicator_*` | Stock (fallback) | `https://w3id.org/gcdfo/salmon#Stock` |
| `pfma_*` | Stock | `https://w3id.org/gcdfo/salmon#Stock` |

**Override rules:**
- Column contains `CU_` in non-cu_* table → use ConservationUnit
- Column contains `SMU_` in non-smu_* table → use StockManagementUnit
- Column describes individual fish (LENGTH, WEIGHT) → use `dwc:Organism`
- Column describes spawning adults → use Stock + spawner constraint
- If unsure → ask user explicitly

---

## Salmon Patterns (Quick Cheatsheet)

| Pattern | Property | Entity | Unit | Constraints |
|---------|----------|--------|------|-------------|
| Age/location counts | count | [table context] | NUM | age class; location |
| Rates (exploitation/survival/mortality) | ratio | [table context] | UNITLESS | process or fishery segment |
| Reference points (LRP/USR) | benchmark | [table context] | depends | metric type |
| Length/weight | length or mass | dwc:Organism | cm or g | age class if present |

---

## Property IRI Conventions

### Counts and Abundance
- **Default**: `http://qudt.org/vocab/quantitykind/Count`
- **Alternative**: PATO count `http://purl.obolibrary.org/obo/PATO_0000070`

### Rates, Proportions, and Ratios
- **Default (unitless)**: `http://qudt.org/vocab/quantitykind/DimensionlessRatio`
- **If not unitless**: use closest QUDT quantity kind or propose a term

### Lengths and Masses
- **Length**: `http://qudt.org/vocab/quantitykind/Length`
- **Mass**: `http://qudt.org/vocab/quantitykind/Mass`

### Thresholds and Benchmarks
- Prefer `gcdfo:` reference point terms from `07-dfo-salmon-terms.csv`
- Use constraints to indicate underlying metric

### Unit IRIs (QUDT Preferred)
| Unit | IRI |
|------|-----|
| Counts | `http://qudt.org/vocab/unit/NUM` |
| Unitless ratios | `http://qudt.org/vocab/unit/UNITLESS` |
| Years | `http://qudt.org/vocab/unit/YR` |
| Centimeters | `http://qudt.org/vocab/unit/CentiM` |
| Grams | `http://qudt.org/vocab/unit/GM` |
| Kilograms | `http://qudt.org/vocab/unit/KiloGM` |

---

## Decomposition Hints (Name-Based Heuristics)

| Column Contains | Interpretation |
|-----------------|----------------|
| `AGE_` + number | constraint_iri = life-stage/age-class |
| `EXPLOITATION`, `MORTALITY`, `SURVIVAL`, `RATE` | property = DimensionlessRatio; unit = UNITLESS |
| `CPUE`, `CUE`, `EFFORT` | property = catch per effort; context includes gear |
| `LRP`, `USR`, `BENCHMARK` | property = reference point; constraint = underlying metric |
| `HATCHERY`, `WILD`, `MARKED`, `UNMARKED` | constraint_iri for origin/mark-status |
| `OCEAN`, `TERMINAL`, `MAINSTEM`, `TRIBUTARY` | constraint_iri for location segment |
| `METHOD`, `MODEL`, `SURVEY` suffix | method_iri (procedure); not constraint |

---

## Worked Examples (Expanded)

### Age/location catch (MAINSTEM_AGE_3 in smu_timeseries)
```
term_iri: http://rs.tdwg.org/dwc/terms/individualCount
unit_iri: http://qudt.org/vocab/unit/NUM
property_iri: http://qudt.org/vocab/quantitykind/Count
entity_iri: https://w3id.org/gcdfo/salmon#StockManagementUnit
constraint_iri: <age_3_IRI>;<mainstem_location_IRI>
method_iri: <procedure_IRI_if_applicable>
```

### Exploitation rate (TOTAL_EXPLOITATION_RATE in smu_timeseries)
```
term_iri: https://w3id.org/gcdfo/salmon#TotalExploitationRate
unit_iri: http://qudt.org/vocab/unit/UNITLESS
property_iri: http://qudt.org/vocab/quantitykind/DimensionlessRatio
entity_iri: https://w3id.org/gcdfo/salmon#StockManagementUnit
constraint_iri: <fishing_mortality_IRI>
```

### Escapement count (ESCAPEMENT_COUNT)
```
term_iri: https://w3id.org/gcdfo/salmon#EscapementMeasurement
unit_iri: http://qudt.org/vocab/unit/NUM
property_iri: http://qudt.org/vocab/quantitykind/Count
entity_iri: https://w3id.org/gcdfo/salmon#Stock
constraint_iri: <river_system_IRI>
```

### Length at age (LENGTH_AGE_3)
```
term_iri: http://purl.obolibrary.org/obo/CMO_0000013
unit_iri: http://qudt.org/vocab/unit/CentiM
property_iri: http://qudt.org/vocab/quantitykind/Length
entity_iri: http://rs.tdwg.org/dwc/terms/Organism
constraint_iri: <age_3_IRI>
```

### Reference point (LRP in cu_year)
```
term_iri: https://w3id.org/gcdfo/salmon#LimitReferencePoint
unit_iri: http://qudt.org/vocab/unit/NUM
property_iri: http://qudt.org/vocab/quantitykind/Count
entity_iri: https://w3id.org/gcdfo/salmon#ConservationUnit
constraint_iri: <metric_IRI_for_reference_point>
```

---

## Output Rules
- Keep SDP output order: dataset.csv, tables.csv, column_dictionary.csv, codes.csv
- If constraints >1, join with `;` in constraint_iri
- Do not invent IRIs; leave blank and propose new terms
