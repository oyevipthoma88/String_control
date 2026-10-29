import glob
from os.path import basename, dirname, isfile


def __list_all_modules():
    mod_paths = glob.glob(dirname(__file__) + "/*.py")
    return sorted(
        basename(f)[:-3]
        for f in mod_paths
        if isfile(f) and not f.endswith("__init__.py")
    )


ALL_MODULES = __list_all_modules()
__all__ = ALL_MODULES + ["ALL_MODULES"]
