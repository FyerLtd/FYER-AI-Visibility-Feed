"""Build a canonical feed from governed manual seed observations."""

from __future__ import annotations

from dataclasses import dataclass

from .conflicts import detect_conflicts
from .dedupe import deduplicate_records
from .models import GovernanceRecord, RecordConflict, SourcePolicy
from .source_registry import validate_source_registry
from .validators import source_is_collection_eligible, validate_record


@dataclass(frozen=True)
class SeedBuildResult:
    """Result of validating and processing manual seed observations."""

    records: tuple[GovernanceRecord, ...]
    conflicts: tuple[RecordConflict, ...]
    errors: tuple[str, ...]

    @property
    def succeeded(self) -> bool:
        """Return whether the seed build completed without errors."""

        return not self.errors


def _normalize_source_name(value: str) -> str:
    """Return a conservative key for matching registered source names."""

    return value.strip().lower()


def build_manual_seed(
    records: list[GovernanceRecord],
    policies: list[SourcePolicy],
) -> SeedBuildResult:
    """Validate, govern, conflict-check, and deduplicate seed records.

    The build fails closed. It produces no canonical records when the source
    registry is invalid, a record is invalid, evidence is missing, evidence
    references an unregistered source, or the referenced source is not
    collection-eligible.
    """

    errors = validate_source_registry(policies)

    policies_by_name = {
        _normalize_source_name(policy.name): policy
        for policy in policies
    }

    for index, record in enumerate(records, start=1):
        for error in validate_record(record):
            errors.append(
                f"record {index} ({record.domain}): {error}"
            )

        if not record.evidence:
            errors.append(
                f"record {index} ({record.domain}): "
                "structured source evidence is required"
            )
            continue

        for evidence in record.evidence:
            source_key = _normalize_source_name(
                evidence.source_name
            )
            policy = policies_by_name.get(source_key)

            if policy is None:
                errors.append(
                    f"record {index} ({record.domain}): "
                    f"unregistered evidence source: "
                    f"{evidence.source_name}"
                )
                continue

            if not source_is_collection_eligible(policy):
                errors.append(
                    f"record {index} ({record.domain}): "
                    f"source is not collection-eligible: "
                    f"{policy.name}"
                )

    if errors:
        return SeedBuildResult(
            records=(),
            conflicts=(),
            errors=tuple(errors),
        )

    conflicts = detect_conflicts(records)
    canonical_records = deduplicate_records(records)

    return SeedBuildResult(
        records=tuple(canonical_records),
        conflicts=tuple(conflicts),
        errors=(),
    )
