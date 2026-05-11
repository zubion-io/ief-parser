# ief-parser

Read-only parser for Azure AD B2C custom policies (IEF) -> normalized JSON. MIT-licensed.

## Status

Early public scaffold.

This repository currently contains the project structure, packaging metadata, test scaffolding and CI only. Product logic will be added in later milestones.

## What this project is for

ief-parser is intended to become a read-only parser for Azure AD B2C Identity Experience Framework custom policy XML files.

The initial goal is to normalize public/custom policy structure into JSON so identity teams can inspect, document and reason about B2C legacy tenants before migration or modernization work.

## What this project is not

- Not a migration tool.
- Not a compiler.
- Not a production-ready security product.
- Not connected to any customer tenant.
- Not based on private customer data.

## Planned direction

- TrustFrameworkPolicy metadata
- ClaimsSchema
- ClaimsProviders
- TechnicalProfiles
- UserJourneys
- RelyingParty definitions

## Development

Install dependencies:

    python -m pip install -e ".[dev]"

Run checks:

    ruff check .
    pytest

## License

MIT.
