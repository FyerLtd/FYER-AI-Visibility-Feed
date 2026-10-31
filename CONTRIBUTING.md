# Contributing to FYER AI Visibility Feed

Thank you for helping improve FYER AI Visibility Feed.

This project maintains an evidence-led catalogue of publicly discoverable AI services and domains for Shadow AI visibility, governance review, and security-tool integration.

> Inclusion supports visibility and review. It is not a recommendation to allow or block a service.

## Ways to contribute

Useful contributions include:

- proposing a publicly discoverable AI service;
- correcting an existing service name or domain;
- adding or improving first-party evidence;
- identifying stale or retired services;
- improving tests, documentation, validation, or export formats;
- proposing a potential public metadata source;
- improving approved source adapters;
- reporting data-quality or security issues.

## Before contributing

Please:

1. search existing Issues and Pull Requests;
2. confirm the proposed change is not already being discussed;
3. use public, attributable evidence;
4. avoid copying proprietary or promotional content;
5. keep the proposed change narrow and reviewable;
6. explain why the change is needed.

## Proposing an AI service

A service proposal should include:

- tool or service name;
- primary service domain;
- broad category;
- official or otherwise permitted evidence URL;
- date observed;
- a short factual note;
- any known ambiguity or conflicting evidence.

Prefer first-party evidence such as:

- an official product page;
- official documentation;
- an official service or sign-in page;
- an official vendor announcement.

Third-party sources may support a proposal, but should not replace available first-party evidence.

## Evidence requirements

Every feed record must retain:

- `source_name`
- `source_url`
- `observed_at`

Evidence must be:

- publicly accessible;
- relevant to the proposed service or domain;
- attributable to a named source;
- factual rather than promotional;
- sufficient for another reviewer to verify the observation.

Do not submit:

- private or confidential information;
- personal information;
- copied proprietary descriptions;
- copied rankings or reviews;
- bulk exports from third-party directories;
- evidence that requires bypassing access controls;
- unsupported claims about service safety or risk.

## Risk ratings

New records should normally use:

```text
risk_rating: unknown
```

`unknown` means the service has not been assessed under an approved, versioned risk methodology.

Do not assign `low`, `medium`, or `high` solely because:

- a service is well known;
- a service is unfamiliar;
- a service uses generative AI;
- a service appears in another blocklist;
- a reviewer personally approves or dislikes the service.

Until a versioned assessment methodology is published, risk-rating changes require maintainer review and supporting evidence.

## Source proposals

A source proposal is different from a service proposal.

Registering a source does not authorise collection from it.

A source proposal should include:

- source name;
- homepage URL;
- proposed collection method;
- proposed permitted metadata;
- Terms or usage-policy URL where applicable;
- robots URL for proposed HTML collection;
- known licensing or attribution requirements;
- the reason the source is useful;
- known limitations or risks.

Supported source states are:

```text
pending-review
approved
prohibited
```

New sources must begin as:

```text
pending-review
```

Only a maintainer may approve a source policy.

Automated collection must not be introduced until the source policy is approved and the relevant adapter is tested.

## Unacceptable contributions

The project will not accept:

- indiscriminate domain dumps;
- copied proprietary directories;
- copied marketing descriptions;
- copied rankings, ratings, or reviews;
- automated scraping without source approval;
- unexplained risk scores;
- automatic blocking recommendations;
- intentionally misleading or poisoned records;
- entries based on private user activity;
- changes that remove provenance to make a record appear more certain;
- source approval with no recorded reviewer or review date.

## Development setup

Requirements:

- Python 3.11 or later;
- Git.

Clone the repository:

```bash
git clone https://github.com/FyerLtd/FYER-AI-Visibility-Feed.git
cd FYER-AI-Visibility-Feed
```

Create a virtual environment:

```bash
python -m venv .venv
```

Install the project and development dependencies:

```bash
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

Run the test suite:

```bash
python -m pytest -q
```

Run the CLI:

```bash
python -m fyer_ai_visibility_feed.cli --help
python -m fyer_ai_visibility_feed.cli version
```

Build the governed manual feed:

```bash
python -m fyer_ai_visibility_feed.cli build-seed \
  --seed data/manual-seed.json \
  --registry data/sources.json \
  --output-dir outputs
```

On Windows PowerShell, the build command can be entered on one line:

```powershell
python -m fyer_ai_visibility_feed.cli build-seed --seed data/manual-seed.json --registry data/sources.json --output-dir outputs
```

Expected current results include:

```text
89 passed
Built 3 canonical record(s).
Conflicts: 0
```

## Tests

Add or update tests when changing:

- validation rules;
- normalisation behaviour;
- deduplication;
- conflict detection;
- source governance;
- provenance handling;
- loading or export formats;
- CLI behaviour;
- workflow behaviour.

A Pull Request should not reduce the test count without explaining why tests were removed or consolidated.

All tests and the governed feed build must pass before merge.

## Pull Request guidance

Keep Pull Requests focused.

A strong Pull Request includes:

- a clear title;
- a short explanation of the problem;
- the proposed change;
- evidence URLs where relevant;
- tests for changed behaviour;
- confirmation that the feed still builds;
- any policy or compatibility impact.

Avoid mixing unrelated code, data, policy, and documentation changes unless they are required for one controlled migration.

## Review and approval

Maintainers may request:

- stronger evidence;
- narrower scope;
- additional tests;
- a source-policy review;
- changes to wording or metadata;
- separation into multiple Pull Requests;
- removal of copied or unsupported content.

Maintainer acceptance of a record means the contribution meets the project's evidence and governance requirements. It does not mean FYER Ltd endorses the listed service.

## Security issues

Do not disclose exploitable security vulnerabilities in a public Issue.

Security reporting instructions will be maintained in `SECURITY.md`.

General data corrections and evidence improvements may use public Issues.

## Licence

By contributing, contributors agree that accepted contributions will be licensed under the repository's MIT License.
