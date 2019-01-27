import torch
import itertools
import warnings
from .._compat import _TORCH_LESS_THAN_ONE

__all__ = ["svd", "qr", "sym", "extract_diag", "matrix_rank"]


def _warn_lost_grad(x, op):
    if torch.is_grad_enabled() and x.requires_grad:
        warnings.warn(
            "Gradient for operation {0}(...) is lost, please use the pytorch native analog as {0} this "
            "is more optimized for internal purposes which do not require gradients but vectorization".format(
                op
            )
        )


def svd(x):
    # https://discuss.pytorch.org/t/multidimensional-svd/4366/2
    _warn_lost_grad(x, "geoopt.utils.linalg.svd")
    with torch.no_grad():
        batches = x.shape[:-2]
        if batches:
            # in most cases we do not require gradients when applying svd (e.g. in projection)
            n, m = x.shape[-2:]
            k = min(n, m)
            U, d, V = x.new(*batches, n, k), x.new(*batches, k), x.new(*batches, m, k)
            for idx in itertools.product(*map(range, batches)):
                U[idx], d[idx], V[idx] = torch.svd(x[idx])
            return U, d, V
        else:
            return torch.svd(x)


def qr(x):
    # vectorized version as svd
    _warn_lost_grad(x, "geoopt.utils.linalg.qr")
    with torch.no_grad():
        batches = x.shape[:-2]
        if batches:
            # in most cases we do not require gradients when applying qr (e.g. in retraction)
            assert not x.requires_grad
            n, m = x.shape[-2:]
            Q, R = x.new(*batches, n, m), x.new(*batches, m, m)
            for idx in itertools.product(*map(range, batches)):
                Q[idx], R[idx] = torch.qr(x[idx])
            return Q, R
        else:
            return torch.qr(x)


def sym(x):
    return 0.5 * (x.transpose(-1, -2) + x)


def extract_diag(x):
    n, m = x.shape[-2:]
    k = min(n, m)
    return x[..., torch.arange(k), torch.arange(k)]


def matrix_rank(x):
    if _TORCH_LESS_THAN_ONE:
        import numpy as np

        return torch.from_numpy(
            np.asarray(np.linalg.matrix_rank(x.detach().cpu().numpy()))
        ).type_as(x)
    with torch.no_grad():
        batches = x.shape[:-2]
        if batches:
            out = x.new(*batches)
            for idx in itertools.product(*map(range, batches)):
                out[idx] = torch.matrix_rank(x[idx])
            return out
        else:
            return torch.matrix_rank(x)
