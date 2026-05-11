import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from ief_parser.cli import app
from ief_parser.parser import parse_policy

FIXTURES = Path(__file__).parent / "fixtures"


def test_parse_local_accounts_extracts_claims_provider_and_journey() -> None:
    result = parse_policy(FIXTURES / "local_accounts.xml")

    assert result["policy"]["policyId"] == "B2C_1A_LocalAccounts"
    assert {"id": "email", "type": "string", "displayName": "Email Address"} in result["claims"]
    assert result["claimsProviders"][0]["displayName"] == "Local Account"
    assert result["claimsProviders"][0]["technicalProfiles"] == [
        {"id": "SelfAsserted-LocalAccountSignin-Email"}
    ]
    assert result["userJourneys"][0]["id"] == "SignUpOrSignIn"
    assert result["userJourneys"][0]["orchestrationSteps"][0]["technicalProfileReferences"] == [
        "SelfAsserted-LocalAccountSignin-Email"
    ]


@pytest.mark.parametrize(
    "fixture_name",
    [
        "local_accounts.xml",
        "social_accounts.xml",
        "social_and_local_accounts.xml",
    ],
)
def test_parse_all_public_style_fixtures(fixture_name: str) -> None:
    result = parse_policy(FIXTURES / fixture_name)

    assert result["claims"]
    assert result["claimsProviders"]
    assert result["userJourneys"]


def test_cli_parse_writes_json(tmp_path: Path) -> None:
    output_path = tmp_path / "policy.json"
    runner = CliRunner()

    result = runner.invoke(
        app,
        [
            "parse",
            str(FIXTURES / "local_accounts.xml"),
            "--output",
            str(output_path),
        ],
    )

    assert result.exit_code == 0
    data = json.loads(output_path.read_text(encoding="utf-8"))
    assert data["policy"]["policyId"] == "B2C_1A_LocalAccounts"
    assert data["claims"]
