## Summary

Briefly explain the change and why it is needed.

## Change type

Select all that apply:

- [ ] AI service or domain proposal
- [ ] Evidence or data correction
- [ ] Source policy proposal or change
- [ ] Code change
- [ ] Test change
- [ ] Documentation change
- [ ] Workflow or dependency change
- [ ] Security-related change

## Evidence and provenance

Complete this section for data, service, domain, or source-policy changes.

- Evidence source name:
- Evidence URL:
- Date observed:
- Known ambiguity or conflicting evidence:

## Governance checks

- [ ] The change supports visibility and review; it is not an automatic allow or block recommendation.
- [ ] Public, attributable evidence is included where relevant.
- [ ] No private, confidential, or personal information is included.
- [ ] No proprietary descriptions, rankings, ratings, reviews, or bulk directory exports are copied.
- [ ] New records use `risk_rating: unknown` unless an approved, versioned methodology and supporting evidence justify another value.
- [ ] New sources begin as `pending-review` unless this Pull Request records an explicit maintainer approval decision.
- [ ] Automated collection is not introduced without an approved source policy and tested adapter.
- [ ] Provenance and conflicting evidence have not been removed or hidden.

## Testing

Describe the checks performed.

- [ ] `python -m pytest -q` passes.
- [ ] `python -m fyer_ai_visibility_feed.cli --help` succeeds.
- [ ] `python -m fyer_ai_visibility_feed.cli version` succeeds.
- [ ] The governed feed build succeeds where relevant.
- [ ] Tests were added or updated for changed behaviour.
- [ ] The test count was not reduced without explanation.

Current governed feed build command:

```bash
python -m fyer_ai_visibility_feed.cli build-seed \
  --seed data/manual-seed.json \
  --registry data/sources.json \
  --output-dir outputs
```

## Security and compatibility impact

Describe any effect on:

- validation or fail-closed behaviour;
- source eligibility;
- provenance or conflict detection;
- canonical CSV or JSON output;
- GitHub Actions or artifact generation;
- downstream consumers;
- backward compatibility.

Write `None` where there is no impact.

## Maintainer review notes

For maintainer use:

- [ ] Evidence reviewed
- [ ] Source policy reviewed, if applicable
- [ ] Security impact reviewed
- [ ] CI checks passed
- [ ] Conversations resolved
- [ ] Ready for squash merge
