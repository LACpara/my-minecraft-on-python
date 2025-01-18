from settings import *
from opensimplex.internals import _noise2, _noise3, _init

perm, prem_grad_index3 = _init(seed=SEED)

@njit(cache=True)
def noise2(x, y):
    return _noise2(x, y, perm)

@njit(cache=True)
def noise3(x, y, z):
    return _noise3(x, y, z, perm, prem_grad_index3)