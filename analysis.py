
# ============================================================
# NEURAL ANALYSIS / PIPELINE COMPILATION SYSTEM
# ============================================================
#
# analysis.py is the orchestration layer between:
#
#     ingestion.py
#          |
#          v
#     parameter object
#          |
#          v
#     analysis.py
#          |
#          v
#     generation specification
#          |
#          v
#     generator.py
#          |
#          v
#     Master-DOC raw-material resolution
#
#
# IMPORTANT:
#
# analysis.py does NOT resolve individual scientific resources.
#
# It does NOT search for:
#
#     band_pass_filter
#     calculate_mean
#     EEG_EEGLAB
#     calculate_dominant_frequency
#
# That responsibility belongs to generator.py.
#
# analysis.py prepares the request and hands the resulting
# generation specification to generator.py.
# ============================================================


# ============================================================
# IMPORTS
# ============================================================

from pathlib import Path
import importlib.util
from importlib.machinery import SourceFileLoader
from types import ModuleType


# ============================================================
# GENERATOR PATH
# ============================================================
#
# generator.py lives beside analysis.py.
#
# The path is resolved relative to this file so the system does
# not depend on the user's current terminal directory.
# ============================================================

GENERATOR_PATH = (
    Path(__file__).resolve().parent /
    "generator.py"
)


# ============================================================
# LOAD GENERATOR MODULE
# ============================================================
#
# analysis.py loads generator.py dynamically.
#
# This keeps the architecture:
#
#     analysis
#         |
#         +----> generator
#
# without duplicating generator logic here.
# ============================================================

def load_generator_module():

    if not GENERATOR_PATH.exists():

        raise FileNotFoundError(
            "generator.py was not found:\n"
            f"{GENERATOR_PATH}"
        )

    module_name = (
        "pipeline_generator_runtime"
    )

    loader = SourceFileLoader(
        module_name,
        str(GENERATOR_PATH)
    )

    specification = (
        importlib.util.spec_from_loader(
            module_name,
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

    loader.exec_module(
        module
    )

    return module


# ============================================================
# REQUIRE GENERATOR FUNCTION
# ============================================================
#
# analysis.py requires only the public handoff function.
#
# generator.py owns everything that happens after the handoff.
# ============================================================

def require_generator_function(
    generator_module,
    function_name
):

    function = getattr(
        generator_module,
        function_name,
        None
    )

    if not callable(function):

        raise AttributeError(
            "generator.py does not expose required "
            f"function '{function_name}'."
        )

    return function


# ============================================================
# PARAMETER OBJECT → REQUEST DICTIONARY
# ============================================================
#
# ingestion.py supplies the parameter object.
#
# The parameter object may be:
#
#     dictionary
#     dataclass
#     object with to_dict()
#     Pydantic-style object with model_dump()
#     ordinary object with public attributes
#
# analysis.py converts it into a dictionary without changing
# the scientific meaning of the parameters.
# ============================================================

def parameter_object_to_request(
    parameters
):

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

    if callable(
        to_dict
    ):

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

    if callable(
        model_dump
    ):

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
    # PUBLIC ATTRIBUTES
    # --------------------------------------------------------

    attributes = {}

    for name in dir(
        parameters
    ):

        if name.startswith(
            "_"
        ):

            continue

        try:

            value = getattr(
                parameters,
                name
            )

        except Exception:

            continue

        if callable(
            value
        ):

            continue

        attributes[
            name
        ] = value

    return attributes


# ============================================================
# NORMALIZE REQUEST STRUCTURE
# ============================================================
#
# This function does NOT translate scientific function names.
#
# It simply ensures the request has the expected top-level
# structure before the generator receives it.
# ============================================================

def normalize_request_structure(
    request
):

    normalized = dict(
        request
    )

    # --------------------------------------------------------
    # DEFAULT COLLECTIONS
    # --------------------------------------------------------

    collection_defaults = {

        "preprocessing":
            [],

        "statistics":
            [],

        "signal_analysis":
            [],

        "features":
            [],

        "decoder":
            None,

        "target_type":
            None,

        "visualization":
            False,

        "output":
            [],
    }

    for key, default in (
        collection_defaults.items()
    ):

        if key not in normalized:

            normalized[
                key
            ] = default

    # --------------------------------------------------------
    # ENSURE LIST-LIKE COMPONENTS ARE LISTS
    # --------------------------------------------------------

    list_fields = (

        "preprocessing",

        "statistics",

        "signal_analysis",

        "features",

        "output",
    )

    for field in list_fields:

        value = normalized.get(
            field
        )

        if value is None:

            normalized[
                field
            ] = []

        elif isinstance(
            value,
            str
        ):

            normalized[
                field
            ] = [
                value
            ]

    return normalized


# ============================================================
# BUILD GENERATION SPECIFICATION
# ============================================================
#
# This is the key handoff object.
#
# It contains:
#
#     components
#         |
#         +-- neural_data
#         +-- file_type
#         +-- pipeline_type
#         +-- preprocessing
#         +-- statistics
#         +-- signal_analysis
#         +-- features
#         +-- decoder
#         +-- target_type
#         +-- visualization
#         +-- output
#
#
# The generator receives this object.
#
# The generator then decides which Master-DOC resources
# correspond to each component.
# ============================================================

def build_generation_specification(
    request
):

    return {

        "specification_type":
            "neural_pipeline_generation",

        "version":
            "1.0",

        "components":
            dict(request),

        "source":
            "analysis.py",

        "handoff":
            "analysis_to_generator",
    }


# ============================================================
# VALIDATE BASIC GENERATION SPECIFICATION
# ============================================================
#
# This is intentionally structural validation.
#
# It does NOT validate scientific compatibility.
#
# The generator / Master-DOC system owns resource resolution
# and later compatibility validation.
# ============================================================

def validate_generation_specification(
    specification
):

    errors = []

    if not isinstance(
        specification,
        dict
    ):

        errors.append(
            "Generation specification must "
            "be a dictionary."
        )

        return {

            "valid":
                False,

            "errors":
                errors,
        }

    components = specification.get(
        "components"
    )

    if not isinstance(
        components,
        dict
    ):

        errors.append(
            "Generation specification is missing "
            "the components dictionary."
        )

        return {

            "valid":
                False,

            "errors":
                errors,
        }

    # --------------------------------------------------------
    # REQUIRED INPUT FIELDS
    # --------------------------------------------------------

    required_fields = (

        "neural_data",

        "file_type",

        "pipeline_type",
    )

    for field in required_fields:

        value = components.get(
            field
        )

        if value is None:

            errors.append(
                f"Required parameter missing: "
                f"{field}"
            )

        elif isinstance(
            value,
            str
        ) and not value.strip():

            errors.append(
                f"Required parameter is empty: "
                f"{field}"
            )

    return {

        "valid":
            len(errors) == 0,

        "errors":
            errors,
    }


# ============================================================
# HAND OFF TO GENERATOR
# ============================================================
#
# This is the actual boundary between analysis.py and
# generator.py.
#
# analysis.py creates the object.
#
# generator.py receives the object.
#
# generator.py then accesses the Master-DOCs.
# ============================================================

def handoff_to_generator(
    generation_specification,
    generator_module
):

    receive_function = (
        require_generator_function(
            generator_module,
            "receive_generation_specification"
        )
    )

    return receive_function(
        generation_specification
    )


# ============================================================
# ANALYZE PARAMETER OBJECT
# ============================================================
#
# Public function called by ingestion.py:
#
#     analyze(parameters)
#
# ============================================================

def analyze(
    parameters
):

    # ========================================================
    # STEP 1
    # RECEIVE PARAMETER OBJECT
    # ========================================================

    request = (
        parameter_object_to_request(
            parameters
        )
    )


    # ========================================================
    # STEP 2
    # NORMALIZE REQUEST STRUCTURE
    # ========================================================

    normalized_request = (
        normalize_request_structure(
            request
        )
    )


    # ========================================================
    # STEP 3
    # BUILD GENERATION SPECIFICATION
    # ========================================================

    generation_specification = (
        build_generation_specification(
            normalized_request
        )
    )


    # ========================================================
    # STEP 4
    # STRUCTURAL VALIDATION
    # ========================================================

    validation = (
        validate_generation_specification(
            generation_specification
        )
    )

    if not validation[
        "valid"
    ]:

        return {

            "status":
                "INVALID",

            "parameters":
                parameters,

            "request":
                normalized_request,

            "generation_specification":
                generation_specification,

            "validation":
                validation,

            "generator":
                None,

            "raw_material_resolution":
                None,

            "compilation_plan":
                None,

            "ready_for_compilation":
                False,
        }


    # ========================================================
    # STEP 5
    # LOAD GENERATOR
    # ========================================================

    generator_module = (
        load_generator_module()
    )


    # ========================================================
    # STEP 6
    # HAND OFF OBJECT
    # ========================================================
    #
    # This is where the generator actually receives the
    # generation specification.
    # ========================================================

    generator_state = (
        handoff_to_generator(
            generation_specification,
            generator_module
        )
    )


    # ========================================================
    # STEP 7
    # RETURN COMPLETE ANALYSIS STATE
    # ========================================================

    return {

        "status":
            (
                "READY"
                if generator_state.get(
                    "ready_for_compilation",
                    False
                )
                else generator_state.get(
                    "status",
                    "PARTIAL"
                )
            ),

        "parameters":
            parameters,

        "request":
            normalized_request,

        "generation_specification":
            generation_specification,

        "validation":
            validation,

        "generator":
            generator_state,

        "raw_material_resolution":
            generator_state.get(
                "raw_material_resolution"
            ),

        "compilation_plan":
            generator_state.get(
                "compilation_plan"
            ),

        "ready_for_compilation":
            generator_state.get(
                "ready_for_compilation",
                False
            ),
    }


# ============================================================
# PRINT ANALYSIS REPORT
# ============================================================

def print_analysis_report(
    analysis_state
):

    print()

    print(
        "=" * 70
    )

    print(
        "NEURAL ANALYSIS"
    )

    print(
        "=" * 70
    )

    print()

    print(
        "Analysis status:"
    )

    print(
        f"  "
        f"{analysis_state.get('status')}"
    )

    print()

    # --------------------------------------------------------
    # GENERATION SPECIFICATION
    # --------------------------------------------------------

    specification = (
        analysis_state.get(
            "generation_specification"
        )
    )

    print(
        "Generation specification:"
    )

    if specification is None:

        print(
            "  NONE"
        )

    else:

        print(
            "  specification_type: "
            f"{specification.get('specification_type')}"
        )

        print(
            "  version: "
            f"{specification.get('version')}"
        )

        print(
            "  handoff: "
            f"{specification.get('handoff')}"
        )

    print()

    # --------------------------------------------------------
    # GENERATOR
    # --------------------------------------------------------

    generator_state = (
        analysis_state.get(
            "generator"
        )
    )

    if generator_state is None:

        print(
            "Generator:"
        )

        print(
            "  NOT CALLED"
        )

        print()

    else:

        print(
            "Generator:"
        )

        print(
            "  Status: "
            f"{generator_state.get('status')}"
        )

        print(
            "  Ready for compilation: "
            f"{generator_state.get('ready_for_compilation')}"
        )

        print()

    # --------------------------------------------------------
    # RAW MATERIAL RESOLUTION
    # --------------------------------------------------------

    resolution = (
        analysis_state.get(
            "raw_material_resolution"
        )
    )

    if resolution is not None:

        print(
            "Raw-material resolution:"
        )

        print(
            f"  Status: "
            f"{resolution.get('status')}"
        )

        print()

        unresolved = (
            resolution.get(
                "unresolved",
                []
            )
        )

        if unresolved:

            print(
                "  Unresolved:"
            )

            for item in unresolved:

                print(
                    f"    - "
                    f"{item.get('role')}: "
                    f"{item.get('requested')} "
                    f"-> "
                    f"{item.get('reason')}"
                )

        else:

            print(
                "  Unresolved:"
            )

            print(
                "    NONE"
            )

        print()

    # --------------------------------------------------------
    # COMPILATION PLAN
    # --------------------------------------------------------

    compilation_plan = (
        analysis_state.get(
            "compilation_plan"
        )
    )

    print(
        "Compilation plan:"
    )

    if not compilation_plan:

        print(
            "  NONE"
        )

    else:

        for number, item in enumerate(
            compilation_plan,
            start=1
        ):

            print(
                f"  {number}. "
                f"{item.get('stage')} -> "
                f"{item.get('resolved')}"
            )

    print()

    print(
        "=" * 70
    )


# ============================================================
# DIRECT TEST
# ============================================================
#
# Running:
#
#     python analysis.py
#
# tests:
#
#     parameter object
#          ↓
#     request normalization
#          ↓
#     generation specification
#          ↓
#     generator handoff
#          ↓
#     Master-DOC resource resolution
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # TEST PARAMETER OBJECT
    # --------------------------------------------------------

    test_parameters = {

        "neural_data":
            "EEG",

        "file_type":
            ".set",

        "pipeline_type":
            "EEG",

        "preprocessing": [

            "bandpass_filter",

            "notch_filter",
        ],

        "statistics": [

            "mean",

            "std",

            "variance",

            "rms",

            "spectral_power",

            "dominant_frequency",
        ],

        "features":
            [],

        "decoder":
            None,

        "target_type":
            None,

        "visualization":
            False,

    }


    # --------------------------------------------------------
    # RUN ANALYSIS
    # --------------------------------------------------------

    analysis_state = analyze(
        test_parameters
    )


    # --------------------------------------------------------
    # DISPLAY RESULT
    # --------------------------------------------------------

    print_analysis_report(
        analysis_state
    )

