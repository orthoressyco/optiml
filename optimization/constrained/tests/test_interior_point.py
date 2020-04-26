import numpy as np
import pytest

from optimization.constrained.interior_point import InteriorPoint
from optimization.optimization_function import BoxConstrained


def test():
    np.random.seed(2)
    assert np.allclose(InteriorPoint(BoxConstrained(n=2)).minimize()[0], 0.)


if __name__ == "__main__":
    pytest.main()
