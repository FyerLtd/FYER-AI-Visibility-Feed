FYER AI Visibility Feed
An open-source, evidence-led foundation for building governed AI visibility feeds for Shadow AI discovery, governance review, and security-tool integration.

Operators define the public sources used to build their feed. FYER AI Visibility Feed validates, normalises, deduplicates, preserves provenance, and produces integrity-verifiable feed artifacts from those inputs.

Feed inclusion supports visibility and review. It is not a recommendation to allow or block a service.

Why this project exists
Organisations need visibility of AI services that may be used outside approved technology, security, privacy, and data-governance processes.

Existing AI directories are generally designed for product discovery, promotion, rankings, or reviews. They are not necessarily suitable as governance evidence or security-control inputs.

FYER AI Visibility Feed provides a transparent and auditable way to:

build an AI visibility feed from operator-defined sources;
retain source evidence and observation timestamps;
detect conflicting information between observations;
normalise and conservatively deduplicate domains;
support Shadow AI discovery and governance review;
produce canonical feeds for later security-tool integration;
verify the integrity and provenance of generated feed artifacts;
preserve human review before enforcement decisions.
The project provides the governed processing foundation. It does not require or prescribe a centrally maintained catalogue of third-party AI services.

Governance principles
Visibility before restriction
Inclusion in a feed does not mean a service should be blocked.

Evidence before assertion
Every record must retain source evidence supporting the observation.

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
The project is designed to process the minimum metadata necessary to support AI visibility and governance. It is not intended to republish proprietary descriptions, rankings, reviews, or promotional content.

Operator-defined sources
Source selection is controlled by the operator. Operators are responsible for selecting and approving the sources used to construct their feed.

Integrity is verifiable
Generated artifacts include integrity metadata so that consumers can verify that feed outputs have not changed after generation.

Current capabilities
The project currently provides:

a Python 3.11 package and command-line interface;
governance-record validation;
structured source evidence;
conservative hostname normalisation;
domain-based deduplication;
provenance conflict detection;
a governed source registry;
a fail-closed feed-build pipeline;
canonical CSV and JSON exports;
feed-level generation metadata;
SHA-256 artifact checksums;
CI checksum verification;
GitHub artifact attestation;
GitHub Actions continuous integration;
downloadable governed feed artifacts;
97 automated tests.

Data flow
Operator-defined sources
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
       \         /
        \       /
         v     v
      manifest.json
           |
           v
       SHA256SUMS
           |
           v
   Artifact attestation
