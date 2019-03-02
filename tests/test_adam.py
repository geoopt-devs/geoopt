import geoopt
import torch
import numpy as np
import pytest


@pytest.mark.parametrize("params", [dict(lr=1e-2), dict(lr=1, amsgrad=True)])
def test_adam_stiefel(params):
    stiefel = geoopt.manifolds.Stiefel()
    torch.manual_seed(42)
    X = geoopt.ManifoldParameter(torch.randn(20, 10), manifold=stiefel).proj_()
    Xstar = torch.randn(20, 10)
    Xstar.set_(stiefel.projx(Xstar))

    def closure():
        optim.zero_grad()
        loss = (X - Xstar).pow(2).sum()
        # manifold constraint that makes optimization hard if violated
        loss += (X.t() @ X - torch.eye(X.shape[1])).pow(2).sum() * 100
        loss.backward()
        return loss.item()

    optim = geoopt.optim.RiemannianAdam([X], stabilize=4500, **params)
    assert (X - Xstar).norm() > 1e-5
    for _ in range(10000):
        if (X - Xstar).norm() < 1e-5:
            break
        optim.step(closure)

    np.testing.assert_allclose(X.data, Xstar, atol=1e-5, rtol=1e-5)
    optim.load_state_dict(optim.state_dict())
    optim.step(closure)


def test_adam_poincare():
    ideal = torch.tensor([.5, .5])
    start = torch.randn(1, 1)
    start = geoopt.manifolds.poincare.math.expmap0(start, c=1.0)
    start = geoopt.ManifoldParameter(start, manifold=geoopt.PoincareBall())

    def closure():
        loss = geoopt.manifolds.poincare.math.dist(start, ideal)
        loss.backward()
        return loss.item()

    optim = geoopt.optim.RiemannianAdam([start])

    for _ in range(10000):
        optim.step(closure)

    np.testing.assert_allclose(start, ideal, atol=1e-5, rtol=1e-5)