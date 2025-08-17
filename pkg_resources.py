from importlib import metadata
import numpy as _np

# Ensure compatibility with packages expecting `numpy.NaN`
if not hasattr(_np, "NaN"):
    _np.NaN = _np.nan


class DistributionNotFound(Exception):
    """Exception raised when a distribution cannot be found."""


def get_distribution(dist_name: str):
    """Minimal replacement for pkg_resources.get_distribution.

    Returns an object with ``version`` and ``location`` attributes
    for the requested distribution.
    """
    try:
        dist = metadata.distribution(dist_name)
    except metadata.PackageNotFoundError as exc:
        raise DistributionNotFound(str(exc)) from exc

    class DistInfo:
        version = dist.version
        location = str(dist.locate_file(""))

    return DistInfo()
