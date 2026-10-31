"""Load and assess the governed public-source registry."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from .models import SourcePolicy
from .validators import (
    source_is_collection_eligible,
    validate_source_policy,
)


def load_source_registry(
    input_path: Path,
) -> list[SourcePolicy]:
    """Load source policies from a JSON registry."""

    with input_path.open(
        "r",
        encoding="utf-8",
    ) as registry_file:
        payload = json.load(registry_file)

    if not isinstance(payload, list):
        raise ValueError(
            "source registry must contain a JSON array"
        )

    policies: list[SourcePolicy] = []

    for index, item in enumerate(payload, start=1):
        if not isinstance(item, dict):
            raise ValueError(
                f"source registry item {index} must be an object"
            )

        reviewed_at_value = item.get("reviewed_at")

        policy = SourcePolicy(
            name=item["name"],
            homepage_url=item["homepage_url"],
            collection_status=item.get(
                "collection_status",
                "pending-review",
            ),
            collection_method=item.get(
                "collection_method",
                "manual",
            ),
            terms_url=item.get("terms_url"),
            robots_url=item.get("robots_url"),
          =list(
                item.get("permitted_metadata", [])
            ),
            reviewed_at=(
                date.fromisoformat(reviewed_at_value)
                if reviewed_at_value
                else None
            ),
            reviewer=item.get("reviewer"),
            notes=item.get("notes", ""),
        )

        policies.append(policy)

    return policies


def validate_source_registry(
    policies: list[SourcePolicy],
) -> list"""Return validation errors for all registered sources."""

    errors: list[str] = []
    seen_names: set[str] = set()

    for index, policy in enumerate(policies, start=1):
        normalized_name = policy.name.strip().lower()

        if normalized_name in seen_names:
            errors.append(
                f"source {index} has duplicate name: "
                f"{policy.name}"
            )
        else:
            seen_names.add(normalized_name)

        for error in validate_source_policy(policy):
            errors.append(
                f"source {index} ({policy.name}): {error}"
            )

    return errors


def collection_eligible_sources(
    policies: list[SourcePolicy],
) -> list"""Return only approved and valid collection sources."""

    return [
        policy
        for policy in policies
        if source_is_collection_eligible(policy)
    ]
