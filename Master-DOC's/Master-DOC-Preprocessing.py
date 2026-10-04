
# ============================================================
# MASTER-DOC — PREPROCESSING
# ============================================================
#
# This Master-DOC owns preprocessing resources for the
# Neural Analysis Pipeline Generator.
#
# IMPORTANT:
#
# This file is both:
#
#   1. A scientific preprocessing library
#   2. A resource registry consumed by generator.py
#
# The generator MUST acquire preprocessing resources from this
# Master-DOC rather than searching unrelated Master-DOCs.
#
# The Master-DOC therefore exposes:
#
#   RESOURCE_DEFINITIONS
#   RESOURCE_ALIASES
#   resolve_resource()
#   get_resource()
#   list_resources()
#
# Scientific implementations remain in this file.
# ============================================================


# ============================================================
# IMPORTS
# ============================================================

from __future__ import annotations

from typing import Any, Callable, Dict, Iterable, Optional

import numpy as np

from scipy import signal


# ============================================================
# MASTER-DOC IDENTITY
# ============================================================

MASTER_DOC_ROLE = "preprocessing"

MASTER_DOC_NAME = "Master-DOC-Preprocessing"

MASTER_DOC_VERSION = "1.0"


# ============================================================
# RESOURCE NORMALIZATION
# ============================================================
#
# Resource names coming from analysis.py / generator.py may
# contain:
#
#   spaces
#   hyphens
#   underscores
#   capitalization differences
#
# Normalize them before lookup.
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
# VALIDATE NUMERIC DATA
# ============================================================
#
# All preprocessing functions operate on numerical neural
# signal data.
#
# Accepted forms:
#
#   1-D:
#       samples
#
#   2-D:
#       channels x samples
#
# The returned array is always floating point.
# ============================================================

def _validate_signal(
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
            "Neural signal must be "
            "1-D or 2-D."
        )

    if array.size == 0:

        raise ValueError(
            "Neural signal cannot be empty."
        )

    return array


# ============================================================
# VALIDATE SAMPLING RATE
# ============================================================

def _validate_sampling_rate(
    sampling_rate: float
) -> float:

    try:

        sampling_rate = float(
            sampling_rate
        )

    except (
        TypeError,
        ValueError
    ):

        raise ValueError(
            "sampling_rate must be numeric."
        )

    if sampling_rate <= 0:

        raise ValueError(
            "sampling_rate must be greater than zero."
        )

    return sampling_rate


# ============================================================
# BANDPASS FILTER
# ============================================================
#
# Resource:
#
#   bandpass_filter
#
# Aliases:
#
#   band_pass_filter
#   bandpass
#   band_pass
#   apply_bandpass_filter
#   apply_band_pass_filter
#
# This is the actual executable preprocessing resource.
# ============================================================

def band_pass_filter(
    data: Any,
    sampling_rate: float,
    low_frequency: float = 1.0,
    high_frequency: float = 40.0,
    order: int = 4
) -> np.ndarray:

    data = _validate_signal(
        data
    )

    sampling_rate = _validate_sampling_rate(
        sampling_rate
    )

    low_frequency = float(
        low_frequency
    )

    high_frequency = float(
        high_frequency
    )

    order = int(
        order
    )

    nyquist = sampling_rate / 2.0

    if low_frequency <= 0:

        raise ValueError(
            "low_frequency must be greater than zero."
        )

    if high_frequency <= low_frequency:

        raise ValueError(
            "high_frequency must be greater than "
            "low_frequency."
        )

    if high_frequency >= nyquist:

        raise ValueError(
            "high_frequency must be below the "
            "Nyquist frequency."
        )

    if order < 1:

        raise ValueError(
            "Filter order must be at least 1."
        )

    low = (
        low_frequency /
        nyquist
    )

    high = (
        high_frequency /
        nyquist
    )

    coefficients = signal.butter(
        order,
        [
            low,
            high
        ],
        btype="bandpass"
    )

    b, a = coefficients

    return signal.filtfilt(
        b,
        a,
        data,
        axis=-1
    )


# ============================================================
# BANDPASS ALIAS
# ============================================================

bandpass_filter = (
    band_pass_filter
)


# ============================================================
# NOTCH FILTER
# ============================================================
#
# Resource:
#
#   notch_filter
#
# Aliases:
#
#   notch
#   apply_notch_filter
#
# Default:
#
#   60 Hz
#
# This can be overridden for 50 Hz electrical environments.
# ============================================================

def notch_filter(
    data: Any,
    sampling_rate: float,
    frequency: float = 60.0,
    quality_factor: float = 30.0
) -> np.ndarray:

    data = _validate_signal(
        data
    )

    sampling_rate = _validate_sampling_rate(
        sampling_rate
    )

    frequency = float(
        frequency
    )

    quality_factor = float(
        quality_factor
    )

    nyquist = sampling_rate / 2.0

    if frequency <= 0:

        raise ValueError(
            "Notch frequency must be greater than zero."
        )

    if frequency >= nyquist:

        raise ValueError(
            "Notch frequency must be below "
            "the Nyquist frequency."
        )

    if quality_factor <= 0:

        raise ValueError(
            "quality_factor must be greater than zero."
        )

    b, a = signal.iirnotch(
        frequency,
        quality_factor,
        fs=sampling_rate
    )

    return signal.filtfilt(
        b,
        a,
        data,
        axis=-1
    )


# ============================================================
# LOW-PASS FILTER
# ============================================================

def low_pass_filter(
    data: Any,
    sampling_rate: float,
    cutoff_frequency: float,
    order: int = 4
) -> np.ndarray:

    data = _validate_signal(
        data
    )

    sampling_rate = _validate_sampling_rate(
        sampling_rate
    )

    cutoff_frequency = float(
        cutoff_frequency
    )

    order = int(
        order
    )

    nyquist = sampling_rate / 2.0

    if cutoff_frequency <= 0:

        raise ValueError(
            "cutoff_frequency must be greater than zero."
        )

    if cutoff_frequency >= nyquist:

        raise ValueError(
            "cutoff_frequency must be below "
            "the Nyquist frequency."
        )

    if order < 1:

        raise ValueError(
            "Filter order must be at least 1."
        )

    normalized_cutoff = (
        cutoff_frequency /
        nyquist
    )

    b, a = signal.butter(
        order,
        normalized_cutoff,
        btype="lowpass"
    )

    return signal.filtfilt(
        b,
        a,
        data,
        axis=-1
    )


# ============================================================
# HIGH-PASS FILTER
# ============================================================

def high_pass_filter(
    data: Any,
    sampling_rate: float,
    cutoff_frequency: float,
    order: int = 4
) -> np.ndarray:

    data = _validate_signal(
        data
    )

    sampling_rate = _validate_sampling_rate(
        sampling_rate
    )

    cutoff_frequency = float(
        cutoff_frequency
    )

    order = int(
        order
    )

    nyquist = sampling_rate / 2.0

    if cutoff_frequency <= 0:

        raise ValueError(
            "cutoff_frequency must be greater than zero."
        )

    if cutoff_frequency >= nyquist:

        raise ValueError(
            "cutoff_frequency must be below "
            "the Nyquist frequency."
        )

    if order < 1:

        raise ValueError(
            "Filter order must be at least 1."
        )

    normalized_cutoff = (
        cutoff_frequency /
        nyquist
    )

    b, a = signal.butter(
        order,
        normalized_cutoff,
        btype="highpass"
    )

    return signal.filtfilt(
        b,
        a,
        data,
        axis=-1
    )


# ============================================================
# BAND-STOP FILTER
# ============================================================

def band_stop_filter(
    data: Any,
    sampling_rate: float,
    low_frequency: float,
    high_frequency: float,
    order: int = 4
) -> np.ndarray:

    data = _validate_signal(
        data
    )

    sampling_rate = _validate_sampling_rate(
        sampling_rate
    )

    low_frequency = float(
        low_frequency
    )

    high_frequency = float(
        high_frequency
    )

    order = int(
        order
    )

    nyquist = sampling_rate / 2.0

    if low_frequency <= 0:

        raise ValueError(
            "low_frequency must be greater than zero."
        )

    if high_frequency <= low_frequency:

        raise ValueError(
            "high_frequency must be greater than "
            "low_frequency."
        )

    if high_frequency >= nyquist:

        raise ValueError(
            "high_frequency must be below "
            "the Nyquist frequency."
        )

    if order < 1:

        raise ValueError(
            "Filter order must be at least 1."
        )

    low = (
        low_frequency /
        nyquist
    )

    high = (
        high_frequency /
        nyquist
    )

    b, a = signal.butter(
        order,
        [
            low,
            high
        ],
        btype="bandstop"
    )

    return signal.filtfilt(
        b,
        a,
        data,
        axis=-1
    )


# ============================================================
# RESAMPLE SIGNAL
# ============================================================

def resample_signal(
    data: Any,
    original_sampling_rate: float,
    target_sampling_rate: float
) -> np.ndarray:

    data = _validate_signal(
        data
    )

    original_sampling_rate = (
        _validate_sampling_rate(
            original_sampling_rate
        )
    )

    target_sampling_rate = (
        _validate_sampling_rate(
            target_sampling_rate
        )
    )

    if (
        original_sampling_rate ==
        target_sampling_rate
    ):

        return np.array(
            data,
            copy=True
        )

    original_samples = (
        data.shape[-1]
    )

    duration = (
        original_samples /
        original_sampling_rate
    )

    target_samples = int(
        round(
            duration *
            target_sampling_rate
        )
    )

    if target_samples < 1:

        raise ValueError(
            "Target sampling rate produces "
            "zero samples."
        )

    return signal.resample(
        data,
        target_samples,
        axis=-1
    )


# ============================================================
# REMOVE DC OFFSET
# ============================================================

def remove_dc_offset(
    data: Any
) -> np.ndarray:

    data = _validate_signal(
        data
    )

    mean = np.mean(
        data,
        axis=-1,
        keepdims=True
    )

    return data - mean


# ============================================================
# DETREND
# ============================================================

def detrend_signal(
    data: Any,
    axis: int = -1
) -> np.ndarray:

    data = _validate_signal(
        data
    )

    return signal.detrend(
        data,
        axis=axis
    )


# ============================================================
# BASELINE CORRECTION
# ============================================================

def baseline_correction(
    data: Any,
    baseline_start: int = 0,
    baseline_end: Optional[int] = None
) -> np.ndarray:

    data = _validate_signal(
        data
    )

    samples = (
        data.shape[-1]
    )

    if baseline_end is None:

        baseline_end = samples

    baseline_start = int(
        baseline_start
    )

    baseline_end = int(
        baseline_end
    )

    if baseline_start < 0:

        raise ValueError(
            "baseline_start cannot be negative."
        )

    if baseline_end > samples:

        raise ValueError(
            "baseline_end cannot exceed "
            "the number of samples."
        )

    if baseline_end <= baseline_start:

        raise ValueError(
            "baseline_end must be greater than "
            "baseline_start."
        )

    baseline = np.mean(
        data[..., baseline_start:baseline_end],
        axis=-1,
        keepdims=True
    )

    return data - baseline


# ============================================================
# COMMON AVERAGE REFERENCE
# ============================================================
#
# Intended for channel x samples data.
# ============================================================

def common_average_reference(
    data: Any
) -> np.ndarray:

    data = _validate_signal(
        data
    )

    if data.ndim == 1:

        raise ValueError(
            "Common-average reference requires "
            "multi-channel data."
        )

    reference = np.mean(
        data,
        axis=0,
        keepdims=True
    )

    return data - reference


# ============================================================
# SELECT CHANNELS
# ============================================================

def select_channels(
    data: Any,
    channel_indices: Iterable[int]
) -> np.ndarray:

    data = _validate_signal(
        data
    )

    if data.ndim == 1:

        raise ValueError(
            "Channel selection requires "
            "multi-channel data."
        )

    indices = [
        int(index)
        for index in channel_indices
    ]

    if not indices:

        raise ValueError(
            "channel_indices cannot be empty."
        )

    channel_count = (
        data.shape[0]
    )

    for index in indices:

        if index < 0 or index >= channel_count:

            raise IndexError(
                f"Channel index {index} is "
                f"outside the available range."
            )

    return data[
        indices,
        :
    ]


# ============================================================
# REMOVE INVALID SAMPLES
# ============================================================

def remove_invalid_samples(
    data: Any
) -> np.ndarray:

    data = _validate_signal(
        data
    )

    if data.ndim == 1:

        valid = np.isfinite(
            data
        )

    else:

        valid = np.all(
            np.isfinite(data),
            axis=0
        )

    return data[
        ...,
        valid
    ]


# ============================================================
# RESOURCE ALIASES
# ============================================================
#
# THIS IS THE IMPORTANT GENERATOR INTERFACE.
#
# The generator should request a logical resource name.
#
# Example:
#
#     "bandpass_filter"
#
# resolves to:
#
#     band_pass_filter
#
# The generator does not need to know the physical function
# naming convention used inside this Master-DOC.
# ============================================================

RESOURCE_ALIASES = {

    "bandpass_filter":
        "band_pass_filter",

    "band_pass_filter":
        "band_pass_filter",

    "bandpass":
        "band_pass_filter",

    "band_pass":
        "band_pass_filter",

    "apply_bandpass_filter":
        "band_pass_filter",

    "apply_band_pass_filter":
        "band_pass_filter",

    "notch_filter":
        "notch_filter",

    "notch":
        "notch_filter",

    "apply_notch_filter":
        "notch_filter",

    "lowpass_filter":
        "low_pass_filter",

    "low_pass_filter":
        "low_pass_filter",

    "highpass_filter":
        "high_pass_filter",

    "high_pass_filter":
        "high_pass_filter",

    "bandstop_filter":
        "band_stop_filter",

    "band_stop_filter":
        "band_stop_filter",

    "resample":
        "resample_signal",

    "resample_signal":
        "resample_signal",

    "remove_dc":
        "remove_dc_offset",

    "remove_dc_offset":
        "remove_dc_offset",

    "detrend":
        "detrend_signal",

    "detrend_signal":
        "detrend_signal",

    "baseline":
        "baseline_correction",

    "baseline_correction":
        "baseline_correction",

    "common_average_reference":
        "common_average_reference",

    "car":
        "common_average_reference",

    "select_channels":
        "select_channels",

    "remove_invalid_samples":
        "remove_invalid_samples"

}


# ============================================================
# RESOURCE DEFINITIONS
# ============================================================
#
# This gives the generator structured metadata instead of
# requiring it to inspect arbitrary module attributes.
# ============================================================

RESOURCE_DEFINITIONS = {

    "band_pass_filter": {

        "name":
            "bandpass_filter",

        "canonical_name":
            "band_pass_filter",

        "type":
            "preprocessing",

        "callable":
            band_pass_filter,

        "aliases": (
            "bandpass_filter",
            "band_pass_filter",
            "bandpass",
            "band_pass",
            "apply_bandpass_filter",
            "apply_band_pass_filter"
        ),

        "description":
            "Applies a Butterworth band-pass filter."

    },

    "notch_filter": {

        "name":
            "notch_filter",

        "canonical_name":
            "notch_filter",

        "type":
            "preprocessing",

        "callable":
            notch_filter,

        "aliases": (
            "notch_filter",
            "notch",
            "apply_notch_filter"
        ),

        "description":
            "Applies an IIR notch filter."

    },

    "low_pass_filter": {

        "name":
            "low_pass_filter",

        "canonical_name":
            "low_pass_filter",

        "type":
            "preprocessing",

        "callable":
            low_pass_filter,

        "aliases": (
            "low_pass_filter",
            "lowpass_filter"
        ),

        "description":
            "Applies a Butterworth low-pass filter."

    },

    "high_pass_filter": {

        "name":
            "high_pass_filter",

        "canonical_name":
            "high_pass_filter",

        "type":
            "preprocessing",

        "callable":
            high_pass_filter,

        "aliases": (
            "high_pass_filter",
            "highpass_filter"
        ),

        "description":
            "Applies a Butterworth high-pass filter."

    },

    "band_stop_filter": {

        "name":
            "band_stop_filter",

        "canonical_name":
            "band_stop_filter",

        "type":
            "preprocessing",

        "callable":
            band_stop_filter,

        "aliases": (
            "band_stop_filter",
            "bandstop_filter"
        ),

        "description":
            "Applies a Butterworth band-stop filter."

    },

    "resample_signal": {

        "name":
            "resample_signal",

        "canonical_name":
            "resample_signal",

        "type":
            "preprocessing",

        "callable":
            resample_signal,

        "aliases": (
            "resample_signal",
            "resample"
        ),

        "description":
            "Resamples neural data to a target sampling rate."

    },

    "remove_dc_offset": {

        "name":
            "remove_dc_offset",

        "canonical_name":
            "remove_dc_offset",

        "type":
            "preprocessing",

        "callable":
            remove_dc_offset,

        "aliases": (
            "remove_dc_offset",
            "remove_dc"
        ),

        "description":
            "Removes the channel-wise DC offset."

    },

    "detrend_signal": {

        "name":
            "detrend_signal",

        "canonical_name":
            "detrend_signal",

        "type":
            "preprocessing",

        "callable":
            detrend_signal,

        "aliases": (
            "detrend_signal",
            "detrend"
        ),

        "description":
            "Removes linear trends from neural data."

    },

    "baseline_correction": {

        "name":
            "baseline_correction",

        "canonical_name":
            "baseline_correction",

        "type":
            "preprocessing",

        "callable":
            baseline_correction,

        "aliases": (
            "baseline_correction",
            "baseline"
        ),

        "description":
            "Subtracts the selected baseline mean."

    },

    "common_average_reference": {

        "name":
            "common_average_reference",

        "canonical_name":
            "common_average_reference",

        "type":
            "preprocessing",

        "callable":
            common_average_reference,

        "aliases": (
            "common_average_reference",
            "car"
        ),

        "description":
            "Applies a common-average reference."

    },

    "select_channels": {

        "name":
            "select_channels",

        "canonical_name":
            "select_channels",

        "type":
            "preprocessing",

        "callable":
            select_channels,

        "aliases": (
            "select_channels",
        ),

        "description":
            "Selects requested EEG channels."

    },

    "remove_invalid_samples": {

        "name":
            "remove_invalid_samples",

        "canonical_name":
            "remove_invalid_samples",

        "type":
            "preprocessing",

        "callable":
            remove_invalid_samples,

        "aliases": (
            "remove_invalid_samples",
        ),

        "description":
            "Removes samples containing invalid numerical values."

    }

}


# ============================================================
# BUILD COMPLETE RESOURCE LOOKUP
# ============================================================

def _build_resource_lookup() -> Dict[str, Dict[str, Any]]:

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
# This is the primary interface used by generator.py.
#
# It returns the ACTUAL executable resource.
#
# No unrelated Master-DOC is searched.
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
#
# Alias-compatible public API.
# ============================================================

def get_resource(
    resource_name: str
) -> Optional[Dict[str, Any]]:

    return resolve_resource(
        resource_name
    )


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
# GET RESOURCE FUNCTION
# ============================================================
#
# Convenience interface when the generator only needs the
# callable itself.
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
# MASTER-DOC VALIDATION
# ============================================================
#
# The generator can use this to verify that the designated
# preprocessing Master-DOC is healthy before attempting
# compilation.
# ============================================================

def validate_master_doc():

    errors = []

    for canonical_name, definition in (
        RESOURCE_DEFINITIONS.items()
    ):

        if not callable(
            definition.get(
                "callable"
            )
        ):

            errors.append(
                f"Resource '{canonical_name}' "
                "does not expose a callable."
            )

        if not definition.get(
            "aliases"
        ):

            errors.append(
                f"Resource '{canonical_name}' "
                "does not define aliases."
            )

    required_resources = (
        "band_pass_filter",
        "notch_filter"
    )

    for resource_name in (
        required_resources
    ):

        if (
            normalize_resource_name(
                resource_name
            )
            not in RESOURCE_LOOKUP
        ):

            errors.append(
                f"Required preprocessing resource "
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
# This does not execute a full EEG pipeline.
#
# It verifies the resource interface that generator.py needs.
#
# Run:
#
#     python Master-DOC-Preprocessing.py
#
# Expected:
#
#     bandpass_filter -> acquired
#     notch_filter    -> acquired
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 70)
    print(
        "MASTER-DOC PREPROCESSING"
    )
    print("=" * 70)
    print()

    validation = (
        validate_master_doc()
    )

    print(
        f"Master-DOC: {MASTER_DOC_NAME}"
    )

    print(
        f"Role: {MASTER_DOC_ROLE}"
    )

    print(
        f"Version: {MASTER_DOC_VERSION}"
    )

    print()

    print(
        "Validation:"
    )

    print(
        f"  Valid: {validation['valid']}"
    )

    if validation["errors"]:

        for error in validation["errors"]:

            print(
                f"  ERROR: {error}"
            )

    print()

    print(
        "Required resources:"
    )

    for requested_name in (
        "bandpass_filter",
        "notch_filter"
    ):

        resource = resolve_resource(
            requested_name
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
        "Available preprocessing resources:"
    )

    for resource in list_resources():

        print(
            f"  - "
            f"{resource['name']}"
        )

    print()

    print("=" * 70)

