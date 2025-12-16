import typer
from typing_extensions import Annotated
import sys
from pathlib import Path


app = typer.Typer()


def tail_lines(lines: list[str], n: int) -> list[str]:
    return lines[-n:] if len(lines) >= n else lines


@app.command()
def main(
    files: Annotated[
        list[Path],
        typer.Argument(metavar="files", help="Input files"),
    ] = None,
):
    if not files:
        lines = sys.stdin.readlines()
        for line in tail_lines(lines, 17):
            typer.echo(line, nl=False)
    else:
        for i, filepath in enumerate(files):
            if len(files) > 1:
                if i > 0:
                    typer.echo()
                typer.echo(f"==> {filepath} <==")
            with open(filepath) as f:
                lines = f.readlines()
            for line in tail_lines(lines, 10):
                typer.echo(line, nl=False)


if __name__ == "__main__":
    app()
