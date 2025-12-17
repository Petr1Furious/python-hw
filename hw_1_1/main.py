import typer
from typing_extensions import Annotated
import sys


app = typer.Typer()


@app.command()
def main(
    infile: Annotated[
        typer.FileText,
        typer.Argument(metavar="filename", help="Input file or stdin if not set"),
    ] = sys.stdin,
):
    for num, line in enumerate(infile.readlines()):
        typer.echo(f"{num + 1:6}\t{line}", nl=False)


if __name__ == "__main__":
    app()
