from __future__ import annotations

from typing import Any

import numpy as np
from numpy.lib.mixins import NDArrayOperatorsMixin

from .mixins import AccessorsMixin, FileSaveMixin, HashMixin, MatmulCacheMixin, PrettyStrMixin


class Matrix(
    NDArrayOperatorsMixin,
    FileSaveMixin,
    PrettyStrMixin,
    AccessorsMixin,
    HashMixin,
    MatmulCacheMixin,
):
    __hash__ = HashMixin.__hash__

    def __init__(self, data: Any) -> None:
        self.data = np.asarray(data)

    def __array__(self, dtype: Any | None = None) -> np.ndarray:
        return np.asarray(self.data, dtype=dtype)

    @staticmethod
    def _require_same_shape(a: Matrix, b: Matrix, op: str) -> None:
        if a.data.shape != b.data.shape:
            raise ValueError(
                f"Invalid shape for '{op}': {a.data.shape} vs {b.data.shape}"
            )

    def __array_ufunc__(
        self,
        ufunc: np.ufunc,
        method: str,
        *inputs: Any,
        **kwargs: Any,
    ) -> Any:
        if method == "__call__" and len(inputs) == 2:
            a, b = inputs
            if isinstance(a, Matrix) and isinstance(b, Matrix):
                Matrix._require_same_shape(a, b, ufunc.__name__)

        unwrapped_inputs = [x.data if isinstance(
            x, Matrix) else x for x in inputs]

        if "out" in kwargs and kwargs["out"] is not None:
            out = kwargs["out"]
            kwargs["out"] = tuple(
                x.data if isinstance(x, Matrix) else x
                for x in out
            )

        result = getattr(ufunc, method)(*unwrapped_inputs, **kwargs)

        if method == "at":
            return None

        if isinstance(result, tuple):
            return tuple(Matrix(x) if isinstance(x, np.ndarray) else x for x in result)

        return Matrix(result) if isinstance(result, np.ndarray) else result

    def __matmul__(self, other: Any) -> Matrix:
        rhs = other.data
        if self.data.shape[1] != rhs.shape[0]:
            raise ValueError(
                f"Invalid shape for '@': {self.data.shape} vs {rhs.shape}"
            )
        key = (hash(self), hash(other))
        cached = self._matmul_cache.get(key)
        if cached is None:
            cached = self.data @ rhs
            self._matmul_cache[key] = cached
        return Matrix(cached)
