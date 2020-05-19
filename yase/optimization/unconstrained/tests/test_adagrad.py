import numpy as np
import pytest

from yase.optimization.unconstrained import quad1, quad2, Rosenbrock
from yase.optimization.unconstrained.stochastic import AdaGrad


def test_AdaGrad_quadratic():
    assert np.allclose(AdaGrad(f=quad1, x=np.random.uniform(size=2), step_size=0.1).minimize().x,
                       quad1.x_star(), rtol=0.1)
    assert np.allclose(AdaGrad(f=quad2, x=np.random.uniform(size=2), step_size=0.15).minimize().x,
                       quad2.x_star(), rtol=0.1)


def test_AdaGrad_Rosenbrock():
    rosen = Rosenbrock()
    assert np.allclose(AdaGrad(f=rosen, x=np.random.uniform(size=2), step_size=0.1).minimize().x,
                       rosen.x_star(), rtol=0.1)


def test_AdaGrad_standard_momentum_quadratic():
    assert np.allclose(AdaGrad(f=quad1, x=np.random.uniform(size=2), momentum_type='standard').minimize().x,
                       quad1.x_star(), rtol=0.1)
    assert np.allclose(AdaGrad(f=quad2, x=np.random.uniform(size=2), step_size=0.1,
                               momentum_type='standard').minimize().x, quad2.x_star(), rtol=0.1)


def test_AdaGrad_standard_momentum_Rosenbrock():
    rosen = Rosenbrock()
    assert np.allclose(AdaGrad(f=rosen, x=np.random.uniform(size=2), momentum_type='standard').minimize().x,
                       rosen.x_star(), rtol=0.1)


def test_AdaGrad_nesterov_momentum_quadratic():
    assert np.allclose(AdaGrad(f=quad1, x=np.random.uniform(size=2), momentum_type='nesterov').minimize().x,
                       quad1.x_star(), rtol=0.1)
    assert np.allclose(AdaGrad(f=quad2, x=np.random.uniform(size=2), step_size=0.1,
                               momentum_type='nesterov').minimize().x, quad2.x_star(), rtol=0.1)


def test_AdaGrad_nesterov_momentum_Rosenbrock():
    rosen = Rosenbrock()
    assert np.allclose(AdaGrad(f=rosen, x=np.random.uniform(size=2), momentum_type='nesterov').minimize().x,
                       rosen.x_star(), rtol=0.1)


if __name__ == "__main__":
    pytest.main()
