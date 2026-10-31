# Source Governance

## Purpose

Source governance controls which public metadata sources FYER AI Visibility Feed may use, how metadata may be recorded or collected, and which fields are permitted.

A public URL is evidence of availability. A public URL is not automatically permission to crawl, scrape, copy, republish, or rely on a source.

> Registration does not authorise collection.

## Source registry

Source policies are stored in:

```text
data/sources.json
```

Policies are loaded and validated by:

```text
src/fyer_ai_visibility_feed/source_registry.py
```

Eligibility rules are enforced by:

```text
src/fyer_ai_visibility_feed/validators.py
```

The governed manual-seed pipeline is implemented in:

```text
src/fyer_ai_visibility_feed/seed_pipeline.py
```

## Policy states

Every source uses one of three states:

### `pending-review`

The source is known to the project but has not been approved for collection.

Pending sources are not collection-eligible.

### `approved`

The source has a recorded governance decision defining:

- reviewer;
- review date;
- collection method;
- permitted metadata;
- restrictions and limitations;
- relevant Terms and robots references.

Approval is scoped to the recorded policy. Approval is not blanket permission to reuse all available content.

### `prohibited`

The source must not be used for collection under the current policy decision.

A prohibited source is not collection-eligible even if other fields appear complete.

## Collection methods

Allowed methods are:

```text
manual
api
feed
html
```

### Manual

A person individually reviews public evidence and records minimal factual metadata.

Manual approval does not permit bulk copying, automation, or collection beyond the recorded fields.

### API

Metadata is obtained through an API under the source's applicable terms and access controls.

Approved API collection requires a Terms or usage-policy reference.

Credentials, quotas, rate limits, attribution, retention, and redistribution conditions must be reviewed before implementation.

### Feed

Metadata is obtained from a published machine-readable feed.

Approved feed collection requires a Terms or usage-policy reference. Publication of a feed does not automatically permit unrestricted republication.

### HTML

Metadata is collected from rendered or source HTML.

Approved HTML collection requires:

- a Terms or usage-policy reference;
- a robots reference;
- explicit permitted metadata;
- a tested adapter;
- conservative request behaviour.

Robots information is one input to review. Robots permission alone does not establish copyright, database, contractual, privacy, or redistribution permission.

## Required policy fields

An approved source requires:

- a non-empty source name;
- a valid HTTP or HTTPS homepage URL;
- a supported collection status;
- a supported collection method;
- non-empty permitted metadata;
- a review date;
- a reviewer.

Approved automated sources require a Terms or usage-policy URL.

Approved HTML sources additionally require a robots URL.

## Permitted metadata

The source policy must list the minimum metadata approved for collection.

Examples include:

```text
tool_name
domain
category
source_url
last_seen
observed_at
```

Permitted metadata does not include unrelated content by implication.

The project does not accept copied proprietary descriptions, rankings, ratings, reviews, promotional content, or bulk directory exports unless a future policy explicitly documents a valid permission and use case.

## Current Manual Seed Dataset policy

The current repository policy approves `Manual Seed Dataset` for individually researched public metadata.

The approval permits the fields recorded in `data/sources.json` and does not authorise:

- automated crawling;
- automated scraping;
- proprietary content reuse;
- rankings or reviews;
- bulk copying from external directories;
- automatic risk assessment;
- automatic blocking recommendations.

## Source proposal process

A source proposal should provide:

- source name;
- homepage URL;
- proposed collection method;
- proposed permitted metadata;
- Terms or usage-policy URL where applicable;
- robots URL for proposed HTML collection;
- known licensing or attribution requirements;
- reason the source is useful;
- known limitations or risks.

New proposals begin as:

```text
pending-review
```

Source proposals should use the structured GitHub Issue form.

## Review considerations

A maintainer should assess:

- whether the source is first-party, third-party, promotional, community-maintained, or user-generated;
- whether evidence is attributable and independently reviewable;
- whether metadata is factual or opinion-based;
- access controls and authentication;
- Terms, usage policies, licences, and attribution requirements;
- robots information for HTML collection;
- privacy and personal-data exposure;
- database or compilation rights;
- redistribution restrictions;
- rate limits and service impact;
- content stability and stale-data risk;
- domain confusion or takeover risk;
- source poisoning or manipulation risk;
- whether a narrower method or field set would meet the need.

This list supports governance review and is not legal advice.

## Approval changes

Changing a source from `pending-review` to `approved` is a governance decision and should be isolated in a focused Pull Request.

The Pull Request should include:

- the policy change;
- review evidence;
- explicit permitted metadata;
- reviewer and review date;
- method-specific references;
- tests for eligibility and fail-closed behaviour;
- any adapter changes as a separate or clearly reviewable component.

Source approval must not be hidden inside an unrelated code or data change.

## Suspension and prohibition

A source should be suspended or prohibited when:

- permission is unclear or withdrawn;
- Terms materially change;
- robots information changes for HTML collection;
- evidence becomes unreliable or systematically stale;
- the source exposes personal or confidential information;
- an adapter causes harm or excessive load;
- provenance cannot be retained;
- source poisoning or manipulation is suspected;
- continued use creates unacceptable legal, security, privacy, or integrity risk.

A policy may be changed to `prohibited` while existing records are reviewed.

## Adapter requirements

A future automated source adapter must:

1. reference an approved source policy;
2. collect only permitted metadata;
3. retain source name, source URL, and observation timestamp;
4. respect method-specific controls;
5. return observations through the normal validation pipeline;
6. fail closed when policy or validation fails;
7. avoid silently resolving conflicts;
8. include deterministic tests;
9. avoid introducing credentials unless an approved design requires them;
10. avoid copying descriptions, rankings, or reviews outside approved scope.

An adapter must not approve its own source policy.

## Fail-closed enforcement

The manual-seed pipeline creates no canonical records when:

- the source registry is invalid;
- a record is invalid;
- structured evidence is missing;
- evidence names an unregistered source;
- the matched source is not collection-eligible.

The CLI returns a non-zero exit code and does not write feed outputs for failed builds.

## Provenance requirements

Every governed observation requires:

- `source_name`
- `source_url`
- `observed_at`

Source evidence should be sufficient for another reviewer to reproduce the observation.

Evidence may support visibility without establishing risk, approval, or enforcement status.

## Review frequency

The current project does not yet enforce automatic source-policy expiry.

Future policy metadata may include:

- next review date;
- review interval;
- Terms digest;
- robots digest;
- last successful collection;
- last evidence sample;
- suspension reason;
- policy version.

Until then, material source or adapter changes require a fresh maintainer review.

## Security reporting

Potential source poisoning, malicious adapters, collection-policy bypass, provenance substitution, or systematic feed manipulation should be reported privately under `SECURITY.md`.

Ordinary evidence corrections and stale-record reports should use the public Issue forms.
