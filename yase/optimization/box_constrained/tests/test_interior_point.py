import numpy as np
import pytest

from yase.optimization.box_constrained import BoxConstrainedQuadratic, InteriorPoint


def test():
    assert np.allclose(InteriorPoint(BoxConstrainedQuadratic(seed=2)).minimize().x, 0.)


if __name__ == "__main__":
    pytest.main()
