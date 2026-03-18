# Custom GPT upload pack for smn-gpt

This folder is the **canonical knowledge-base upload folder** for the ChatGPT Custom GPT deployment of `smn-gpt`.

If you want one place to upload from, use **this folder**.

## Upload rule

Upload the **20 numbered files** in this folder to the Custom GPT knowledge base.

Do **not** upload this `README.md` file itself unless you explicitly want it included as extra context.

## Files to upload

### Core guidance
1. `01-SYSTEM-PROMPT.md`
2. `02-SPECIFICATION.md`
3. `03-GLOSSARY.md`
4. `04-SKILLS-GUIDE.md`
5. `05-VOCABULARY-GUIDE.md`
6. `06-I-ADOPT-PATTERNS.md`

### Offline terminology and vocabulary files
7. `07-dfo-salmon-terms.csv`
8. `08-qudt-units.csv`
9. `09-qudt-quantity-kinds.csv`
10. `10-dwc-terms.csv`
11. `11-ontology-preferences.csv`
12. `12-iadopt-terminologies.csv`
19. `19-salmon-domain-terms.csv`

### Examples
13. `13-example-dataset.csv`
14. `14-example-tables.csv`
15. `15-example-column-dictionary.csv`
16. `16-example-codes.csv`

### Review and governance
17. `17-github-issue-templates.md`
18. `18-validation-checklist.md`
20. `20-metasalmon-workflow.md`

## Why this pack exists

A number of the numbered knowledge-base files referenced by earlier `smn-gpt` materials were not actually living in the `smn-gpt` repo. They were sitting in the older `smn-data-gpt` repo, especially under `custom-gpt-packs/`.

This folder fixes that by putting a concrete upload pack **inside the `smn-gpt` repo**.

## Source provenance

This pack was assembled by moving/copying the Custom GPT pack assets that were previously living in:

- `smn-data-gpt/custom-gpt-packs/smn-gpt-custom/`
- `smn-data-gpt/custom-gpt-packs/smn-gpt-custom-salmon-domain-first/`

Then adding one explicit workflow file for the current package-first direction:

- `20-metasalmon-workflow.md`

## Design intent

This upload pack is meant to support a GPT that connects:

- the MetaSalmon / `metasalmon` R package
- the Salmon Data Package specification
- the DFO Salmon Ontology (`gcdfo`)
- the shared Salmon Domain Ontology (`smn`)

The intended operating stance is:

- **package-first** when `metasalmon` is available
- **CSV-first** for standard outputs
- **review-first** for ambiguous semantics
- **shared `smn:` first, then `gcdfo:` when DFO-specific or needed as fallback**
- **no invented IRIs**

## Recommended operational use

### Preferred path
Use `metasalmon` first, then bring the package into the GPT for semantic review and gap triage.

### Alternate path
Use the GPT for a one-shot first pass only when the user is not starting in R.

## Repo relationship

The repo root no longer needs its own separate deployment prompt.

Use this folder for the offline Custom GPT deployment bundle.
Use the root `skills/` folder only for modular working-repo skills that may assume local tooling and, in some cases, network/API access.
