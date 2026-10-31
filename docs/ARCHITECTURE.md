# Architecture

## Overview

FYER AI Visibility Feed is an evidence-led pipeline for producing canonical records of publicly discoverable AI services and domains.

The architecture separates observation, source approval, validation, normalisation, conflict detection, deduplication, and export. This prevents raw discoveries from becoming enforcement inputs without passing explicit governance controls.

> Inclusion supports visibility and review. It is not a recommendation to allow or block a service.

## Architectural goals

The system is designed to provide:

- attributable public-source evidence;
- deterministic and testable processing;
- conservative domain normalisation;
- conservative deduplication;
- visible disagreement between observations;
- explicit source approval before collection;
- fail-closed behaviour;
- canonical CSV and JSON outputs;
- a stable base for future vendor-specific exporters;
- reviewable GitHub-based change control.

The system is not currently designed to provide:

- automatic risk verdicts;
- automatic allow or block decisions;
- unrestricted scraping;
- real-time service availability monitoring;
- a complete inventory of all AI services;
- production-ready vendor policy imports;
- signed or attested feed manifests.

## High-level data flow

```text
Candidate public evidence
          |
          v
Governed source registry
          |
          v
Load manual observations
          |
          v
Normalise domains
          |
          v
Validate records and evidence
          |
          v
Check evidence source registration and eligibility
          |
     +----+----+
     |         |
   invalid    valid
     |         |
     v         v
Fail closed   Detect conflicts
No outputs          |
                    v
             Deduplicate records
                    |
                    v
              Canonical records
               |           |
               v           v
            feed.csv    feed.json
               \           /
                \         /
                 v       v
          GitHub Actions artifact
```

## Trust boundaries

### 1. External evidence boundary

Public web pages and public service domains are external inputs. Public accessibility does not establish correctness, permission for automated collection, or suitability for enforcement.

Each observation must retain structured evidence:

- `source_name`
- `source_url`
- `observed_at`

### 2. Source-policy boundary

Potential sources are registered in `data/sources.json`.

A registered source is not automatically collection-eligible. Supported policy states are:

```text
pending-review
approved
prohibited
```

Eligibility requires an approved and valid source policy. The policy records the collection method, permitted metadata, reviewer, review date, and relevant Terms or robots references.

### 3. Repository boundary

Changes enter through protected branches and Pull Requests. The `main` branch requires the configured CI status check and uses squash merging.

Repository controls include:

- required Pull Requests;
- required CI;
- CodeQL analysis;
- secret scanning and push protection;
- private vulnerability reporting;
- structured Issue forms;
- Pull Request template;
- CODEOWNERS;
- Dependabot configuration.

### 4. Artifact boundary

Generated `feed.csv` and `feed.json` files are build outputs. They are uploaded from GitHub Actions rather than committed to `main`.

Consumers must retain the associated commit and workflow-run information. Signed project-level manifests and attestations are planned but are not yet implemented.

## Core data models

The core models are defined in:

```text
src/fyer_ai_visibility_feed/models.py
```

### GovernanceRecord

A canonical observation contains:

- `tool_name`
- `domain`
- `category`
- `sources`
- `risk_rating`
- `last_seen`
- `notes`
- `evidence`

The default risk rating is:

```text
unknown
```

`unknown` means the service has not been assessed under an approved, versioned risk methodology.

### SourceEvidence

Structured provenance for an observation contains:

- source name;
- source URL;
- UTC-capable observation timestamp.

### RecordConflict

A conflict records disagreement between observations that share a canonical domain. Conflict records contain:

- canonical domain;
- disputed field;
- observed values;
- contributing source URLs.

Conflict detection reports disagreement. Conflict detection does not decide which source is correct.

### SourcePolicy

A source policy contains:

- name;
- homepage URL;
- collection status;
- collection method;
- Terms URL;
- robots URL;
- permitted metadata;
- review date;
- reviewer;
- notes.

New policies default to `pending-review` and `manual`.

## Package structure

```text
src/fyer_ai_visibility_feed/
├── __init__.py
├── cli.py
├── conflicts.py
├── dedupe.py
├── exporters.py
├── loaders.py
├── models.py
├── normalizers.py
├── seed_pipeline.py
├── source_registry.py
└── validators.py
```

### `cli.py`

Provides the command-line interface:

```text
version
export
build-seed
```

`build-seed` is the governed end-to-end path for the current repository dataset.

### `models.py`

Defines governance records, source evidence, conflicts, and source policies.

### `validators.py`

Validates:

- required record fields;
- hostnames;
- HTTP and HTTPS evidence URLs;
- risk-rating values;
- structured evidence;
- source-policy states and methods;
- approval metadata;
- Terms and robots requirements for relevant collection methods.

The module also determines source collection eligibility.

### `normalizers.py`

Provides conservative hostname normalisation:

- trims surrounding whitespace;
- lowercases hostnames;
- removes a trailing DNS root dot;
- removes the conventional `www.` prefix;
- preserves other subdomains;
- does not treat an arbitrary URL as a hostname.

### `conflicts.py`

Groups observations by canonical domain and reports disagreement in governed fields such as:

- tool name;
- category;
- risk rating.

### `dedupe.py`

Merges records only when canonical hostnames match exactly.

The merge preserves:

- source URLs;
- structured evidence;
- the newest available `last_seen` date.

Similar names or related-looking domains are not sufficient for a merge.

### `loaders.py`

Loads canonical JSON into typed governance records and reconstructs dates, timestamps, and structured evidence.

### `exporters.py`

Writes canonical records to:

- CSV for simple review and later transformation;
- JSON for complete structured provenance.

### `source_registry.py`

Loads and validates `data/sources.json`, detects duplicate source names, and returns only approved and valid collection-eligible sources.

### `seed_pipeline.py`

Coordinates the governed manual-seed process:

1. validate the source registry;
2. normalise record domains;
3. validate records and evidence;
4. require structured evidence;
5. match evidence to registered source policies;
6. reject unregistered or ineligible sources;
7. fail closed when any error exists;
8. detect conflicts;
9. deduplicate canonical records.

## Repository data

```text
data/
├── manual-seed.json
└── sources.json
```

### `sources.json`

Stores governed source policies.

The current Manual Seed Dataset policy permits individually researched public metadata. The policy does not authorise automated crawling, scraping, proprietary content reuse, rankings, reviews, or bulk directory copying.

### `manual-seed.json`

Stores the current manually reviewed observations. The initial dataset contains first-party-evidenced records for:

- Microsoft Copilot;
- ChatGPT;
- Claude.

These records currently use `risk_rating: unknown`.

## Validation and fail-closed behaviour

The pipeline returns no canonical records when any governed input fails validation.

Examples include:

- invalid source registry;
- invalid record;
- missing evidence;
- unregistered evidence source;
- source that is not collection-eligible.

The CLI returns a non-zero exit code for failed builds. Failed builds do not create canonical feed files.

## Conflict handling

Conflicts are not validation failures by themselves.

A successful build may produce:

- canonical records;
- a non-zero conflict count.

This permits governance review without silently discarding or resolving contradictory observations.

Future work may add an explicit review queue and value-to-source conflict mapping.

## Output formats

### CSV

`feed.csv` contains a flat representation suitable for review, spreadsheets, and future vendor transformation.

Multiple source URLs are represented in a delimited field. Structured evidence is not flattened into CSV.

### JSON

`feed.json` contains the complete canonical record and structured evidence.

JSON is the richer canonical interchange format for future APIs, schemas, manifests, and attestations.

## Command-line interfaces

Display version:

```bash
python -m fyer_ai_visibility_feed.cli version
```

Validate and re-export canonical JSON:

```bash
python -m fyer_ai_visibility_feed.cli export \
  --input canonical.json \
  --output-dir outputs
```

Build the governed repository seed:

```bash
python -m fyer_ai_visibility_feed.cli build-seed \
  --seed data/manual-seed.json \
  --registry data/sources.json \
  --output-dir outputs
```

## Continuous integration

The GitHub Actions workflow:

1. checks out the repository;
2. installs Python 3.11;
3. installs the project and development dependencies;
4. verifies CLI help and version behaviour;
5. runs the automated test suite;
6. builds the governed feed;
7. verifies both outputs are non-empty;
8. uploads the feed artifact.

The workflow uses read-only repository-content permissions and does not commit generated artifacts to `main`.

## Security design

Current security properties include:

- minimal runtime dependencies;
- explicit validation;
- fail-closed source governance;
- no repository secrets required by the feed build;
- protected `main` branch;
- required CI;
- CodeQL analysis;
- secret scanning and push protection;
- Dependabot alerts and scheduled update proposals;
- private vulnerability reporting;
- generated artifacts kept outside source control.

Security reporting is defined in `SECURITY.md`.

## Testing strategy

The test suite covers:

- CLI help, version, export, and governed seed build;
- governance-record validation;
- evidence validation;
- domain normalisation;
- conservative deduplication;
- provenance preservation;
- conflict detection;
- CSV and JSON exports;
- JSON round trips;
- source-policy validation;
- source-registry validation;
- fail-closed manual-seed behaviour;
- the actual repository seed;
- end-to-end artifact generation behaviour.

Changes to security-relevant or governance-relevant behaviour require corresponding tests.

## Extension points

Planned extension points include:

- approved public-source adapters;
- JSON Schema publication;
- feed-level metadata;
- schema and feed versioning;
- evidence-ageing and retirement handling;
- reviewed risk methodology;
- vendor-specific exporters;
- checksums and signed manifests;
- keyless artifact attestations;
- conflict-review workflows.

Each source adapter must remain behind source-policy approval and must return observations through the same validation and provenance pipeline.

## Architectural decisions

### Domain is the conservative identity key

The current deduplication key is the normalised hostname. Fuzzy service-name matching is deliberately excluded because a false merge can corrupt evidence and downstream governance decisions.

### Source policy is separate from evidence

Evidence says where an observation came from. Source policy says whether and how the project is allowed to collect metadata from that source.

Keeping these concepts separate prevents a public URL from being treated as collection permission.

### Canonical data is separate from vendor enforcement formats

The project produces a neutral canonical feed first. Microsoft Defender, Cloudflare Gateway, Cisco Umbrella, and other outputs should be derived from that canonical source rather than maintained independently.

### Human review remains part of the system

The software validates evidence, reports conflicts, and generates consistent artifacts. The software does not replace organisational risk assessment, exception handling, privacy review, legal review, or business approval.
