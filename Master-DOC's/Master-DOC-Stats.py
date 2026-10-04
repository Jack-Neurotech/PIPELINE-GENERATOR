
# ============================================================
# MASTER-DOC — STATISTICS
# ============================================================
#
# This Master-DOC owns statistical analysis resources for the
# Neural Analysis Pipeline Generator.
#
# It serves two purposes:
#
#   1. Scientific statistics library
#   2. Executable resource registry for generator.py
#
# IMPORTANT:
#
# generator.py must acquire statistical resources from THIS
# Master-DOC.
#
# It must NOT search:
#
#   Master-DOC-Decoding.py
#   Master-DOC-Validation.py
#   Master-DOC-Signal_Analysis.py
#
# for statistics that belong here.
#
# Every resource exposes:
#
#   - canonical name
#   - aliases
#   - executable callable
#   - description
#   - Master-DOC identity
#
# ============================================================


# ============================================================
# IMPORTS
# ============================================================

from __future__ import annotations

from typing import Any, Callable, Dict, Iterable, Optional

import numpy as np


# ============================================================
# MASTER-DOC IDENTITY
# ============================================================

MASTER_DOC_ROLE = "statistics"

MASTER_DOC_NAME = "Master-DOC-Stats"

MASTER_DOC_VERSION = "1.0"


# ============================================================
# RESOURCE NAME NORMALIZATION
# ============================================================

def normalize_resource_name(
    name: Any
) -> str:

    if name is None:

        return ""

    value = str(
        name
    ).strip().lower()

    value = value.replace(
        "-",
        "_"
    )

    value = value.replace(
        " ",
        "_"
    )

    while "__" in value:

        value = value.replace(
            "__",
            "_"
        )

    return value


# ============================================================
# VALIDATE INPUT DATA
# ============================================================
#
# Statistics operate on numerical neural data.
#
# Supported:
#
#   1-D:
#       samples
#
#   2-D:
#       channels x samples
#
# By default statistics operate across the sample axis.
# ============================================================

def _validate_data(
    data: Any
) -> np.ndarray:

    array = np.asarray(
        data,
        dtype=float
    )

    if array.ndim not in (
        1,
        2
    ):

        raise ValueError(
            "Statistical input must be "
            "1-D or 2-D."
        )

    if array.size == 0:

        raise ValueError(
            "Statistical input cannot be empty."
        )

    return array


# ============================================================
# RESOLVE AXIS
# ============================================================
#
# Default:
#
#   axis=-1
#
# This means:
#
#   1-D -> statistics over samples
#
#   2-D -> statistics independently for each channel
# ============================================================

def _resolve_axis(
    data: np.ndarray,
    axis: int = -1
) -> int:

    if axis < -data.ndim or axis >= data.ndim:

        raise ValueError(
            f"axis {axis} is invalid for "
            f"data with {data.ndim} dimensions."
        )

    return axis


# ============================================================
# MEAN
# ============================================================
#
# Resource:
#
#   mean
#
# Aliases:
#
#   calculate_mean
#   compute_mean
# ============================================================

def calculate_mean(
    data: Any,
    axis: int = -1,
    keepdims: bool = False
) -> np.ndarray:

    array = _validate_data(
        data
    )

    axis = _resolve_axis(
        array,
        axis
    )

    return np.mean(
        array,
        axis=axis,
        keepdims=keepdims
    )


# Canonical convenience name.
mean = calculate_mean


# ============================================================
# STANDARD DEVIATION
# ============================================================
#
# Resource:
#
#   std
#
# Aliases:
#
#   standard_deviation
#   calculate_std
#   calculate_standard_deviation
#   compute_standard_deviation
# ============================================================

def calculate_standard_deviation(
    data: Any,
    axis: int = -1,
    ddof: int = 0,
    keepdims: bool = False
) -> np.ndarray:

    array = _validate_data(
        data
    )

    axis = _resolve_axis(
        array,
        axis
    )

    ddof = int(
        ddof
    )

    if ddof < 0:

        raise ValueError(
            "ddof cannot be negative."
        )

    sample_count = (
        array.shape[axis]
    )

    if ddof >= sample_count:

        raise ValueError(
            "ddof must be smaller than the "
            "number of observations."
        )

    return np.std(
        array,
        axis=axis,
        ddof=ddof,
        keepdims=keepdims
    )


std = calculate_standard_deviation

standard_deviation = (
    calculate_standard_deviation
)

calculate_std = (
    calculate_standard_deviation
)


# ============================================================
# VARIANCE
# ============================================================
#
# Resource:
#
#   variance
#
# Aliases:
#
#   calculate_variance
#   compute_variance
# ============================================================

def calculate_variance(
    data: Any,
    axis: int = -1,
    ddof: int = 0,
    keepdims: bool = False
) -> np.ndarray:

    array = _validate_data(
        data
    )

    axis = _resolve_axis(
        array,
        axis
    )

    ddof = int(
        ddof
    )

    if ddof < 0:

        raise ValueError(
            "ddof cannot be negative."
        )

    sample_count = (
        array.shape[axis]
    )

    if ddof >= sample_count:

        raise ValueError(
            "ddof must be smaller than the "
            "number of observations."
        )

    return np.var(
        array,
        axis=axis,
        ddof=ddof,
        keepdims=keepdims
    )


variance = calculate_variance


# ============================================================
# ROOT MEAN SQUARE
# ============================================================
#
# Resource:
#
#   rms
#
# Aliases:
#
#   calculate_rms
#   compute_rms
#   root_mean_square
# ============================================================

def calculate_rms(
    data: Any,
    axis: int = -1,
    keepdims: bool = False
) -> np.ndarray:

    array = _validate_data(
        data
    )

    axis = _resolve_axis(
        array,
        axis
    )

    return np.sqrt(
        np.mean(
            np.square(array),
            axis=axis,
            keepdims=keepdims
        )
    )


rms = calculate_rms

root_mean_square = (
    calculate_rms
)


# ============================================================
# MINIMUM
# ============================================================

def calculate_minimum(
    data: Any,
    axis: int = -1,
    keepdims: bool = False
) -> np.ndarray:

    array = _validate_data(
        data
    )

    axis = _resolve_axis(
        array,
        axis
    )

    return np.min(
        array,
        axis=axis,
        keepdims=keepdims
    )


minimum = calculate_minimum

min_value = calculate_minimum


# ============================================================
# MAXIMUM
# ============================================================

def calculate_maximum(
    data: Any,
    axis: int = -1,
    keepdims: bool = False
) -> np.ndarray:

    array = _validate_data(
        data
    )

    axis = _resolve_axis(
        array,
        axis
    )

    return np.max(
        array,
        axis=axis,
        keepdims=keepdims
    )


maximum = calculate_maximum

max_value = calculate_maximum


# ============================================================
# MEDIAN
# ============================================================

def calculate_median(
    data: Any,
    axis: int = -1,
    keepdims: bool = False
) -> np.ndarray:

    array = _validate_data(
        data
    )

    axis = _resolve_axis(
        array,
        axis
    )

    return np.median(
        array,
        axis=axis,
        keepdims=keepdims
    )


median = calculate_median


# ============================================================
# RANGE
# ============================================================

def calculate_range(
    data: Any,
    axis: int = -1,
    keepdims: bool = False
) -> np.ndarray:

    array = _validate_data(
        data
    )

    axis = _resolve_axis(
        array,
        axis
    )

    return (
        np.max(
            array,
            axis=axis,
            keepdims=keepdims
        )
        -
        np.min(
            array,
            axis=axis,
            keepdims=keepdims
        )
    )


data_range = calculate_range


# ============================================================
# ABSOLUTE MEAN
# ============================================================

def calculate_absolute_mean(
    data: Any,
    axis: int = -1,
    keepdims: bool = False
) -> np.ndarray:

    array = _validate_data(
        data
    )

    axis = _resolve_axis(
        array,
        axis
    )

    return np.mean(
        np.abs(array),
        axis=axis,
        keepdims=keepdims
    )


absolute_mean = calculate_absolute_mean


# ============================================================
# PEAK-TO-PEAK
# ============================================================

def calculate_peak_to_peak(
    data: Any,
    axis: int = -1,
    keepdims: bool = False
) -> np.ndarray:

    array = _validate_data(
        data
    )

    axis = _resolve_axis(
        array,
        axis
    )

    return np.ptp(
        array,
        axis=axis,
        keepdims=keepdims
    )


peak_to_peak = calculate_peak_to_peak


# ============================================================
# ENERGY
# ============================================================

def calculate_energy(
    data: Any,
    axis: int = -1,
    keepdims: bool = False
) -> np.ndarray:

    array = _validate_data(
        data
    )

    axis = _resolve_axis(
        array,
        axis
    )

    return np.sum(
        np.square(array),
        axis=axis,
        keepdims=keepdims
    )


energy = calculate_energy


# ============================================================
# POWER
# ============================================================

def calculate_power(
    data: Any,
    axis: int = -1,
    keepdims: bool = False
) -> np.ndarray:

    array = _validate_data(
        data
    )

    axis = _resolve_axis(
        array,
        axis
    )

    return np.mean(
        np.square(array),
        axis=axis,
        keepdims=keepdims
    )


power = calculate_power


# ============================================================
# ZERO CROSSING COUNT
# ============================================================

def calculate_zero_crossings(
    data: Any,
    axis: int = -1
) -> np.ndarray:

    array = _validate_data(
        data
    )

    axis = _resolve_axis(
        array,
        axis
    )

    if axis != -1:

        array = np.moveaxis(
            array,
            axis,
            -1
        )

    signs = (
        np.sign(array)
    )

    crossings = (
        signs[..., :-1]
        *
        signs[..., 1:]
        < 0
    )

    return np.sum(
        crossings,
        axis=-1
    )


zero_crossings = (
    calculate_zero_crossings
)


# ============================================================
# STATISTICAL SUMMARY
# ============================================================
#
# Useful when the pipeline needs a compact statistical object.
#
# This function does NOT replace individual resources.
# ============================================================

def statistical_summary(
    data: Any,
    axis: int = -1
) -> Dict[str, Any]:

    array = _validate_data(
        data
    )

    axis = _resolve_axis(
        array,
        axis
    )

    return {

        "mean":
            calculate_mean(
                array,
                axis=axis
            ),

        "std":
            calculate_standard_deviation(
                array,
                axis=axis
            ),

        "variance":
            calculate_variance(
                array,
                axis=axis
            ),

        "rms":
            calculate_rms(
                array,
                axis=axis
            ),

        "minimum":
            calculate_minimum(
                array,
                axis=axis
            ),

        "maximum":
            calculate_maximum(
                array,
                axis=axis
            ),

        "median":
            calculate_median(
                array,
                axis=axis
            ),

        "range":
            calculate_range(
                array,
                axis=axis
            ),

        "absolute_mean":
            calculate_absolute_mean(
                array,
                axis=axis
            ),

        "peak_to_peak":
            calculate_peak_to_peak(
                array,
                axis=axis
            ),

        "energy":
            calculate_energy(
                array,
                axis=axis
            ),

        "power":
            calculate_power(
                array,
                axis=axis
            ),

        "zero_crossings":
            calculate_zero_crossings(
                array,
                axis=axis
            )

    }


# ============================================================
# RESOURCE ALIASES
# ============================================================
#
# The logical names used by analysis.py are mapped to the
# actual scientific functions.
#
# IMPORTANT:
#
# These aliases belong HERE.
#
# generator.py does not need to maintain a second copy.
# ============================================================

RESOURCE_ALIASES = {

    # --------------------------------------------------------
    # MEAN
    # --------------------------------------------------------

    "mean":
        "calculate_mean",

    "calculate_mean":
        "calculate_mean",

    "compute_mean":
        "calculate_mean",

    # --------------------------------------------------------
    # STANDARD DEVIATION
    # --------------------------------------------------------

    "std":
        "calculate_standard_deviation",

    "standard_deviation":
        "calculate_standard_deviation",

    "calculate_std":
        "calculate_standard_deviation",

    "calculate_standard_deviation":
        "calculate_standard_deviation",

    "compute_standard_deviation":
        "calculate_standard_deviation",

    # --------------------------------------------------------
    # VARIANCE
    # --------------------------------------------------------

    "variance":
        "calculate_variance",

    "calculate_variance":
        "calculate_variance",

    "compute_variance":
        "calculate_variance",

    # --------------------------------------------------------
    # RMS
    # --------------------------------------------------------

    "rms":
        "calculate_rms",

    "calculate_rms":
        "calculate_rms",

    "compute_rms":
        "calculate_rms",

    "root_mean_square":
        "calculate_rms",

    # --------------------------------------------------------
    # MINIMUM
    # --------------------------------------------------------

    "minimum":
        "calculate_minimum",

    "min":
        "calculate_minimum",

    "min_value":
        "calculate_minimum",

    # --------------------------------------------------------
    # MAXIMUM
    # --------------------------------------------------------

    "maximum":
        "calculate_maximum",

    "max":
        "calculate_maximum",

    "max_value":
        "calculate_maximum",

    # --------------------------------------------------------
    # MEDIAN
    # --------------------------------------------------------

    "median":
        "calculate_median",

    "calculate_median":
        "calculate_median",

    # --------------------------------------------------------
    # RANGE
    # --------------------------------------------------------

    "range":
        "calculate_range",

    "data_range":
        "calculate_range",

    "calculate_range":
        "calculate_range",

    # --------------------------------------------------------
    # ABSOLUTE MEAN
    # --------------------------------------------------------

    "absolute_mean":
        "calculate_absolute_mean",

    "calculate_absolute_mean":
        "calculate_absolute_mean",

    # --------------------------------------------------------
    # PEAK-TO-PEAK
    # --------------------------------------------------------

    "peak_to_peak":
        "calculate_peak_to_peak",

    "calculate_peak_to_peak":
        "calculate_peak_to_peak",

    "ptp":
        "calculate_peak_to_peak",

    # --------------------------------------------------------
    # ENERGY
    # --------------------------------------------------------

    "energy":
        "calculate_energy",

    "calculate_energy":
        "calculate_energy",

    # --------------------------------------------------------
    # POWER
    # --------------------------------------------------------

    "power":
        "calculate_power",

    "calculate_power":
        "calculate_power",

    # --------------------------------------------------------
    # ZERO CROSSINGS
    # --------------------------------------------------------

    "zero_crossings":
        "calculate_zero_crossings",

    "calculate_zero_crossings":
        "calculate_zero_crossings",

    "zero_crossing_count":
        "calculate_zero_crossings",

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    "statistical_summary":
        "statistical_summary",

    "summary":
        "statistical_summary"

}


# ============================================================
# RESOURCE DEFINITIONS
# ============================================================
#
# This is the authoritative executable resource registry for
# the Statistics Master-DOC.
# ============================================================

RESOURCE_DEFINITIONS = {

    "calculate_mean": {

        "name":
            "mean",

        "canonical_name":
            "calculate_mean",

        "type":
            "statistics",

        "callable":
            calculate_mean,

        "aliases": (
            "mean",
            "calculate_mean",
            "compute_mean"
        ),

        "description":
            "Calculates the arithmetic mean."

    },

    "calculate_standard_deviation": {

        "name":
            "std",

        "canonical_name":
            "calculate_standard_deviation",

        "type":
            "statistics",

        "callable":
            calculate_standard_deviation,

        "aliases": (
            "std",
            "standard_deviation",
            "calculate_std",
            "calculate_standard_deviation",
            "compute_standard_deviation"
        ),

        "description":
            "Calculates standard deviation."

    },

    "calculate_variance": {

        "name":
            "variance",

        "canonical_name":
            "calculate_variance",

        "type":
            "statistics",

        "callable":
            calculate_variance,

        "aliases": (
            "variance",
            "calculate_variance",
            "compute_variance"
        ),

        "description":
            "Calculates statistical variance."

    },

    "calculate_rms": {

        "name":
            "rms",

        "canonical_name":
            "calculate_rms",

        "type":
            "statistics",

        "callable":
            calculate_rms,

        "aliases": (
            "rms",
            "calculate_rms",
            "compute_rms",
            "root_mean_square"
        ),

        "description":
            "Calculates root mean square amplitude."

    },

    "calculate_minimum": {

        "name":
            "minimum",

        "canonical_name":
            "calculate_minimum",

        "type":
            "statistics",

        "callable":
            calculate_minimum,

        "aliases": (
            "minimum",
            "min",
            "min_value"
        ),

        "description":
            "Calculates the minimum value."

    },

    "calculate_maximum": {

        "name":
            "maximum",

        "canonical_name":
            "calculate_maximum",

        "type":
            "statistics",

        "callable":
            calculate_maximum,

        "aliases": (
            "maximum",
            "max",
            "max_value"
        ),

        "description":
            "Calculates the maximum value."

    },

    "calculate_median": {

        "name":
            "median",

        "canonical_name":
            "calculate_median",

        "type":
            "statistics",

        "callable":
            calculate_median,

        "aliases": (
            "median",
            "calculate_median"
        ),

        "description":
            "Calculates the median."

    },

    "calculate_range": {

        "name":
            "range",

        "canonical_name":
            "calculate_range",

        "type":
            "statistics",

        "callable":
            calculate_range,

        "aliases": (
            "range",
            "data_range",
            "calculate_range"
        ),

        "description":
            "Calculates maximum minus minimum."

    },

    "calculate_absolute_mean": {

        "name":
            "absolute_mean",

        "canonical_name":
            "calculate_absolute_mean",

        "type":
            "statistics",

        "callable":
            calculate_absolute_mean,

        "aliases": (
            "absolute_mean",
            "calculate_absolute_mean"
        ),

        "description":
            "Calculates mean absolute amplitude."

    },

    "calculate_peak_to_peak": {

        "name":
            "peak_to_peak",

        "canonical_name":
            "calculate_peak_to_peak",

        "type":
            "statistics",

        "callable":
            calculate_peak_to_peak,

        "aliases": (
            "peak_to_peak",
            "calculate_peak_to_peak",
            "ptp"
        ),

        "description":
            "Calculates peak-to-peak amplitude."

    },

    "calculate_energy": {

        "name":
            "energy",

        "canonical_name":
            "calculate_energy",

        "type":
            "statistics",

        "callable":
            calculate_energy,

        "aliases": (
            "energy",
            "calculate_energy"
        ),

        "description":
            "Calculates signal energy."

    },

    "calculate_power": {

        "name":
            "power",

        "canonical_name":
            "calculate_power",

        "type":
            "statistics",

        "callable":
            calculate_power,

        "aliases": (
            "power",
            "calculate_power"
        ),

        "description":
            "Calculates mean-square signal power."

    },

    "calculate_zero_crossings": {

        "name":
            "zero_crossings",

        "canonical_name":
            "calculate_zero_crossings",

        "type":
            "statistics",

        "callable":
            calculate_zero_crossings,

        "aliases": (
            "zero_crossings",
            "calculate_zero_crossings",
            "zero_crossing_count"
        ),

        "description":
            "Counts sign changes in the signal."

    },

    "statistical_summary": {

        "name":
            "statistical_summary",

        "canonical_name":
            "statistical_summary",

        "type":
            "statistics",

        "callable":
            statistical_summary,

        "aliases": (
            "statistical_summary",
            "summary"
        ),

        "description":
            "Calculates a complete statistical summary."

    }

}


# ============================================================
# BUILD RESOURCE LOOKUP
# ============================================================

def _build_resource_lookup():

    lookup = {}

    for canonical_name, definition in (
        RESOURCE_DEFINITIONS.items()
    ):

        lookup[
            normalize_resource_name(
                canonical_name
            )
        ] = definition

        for alias in definition.get(
            "aliases",
            ()
        ):

            lookup[
                normalize_resource_name(
                    alias
                )
            ] = definition

    return lookup


RESOURCE_LOOKUP = (
    _build_resource_lookup()
)


# ============================================================
# RESOLVE RESOURCE
# ============================================================
#
# Primary generator interface.
# ============================================================

def resolve_resource(
    resource_name: str
) -> Optional[Dict[str, Any]]:

    normalized_name = (
        normalize_resource_name(
            resource_name
        )
    )

    definition = (
        RESOURCE_LOOKUP.get(
            normalized_name
        )
    )

    if definition is None:

        return None

    return {

        "name":
            definition["name"],

        "canonical_name":
            definition["canonical_name"],

        "type":
            definition["type"],

        "callable":
            definition["callable"],

        "description":
            definition["description"],

        "master_doc":
            MASTER_DOC_NAME,

        "master_doc_role":
            MASTER_DOC_ROLE,

        "source_acquired":
            True

    }


# ============================================================
# GET RESOURCE
# ============================================================

def get_resource(
    resource_name: str
) -> Optional[Dict[str, Any]]:

    return resolve_resource(
        resource_name
    )


# ============================================================
# GET RESOURCE FUNCTION
# ============================================================

def get_resource_function(
    resource_name: str
) -> Optional[Callable]:

    resource = resolve_resource(
        resource_name
    )

    if resource is None:

        return None

    return resource[
        "callable"
    ]


# ============================================================
# LIST RESOURCES
# ============================================================

def list_resources():

    resources = []

    seen = set()

    for definition in (
        RESOURCE_DEFINITIONS.values()
    ):

        canonical_name = (
            definition[
                "canonical_name"
            ]
        )

        if canonical_name in seen:

            continue

        seen.add(
            canonical_name
        )

        resources.append({

            "name":
                definition["name"],

            "canonical_name":
                canonical_name,

            "type":
                definition["type"],

            "aliases":
                list(
                    definition.get(
                        "aliases",
                        ()
                    )
                ),

            "description":
                definition["description"]

        })

    return resources


# ============================================================
# VALIDATE MASTER-DOC
# ============================================================

def validate_master_doc():

    errors = []

    for canonical_name, definition in (
        RESOURCE_DEFINITIONS.items()
    ):

        function = definition.get(
            "callable"
        )

        if not callable(
            function
        ):

            errors.append(
                f"Resource '{canonical_name}' "
                "does not expose a callable."
            )

        aliases = definition.get(
            "aliases"
        )

        if not aliases:

            errors.append(
                f"Resource '{canonical_name}' "
                "does not define aliases."
            )

    required_resources = (
        "mean",
        "std",
        "variance",
        "rms"
    )

    for resource_name in (
        required_resources
    ):

        if resolve_resource(
            resource_name
        ) is None:

            errors.append(
                f"Required statistical resource "
                f"'{resource_name}' is unavailable."
            )

    return {

        "valid":
            not errors,

        "master_doc":
            MASTER_DOC_NAME,

        "role":
            MASTER_DOC_ROLE,

        "version":
            MASTER_DOC_VERSION,

        "resource_count":
            len(
                RESOURCE_DEFINITIONS
            ),

        "errors":
            errors

    }


# ============================================================
# MASTER-DOC SUMMARY
# ============================================================

def get_master_doc_summary():

    return {

        "name":
            MASTER_DOC_NAME,

        "role":
            MASTER_DOC_ROLE,

        "version":
            MASTER_DOC_VERSION,

        "resource_count":
            len(
                RESOURCE_DEFINITIONS
            ),

        "resources":
            list_resources(),

        "validation":
            validate_master_doc()

    }


# ============================================================
# DIRECT SELF-TEST
# ============================================================
#
# This verifies the exact four statistical resources currently
# requested by the pipeline handoff.
# ============================================================

if __name__ == "__main__":

    print()

    print(
        "=" * 70
    )

    print(
        "MASTER-DOC STATISTICS"
    )

    print(
        "=" * 70
    )

    print()

    validation = (
        validate_master_doc()
    )

    print(
        f"Master-DOC: "
        f"{MASTER_DOC_NAME}"
    )

    print(
        f"Role: "
        f"{MASTER_DOC_ROLE}"
    )

    print(
        f"Version: "
        f"{MASTER_DOC_VERSION}"
    )

    print()

    print(
        "Validation:"
    )

    print(
        f"  Valid: "
        f"{validation['valid']}"
    )

    for error in (
        validation["errors"]
    ):

        print(
            f"  ERROR: {error}"
        )

    print()

    print(
        "Required statistical resources:"
    )

    for requested_name in (
        "mean",
        "std",
        "variance",
        "rms"
    ):

        resource = (
            resolve_resource(
                requested_name
            )
        )

        if resource is None:

            print(
                f"  ✗ {requested_name}"
            )

            continue

        print(
            f"  ✓ {requested_name}"
            f" -> "
            f"{resource['canonical_name']}"
        )

        print(
            f"      callable: "
            f"{resource['callable'].__name__}"
        )

        print(
            f"      source acquired: "
            f"{resource['source_acquired']}"
        )

    print()

    print(
        "Available statistical resources:"
    )

    for resource in (
        list_resources()
    ):

        print(
            f"  - "
            f"{resource['name']}"
        )

    print()

    print(
        "=" * 70
    )
