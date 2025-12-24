from pathlib import Path

import numpy as np
import typer
from typing_extensions import Annotated

from .matrix import Matrix


app = typer.Typer(add_completion=False)


@app.command()
def main(
    outdir: Annotated[
        Path,
        typer.Option("--outdir", "-o",
                     help="Directory where to save artifacts"),
    ] = Path("artifacts"),
) -> None:
    # 3.1 && 3.2:
    np.random.seed(0)
    a = Matrix(np.random.randint(0, 10, (10, 10)))
    b = Matrix(np.random.randint(0, 10, (10, 10)))

    (a + b).to_file(outdir / "matrix+.txt")
    (a * b).to_file(outdir / "matrix*.txt")
    (a @ b).to_file(outdir / "matrix@.txt")

    # 3.3:
    Matrix.clear_matmul_cache()
    np.random.seed(0)

    A = Matrix(np.array([[1, 2], [3, 4]]))
    B = Matrix(np.eye(2))
    C = Matrix(np.array([[2, 2], [3, 3]]))
    D = Matrix(np.eye(2))

    AB = A @ B
    CD = C @ D
    CD_true = Matrix(C.data @ D.data)
    
    assert hash(A) == hash(C)
    assert A != C
    assert B == D
    assert AB != CD_true

    outdir.mkdir(parents=True, exist_ok=True)
    A.to_file(outdir / "A.txt")
    B.to_file(outdir / "B.txt")
    C.to_file(outdir / "C.txt")
    D.to_file(outdir / "D.txt")
    AB.to_file(outdir / "AB.txt")
    CD_true.to_file(outdir / "CD.txt")

    (outdir / "hash.txt").write_text(
        f"hash(AB)={hash(AB)}\n"
        f"hash(CD)={hash(CD_true)}\n",
    )
    return


if __name__ == "__main__":
    app()
