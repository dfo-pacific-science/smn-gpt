# ExecPlan: Align procedure/method semantics (`method_iri`, `gcdfo:usedProcedure`)

## Purpose / Big Picture

Bring the ecosystem into sync on **procedures/methods**:

- Ontology-side: use `gcdfo:usedProcedure` (an annotation subproperty of `sosa:usedProcedure`) for linking a **variable SKOS concept** to a procedure/method concept.
- SDP-side: keep the existing `column_dictionary.csv.method_iri` column name (for compatibility), but document it as a **procedure/method IRI** (not an I-ADOPT property), aligned to SOSA `sosa:Procedure` / `sosa:usedProcedure`.

The goal is to remove lingering references to `gcdfo:iadoptMethod` and to stop describing `method_iri` as “I-ADOPT method”, since I-ADOPT intentionally does not model methods/procedures.

## Progress

- [x] 2026-01-14: Draft ExecPlan (this document).
- [x] 2026-01-14 15:01: Confirm remaining `gcdfo:iadoptMethod` references; keep only explicit legacy/deprecation mentions.
- [x] 2026-01-14 15:01: Update SDP + guidance docs to clarify `method_iri` semantics as procedure/method.
- [x] 2026-01-14 15:01: Run right-sized validation (cross-repo `rg` checks).

## Surprises & Discoveries

- `gcdfo:iadoptMethod` appeared outside `dfo-salmon-ontology/docs/CONVENTIONS.md` (e.g., `../metasalmon/inst/extdata/custom-gpt-prompt.md`); it is now only referenced as legacy/deprecated.
- `method_iri` was documented as “I-ADOPT method IRI” in multiple places (e.g., `../smn-data-pkg/SPECIFICATION.md`), but I-ADOPT scope explicitly excludes methods/procedures (this has now been corrected in docs).
- `gcdfo:usedProcedure` is currently a **documented convention** and may not yet be declared in `../dfo-salmon-ontology/ontology/dfo-salmon.ttl` (doc-only phase is OK if that remains the project stance).

## Decision Log

- 2026-01-14: Keep SDP schema column name `method_iri` (backwards compatibility) and update documentation to treat it as a **procedure/method IRI** aligned to SOSA, not as an I-ADOPT property.
- 2026-01-14: Use `gcdfo:usedProcedure` (annotation subproperty of `sosa:usedProcedure`) for variable-concept → procedure links; reserve `sosa:usedProcedure` for observation/sampling instance data.

## Outcomes & Retrospective

- Completed: docs/prompts updated across `../dfo-salmon-ontology`, `../smn-data-pkg`, `../metasalmon`, and `smn-gpt` so `gcdfo:usedProcedure` is canonical and `method_iri` is a procedure/method IRI (SOSA-aligned, not an I-ADOPT role).
- Remaining (optional): if/when moving beyond doc-only, declare `gcdfo:usedProcedure` in `../dfo-salmon-ontology/ontology/dfo-salmon.ttl` and run ontology QA.

## Context and Orientation

### Workspace layout (assumed)

Sibling repos live next to `smn-gpt`:

- `../dfo-salmon-ontology`
- `../smn-data-pkg`
- `../metasalmon`
- `../salmonpy`
- `../data-stewardship-unit` (only if term-table regeneration becomes necessary)

### Definitions (terms of art)

- **IRI**: a globally-unique identifier used in RDF/OWL (looks like a URL).
- **SKOS**: W3C standard for controlled vocabularies; a `skos:Concept` is a term/value, not an OWL class.
- **OWL**: W3C ontology language for classes/properties/axioms used for reasoning.
- **Annotation property**: an OWL property used for metadata-style links (not used in logical class axioms).
- **SOSA**: W3C/OGC vocabulary for observations/sampling/sensors; procedures are modeled as `sosa:Procedure`, linked from observations via `sosa:usedProcedure`.
- **I-ADOPT**: an RDA-endorsed framework for decomposing observable variables (property, object-of-interest, constraints, etc.); it intentionally does **not** model methods/procedures.

## Plan of Work (by dependency)

### 1) dfo-salmon-ontology (semantics + conventions)

**Goal:** ensure docs and planning notes consistently use `gcdfo:usedProcedure`, not `gcdfo:iadoptMethod`.

- Update `../dfo-salmon-ontology/docs/todo_list.md`:
  - Replace mentions of `(… iadoptMethod)` with `(… usedProcedure)` and adjust wording from “method” to “procedure” where it refers to the SOSA layer.
- Optional (only if the repo is ready to move beyond doc-only):
  - Declare `gcdfo:usedProcedure a owl:AnnotationProperty ; rdfs:subPropertyOf sosa:usedProcedure` in `../dfo-salmon-ontology/ontology/dfo-salmon.ttl`.
  - If you do this, you must run ontology QA (see Validation section) and potentially regenerate/sync term tables to DSU.

### 2) smn-data-pkg (SDP spec + schema docs)

**Goal:** keep schema stable, but fix the semantics in prose.

- Update `../smn-data-pkg/SPECIFICATION.md`:
  - Change the `method_iri` description from “I-ADOPT method IRI” to “procedure/method IRI (aligns to SOSA `sosa:Procedure`; not part of I-ADOPT)”.
- Update `../smn-data-pkg/schemas/column_dictionary.csv`:
  - Update the `method_iri` description similarly (keep the column name unchanged).
- Consider updating the minimal example docs (`../smn-data-pkg/examples/minimal-example/README.md`) if it repeats the old “I-ADOPT method” framing.

### 3) metasalmon (GPT prompt + docs sources)

**Goal:** ensure metasalmon’s GPT prompt matches the new ontology convention.

- Update `../metasalmon/inst/extdata/custom-gpt-prompt.md`:
  - In the “copied I-ADOPT annotations” rule, replace `gcdfo:iadoptMethod` with `gcdfo:usedProcedure`.
  - Keep the `method_iri` guidance but clarify it points to a procedure/method concept (SOSA-aligned), not “I-ADOPT method”.
- If you update any `vignettes/` sources, regenerate the pkgdown site (do not edit `../metasalmon/docs/` directly).

### 4) smn-gpt (skills + vocabulary docs + examples)

**Goal:** stop calling `method_iri` “I-ADOPT methods” and align guidance with SOSA procedure semantics.

- Update:
  - `docs/vocabulary.md` and `docs/vocabulary_refined.md` (`method_iri` section heading + text)
  - `skills/i-adopt-decomposition/i-adopt-decomposition.md` (replace “I-ADOPT … method” language; describe procedure/method and SOSA alignment)
  - `skills/ontology-term-mapping/ontology-term-mapping.md` (same)
  - `examples/spsr-reference/iadopt_decompositions.md` (ensure “method_iri” description matches procedure/method semantics)
  - `naming_conventions.md` if it frames method_iri as I-ADOPT

### 5) salmonpy (only if schema changes)

If (and only if) you decide to rename `method_iri` → `procedure_iri` at the schema level, you must update salmonpy’s schema handling and any validators/readers. This ExecPlan assumes **no rename** (docs-only semantics fix), so salmonpy changes should not be required.

## Concrete Steps (commands + expected results)

Run these from `smn-gpt`:

1) Find remaining references to the deprecated property:
   - `rg --follow -n "gcdfo:iadoptMethod|iadoptMethod" ..`
   - Expect: only intentional deprecation notes remain (ideally zero).

2) Find “I-ADOPT method” phrasing that should become “procedure/method”:
   - `rg --follow -n "\\bI-ADOPT method\\b|\\bI-ADOPT methods\\b" ..`

3) After edits, confirm the canonical property shows up where expected:
   - `rg --follow -n "gcdfo:usedProcedure" ../dfo-salmon-ontology ../metasalmon smn-gpt ../smn-data-pkg`

## Validation and Acceptance

**Acceptance criteria:**

- No remaining functional references to `gcdfo:iadoptMethod` in docs/prompts (unless explicitly called out as deprecated).
- `method_iri` is consistently described as **procedure/method** and explicitly **not** an I-ADOPT property.
- No schema column rename occurs (unless you choose to expand this ExecPlan to cover a breaking change).

**Right-sized validation:**

- Doc-only changes:
  - Re-run the `rg` checks above.
- If ontology TTL is changed:
  - In `../dfo-salmon-ontology`: run `devenv shell make test` (or at least `devenv shell make theme-coverage`) and ensure it passes.
- If smn-data-pkg schemas change (CSV schema text updates):
  - Sanity-check CSV formatting (no stray commas/quotes) and confirm examples still match headers.

## Idempotence and Recovery

- All changes should be safe to re-run: `rg` searches are read-only; doc edits are deterministic.
- If you need to roll back, use `git checkout -- <file>` in the affected repo (or `git restore <file>`).
- Prefer doing the work repo-by-repo with small commits to reduce cross-repo confusion (do not mix unrelated changes).
