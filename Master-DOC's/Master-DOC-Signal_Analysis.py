
# ============================================================
# MASTER-DOC — SIGNAL ANALYSIS
# ============================================================
#
# Owner:
#
#     Signal processing frequency-domain analysis
#
# This Master-DOC provides executable resources for:
#
#     spectral_power
#     dominant_frequency
#
# The generator acquires these resources directly from here.
#
# ============================================================


from __future__ import annotations

from typing import Any, Dict, Optional

import numpy as np


# ============================================================
# MASTER DOC IDENTITY
# ============================================================

MASTER_DOC_NAME = "Master-DOC-Signal_Analysis"

MASTER_DOC_ROLE = "signal_analysis"

MASTER_DOC_VERSION = "1.0"


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_resource_name(
    name: Any
) -> str:

    if name is None:

        return ""

    value = str(name).strip().lower()

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
# INPUT VALIDATION
# ============================================================

def _validate_signal(
    signal
):

    array = np.asarray(
        signal,
        dtype=float
    )

    if array.ndim != 1:

        raise ValueError(
            "Signal analysis expects a 1-D signal."
        )

    if array.size == 0:

        raise ValueError(
            "Signal cannot be empty."
        )

    return array


# ============================================================
# SPECTRAL POWER
# ============================================================
#
# Computes power spectral density using FFT.
#
# Resource:
#
#     spectral_power
#
# ============================================================

def calculate_spectral_power(
    signal,
    sampling_rate: float
) -> Dict[str, np.ndarray]:

    signal = _validate_signal(
        signal
    )

    sampling_rate = float(
        sampling_rate
    )


    frequencies = np.fft.rfftfreq(
        len(signal),
        d=1 / sampling_rate
    )


    fft_values = np.fft.rfft(
        signal
    )


    power = (
        np.abs(
            fft_values
        ) ** 2
    ) / len(signal)


    return {

        "frequencies":
            frequencies,

        "power":
            power

    }



spectral_power = calculate_spectral_power


# ============================================================
# DOMINANT FREQUENCY
# ============================================================
#
# Finds frequency with maximum spectral power.
#
# Resource:
#
#     dominant_frequency
#
# ============================================================

def calculate_dominant_frequency(
    signal,
    sampling_rate: float
):

    spectrum = calculate_spectral_power(
        signal,
        sampling_rate
    )


    frequencies = (
        spectrum["frequencies"]
    )

    power = (
        spectrum["power"]
    )


    index = np.argmax(
        power
    )


    return float(
        frequencies[index]
    )



dominant_frequency = (
    calculate_dominant_frequency
)


# ============================================================
# BAND POWER
# ============================================================
#
# General EEG frequency band extraction.
#
# Useful for:
#
#     alpha
#     beta
#     theta
#     delta
#
# ============================================================

def calculate_band_power(
    signal,
    sampling_rate,
    low_frequency,
    high_frequency
):

    spectrum = calculate_spectral_power(
        signal,
        sampling_rate
    )


    frequencies = (
        spectrum["frequencies"]
    )

    power = (
        spectrum["power"]
    )


    mask = (
        (frequencies >= low_frequency)
        &
        (frequencies <= high_frequency)
    )


    return float(
        np.sum(
            power[mask]
        )
    )


band_power = calculate_band_power


# ============================================================
# TOTAL SPECTRAL POWER
# ============================================================

def calculate_total_spectral_power(
    signal,
    sampling_rate
):

    spectrum = calculate_spectral_power(
        signal,
        sampling_rate
    )


    return float(
        np.sum(
            spectrum["power"]
        )
    )


total_spectral_power = (
    calculate_total_spectral_power
)


# ============================================================
# SPECTRAL ENTROPY
# ============================================================

def calculate_spectral_entropy(
    signal,
    sampling_rate
):

    spectrum = calculate_spectral_power(
        signal,
        sampling_rate
    )


    power = (
        spectrum["power"]
    )


    probability = (
        power /
        np.sum(power)
    )


    entropy = -np.sum(
        probability *
        np.log2(
            probability + 1e-12
        )
    )


    return float(
        entropy
    )



spectral_entropy = (
    calculate_spectral_entropy
)


# ============================================================
# RESOURCE DEFINITIONS
# ============================================================

RESOURCE_DEFINITIONS = {


    "calculate_spectral_power": {


        "name":
            "spectral_power",


        "canonical_name":
            "calculate_spectral_power",


        "type":
            "signal_analysis",


        "callable":
            calculate_spectral_power,


        "aliases": (

            "spectral_power",

            "calculate_spectral_power",

            "compute_spectral_power",

            "power_spectral_density",

            "calculate_power_spectral_density",

            "compute_power_spectral_density",

            "psd"

        ),


        "description":
            "Computes FFT based spectral power."

    },


    "calculate_dominant_frequency": {


        "name":
            "dominant_frequency",


        "canonical_name":
            "calculate_dominant_frequency",


        "type":
            "signal_analysis",


        "callable":
            calculate_dominant_frequency,


        "aliases": (

            "dominant_frequency",

            "calculate_dominant_frequency",

            "compute_dominant_frequency",

            "find_dominant_frequency"

        ),


        "description":
            "Returns frequency with maximum power."

    },


    "calculate_band_power": {


        "name":
            "band_power",


        "canonical_name":
            "calculate_band_power",


        "type":
            "signal_analysis",


        "callable":
            calculate_band_power,


        "aliases": (

            "band_power",

            "calculate_band_power",

            "compute_band_power"

        ),


        "description":
            "Calculates frequency band power."

    },


    "calculate_total_spectral_power": {


        "name":
            "total_spectral_power",


        "canonical_name":
            "calculate_total_spectral_power",


        "type":
            "signal_analysis",


        "callable":
            calculate_total_spectral_power,


        "aliases": (

            "total_spectral_power",

            "calculate_total_spectral_power"

        ),


        "description":
            "Calculates total frequency-domain power."

    },


    "calculate_spectral_entropy": {


        "name":
            "spectral_entropy",


        "canonical_name":
            "calculate_spectral_entropy",


        "type":
            "signal_analysis",


        "callable":
            calculate_spectral_entropy,


        "aliases": (

            "spectral_entropy",

            "calculate_spectral_entropy"

        ),


        "description":
            "Calculates spectral entropy."

    }

}



# ============================================================
# RESOURCE LOOKUP
# ============================================================

def _build_lookup():

    lookup = {}


    for definition in RESOURCE_DEFINITIONS.values():


        lookup[
            normalize_resource_name(
                definition["canonical_name"]
            )
        ] = definition


        for alias in definition["aliases"]:


            lookup[
                normalize_resource_name(alias)
            ] = definition


    return lookup



RESOURCE_LOOKUP = _build_lookup()



# ============================================================
# RESOURCE RESOLUTION
# ============================================================

def resolve_resource(
    resource_name: str
) -> Optional[Dict]:

    resource = RESOURCE_LOOKUP.get(
        normalize_resource_name(
            resource_name
        )
    )


    if resource is None:

        return None


    return {


        "name":
            resource["name"],


        "canonical_name":
            resource["canonical_name"],


        "type":
            resource["type"],


        "callable":
            resource["callable"],


        "description":
            resource["description"],


        "master_doc":
            MASTER_DOC_NAME,


        "master_doc_role":
            MASTER_DOC_ROLE,


        "source_acquired":
            True

    }



def get_resource(
    resource_name
):

    return resolve_resource(
        resource_name
    )



def list_resources():

    output = []


    for resource in RESOURCE_DEFINITIONS.values():

        output.append({

            "name":
                resource["name"],


            "canonical_name":
                resource["canonical_name"],


            "aliases":
                list(
                    resource["aliases"]
                ),


            "type":
                resource["type"]

        })


    return output



# ============================================================
# VALIDATION
# ============================================================

def validate_master_doc():

    required = (

        "spectral_power",

        "dominant_frequency"

    )


    errors = []


    for item in required:


        if resolve_resource(item) is None:

            errors.append(
                f"{item} unavailable"
            )


    return {


        "valid":
            len(errors) == 0,


        "master_doc":
            MASTER_DOC_NAME,


        "role":
            MASTER_DOC_ROLE,


        "resource_count":
            len(
                RESOURCE_DEFINITIONS
            ),


        "errors":
            errors

    }



# ============================================================
# SELF TEST
# ============================================================

if __name__ == "__main__":


    print("=" * 70)

    print(
        "MASTER-DOC SIGNAL ANALYSIS"
    )

    print("=" * 70)


    result = validate_master_doc()


    print()

    print(
        result
    )


    print()

    print(
        "Required resources:"
    )


    for item in (

        "spectral_power",

        "dominant_frequency"

    ):

        resource = resolve_resource(
            item
        )


        print(
            f"✓ {item}"
            f" -> "
            f"{resource['callable'].__name__}"
        )
