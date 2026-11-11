# Contributing to FYER AI Visibility Feed 

  

Thank you for helping improve FYER AI Visibility Feed. 

  

FYER AI Visibility Feed is an open-source foundation for building evidence-led lists of AI services and domains from operator-defined sources for Shadow AI visibility, governance review, and security-tool integration. 

  

The project provides the governed processing foundation. It does not maintain or accept a central catalogue of third-party AI services. 

  

Feed inclusion supports visibility and review. It is not a recommendation to allow or block a service. 

  

## Ways to contribute 

  

Useful contributions include: 

  

- fixing bugs; 

- improving tests and validation; 

- improving documentation; 

- improving domain normalisation or deduplication; 

- improving provenance and conflict detection; 

- improving source-governance controls; 

- proposing or improving source adapters; 

- developing vendor-specific export adapters; 

- improving artifact integrity or provenance controls; 

- reporting data-quality or security issues; 

- suggesting improvements to the governance model. 

  

Please do not submit third-party service catalogues or bulk domain lists as project data. 

  

## Before contributing 

  

Please: 

  

1. search existing Issues and Pull Requests; 

2. confirm the proposed change is not already being discussed; 

3. keep the proposed change narrow and reviewable; 

4. explain the problem being solved; 

5. add or update tests where behaviour changes; 

6. use synthetic or appropriately controlled example data; 

7. ensure that you have the right to submit any code, data, evidence, or other material included in the contribution. 

  

Do not copy proprietary datasets, descriptions, rankings, reviews, or other protected material into the repository. 

  

## Operator-defined sources 

  

Source selection belongs to the operator. 

  

The project does not prescribe or maintain a canonical list of AI services or third-party sources. 

  

Operators may configure sources appropriate to their own requirements and are responsible for ensuring that their selection and use of those sources complies with applicable law, contractual terms, source policies, licensing requirements, and organisational controls. 

  

A source being technically accessible does not by itself mean that collection from that source is approved. 

  

## Source governance 

  

Sources configured for use with the project are governed through the source registry. 

  

Registration does not authorise collection. 

  

Supported source states are: 

  

```text 

pending-review 

approved 

prohibited 

``` 

  

A newly configured source should begin as: 

  

```text 

pending-review 

``` 

  

Only an explicitly approved and valid source policy can become collection-eligible. 

  

Where applicable, a source policy should record: 

  

- source name; 

- homepage URL; 

- intended collection method; 

- permitted metadata; 

- Terms or usage-policy URL; 

- robots reference for proposed HTML collection; 

- known licensing or attribution requirements; 

- review date; 

- reviewer; 

- governance notes; 

- known limitations or risks. 

  

Automated collection should not be introduced for a source until its policy is approved and the relevant adapter has been tested. 

  

## Source adapters 

  

Contributions may propose support for a source type or source adapter. 

  

An adapter contribution should: 

  

- have a clearly defined purpose; 

- minimise the data collected; 

- preserve provenance; 

- fail closed when source approval is absent or invalid; 

- avoid bypassing authentication or technical access controls; 

- handle failures predictably; 

- include appropriate tests; 

- document any source-specific requirements or limitations. 

  

Acceptance of an adapter does not make the associated source part of a FYER-maintained catalogue and does not itself authorise collection from that source. 

  

## Evidence and provenance 

  

Where a record contains source evidence, the project's provenance requirements must be preserved. 

  

Structured evidence currently includes: 

  

```text 

source_name 

source_url 

observed_at 

``` 

  

Evidence should be: 

  

- attributable to an identified source; 

- relevant to the observation; 

- factual; 

- sufficient for another reviewer to understand the basis of the observation; 

- limited to the metadata necessary for the project's purpose. 

  

Do not submit: 

  

- private or confidential information; 

- personal information that is not necessary for the project; 

- copied proprietary descriptions; 

- copied rankings or reviews; 

- bulk exports from third-party directories; 

- proprietary third-party datasets; 

- evidence obtained by bypassing access controls; 

- unsupported claims about service safety or risk. 

  

## Risk ratings 

  

The canonical schema currently supports: 

  

```text 

risk_rating: unknown 

``` 

  

New or example records should normally retain `unknown`. 

  

`unknown` means that the service has not been assessed under an approved, versioned risk methodology. 

  

Do not assign `low`, `medium`, or `high` solely because: 

  

- a service is well known; 

- a service is unfamiliar; 

- a service uses generative AI; 

- a service appears on another organisation's list; 

- a reviewer personally approves or dislikes the service. 

  

Risk is contextual and may depend on organisational use, data, configuration, users, controls, purpose, and other factors. 

  

Until a versioned assessment methodology is published, changes away from `unknown` require maintainer review and supporting evidence. 

  

## Human review and enforcement 

  

FYER AI Visibility Feed provides visibility data. 

  

It is not itself a filtering or enforcement product. 

  

Feed records must not automatically become blocking rules solely because a service appears in the feed. 

  

Vendor-specific exporters may transform reviewed feed data into formats suitable for downstream security systems. Such outputs must remain subject to appropriate validation and human review before enforcement. 

  

Contributions that introduce automatic enforcement without an explicit review boundary will not be accepted. 

  

## Unacceptable contributions 

  

The project will not accept: 

  

- third-party service catalogues submitted as project data; 

- indiscriminate domain dumps; 

- copied proprietary directories; 

- bulk exports from third-party datasets without appropriate rights; 

- copied marketing descriptions; 

- copied rankings, ratings, or reviews; 

- automated collection that bypasses source governance; 

- attempts to bypass authentication, CAPTCHAs, rate limits, or other technical access controls; 

- unexplained risk scores; 

- automatic blocking recommendations based solely on feed inclusion; 

- intentionally misleading or poisoned records; 

- entries derived from private user activity; 

- changes that remove provenance to make an observation appear more certain; 

- source approval with no recorded review; 

- credentials, API keys, tokens, secrets, or other sensitive authentication material. 

  

## Development setup 

  

### Requirements 

  

- Python 3.13 or later 

- Git 

  

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

  

On Windows PowerShell: 

  

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

  

The current baseline is: 

  

```text 

97 passed 

``` 

  

Run the CLI: 

  

```bash 

python -m fyer_ai_visibility_feed.cli --help 

python -m fyer_ai_visibility_feed.cli version 

``` 

  

Build a governed feed using the configured input data and source registry: 

  

```bash 

python -m fyer_ai_visibility_feed.cli build-seed \ 

  --seed data/manual-seed.json \ 

  --registry data/sources.json \ 

  --output-dir outputs 

``` 

  

On Windows PowerShell, use one line: 

  

```powershell 

python -m fyer_ai_visibility_feed.cli build-seed --seed data/manual-seed.json --registry data/sources.json --output-dir outputs 

``` 

  

A successful governed build produces the project's canonical artifacts. 

  

Do not rely on a fixed number of generated records as a test of correctness. Input datasets and synthetic fixtures may change over time. 

  

## Tests 

  

Add or update tests when changing: 

  

- validation rules; 

- normalisation behaviour; 

- deduplication; 

- conflict detection; 

- source governance; 

- provenance handling; 

- source adapters; 

- loading or export formats; 

- artifact integrity controls; 

- CLI behaviour; 

- workflow behaviour. 

  

A Pull Request should not reduce the test count without explaining why tests were removed, replaced, or consolidated. 

  

All applicable tests and the governed feed build must pass before merge. 

  

## Pull Request guidance 

  

Keep Pull Requests focused. 

  

A strong Pull Request includes: 

  

- a clear title; 

- a short explanation of the problem; 

- the proposed change; 

- tests for changed behaviour; 

- confirmation that the governed build still succeeds; 

- source or technical documentation where relevant; 

- any governance, security, policy, or compatibility impact. 

  

Avoid mixing unrelated code, data, policy, and documentation changes unless they are required for one controlled migration. 

  

## Review and approval 

  

Maintainers may request: 

  

- narrower scope; 

- additional tests; 

- stronger technical justification; 

- stronger provenance; 

- a source-policy review; 

- changes to wording or metadata; 

- separation into multiple Pull Requests; 

- removal of copied or unsupported material; 

- additional validation around an adapter or exporter. 

  

Maintainer acceptance means that a contribution meets the project's technical and governance requirements. 

  

It does not mean that FYER Ltd endorses any third-party service, source, product, vendor, or resulting enforcement decision. 

  

## Security issues 

  

Do not disclose exploitable security vulnerabilities in a public Issue. 

  

Follow the reporting process in: 

  

```text 

SECURITY.md 

``` 

  

General bugs, documentation corrections, governance improvements, and non-sensitive data-quality issues may use public Issues. 

  

Never include credentials, access tokens, API keys, secrets, or sensitive security information in an Issue, Pull Request, test fixture, or example configuration. 

  

## Licence and contribution rights 

  

This project is licensed under the MIT License. See `LICENSE`. 

  

By submitting a contribution, you agree that your contribution may be distributed under the repository's MIT License and that you have the right to submit the contributed material. 

  

The repository's MIT License does not grant rights to third-party websites, datasets, content, trademarks, or other materials referenced or processed by an operator. 

  

## Maintainer 

  

FYER AI Visibility Feed is maintained by FYER Ltd. 

  
