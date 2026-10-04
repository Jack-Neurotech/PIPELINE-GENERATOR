# ============================================================
# NEURAL ANALYSIS / PIPELINE COMPILATION SYSTEM
# ============================================================
#
# analysis.py is the orchestration layer between:
#
#     Ingestion.py
#           |
#           v
#     parameter object
#           |
#           v
#     analysis.py
#           |
#           v
#     generation specification
#           |
#           v
#     generator.py
#
# analysis.py does NOT implement scientific algorithms.
#
# It:
#
#     1. receives the parameter object
#     2. normalizes it
#     3. loads generator.py
#     4. hands the generation specification to generator.py
#
# The actual scientific resources remain inside the
# Master-DOC library.
# ============================================================


# ============================================================
# IMPORTS
# ============================================================

from __future__ import annotations

from pathlib import Path
from importlib.machinery import SourceFileLoader
from types import ModuleType
from typing import Any
import importlib.util
import sys


# ============================================================
# PATHS
# ============================================================

BASE_DIRECTORY = Path(__file__).resolve().parent

GENERATOR_FILE = (
    BASE_DIRECTORY /
    "generator.py"
)


# ============================================================
# GENERATOR MODULE NAME
# ============================================================

GENERATOR_MODULE_NAME = (
    "pipeline_generator_runtime"
)


# ============================================================
# LOAD GENERATOR MODULE
# ============================================================
#
# IMPORTANT:
#
# Python 3.14's dataclasses implementation expects the module
# to exist inside sys.modules while the @dataclass decorator
# executes.
#
# Therefore:
#
#     module_from_spec()
#
# MUST be followed by:
#
#     sys.modules[module_name] = module
#
# BEFORE:
#
#     loader.exec_module(module)
#
# This fixes:
#
#     AttributeError:
#     'NoneType' object has no attribute '__dict__'
#
# ============================================================

def load_generator_module() -> ModuleType:

    if not GENERATOR_FILE.exists():

        raise FileNotFoundError(
            "generator.py was not found:\n"
            f"{GENERATOR_FILE}"
        )

    loader = SourceFileLoader(
        GENERATOR_MODULE_NAME,
        str(GENERATOR_FILE)
    )

    specification = (
        importlib.util.spec_from_loader(
            GENERATOR_MODULE_NAME,
            loader
        )
    )

    if specification is None:

        raise ImportError(
            "Unable to create module specification "
            "for generator.py."
        )

    module = (
        importlib.util.module_from_spec(
            specification
        )
    )

    # --------------------------------------------------------
    # CRITICAL PYTHON 3.14 FIX
    # --------------------------------------------------------

    sys.modules[
        GENERATOR_MODULE_NAME
    ] = module

    try:

        loader.exec_module(
            module
        )

    except Exception:

        # Remove the partially loaded module so that a future
        # attempt starts cleanly.
        sys.modules.pop(
            GENERATOR_MODULE_NAME,
            None
        )

        raise

    return module


# ============================================================
# CONVERT PARAMETER OBJECT TO DICTIONARY
# ============================================================

def parameter_object_to_request(
    parameters: Any
) -> dict[str, Any]:

    if parameters is None:

        return {}

    # --------------------------------------------------------
    # DICTIONARY
    # --------------------------------------------------------

    if isinstance(
        parameters,
        dict
    ):

        return dict(
            parameters
        )

    # --------------------------------------------------------
    # to_dict()
    # --------------------------------------------------------

    to_dict = getattr(
        parameters,
        "to_dict",
        None
    )

    if callable(to_dict):

        result = to_dict()

        if not isinstance(
            result,
            dict
        ):

            raise TypeError(
                "parameters.to_dict() must return "
                "a dictionary."
            )

        return dict(
            result
        )

    # --------------------------------------------------------
    # model_dump()
    # --------------------------------------------------------

    model_dump = getattr(
        parameters,
        "model_dump",
        None
    )

    if callable(model_dump):

        result = model_dump()

        if not isinstance(
            result,
            dict
        ):

            raise TypeError(
                "parameters.model_dump() must return "
                "a dictionary."
            )

        return dict(
            result
        )

    # --------------------------------------------------------
    # GENERIC OBJECT
    # --------------------------------------------------------

    result = {}

    for name in dir(
        parameters
    ):

        if name.startswith("_"):

            continue

        try:

            value = getattr(
                parameters,
                name
            )

        except Exception:

            continue

        if callable(value):

            continue

        result[name] = value

    return result


# ============================================================
# NORMALIZE REQUEST
# ============================================================

def normalize_request(
    request: dict[str, Any]
) -> dict[str, Any]:

    normalized = dict(
        request
    )

    list_fields = (
        "preprocessing",
        "statistics",
        "features",
        "signal_analysis",
    )

    for field_name in list_fields:

        value = normalized.get(
            field_name
        )

        if value is None:

            normalized[
                field_name
            ] = []

        elif isinstance(
            value,
            str
        ):

            normalized[
                field_name
            ] = [value]

        else:

            normalized[
                field_name
            ] = list(value)

    return normalized


# ============================================================
# BUILD GENERATION SPECIFICATION
# ============================================================
#
# This is intentionally simple.
#
# analysis.py creates the handoff object.
#
# generator.py performs the actual resource acquisition.
# ============================================================

def build_generation_specification(
    parameters: Any
) -> dict[str, Any]:

    request = (
        parameter_object_to_request(
            parameters
        )
    )

    return normalize_request(
        request
    )


# ============================================================
# ANALYZE
# ============================================================
#
# Public entry point used by Ingestion.py.
#
# The object handoff occurs here:
#
#     parameters
#          ↓
#     generation_specification
#          ↓
#     generator.generate()
#
# ============================================================

def analyze(
    parameters: Any
):

    print()
    print(
        "=" * 70
    )
    print(
        "NEURAL PIPELINE ANALYSIS"
    )
    print(
        "=" * 70
    )

    # --------------------------------------------------------
    # RECEIVE OBJECT
    # --------------------------------------------------------

    generation_specification = (
        build_generation_specification(
            parameters
        )
    )

    print()
    print(
        "GENERATION SPECIFICATION CREATED"
    )

    print(
        "Object handed from analysis.py to generator.py."
    )

    print()

    for key, value in (
        generation_specification.items()
    ):

        print(
            f"  {key}: {value}"
        )

    # --------------------------------------------------------
    # LOAD GENERATOR
    # --------------------------------------------------------

    generator_module = (
        load_generator_module()
    )

    # --------------------------------------------------------
    # REQUIRE GENERATE FUNCTION
    # --------------------------------------------------------

    generate_function = getattr(
        generator_module,
        "generate",
        None
    )

    if not callable(
        generate_function
    ):

        raise AttributeError(
            "generator.py does not expose "
            "required function 'generate'."
        )

    # --------------------------------------------------------
    # HAND OFF OBJECT
    # --------------------------------------------------------

    print()
    print(
        "HANDING SPECIFICATION TO GENERATOR..."
    )

    result = generate_function(
        generation_specification
    )

    print()
    print(
        "GENERATOR RETURNED RESULT."
    )

    return result


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    test_parameters = {

        "neural_data":
            "EEG",

        "file_type":
            ".edf",

        "pipeline_type":
            "EEG",

        "preprocessing":
            [
                "bandpass_filter",
                "notch_filter",
            ],

        "statistics":
            [
                "mean",
                "std",
                "variance",
                "rms",
            ],

        "signal_analysis":
            [
                "spectral_power",
                "dominant_frequency",
            ],

        "decoder":
            None,

        "visualization":
            False,

        "output":
            None,
    }

    result = analyze(
        test_parameters
    )

    print()
    print(
        "=" * 70
    )

    print(
        "ANALYSIS RESULT"
    )

    print(
        "=" * 70
    )

    print(
        result
    )

