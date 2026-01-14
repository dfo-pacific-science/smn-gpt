# Cross-repo Dependencies

## At-a-glance graph (source → depends on)

- smn-data-pkg → foundation for metasalmon, salmonpy, smn-gpt (SPECIFICATION.md + schemas).
- dfo-salmon-ontology → semantics source for metasalmon, salmonpy, smn-gpt; term tables feed data-stewardship-unit.
- metasalmon ↔ salmonpy: salmonpy mirrors metasalmon (parity tests), metasalmon changes must be ported to salmonpy.
- smn-gpt → metasalmon workflows (skill), salmonpy CLI/helpers, dfo-salmon-ontology issue templates/TTL copy, smn-data-pkg spec copy.
- data-stewardship-unit → dfo-salmon-ontology term tables and theme config; hosts parity script that installs metasalmon and runs salmonpy tests.

## Per-repo notes and manual prompts

### smn-data-pkg

- Provides the canonical Salmon Data Package spec consumed by metasalmon and salmonpy (README.md, SPECIFICATION.md).
- Related projects listed in README.md include metasalmon and dfo-salmon-ontology; changelog calls out I-ADOPT adoption work.
- **Manual prompts when spec changes:** update metasalmon schemas/validation, salmonpy schemas/validators, and the smn-gpt copies of `SPECIFICATION.md` + `schema/` to avoid drift; refresh any example packages referenced by smn-gpt skills.

### metasalmon

- Uses dfo-salmon-ontology for semantics (README.md) and the smn-data-pkg spec for package structure.
- Vignettes reference `smn-gpt/SYSTEM-PROMPT.md` (vignettes/gpt-collaboration.Rmd) so GPT guidance stays aligned.
- AGENTS.md: any function changes must be reflected in the Python mirror at `../salmonpy`.
- **Manual prompts when metasalmon changes:** port equivalent updates to salmonpy (keep version parity noted in salmonpy README), rerun parity tests (`../salmonpy/tests/test_roundtrip.py` or `data-stewardship-unit/salmonpy/scripts/run-parity.sh`), and adjust smn-gpt skill text (`skills/metasalmon-usage/*`) plus any salmonpy helper snippets embedded in smn-gpt.

### salmonpy

- Python mirror of metasalmon; README notes alignment with metasalmon 0.0.3. Round-trip tests import metasalmon via R (`tests/test_roundtrip.py`, `scripts/run-parity.sh`).
- smn-gpt skills and entrypoints call salmonpy CLIs (`scripts/validate_sdp.py`, `scripts/draft_new_term.py`) and modules (`dictionary.py`, `semantics.py`, `term_search.py`, `package_io.py`).
- Uses dfo-salmon-ontology issue template in `scripts/draft_new_term.py`; term search honors BIOPORTAL_APIKEY and optional `SALMONPY_CACHE`.
- **Manual prompts when salmonpy API/CLIs change:** update smn-gpt entrypoints (`docs/entrypoints.md`) and skills that show salmonpy code paths, re-run parity tests against metasalmon, and bump the compatibility note in salmonpy README/CHANGELOG to match metasalmon.

### smn-gpt

- System prompt and skills point to metasalmon workflows (`skills/metasalmon-usage`) and salmonpy helpers (multiple skills + docs/entrypoints.md). RESOURCE preload expects `SPECIFICATION.md`, `schema/glossary.md`, `dfo-salmon.ttl`, canonical examples.
- Contains local copies of the spec/TTL (`SPECIFICATION.md`, `schema/*`, `dfo-salmon.ttl`) that should track smn-data-pkg and dfo-salmon-ontology.
- New-term flows link to dfo-salmon-ontology issue templates (skills/ontology-term-creation, ontology-term-mapping).
- **Manual prompts when upstreams change:** if metasalmon or salmonpy behavior/paths change, refresh the skills and system prompt examples; when smn-data-pkg spec or dfo-salmon-ontology TTL updates, sync the copies here to avoid stale guidance; keep I-ADOPT references consistent with metasalmon terminology files.

### data-stewardship-unit

- Hosts term tables from dfo-salmon-ontology under `data/ontology/release/artifacts/term-tables/` (meta files record `source_file` back to `../dfo-salmon-ontology/ontology/dfo-salmon.ttl`). `reference_info/data_standards/controlled-vocabulary-thesauri.qmd` prefers the sibling `../dfo-salmon-ontology/scripts/config/themes.yml` and falls back to the synced tables.
- README.md and `docs/TERM_TABLE_DOCUMENTATION_WORKFLOW.md` (in ontology repo) describe the sync flow via `../dfo-salmon-ontology/scripts/sync_term_tables_to_dsu.sh`.
- Contains a parity helper `salmonpy/scripts/run-parity.sh` that installs metasalmon (default `../metasalmon`) and runs salmonpy round-trip tests.
- Exec plan `docs/plans/2026-01-13-salmonpy-system-updates.md` documents co-development of salmonpy and smn-gpt (resource preload, ontology tracker links).
- **Manual prompts:** after ontology updates, regenerate and sync term tables from dfo-salmon-ontology then rebuild Quarto; when metasalmon/salmonpy change, update or rerun the parity script and adjust site notes if any guidance is embedded.

### dfo-salmon-ontology

- Script `scripts/sync_term_tables_to_dsu.sh` pushes generated term tables to `../data-stewardship-unit/data/ontology`; docs/TERM_TABLE_DOCUMENTATION_WORKFLOW.md details the pipeline that DSU renders.
- CONTRIBUTING.md directs contributors to check DSU’s Controlled Vocabulary page before filing issues.
- Upstream for semantic fields used by metasalmon/salmonpy/smn-gpt; smn-gpt ships a local `dfo-salmon.ttl`.
- **Manual prompts when ontology changes:** regenerate term tables (`python scripts/extract-term-tables.py`), sync to data-stewardship-unit, and refresh the TTL copy in smn-gpt; verify salmonpy new-term script links still match the GitHub issue templates.
