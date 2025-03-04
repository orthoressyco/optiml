import numpy as np
import pytest

from optiml.opti import Quadratic
from optiml.opti.constrained import ActiveSet
from optiml.opti.utils import generate_box_constrained_quadratic


def test_ActiveSet():
    Q, q, ub = generate_box_constrained_quadratic(ndim=2)
    bcqp = ActiveSet(quad=Quadratic(Q, q), ub=ub)
    assert np.allclose(bcqp.minimize().x, bcqp.x_star())


if __name__ == "__main__":
    pytest.main()
