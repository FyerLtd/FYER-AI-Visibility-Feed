# Export Formats

## Purpose

FYER AI Visibility Feed produces neutral canonical outputs before any vendor-specific security format is created.

The current governed build writes:

```text
feed.csv
feed.json
```

These files support review, integration development, and future transformation. They are not automatic blocklists or production-ready vendor policy imports.

## Output generation

Build the governed repository seed with:

```bash
python -m fyer_ai_visibility_feed.cli build-seed \
  --seed data/manual-seed.json \
  --registry data/sources.json \
  --output-dir outputs
```

On Windows PowerShell:

```powershell
python -m fyer_ai_visibility_feed.cli build-seed --seed data/manual-seed.json --registry data/sources.json --output-dir outputs
```

Successful output:

```text
outputs/feed.csv
outputs/feed.json
```

The GitHub Actions workflow builds the same outputs, verifies both files are non-empty, and uploads them as the `fyer-ai-visibility-feed` artifact.

## Canonical CSV

### Purpose

CSV provides a flat, human-reviewable representation suitable for:

- spreadsheets;
- simple analysis;
- import prototyping;
- controlled transformation into downstream formats.

### Columns

The current column order is:

```text
tool_name
domain
category
sources
risk_rating
last_seen
notes
```

### Field representation

| Column | Representation |
| --- | --- |
| `tool_name` | Plain text. |
| `domain` | Canonical hostname. |
| `category` | Broad factual category. |
| `sources` | Source URLs joined with semicolons. |
| `risk_rating` | One of `unknown`, `low`, `medium`, or `high`. |
| `last_seen` | ISO date or empty string. |
| `notes` | Plain factual text. |

### CSV example

```csv
tool_name,domain,category,sources,risk_rating,last_seen,notes
Example AI,example.ai,general-purpose-ai,https://example.ai/product,unknown,2026-10-31,Manually reviewed from first-party evidence.
```

CSV quoting is handled by Python's standard CSV writer.

### CSV limitations

CSV does not include structured evidence because evidence is nested data.

The CSV `sources` field supports a simple list of URLs, but does not preserve each source's observation timestamp or source-policy identity.

Use JSON when complete provenance is required.

## Canonical JSON

### Purpose

JSON is the richer canonical interchange format.

It preserves:

- all canonical record fields;
- source URLs as an array;
- null values;
- structured evidence;
- observation timestamps.

### Current structure

The current JSON root is an array of records.

```json
[
  {
    "tool_name": "Example AI",
    "domain": "example.ai",
    "category": "general-purpose-ai",
    "sources": [
      "https://example.ai/product"
    ],
    "risk_rating": "unknown",
    "last_seen": "2026-10-31",
    "notes": "Manually reviewed from first-party evidence.",
    "evidence": [
      {
        "source_name": "Manual Seed Dataset",
        "source_url": "https://example.ai/product",
        "observed_at": "2026-10-31T10:08:00+00:00"
      }
    ]
  }
]
```

### JSON field representation

| Field | Representation |
| --- | --- |
| `tool_name` | JSON string. |
| `domain` | JSON string containing a canonical hostname. |
| `category` | JSON string. |
| `sources` | Array of URL strings. |
| `risk_rating` | JSON string. |
| `last_seen` | ISO date string or `null`. |
| `notes` | JSON string. |
| `evidence` | Array of evidence objects. |

Each evidence object contains:

```text
source_name
source_url
observed_at
```

`observed_at` is serialised using ISO 8601.

## Determinism and ordering

The current pipeline preserves input order for canonical records unless processing changes the record set through deduplication.

Within merged records:

- unique source URLs retain first-seen order;
- unique evidence items retain first-seen order;
- canonical domain values are normalised deterministically.

The current project does not sort records alphabetically during export.

Consumers must not rely on array or row position as a permanent identifier.

## Null and empty values

JSON uses:

```json
"last_seen": null
```

when no governed date exists.

CSV uses an empty field for the same state.

An empty `sources` list is invalid. A governed seed record without structured evidence is rejected by the manual-seed pipeline.

## Encoding

Exports use UTF-8.

CSV is written with newline handling suitable for Python's standard CSV module.

JSON is indented for review, preserves non-ASCII characters, and ends with a newline.

## Validation before export

The `export` command validates canonical records before writing outputs.

The `build-seed` command additionally validates:

- source registry;
- source eligibility;
- structured evidence;
- record fields;
- canonical domains.

A failed build returns a non-zero exit code and does not create feed files.

## GitHub Actions artifact

The CI workflow:

1. runs all tests;
2. builds the governed feed;
3. verifies `feed.csv` and `feed.json` are present and non-empty;
4. uploads both files as the `fyer-ai-visibility-feed` artifact.

Generated outputs are not committed to `main`.

Artifact consumers should retain:

- repository name;
- source commit;
- GitHub Actions run;
- download date;
- artifact digest where available.

## Integrity and signing roadmap

The current GitHub artifact has platform-provided run and artifact information, but the project does not yet publish a signed project-level manifest.

Planned integrity layers are:

1. SHA-256 digest for each output;
2. a machine-readable manifest listing files and digests;
3. feed-level metadata;
4. source commit and generator version;
5. source-registry and seed-data digests;
6. signed or keyless artifact attestation;
7. downstream verification instructions.

The planned model is:

```text
feed.csv  ---- SHA-256 ---+
                         |
feed.json ---- SHA-256 ---+--> manifest.json
                                  |
                                  v
                           signed attestation
```

## Feed-level metadata roadmap

The current JSON root is a record array. A future version may use an envelope:

```json
{
  "metadata": {
    "feed_name": "FYER AI Visibility Feed",
    "schema_version": "1.0",
    "feed_version": "0.1.0",
    "generated_at": "2026-10-31T11:54:27+00:00",
    "record_count": 3,
    "conflict_count": 0,
    "source_commit": "example",
    "licence": "MIT",
    "intended_use": "Governance visibility; not an automatic blocking recommendation."
  },
  "records": []
}
```

This is a roadmap example, not the current production schema.

## Vendor-specific exports

Vendor-specific formats are planned for systems such as:

- Microsoft Defender;
- Cloudflare Gateway;
- Cisco Umbrella.

These exports must be derived from the canonical feed.

They must not create separate independently maintained truth sets.

Before a vendor exporter is described as production-ready, it should document and test:

- accepted import schema;
- domain syntax;
- wildcard behaviour;
- maximum record counts;
- duplicate handling;
- allow or block semantics;
- comments and metadata support;
- update and rollback behaviour;
- exception handling;
- validation against the relevant vendor product.

The current CSV is not automatically equivalent to any vendor's enforcement format.

## Consumer responsibilities

Consumers must:

- verify evidence and service identity;
- review relevant domains;
- assess organisational context;
- apply an approved risk methodology;
- test downstream transformations;
- review allow or block consequences;
- operate exception and rollback processes;
- validate artifact integrity;
- avoid treating `unknown` as an enforcement verdict.

## Backward compatibility

The project is currently alpha-stage.

Consumers should pin to a known commit or artifact and review release notes before updating.

Future schema changes should distinguish:

- additive, backward-compatible fields;
- changed field meaning;
- removed or renamed fields;
- root-envelope changes;
- category or risk-vocabulary changes.

Breaking changes should use a new schema version with migration guidance.
