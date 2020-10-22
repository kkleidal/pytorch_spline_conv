import importlib
import os.path as osp

import torch

__version__ = '1.2.0'

if torch.cuda.is_available():
    sublib = "gpu"
else:
    sublib = "cpu"

for library in ['_version', '_basis', '_weighting']:
    library = "%s_%s" % (library, sublib)
    torch.ops.load_library(importlib.machinery.PathFinder().find_spec(
        library, [osp.dirname(__file__)]).origin)

if torch.cuda.is_available() and torch.version.cuda:  # pragma: no cover
    cuda_version = torch.ops.torch_spline_conv.cuda_version()

    if cuda_version == -1:
        major = minor = 0
    elif cuda_version < 10000:
        major, minor = int(str(cuda_version)[0]), int(str(cuda_version)[2])
    else:
        major, minor = int(str(cuda_version)[0:2]), int(str(cuda_version)[3])
    t_major, t_minor = [int(x) for x in torch.version.cuda.split('.')]

    if t_major != major or t_minor != minor:
        raise RuntimeError(
            f'Detected that PyTorch and torch_spline_conv were compiled with '
            f'different CUDA versions. PyTorch has CUDA version '
            f'{t_major}.{t_minor} and torch_spline_conv has CUDA version '
            f'{major}.{minor}. Please reinstall the torch_spline_conv that '
            f'matches your PyTorch install.')

from .basis import spline_basis  # noqa
from .weighting import spline_weighting  # noqa
from .conv import spline_conv  # noqa

__all__ = [
    'spline_basis',
    'spline_weighting',
    'spline_conv',
    '__version__',
]
