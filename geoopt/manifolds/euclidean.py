from .base import Manifold
from ..utils import strip_tuple


__all__ = ["Euclidean", "R"]


class R(Manifold):
    """
    Simple Euclidean manifold, every coordinate is treated as an independent element
    """

    name = "R"
    ndim = 0
    reversible = True

    def _check_shape(self, x, name):
        return True, None

    def _check_point_on_manifold(self, x, *, atol=1e-5, rtol=1e-5):
        return True, None

    def _check_vector_on_tangent(self, x, u, *, atol=1e-5, rtol=1e-5):
        return True, None

    def retr(self, x, u):
        return x + u

    def inner(self, x, u, v=None, *, keepdim=False):
        if v is None:
            return u.pow(2)
        else:
            return u * v

    def proju(self, x, u):
        return u

    def projx(self, x):
        return x

    def transp_follow_expmap(self, x, u, v, *more):
        return strip_tuple((v, *more))

    transp_follow_retr = transp_follow_expmap

    def logmap(self, x, y):
        return y - x

    def dist(self, x, y, *, keepdim=False):
        return (x - y).abs()

    def expmap_transp(self, x, u, v, *more):
        return (x + u, v, *more)

    retr_transp = expmap_transp

    def egrad2rgrad(self, x, u):
        return u

    def expmap(self, x, u):
        return x + u

    def transp(self, x, y, v, *more):
        return strip_tuple((v, *more))


class Euclidean(R):
    """
    Simple Euclidean manifold, every row is treated as an independent element
    """

    ndim = 1
    name = "Euclidean"

    def _check_shape(self, x, name):
        dim_is_ok = x.dim() >= 1
        if not dim_is_ok:
            return False, "Not enough dimensions for `{}`".format(name)
        return True, None

    def inner(self, x, u, v=None, *, keepdim=False):
        if v is None:
            v = u
        return (u * v).sum(dim=-1, keepdim=keepdim)

    def norm(self, x, u, *, keepdim=False):
        return u.norm(dim=-1)

    def dist(self, x, y, *, keepdim=False):
        return (x - y).norm(dim=-1, keepdim=keepdim)
