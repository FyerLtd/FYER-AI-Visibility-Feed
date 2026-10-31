# Data Model

## Purpose

This document defines the current data contracts used by FYER AI Visibility Feed.

The data model separates service observations, structured evidence, conflicts, and source-governance policy. This separation supports traceability and prevents a public URL from being treated as permission to collect or as proof of a risk verdict.

> Inclusion supports visibility and review. It is not a recommendation to allow or block a service.

## Canonical models

The Python models are defined in:

```text
src/fyer_ai_visibility_feed/models.py
```

The current models are:

- `GovernanceRecord`
- `SourceEvidence`
- `RecordConflict`
- `SourcePolicy`

## GovernanceRecord

`GovernanceRecord` represents one AI-service observation or one canonical record produced from compatible observations.

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `tool_name` | string | Yes | Public service or product name. |
| `domain` | string | Yes | Service hostname used as the conservative identity key. |
| `category` | string | Yes | Broad factual service category. |
| `sources` | list of strings | Yes | Public evidence URLs associated with the record. |
| `risk_rating` | string | Yes | Current risk state. Defaults to `unknown`. |
| `last_seen` | date or null | No | Most recent observation date represented by the record. |
| `notes` | string | No | Short factual governance note. |
| `evidence` | list of `SourceEvidence` | Required by governed seed pipeline | Structured provenance for observations. |

### Domain requirements

The canonical `domain` field represents a hostname, not a complete URL.

Valid examples:

```text
chatgpt.com
claude.ai
copilot.cloud.microsoft
```

Invalid examples:

```text
https://chatgpt.com/
chatgpt.com/path
not a domain
```

The normaliser currently:

- trims surrounding whitespace;
- lowercases the hostname;
- removes a trailing DNS root dot;
- removes the conventional `www.` prefix;
- preserves other subdomains;
- does not parse arbitrary URLs into hostnames.

### Category requirements

`category` is currently a required non-empty string.

Categories should be broad and factual. A category must not imply safety, approval, quality, or enforcement status.

Example:

```text
general-purpose-ai
```

A controlled category vocabulary is planned but is not yet enforced.

### Sources requirements

`sources` must contain at least one valid HTTP or HTTPS URL.

The list supports simple attribution and CSV export. Structured provenance belongs in `evidence`.

### Risk ratings

Allowed values are:

```text
unknown
low
medium
high
```

New records should normally use:

```text
unknown
```

`unknown` means the service has not been assessed under an approved, versioned risk methodology. It does not mean safe, unsafe, allowed, blocked, low risk, or high risk.

Until a versioned methodology is published, changes to `low`, `medium`, or `high` require explicit maintainer review and supporting evidence.

### Last-seen date

`last_seen` is either:

- an ISO date represented in Python as `date`; or
- `null` when no governed date is available.

JSON example:

```json
"last_seen": "2026-10-31"
```

When duplicate records merge, the newest non-null `last_seen` value is retained.

### Notes

`notes` should be short, factual, and non-promotional.

Notes must not copy proprietary descriptions, rankings, reviews, or marketing text.

## SourceEvidence

`SourceEvidence` represents provenance for an individual observation.

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `source_name` | string | Yes | Name of the registered source policy. |
| `source_url` | string | Yes | Public HTTP or HTTPS evidence URL. |
| `observed_at` | datetime | Yes | Timestamp at which the evidence was observed. |

### Source-name relationship

The governed seed pipeline matches `source_name` to a policy in `data/sources.json` using trimmed, case-insensitive comparison.

An evidence source that is unregistered or not collection-eligible causes the build to fail closed.

### Source URL

`source_url` must be a valid HTTP or HTTPS URL.

The evidence URL should allow another reviewer to verify the observation. First-party evidence is preferred where available.

### Observation timestamp

`observed_at` is serialised to ISO 8601 in JSON.

Example:

```json
"observed_at": "2026-10-31T10:08:00+00:00"
```

Timezone-aware UTC timestamps are preferred.

## RecordConflict

`RecordConflict` records disagreement between observations that share a canonical domain.

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `domain` | string | Yes | Canonical domain shared by disputed observations. |
| `field_name` | string | Yes | Name of the disputed field. |
| `observed_values` | tuple of strings | Yes | Distinct values observed for the field. |
| `sources` | tuple of strings | Yes | Contributing source URLs. |

The current conflict fields are:

```text
tool_name
category
risk_rating
```

Different observation dates, notes, and source lists are not treated as conflicts.

Conflict detection reports disagreement. It does not select a winning value.

## SourcePolicy

`SourcePolicy` represents governance approval for a potential metadata source.

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `name` | string | Yes | Unique source-policy name. |
| `homepage_url` | string | Yes | Public source homepage. |
| `collection_status` | string | Yes | Governance state. Defaults to `pending-review`. |
| `collection_method` | string | Yes | Collection method. Defaults to `manual`. |
| `terms_url` | string or null | Conditional | Terms or usage-policy reference. |
| `robots_url` | string or null | Conditional | Robots reference for HTML collection. |
| `permitted_metadata` | list of strings | Required for approved sources | Minimum approved metadata fields. |
| `reviewed_at` | date or null | Required for approved sources | Governance review date. |
| `reviewer` | string or null | Required for approved sources | Recorded reviewer. |
| `notes` | string | No | Approval scope, restrictions, and limitations. |

### Collection statuses

Allowed values are:

```text
pending-review
approved
prohibited
```

A new source defaults to `pending-review`.

A source is collection-eligible only when:

- status is `approved`; and
- the complete policy validates successfully.

### Collection methods

Allowed values are:

```text
manual
api
html
feed
```

Approved automated methods (`api`, `html`, and `feed`) require a `terms_url`.

Approved HTML collection additionally requires a `robots_url`.

### Permitted metadata

`permitted_metadata` defines the minimum fields approved for collection or recording from a source.

Approval does not permit copying descriptions, rankings, reviews, marketing content, or unrelated fields that are not explicitly listed.

## Valid canonical JSON example

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

## Invalid examples

### Missing source URL

```json
{
  "tool_name": "Example AI",
  "domain": "example.ai",
  "category": "general-purpose-ai",
  "sources": []
}
```

Invalid because at least one source URL is required.

### URL in domain field

```json
{
  "domain": "https://example.ai/path"
}
```

Invalid because the canonical domain field requires a hostname.

### Unsupported risk rating

```json
{
  "risk_rating": "critical"
}
```

Invalid because the current vocabulary is `unknown`, `low`, `medium`, or `high`.

### Approved source without governance metadata

```json
{
  "name": "Example Directory",
  "homepage_url": "https://directory.example/",
  "collection_status": "approved",
  "collection_method": "manual",
  "permitted_metadata": [],
  "reviewed_at": null,
  "reviewer": null
}
```

Invalid because approved sources require permitted metadata, a review date, and a reviewer.

## Deduplication behaviour

Records merge only when their normalised hostnames match exactly.

The merge preserves:

- unique source URLs in first-seen order;
- unique structured evidence items;
- the newest non-null `last_seen` date;
- first-record values for fields not explicitly merged.

Examples that may merge:

```text
www.example.ai
Example.AI.
example.ai
```

Canonical result:

```text
example.ai
```

Examples that do not merge:

```text
chat.example.ai
api.example.ai
```

```text
amazing-ai.com
amazingai.com
```

## CSV representation

CSV contains these fields:

```text
tool_name
domain
category
sources
risk_rating
last_seen
notes
```

Multiple source URLs are joined into one field using a semicolon.

Structured evidence is not represented in CSV because it is nested data.

## JSON representation

JSON preserves all canonical record fields, including structured evidence.

JSON is the richer canonical interchange format and the intended basis for future schemas, APIs, metadata envelopes, manifests, and attestations.

## Schema evolution

The current JSON output does not yet include a feed-level schema envelope.

Planned metadata includes:

- schema version;
- feed version;
- generation timestamp;
- record count;
- conflict count;
- source commit;
- source-registry digest;
- seed-data digest;
- generator version;
- risk-methodology version;
- licence identifier;
- intended-use disclaimer.

Breaking changes should introduce a new schema version and migration guidance rather than silently changing field meaning.
