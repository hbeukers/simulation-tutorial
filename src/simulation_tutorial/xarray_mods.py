"""
This modules extends capabilities of xarray.
So far includes apply_ufunc with multiprocessing capabilities.

Hans Beukers 2024
"""

import warnings
from collections.abc import Mapping, Sequence, Set
from typing import Any, Callable, Literal

import numpy as np
import xarray as xr
from tqdm import tqdm
from xarray.core.computation import _NO_FILL_VALUE
from xarray.core.types import JoinOptions

try:
    from multiprocess import Pool
except ImportError:
    warnings.warn("""
        Using multiprocessing as the multiprocess packages is not installed. 
        This means that you cannot multiprocess functions defined in a jupyter notebook. 
        You need to define them in an external file and import the functions. 
        When you install the multiprocess package this limitation is not there.""")
    from multiprocessing import Pool

MissingCoreDimOptions = Literal["raise", "copy", "drop"]


class Partial(object):
    """
    This is effectively a wrapper function. However multiprocessing does not support wrapper functions, whereas this method works as it can be pickeled and wrapped functions cannot.
    """

    def __init__(self, func, **kwargs):
        self.func = func
        self.kwargs = kwargs

    def __call__(self, args):
        return self.func(*args, **self.kwargs)


def _make_args_list(*args, **kwargs):
    """
    Get a list of all the arguments used if apply_ufunc is vectorized.
    """
    args_list = []

    def wrapper_args(*args):
        args_list.append(args)
        return np.nan

    kwargs["output_dtypes"] = [float]
    xr.apply_ufunc(wrapper_args, *args[1:], **kwargs)
    return args_list


def _apply_func_multiprocessing(partial_func, args_list):
    """
    Apply a list of args to a function using multiprocessing and tqdm.
    """
    with Pool() as p:
        results_list = list(
            tqdm(
                p.imap(partial_func, args_list, chunksize=1),
                total=len(args_list),
            )
        )
    return results_list


def _apply_ufunc_precomputed_results(*args, results_list, **kwargs):
    """
    Use xarray.apply_ufunc to assemble a precomputed list of results to an standard xarray.apply_ufunc output.
    """
    # When using vectorize, xarray calls numpy.vectorize internally.
    # If the output_dtypes is not specified (None) numpy evaluates the first function call twice.
    # In this scenario we need to inerst an extra entry in the list to make it match the list of args.
    if kwargs.get("output_dtypes", None) is None:
        results_list.insert(
            0, results_list[0]
        )  # to counteract the twofold evaluation of the first point

    def wrapper_results(*args, **kwargs):
        return results_list.pop(0)

    return xr.apply_ufunc(wrapper_results, *args[1:], **kwargs)


def _apply_ufunc(*args, multiprocessing: bool = False, **kwargs):
    """
    This funciton imitates the behaviour of xarray.apply_ufunc.
    However it adds the functionality of multiprocessing.
    If you set multiprocessing to true it will use the multiprocessing library of python.
    """
    if not multiprocessing:
        return xr.apply_ufunc(*args, **kwargs)

    if multiprocessing and not kwargs.get("vectorize", False):
        raise ValueError("To allow multiprocessing, vectorize needs to be True.")

    args_list = _make_args_list(*args, **kwargs)
    func = args[0]
    if kwargs["kwargs"] is None:
        kwargs["kwargs"] = {}
    partial_func = Partial(func, **kwargs["kwargs"])
    results_list = _apply_func_multiprocessing(partial_func, args_list)
    return _apply_ufunc_precomputed_results(*args, results_list=results_list, **kwargs)


# apply_ufunc has the type annotation (for autocompletion), _apply_ufunc has the functionality
def apply_ufunc(
    func: Callable,
    *args: Any,
    input_core_dims: Sequence[Sequence] | None = None,
    output_core_dims: Sequence[Sequence] | None = ((),),
    exclude_dims: Set = frozenset(),
    vectorize: bool = False,
    join: JoinOptions = "exact",
    dataset_join: str = "exact",
    dataset_fill_value: object = _NO_FILL_VALUE,
    keep_attrs: bool | str | None = None,
    kwargs: Mapping | None = None,
    dask: Literal["forbidden", "allowed", "parallelized"] = "forbidden",
    output_dtypes: Sequence | None = None,
    output_sizes: Mapping[Any, int] | None = None,
    meta: Any = None,
    dask_gufunc_kwargs: dict[str, Any] | None = None,
    on_missing_core_dim: MissingCoreDimOptions = "raise",
    multiprocessing: bool = False,
) -> Any:
    """
    Wrapper around xarray apply_ufunc, but which allows to do multiprocessing from the standard python library.
    To use this, set multiprocessing=True and vectorize=True.
    """
    return _apply_ufunc(
        func,
        *args,
        input_core_dims=input_core_dims,
        output_core_dims=output_core_dims,
        exclude_dims=exclude_dims,
        vectorize=vectorize,
        join=join,
        dataset_join=dataset_join,
        dataset_fill_value=dataset_fill_value,
        keep_attrs=keep_attrs,
        kwargs=kwargs,
        dask=dask,
        output_dtypes=output_dtypes,
        output_sizes=output_sizes,
        meta=meta,
        dask_gufunc_kwargs=dask_gufunc_kwargs,
        on_missing_core_dim=on_missing_core_dim,
        multiprocessing=multiprocessing,
    )
