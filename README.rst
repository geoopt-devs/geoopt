geoopt
======

|Python Package Index| |Read The Docs| |Build Status| |Coverage Status| |Codestyle Black| |Gitter|

Manifold aware ``pytorch.optim``.

Unofficial implementation for `“Riemannian Adaptive Optimization
Methods”`_ ICLR2019 and more.

Installation
------------
Make sure you have pytorch>=1.0.0 installed

There are two ways to install geoopt:

1. GitHub (preferred so far) due to active development

.. code-block::

    pip install git+https://github.com/ferrine/geoopt.git


2. pypi (this might be significantly behind master branch)

.. code-block::

    pip install geoopt

The preferred way to install geoopt will change once stable project stage is achieved.
Now, pypi is behind master as we actively develop and implement new features.

What is done so far
-------------------

Work is in progress but you can already use this. Note that API might
change in future releases.

Tensors
~~~~~~~

-  ``geoopt.ManifoldTensor`` – just as torch.Tensor with additional
   ``manifold`` keyword argument.
-  ``geoopt.ManifoldParameter`` – same as above, recognized in
   ``torch.nn.Module.parameters`` as correctly subclassed.

All above containers have special methods to work with them as with
points on a certain manifold

-  ``.proj_()`` – inplace projection on the manifold.
-  ``.proju(u)`` – project vector ``u`` on the tangent space. You need
   to project all vectors for all methods below.
-  ``.egrad2rgrad(u)`` – project gradient ``u`` on Riemannian manifold
-  ``.inner(u, v=None)`` – inner product at this point for two
   **tangent** vectors at this point. The passed vectors are not
   projected, they are assumed to be already projected.
-  ``.retr(u, t)`` – retraction map following vector ``u`` for time
   ``t``
-  ``.transp(u, t, v, *more)`` – transport vector ``v`` (and possibly
   more vectors) with direction ``u`` for time ``t``
-  ``.retr_transp(u, t, v, *more)`` – transport ``self``, vector ``v``
   (and possibly more vectors) with direction ``u`` for time ``t``
   (returns are plain tensors)

Manifolds
~~~~~~~~~

-  ``geoopt.Euclidean`` – unconstrained manifold in ``R`` with
   Euclidean metric
-  ``geoopt.Stiefel`` – Stiefel manifold on matrices
   ``A in R^{n x p} : A^t A=I``, ``n >= p``
-  ``geoopt.Sphere`` - Sphere manifold ``||x||=1``

Optimizers
~~~~~~~~~~

-  ``geoopt.optim.RiemannianSGD`` – a subclass of ``torch.optim.SGD``
   with the same API
-  ``geoopt.optim.RiemannianAdam`` – a subclass of ``torch.optim.Adam``

Samplers
~~~~~~~~

-  ``geoopt.samplers.RSGLD`` – Riemannian Stochastic Gradient Langevin
   Dynamics
-  ``geoopt.samplers.RHMC`` – Riemannian Hamiltonian Monte-Carlo
-  ``geoopt.samplers.SGRHMC`` – Stochastic Gradient Riemannian
   Hamiltonian Monte-Carlo

.. _“Riemannian Adaptive Optimization Methods”: https://openreview.net/forum?id=r1eiqi09K7

.. |Python Package Index| image:: https://img.shields.io/pypi/v/geoopt.svg
   :target: https://pypi.python.org/pypi/geoopt
.. |Read The Docs| image:: https://readthedocs.org/projects/geoopt/badge/?version=latest
   :target: https://geoopt.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
.. |Build Status| image:: https://travis-ci.com/ferrine/geoopt.svg?branch=master
   :target: https://travis-ci.com/ferrine/geoopt
.. |Coverage Status| image:: https://coveralls.io/repos/github/ferrine/geoopt/badge.svg?branch=master
   :target: https://coveralls.io/github/ferrine/geoopt?branch=master
.. |Codestyle Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black
.. |Gitter| image:: https://badges.gitter.im/geoopt/community.png
   :target: https://gitter.im/geoopt/community