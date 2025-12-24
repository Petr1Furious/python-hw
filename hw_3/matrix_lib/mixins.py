from __future__ import annotations

from pathlib import Path

import numpy as np


class FileSaveMixin:
    def to_file(self, path: str | Path, *, fmt: str = "%d") -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        np.savetxt(p, self.data, fmt=fmt)


class PrettyStrMixin:
    def __str__(self) -> str:
        return np.array2string(self.data)


class HashMixin:
    def __hash__(self) -> int:
        return int(self.data.sum())


class MatmulCacheMixin:
    _matmul_cache: dict[tuple[int, int], np.ndarray] = {}

    @classmethod
    def clear_matmul_cache(cls) -> None:
        cls._matmul_cache.clear()


class AccessorsMixin:
    _data: np.ndarray

    @property
    def data(self) -> np.ndarray:
        return self._data

    @data.setter
    def data(self, value: np.ndarray) -> None:
        arr = np.asarray(value)
        if arr.ndim != 2:
            raise ValueError("Matrix must be 2-dimensional")
        self._data = arr
