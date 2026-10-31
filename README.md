# FYER AI Visibility Feed

An open-source, evidence-led catalogue of publicly discoverable AI services and domains for Shadow AI visibility, governance review, and security-tool integration.

> Inclusion supports visibility and review. It is not a recommendation to allow or block a service.

## Why this project exists

Organisations need visibility of publicly available AI services that may be used outside approved technology, security, privacy, and data-governance processes.

Existing AI directories are generally designed for product discovery, promotion, rankings, or reviews. They are not necessarily suitable as governance evidence or security-control inputs.

FYER AI Visibility Feed provides a transparent and auditable way to:

- identify publicly discoverable AI services and domains;
- retain source evidence and observation timestamps;
- detect conflicting information between observations;
- normalise and conservatively deduplicate domains;
- support Shadow AI discovery and governance review;
- produce canonical feeds for later security-tool integration;
- preserve human review before enforcement decisions.

## Governance principles

1. **Visibility before restriction**  
   Inclusion in the feed does not mean a service should be blocked.

2. **Evidence before assertion**  
   Every record must retain publicly accessible source evidence.

3. **Unknown is not safe or unsafe**  
   An `unknown` risk rating means the service has not been assessed under an approved risk methodology.

4. **Human review before enforcement**  
   Feed records must not automatically become blocking rules.

5. **Conservative deduplication**  
   Records are merged only when their normalised hostnames match.

6. **Conflicts remain visible**  
   Disagreement between observations is surfaced for review rather than silently resolved.

7. **Collection fails closed**  
   A registered source is not collection-eligible unless its source policy is explicitly approved and valid.

8. **Minimal metadata only**  
   The project does not republish proprietary descriptions, rankings, reviews, or promotional content.

## Current status

The project currently provides:

- a Python 3.11 package and command-line interface;
- governance-record validation;
- structured source evidence;
- conservative hostname normalisation;
- domain-based deduplication;
- provenance conflict detection;
- a governed source registry;
- a fail-closed manual seed pipeline;
- canonical CSV and JSON exports;
- GitHub Actions continuous integration;
- downloadable feed artifacts;
- 89 automated tests.

The initial manually reviewed dataset contains three first-party-evidenced records:

- Microsoft Copilot;
- ChatGPT;
- Claude.

These records begin with `risk_rating: unknown`. Their inclusion supports governance visibility and is not a blocking recommendation.

## Data flow

```text
Approved public evidence
          |
          v
Governed source registry
          |
          v
Record and provenance validation
          |
          v
Domain normalisation
          |
          +----> Conflict detection
          |
          v
Conservative deduplication
          |
          v
Canonical feed
     |           |
     v           v
  feed.csv    feed.json
```

## Canonical record

Each governance record currently contains:

- `tool_name`
- `domain`
- `category`
- `sources`
- `risk_rating`
- `last_seen`
- `notes`
- structured `evidence`

Structured evidence contains:

- `source_name`
- `source_url`
- `observed_at`

## Outputs

The governed build creates:

```text
feed.csv
feed.json
```

### CSV

The CSV output provides a simple, reviewable catalogue suitable for spreadsheets and later vendor-specific transformation.

### JSON

The JSON output preserves the complete canonical record, including structured source evidence and observation timestamps.

Vendor-specific exports for Microsoft Defender, Cloudflare Gateway, and Cisco Umbrella are planned, but they are not yet represented as production-ready import formats.

## Source governance

Potential sources are registered in:

```text
data/sources.json
```

Registration does not authorise collection.

Each source policy records:

- source name and homepage;
- collection status;
- collection method;
- permitted metadata;
- Terms and robots references where applicable;
- review date;
- reviewer;
- governance notes.

Supported collection states are:

```text
pending-review
approved
prohibited
```

Only an approved and valid source policy can become collection-eligible.

The current `Manual Seed Dataset` approval permits individually researched public metadata only. It does not authorise automated crawling, scraping, proprietary content reuse, rankings, reviews, or bulk directory copying.

## Run locally

Requirements:

- Python 3.11 or later;
- Git.

Create a virtual environment and install the project:

```bash
python -m venv .venv
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

On Linux or macOS:

```bash
source .venv/bin/activate
```

Run the tests:

```bash
pytest -q
```

Build the governed manual feed:

```bash
python -m open_ai_governance_feed.cli build-seed \
  --seed data/manual-seed.json \
  --registry data/sources.json \
  --output-dir outputs
```

On Windows PowerShell, use one line:

```powershell
python -m open_ai_governance_feed.cli build-seed --seed data/manual-seed.json --registry data/sources.json --output-dir outputs
```

Successful execution creates:

```text
outputs/feed.csv
outputs/feed.json
```

> The internal Python package retains its original technical name temporarily. A dedicated package-rename checkpoint will migrate it safely without mixing branding changes with functional changes.

## Continuous integration

The GitHub Actions workflow:

1. installs the project using Python 3.11;
2. checks the CLI help and version commands;
3. runs the complete automated test suite;
4. builds the governed feed;
5. verifies both output files are present and non-empty;
6. uploads the outputs as a downloadable artifact.

The workflow has read-only repository permissions and does not commit generated files to the default branch.

## Responsible use

FYER AI Visibility Feed is designed to inform governance decisions.

Before using the feed for web filtering or security enforcement:

- confirm the service identity and relevant domains;
- review the supporting evidence;
- assess the organisational use case;
- consider approved alternatives;
- apply a documented risk methodology;
- involve appropriate security, privacy, legal, and business stakeholders;
- test the effect of any technical control;
- provide an exception and review process.

Do not treat feed inclusion as proof that a service is malicious, unsafe, or unsuitable.

## Current limitations

The project currently:

- uses a small manually reviewed seed dataset;
- does not perform automated public-source collection;
- does not perform live domain or service availability checks;
- does not assign assessed risk ratings;
- does not automatically recommend allow or block actions;
- does not yet publish signed feed manifests;
- does not yet provide production-ready vendor import formats.

These limitations are deliberate while the governance and evidence model is established.

## Roadmap

Planned work includes:

- contributor and source-submission controls;
- documented source-review procedures;
- JSON Schema publication;
- versioned risk-assessment methodology;
- feed-level metadata and generation manifests;
- SHA-256 checksums and signed attestations;
- approved public-source adapters;
- Microsoft Defender export validation;
- Cloudflare Gateway export validation;
- Cisco Umbrella export validation;
- stale-evidence and service-retirement handling.

## Licence

This project is licensed under the MIT License. See `LICENSE`.

## Maintainer

FYER AI Visibility Feed is maintained by FYER Ltd.
