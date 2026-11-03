# FYER AI Visibility Feed 

  

An open-source, evidence-led foundation for building governed AI visibility feeds for **Shadow AI discovery, governance review, and security-tool integration**. 

  

> **Operators define the public sources used to build their feed.** 

> FYER AI Visibility Feed validates, normalises, deduplicates, preserves provenance, and produces integrity-verifiable feed artifacts from those inputs. 

  

**Feed inclusion supports visibility and review. It is not a recommendation to allow or block a service.** 

  

## Why this project exists 

  

Organisations need visibility of AI services that may be used outside approved technology, security, privacy, and data-governance processes. 

  

Existing AI directories are generally designed for product discovery, promotion, rankings, or reviews. They are not necessarily suitable as governance evidence or security-control inputs. 

  

FYER AI Visibility Feed provides a transparent and auditable way to: 

  

- build an AI visibility feed from operator-defined sources; 

- retain source evidence and observation timestamps; 

- detect conflicting information between observations; 

- normalise and conservatively deduplicate domains; 

- support Shadow AI discovery and governance review; 

- produce canonical feeds for later security-tool integration; 

- verify the integrity and provenance of generated feed artifacts; 

- preserve human review before enforcement decisions. 

  

The project provides the governed processing foundation. It does not require or prescribe a centrally maintained catalogue of third-party AI services. 

  

## Governance principles 

  

1. **Visibility before restriction**   

   Inclusion in a feed does not mean a service should be blocked. 

  

2. **Evidence before assertion**   

   Every record must retain source evidence supporting the observation. 

  

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

   The project is designed to process the minimum metadata necessary to support AI visibility and governance. It is not intended to republish proprietary descriptions, rankings, reviews, or promotional content. 

  

9. **Operator-defined sources**   

   Source selection is controlled by the operator. Operators are responsible for selecting and approving the sources used to construct their feed. 

  

10. **Integrity is verifiable**   

    Generated artifacts include integrity metadata so that consumers can verify that feed outputs have not changed after generation. 

  

## Current capabilities 

  

The project currently provides: 

  

- a Python 3.11 package and command-line interface; 

- governance-record validation; 

- structured source evidence; 

- conservative hostname normalisation; 

- domain-based deduplication; 

- provenance conflict detection; 

- a governed source registry; 

- a fail-closed feed-build pipeline; 

- canonical CSV and JSON exports; 

- feed-level generation metadata; 

- SHA-256 artifact checksums; 

- CI checksum verification; 

- GitHub artifact attestation; 

- GitHub Actions continuous integration; 

- downloadable governed feed artifacts; 

- 97 automated tests. 

  

## Data flow 

  

```text 

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
       \\         / 
        \\       / 
         v      v 

      manifest.json 
           | 
           v 

       SHA256SUMS 
           | 
           v 

   Artifact attestation 

``` 

  

## Canonical record 

  

Each governance record contains: 

  

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

  

Records may begin with: 

  

```text 

risk_rating: unknown 

``` 

  

`unknown` is deliberately neutral. It does not mean that a service is safe, unsafe, approved, prohibited, or recommended for blocking. 

  

## Source governance 

  

Sources are defined in: 

  

```text 

data/sources.json 

``` 

  

The source registry is an input to the governed feed-building process. 

  

Registration does not itself authorise collection. 

  

Each source policy can record: 

  

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

  

Source selection belongs to the operator. FYER AI Visibility Feed does not require a centrally maintained catalogue of real-world services or sources to operate. 

  

Example and test configurations should use synthetic or operator-controlled data rather than being interpreted as an endorsed catalogue. 

  

## Outputs 

  

A governed build produces canonical artifacts including: 

  

```text 

feed.csv 

feed.json 

manifest.json 

SHA256SUMS 

``` 

  

### CSV 

  

`feed.csv` provides a simple and reviewable dataset suitable for spreadsheets, analysis, governance workflows, and later vendor-specific transformation. 

  

### JSON 

  

`feed.json` preserves the complete canonical records, including structured source evidence and observation timestamps. 

  

### Manifest 

  

`manifest.json` records metadata about the generated feed and its artifacts. 

  

### Checksums 

  

`SHA256SUMS` provides SHA-256 hashes that allow generated artifacts to be checked for unexpected modification. 

  

The CI workflow verifies artifact integrity and supports GitHub artifact attestation to provide additional provenance for governed builds. 

  

## Security-tool integration 

  

The canonical feed is deliberately vendor-neutral. 

  

Potential downstream integrations include: 

  

- Microsoft Defender; 

- Cloudflare Gateway; 

- Cisco Umbrella; 

- other DNS, Secure Web Gateway, CASB, SSE, or security-control platforms. 

  

Vendor-specific outputs must be separately validated before being treated as production-ready enforcement inputs. 

  

The canonical feed itself should not be interpreted as a blocklist. 

  

## Run locally 

  

### Requirements 

  

- Python 3.11 or later 

- Git 

  

Create a virtual environment and install the project: 

  

```bash 

python -m venv .venv 

python -m pip install --upgrade pip 

python -m pip install -e ".[dev]" 

``` 

  

On Windows PowerShell: 

  

```powershell 

.venv\\Scripts\\Activate.ps1 

``` 

  

On Linux or macOS: 

  

```bash 

source .venv/bin/activate 

``` 

  

Run the test suite: 

  

```bash 

pytest -q 

``` 

  

Build the governed feed using the configured source registry and input dataset: 

  

```bash 

python -m fyer_ai_visibility_feed.cli build-seed \\ 

  --seed data/manual-seed.json \\ 

  --registry data/sources.json \\ 

  --output-dir outputs 

``` 

  

On Windows PowerShell: 

  

```powershell 

python -m fyer_ai_visibility_feed.cli build-seed --seed data/manual-seed.json --registry data/sources.json --output-dir outputs 

``` 

  

The build produces the governed artifacts in the specified output directory. 

  

## Continuous integration 

  

GitHub Actions provides automated validation of the project and governed artifacts. 

  

The CI process: 

  

1. installs the project using Python 3.11; 

2. checks the CLI help and version commands; 

3. runs the complete automated test suite; 

4. builds the governed feed; 

5. validates the generated artifacts; 

6. generates and verifies SHA-256 checksums; 

7. uploads the governed build artifacts; 

8. supports artifact provenance through GitHub artifact attestation. 

  

Generated feed artifacts are build outputs rather than source-controlled substitutes for the underlying governance inputs. 

  

## Responsible use 

  

FYER AI Visibility Feed is designed to inform governance decisions. 

  

Before using a generated feed for web filtering or other security enforcement: 

  

- confirm the service identity and relevant domains; 

- review the supporting evidence; 

- confirm that the selected sources and collection methods are appropriate for the intended use; 

- assess the organisation's actual use case; 

- consider approved alternatives; 

- apply a documented risk methodology; 

- involve appropriate security, privacy, legal, and business stakeholders; 

- test the effect of any technical control; 

- provide an exception and review process. 

  

Do not treat feed inclusion as proof that a service is malicious, unsafe, unsuitable, or unauthorised. 

  

Operators remain responsible for ensuring that their selection and use of sources complies with applicable law, contractual terms, source policies, and organisational requirements. 

  

## Current limitations 

  

The project currently: 

  

- requires operator-defined source and record inputs; 

- does not provide a comprehensive catalogue of AI services; 

- does not automatically determine whether a source may lawfully be collected; 

- does not bypass authentication, access controls, CAPTCHAs, or other technical restrictions; 

- does not assign assessed risk ratings automatically; 

- does not automatically recommend allow or block actions; 

- does not provide production-ready vendor enforcement rules solely from feed inclusion. 

  

These boundaries are deliberate. 

  

The project provides evidence and visibility infrastructure. Governance and enforcement decisions remain human-controlled. 

  

## Roadmap 

  

Planned work includes: 

  

- improved operator source configuration; 

- documented source-review procedures; 

- JSON Schema publication; 

- versioned risk-assessment methodology; 

- controlled source adapters; 

- stale-evidence and service-retirement handling; 

- Microsoft Defender export validation; 

- Cloudflare Gateway export validation; 

- Cisco Umbrella export validation; 

- further integrity and provenance improvements. 

  

The roadmap will prioritise the AI visibility use case rather than general-purpose web scraping. 

  

## Licence 

  

This project is licensed under the MIT License. See `LICENSE`. 

  

The software licence does not grant rights to third-party websites, datasets, content, trademarks, or other materials selected by an operator as sources. 

  

## Maintainer 

  

FYER AI Visibility Feed is maintained by FYER Ltd. 
