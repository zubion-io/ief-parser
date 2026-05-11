from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path


def _local_name(tag: str) -> str:
    if "}" in tag:
        return tag.rsplit("}", 1)[1]
    return tag


def _children(element: ET.Element, name: str) -> list[ET.Element]:
    return [child for child in list(element) if _local_name(child.tag) == name]


def _descendants(element: ET.Element, name: str) -> list[ET.Element]:
    return [node for node in element.iter() if _local_name(node.tag) == name]


def _first_child(element: ET.Element, name: str) -> ET.Element | None:
    for child in _children(element, name):
        return child
    return None


def _first_text(element: ET.Element, name: str) -> str | None:
    child = _first_child(element, name)
    if child is None or child.text is None:
        return None
    text = child.text.strip()
    return text or None


def _to_int(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def parse_policy(path: str | Path) -> dict[str, object]:
    policy_path = Path(path)
    tree = ET.parse(policy_path)
    root = tree.getroot()

    return {
        "policy": {
            "policyId": root.attrib.get("PolicyId"),
            "tenantId": root.attrib.get("TenantId"),
        },
        "claims": _parse_claims(root),
        "claimsProviders": _parse_claims_providers(root),
        "userJourneys": _parse_user_journeys(root),
    }


def _parse_claims(root: ET.Element) -> list[dict[str, str | None]]:
    claims: list[dict[str, str | None]] = []

    for claim_type in _descendants(root, "ClaimType"):
        claim_id = claim_type.attrib.get("Id")
        if not claim_id:
            continue

        claims.append(
            {
                "id": claim_id,
                "type": _first_text(claim_type, "DataType"),
                "displayName": _first_text(claim_type, "DisplayName"),
            }
        )

    return claims


def _parse_claims_providers(root: ET.Element) -> list[dict[str, object]]:
    providers: list[dict[str, object]] = []

    for provider in _descendants(root, "ClaimsProvider"):
        display_name = _first_text(provider, "DisplayName")
        domain = _first_text(provider, "Domain")
        technical_profiles: list[dict[str, str]] = []

        for technical_profile in _descendants(provider, "TechnicalProfile"):
            technical_profile_id = technical_profile.attrib.get("Id")
            if technical_profile_id:
                technical_profiles.append({"id": technical_profile_id})

        providers.append(
            {
                "id": domain or display_name or "unknown",
                "displayName": display_name,
                "technicalProfiles": technical_profiles,
            }
        )

    return providers


def _parse_user_journeys(root: ET.Element) -> list[dict[str, object]]:
    journeys: list[dict[str, object]] = []

    for journey in _descendants(root, "UserJourney"):
        journey_id = journey.attrib.get("Id")
        if not journey_id:
            continue

        orchestration_steps: list[dict[str, object]] = []

        for step in _descendants(journey, "OrchestrationStep"):
            references: list[str] = []

            for exchange in _descendants(step, "ClaimsExchange"):
                reference_id = exchange.attrib.get("TechnicalProfileReferenceId")
                if reference_id:
                    references.append(reference_id)

            orchestration_steps.append(
                {
                    "order": _to_int(step.attrib.get("Order")),
                    "type": step.attrib.get("Type"),
                    "technicalProfileReferences": references,
                }
            )

        journeys.append(
            {
                "id": journey_id,
                "orchestrationSteps": orchestration_steps,
            }
        )

    return journeys
