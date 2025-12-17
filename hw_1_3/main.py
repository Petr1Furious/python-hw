import typer
from typing_extensions import Annotated, List
import sys
from pathlib import Path


app = typer.Typer()


def count_stats(content: str) -> tuple[int, int, int]:
    lines = content.count("\n")
    words = len(content.split())
    bytes_ = len(content.encode())
    return lines, words, bytes_


def format_stats(lines: int, words: int, bytes_: int, width: int) -> str:
    return f"{lines:>{width}} {words:>{width}} {bytes_:>{width}}"


@app.command()
def main(
    files: Annotated[
        list[Path],
        typer.Argument(metavar="files", help="Input files"),
    ] = None,
):
    if not files:
        content = sys.stdin.read()
        lines, words, bytes_ = count_stats(content)
        typer.echo(format_stats(lines, words, bytes_, 7))
    else:
        total_lines, total_words, total_bytes = 0, 0, 0
        stats = []
        for filepath in files:
            with open(filepath, "rb") as f:
                raw = f.read()
            content = raw.decode()
            lines, words, bytes_ = count_stats(content)
            stats.append((lines, words, bytes_, str(filepath)))
            total_lines += lines
            total_words += words
            total_bytes += bytes_

        max_val = max(total_bytes, total_words, total_lines) if len(
            files) > 1 else max(s[2] for s in stats)
        width = len(str(max_val))

        for lines, words, bytes_, name in stats:
            typer.echo(f"{format_stats(lines, words, bytes_, width)} {name}")

        if len(files) > 1:
            typer.echo(
                f"{format_stats(total_lines, total_words, total_bytes, width)} total")


if __name__ == "__main__":
    app()
