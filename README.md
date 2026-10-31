FYER AI Visibility Feed
A source-attributed catalogue of publicly discoverable AI services and domains for Shadow AI visibility, governance review and security-tool integration.

Open AI Governance Feed supports responsible AI adoption and risk-informed decision-making. It is not an indiscriminate AI blocklist.

Why this project exists
Organisations need visibility of publicly available AI services that may be used outside approved technology, security and data-governance processes.

Existing AI directories are primarily designed for product discovery, promotion, rankings or reviews. They are not necessarily suitable as governance evidence or security-control inputs.

Open AI Governance Feed provides a transparent and auditable way to:

identify publicly discoverable AI services and domains;
retain the source and observation time for each record;
detect conflicting information between observations;
normalise and conservatively deduplicate domains;
support Shadow AI discovery and governance review;
create outputs suitable for later security-tool integration;
preserve human review before enforcement decisions.
Governance principles
The project follows these principles:

Visibility before restriction
Inclusion in the feed does not mean a service should be blocked.

Evidence before assertion
Every record must retain publicly accessible source evidence.

Unknown is not safe or unsafe
An unknown risk rating means the service has not been assessed under an approved risk methodology.

Human review before enforcement
Feed records must not automatically become blocking rules.

Conservative deduplication
Records are merged only when their normalised hostnames match.

Conflicts remain visible
Disagreement between observations is surfaced for review rather than silently resolved.

Collection fails closed
A registered source is not collection-eligible unless its source policy is explicitly approved and valid.

Minimal metadata only
The project does not republish proprietary descriptions, rankings, reviews or promotional content.

Current status
The project currently provides:

a Python 3.11 package and command-line interface;
governance-record validation;
structured source evidence;
conservative hostname normalisation;
domain-based deduplication;
provenance conflict detection;
a governed source registry;
a fail-closed manual seed pipeline;
canonical CSV and JSON exports;
GitHub Actions continuous integration;
downloadable feed artifacts;
89 automated tests.
The initial manual dataset contains three first-party-evidenced records:

Microsoft Copilot;
ChatGPT;
Claude.
These records begin with:

risk_rating: unknown
