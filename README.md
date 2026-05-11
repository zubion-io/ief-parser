# ief-parser

Read-only parser for Azure AD B2C custom policies (IEF) -> normalized JSON. MIT-licensed.

## Status

Early functional parser v0.1.0.

This repository contains a minimal read-only parser for Azure AD B2C Identity Experience Framework custom policy XML files.

## What this project is for

ief-parser normalizes selected Azure AD B2C custom policy structures into JSON so identity teams can inspect, document and reason about B2C legacy tenants before migration or modernization work.

Current v0.1.0 scope:

- TrustFrameworkPolicy metadata
- ClaimsSchema / ClaimType
- ClaimsProviders / TechnicalProfile IDs
- UserJourneys / OrchestrationStep references

## What this project is not

- Not a migration tool.
- Not a compiler.
- Not a production-ready security product.
- Not connected to any customer tenant.
- Not based on private customer data.
- Not a semantic translator from IEF to External ID.

## Example

Install dependencies:

    python -m pip install -e ".[dev]"

Parse a sample policy:

    python -m ief_parser parse tests/fixtures/local_accounts.xml --output policy.json

Run checks:

    python -m ruff check .
    python -m pytest

## Normalized JSON shape

The parser returns:

- policy: policyId and tenantId
- claims: id, type and displayName
- claimsProviders: id, displayName and technicalProfiles
- userJourneys: id and orchestrationSteps

## License

MIT.
