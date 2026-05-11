from __future__ import annotations

import json
from pathlib import Path

import typer

from ief_parser.parser import parse_policy

app = typer.Typer(no_args_is_help=True)


@app.callback()
def main() -> None:
    """Read-only parser for Azure AD B2C custom policies."""


@app.command("parse")
def parse_command(
    input_file: Path,
    output: Path | None = typer.Option(None, "--output", "-o"),
) -> None:
    result = parse_policy(input_file)
    text = json.dumps(result, indent=2, ensure_ascii=False)

    if output is None:
        typer.echo(text)
        return

    output.write_text(text + "\n", encoding="utf-8")
    typer.echo(f"Wrote normalized policy JSON to {output}")
