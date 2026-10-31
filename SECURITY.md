# Security Policy

FYER Ltd takes the security and integrity of FYER AI Visibility Feed seriously.

The project produces evidence-led data that may inform governance and security decisions. A vulnerability or malicious contribution could therefore affect not only the software, but also the trustworthiness of generated feed artifacts.

## Supported versions

FYER AI Visibility Feed is currently an alpha-stage project.

Security fixes are applied to the latest version of the `main` branch. Older commits, downloaded artifacts, forks, and locally modified copies are not separately supported.

| Version | Supported |
| --- | --- |
| Latest `main` branch | Yes |
| Older commits or artifacts | No |
| Third-party forks | No |

## Reporting a security vulnerability

Do not disclose exploitable vulnerabilities in a public GitHub Issue, Pull Request, Discussion, commit message, or social-media post.

Use GitHub's private vulnerability reporting feature for this repository when it is available:

1. Open the repository's **Security** tab.
2. Select **Report a vulnerability**.
3. Provide the information requested below.

If private vulnerability reporting is not available, contact FYER Ltd through the contact route published at [FYER](https://fyer.co.uk) and clearly mark the message as a confidential security report.

Do not include secrets, credentials, personal data, or unnecessary sensitive information in an initial report.

## What to include

A useful report includes:

- a concise description of the issue;
- the affected file, module, workflow, artifact, or version;
- the commit hash or GitHub Actions run, where relevant;
- the expected security property;
- the observed behaviour;
- minimal reproduction steps;
- the potential impact;
- any known preconditions;
- suggested remediation, if available;
- whether the issue has been disclosed elsewhere.

Provide evidence sufficient to reproduce and assess the issue, while avoiding unnecessary access to third-party systems or data.

## Security issues in scope

Examples include:

- arbitrary code execution;
- command, path, or data injection;
- unsafe parsing of source, seed, registry, or feed files;
- validation bypasses;
- source-policy or collection-eligibility bypasses;
- provenance removal or substitution;
- conflict suppression that could conceal contradictory evidence;
- deduplication errors that merge unrelated services in a security-relevant way;
- malicious or unauthorised source adapters;
- feed poisoning or unauthorised record insertion;
- artifact tampering or substitution;
- compromised GitHub Actions workflows or dependencies;
- exposure of repository, workflow, or package credentials;
- dependency vulnerabilities that affect this project;
- domain confusion, abandoned-domain, or domain-takeover risks affecting feed integrity;
- a method of causing invalid data to produce apparently valid feed outputs;
- a method of bypassing fail-closed behaviour;
- vulnerabilities in future signature, checksum, manifest, or attestation handling.

## Data-quality reports that are not security vulnerabilities

The following should normally use a public GitHub Issue rather than confidential security reporting:

- a service name correction;
- an outdated official evidence URL;
- a service that has been retired;
- a missing public AI service;
- a category disagreement;
- a duplicate record;
- a normalisation edge case without security impact;
- a general documentation correction.

Use confidential reporting instead when a data-quality issue appears intentional, systematic, exploitable, or capable of misleading downstream security decisions.

## Responsible testing

When investigating this project:

- use repositories, branches, artifacts, and systems that you own or are authorised to test;
- avoid accessing unrelated user or organisational data;
- do not bypass third-party access controls;
- do not scrape or bulk-copy external services without permission;
- do not introduce malicious records into the production branch;
- do not disrupt GitHub Actions, package infrastructure, or downstream consumers;
- use minimal test data;
- remove secrets and personal data from logs and screenshots;
- stop testing if continued activity may harm another party.

A security report does not grant permission to test third-party AI services, domains, vendors, directories, or infrastructure.

## Feed integrity and downstream use

Inclusion in FYER AI Visibility Feed is not proof that a service is malicious, safe, approved, or unsuitable.

Consumers must not treat the feed as an automatic blocklist. Consumers remain responsible for:

- verifying service identity and relevant domains;
- reviewing source evidence;
- applying an appropriate risk methodology;
- assessing organisational context;
- testing technical controls;
- operating exception and review processes;
- validating artifact integrity before use.

Until signed manifests or attestations are published, consumers should obtain artifacts from the repository's official GitHub Actions runs and retain the relevant commit and run information with downloaded artifacts.

## Disclosure and remediation

FYER Ltd will assess reports based on reproducibility, impact, exploitability, and effect on feed or artifact integrity.

Where appropriate, remediation may include:

- a code or configuration fix;
- additional validation;
- new regression tests;
- withdrawal or replacement of an artifact;
- correction or removal of affected feed records;
- source-policy suspension or prohibition;
- dependency or workflow updates;
- documentation of downstream mitigations;
- coordinated disclosure after a fix is available.

Public disclosure should be coordinated with FYER Ltd so that maintainers and downstream consumers have a reasonable opportunity to apply relevant fixes or mitigations.

## Secrets

Do not commit or submit:

- passwords;
- API keys;
- access tokens;
- private keys;
- session cookies;
- personal data;
- confidential client or supplier information;
- private vulnerability details.

If a secret is exposed, revoke or rotate it through the issuing service. Removing a secret from the latest commit does not remove it from Git history or existing clones.

## Dependency and workflow security

Changes to dependencies and GitHub Actions must remain reviewable and narrowly scoped.

Contributors should:

- use official or well-established dependencies;
- avoid unnecessary runtime dependencies;
- preserve least-privilege workflow permissions;
- avoid adding secrets unless an approved design requires them;
- add or update tests for security-relevant behaviour;
- explain changes to artifact generation, validation, provenance, or source governance.

## No bounty commitment

FYER AI Visibility Feed does not currently operate a bug-bounty programme. Submission of a report does not create an entitlement to payment, reward, employment, or public credit.

Any acknowledgement is at FYER Ltd's discretion and will not disclose the reporter's identity without permission.

## Safe harbour intent

FYER Ltd supports good-faith security research that follows this policy, avoids harm, respects applicable law and third-party rights, and reports findings responsibly.

This statement does not authorise activity against third-party systems and is not legal advice.
