
# ============================================================
# NEURAL ANALYSIS / PIPELINE COMPILATION SYSTEM
# ============================================================
#
# analysis.py
#
# RESPONSIBILITY:
#
#     1. Receive the parameter object from ingestion.py.
#     2. Discover the Master-DOC library.
#     3. Load the Master-DOC Python resources.
#     4. Identify their logical roles.
#     5. Match the requested parameters to Master-DOC resources.
#     6. Build a generation specification.
#     7. Hand that specification to generator.py.
#
# IMPORTANT:
#
# analysis.py does NOT generate the final source code.
#
# generator.py will eventually:
#
#     generation specification
#             |
#             v
#     Master-DOC resource selection
#             |
#             v
#     source-code compilation
#             |
#             v
#     generated pipeline
#
# ============================================================


# ============================================================
# IMPORTS
# ============================================================

from pathlib import Path
import importlib.util
from importlib.machinery import SourceFileLoader
from types import ModuleType
from typing import Any


# ============================================================
# MASTER-DOC DIRECTORY
# ============================================================

MASTER_DOC_DIRECTORY = (
    Path(__file__).resolve().parent /
    "Master-DOC's"
)


# ============================================================
# MASTER-DOC IDENTIFIERS
# ============================================================

MASTER_DOC_ROLE_PATTERNS = {

    "ingestion": (
        "master-doc-ingestion",
    ),

    "preprocessing": (
        "master-doc-preprocessing",
    ),

    "statistics": (
        "master-doc-stats",
        "master-doc-statistics",
    ),

    "decoding": (
        "master-doc-decoding",
    ),

    "visualization": (
        "master-doc-visualization",
        "master-doc-visualizatiom",
    ),

    "validation": (
        "master-doc-validation",
    ),

    "pipeline": (
        "master-doc-pipeline",
    ),

    "output": (
        "master-doc-output",
    ),

    "connectivity": (
        "master-doc-connectivity",
    ),

    "signal_analysis": (
        "master-doc-signal_analysis",
        "master-doc-signal-analysis",
    ),

    "generator": (
        "master-doc-generator",
    ),
}


# ============================================================
# NORMALIZE FILE NAME
# ============================================================

def normalize_document_name(
    name: str
) -> str:

    return (
        Path(name)
        .stem
        .lower()
        .replace("_", "-")
        .replace(" ", "-")
    )


# ============================================================
# DISCOVER MASTER-DOC FILES
# ============================================================

def discover_master_docs():

    if not MASTER_DOC_DIRECTORY.exists():

        raise FileNotFoundError(
            "Master-DOC directory not found:\n"
            f"{MASTER_DOC_DIRECTORY}"
        )

    if not MASTER_DOC_DIRECTORY.is_dir():

        raise NotADirectoryError(
            "Master-DOC path is not a directory:\n"
            f"{MASTER_DOC_DIRECTORY}"
        )

    return sorted(
        (
            path
            for path in MASTER_DOC_DIRECTORY.iterdir()
            if (
                path.is_file()
                and not path.name.startswith(".")
                and path.suffix.lower() == ".py"
                and "__pycache__" not in path.parts
            )
        ),
        key=lambda path: path.name.lower()
    )


# ============================================================
# LOAD ONE MASTER-DOC
# ============================================================

def load_master_doc(
    document_path: Path
) -> ModuleType:

    module_name = (
        document_path.stem
        .replace("-", "_")
        .replace(" ", "_")
    )

    loader = SourceFileLoader(
        module_name,
        str(document_path)
    )

    specification = importlib.util.spec_from_loader(
        module_name,
        loader
    )

    if specification is None:

        raise ImportError(
            "Unable to create module specification for "
            f"{document_path.name}"
        )

    module = importlib.util.module_from_spec(
        specification
    )

    loader.exec_module(
        module
    )

    return module


# ============================================================
# LOAD COMPLETE MASTER-DOC LIBRARY
# ============================================================

def load_master_docs():

    document_paths = (
        discover_master_docs()
    )

    loaded = {}

    errors = {}

    for document_path in document_paths:

        try:

            module = load_master_doc(
                document_path
            )

            loaded[
                document_path.name
            ] = module

        except Exception as error:

            errors[
                document_path.name
            ] = error

    return {
        "discovered": document_paths,
        "loaded": loaded,
        "errors": errors,
    }


# ============================================================
# IDENTIFY MASTER-DOC ROLES
# ============================================================

def identify_master_doc_roles(
    loaded_docs
):

    roles = {}

    unmatched = {}

    for document_name, module in loaded_docs.items():

        normalized_name = (
            normalize_document_name(
                document_name
            )
        )

        matched_role = None

        for role, patterns in (
            MASTER_DOC_ROLE_PATTERNS.items()
        ):

            for pattern in patterns:

                if (
                    normalized_name == pattern
                    or
                    normalized_name.startswith(
                        pattern
                    )
                ):

                    matched_role = role
                    break

            if matched_role is not None:
                break

        if matched_role is not None:

            roles[
                matched_role
            ] = module

        else:

            unmatched[
                document_name
            ] = module

    return {
        "roles": roles,
        "unmatched": unmatched,
    }


# ============================================================
# REQUIRE MASTER-DOC ROLE
# ============================================================

def require_master_doc_role(
    roles,
    role
):

    module = roles.get(
        role
    )

    if module is None:

        raise RuntimeError(
            "Required Master-DOC role is unavailable: "
            f"{role}"
        )

    return module


# ============================================================
# VALIDATE MASTER-DOC LIBRARY
# ============================================================

def validate_master_doc_library(
    master_doc_state
):

    errors = []

    loaded_docs = (
        master_doc_state[
            "loaded"
        ]
    )

    load_errors = (
        master_doc_state[
            "errors"
        ]
    )

    if load_errors:

        for document_name, error in (
            load_errors.items()
        ):

            errors.append(
                "Master-DOC failed to execute: "
                f"{document_name} -> "
                f"{type(error).__name__}: {error}"
            )

    roles_state = (
        identify_master_doc_roles(
            loaded_docs
        )
    )

    roles = (
        roles_state[
            "roles"
        ]
    )

    # --------------------------------------------------------
    # Validation is useful for reporting, but the Generator
    # Master-DOC is NOT required to expose functions that
    # analysis.py calls.
    #
    # Therefore we only require the Master-DOC resources
    # themselves to exist.
    # --------------------------------------------------------

    required_roles = (
        "validation",
        "generator",
    )

    for role in required_roles:

        if role not in roles:

            errors.append(
                "Required Master-DOC role missing: "
                f"{role}"
            )

    return {
        "valid": (
            len(errors) == 0
        ),
        "errors": errors,
        "roles": roles,
        "unmatched": (
            roles_state[
                "unmatched"
            ]
        ),
    }


# ============================================================
# CONVERT PARAMETER OBJECT TO REQUEST DICTIONARY
# ============================================================

def parameter_object_to_request(
    parameters
):

    if parameters is None:

        return {}

    if isinstance(
        parameters,
        dict
    ):

        return dict(
            parameters
        )

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

    attributes = {}

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

        attributes[
            name
        ] = value

    return attributes


# ============================================================
# NORMALIZE REQUEST
# ============================================================
#
# IMPORTANT:
#
# This is intentionally local to analysis.py.
#
# We are NOT asking Master-DOC-Generator for a function named
# normalize_request().
#
# The parameter object has already been converted into a
# normal dictionary.
#
# This function simply establishes a predictable structure.
# ============================================================

def normalize_request(
    request
):

    if request is None:

        return {}

    if not isinstance(
        request,
        dict
    ):

        raise TypeError(
            "Normalized request must be a dictionary."
        )

    normalized = dict(
        request
    )

    # --------------------------------------------------------
    # Normalize common list-valued parameters.
    # --------------------------------------------------------

    list_fields = (
        "preprocessing",
        "statistics",
        "features",
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
            ] = [value]

        else:

            normalized[
                field
            ] = list(value)

    return normalized


# ============================================================
# FIND MASTER-DOC RESOURCE FOR REQUEST
# ============================================================
#
# analysis.py identifies which Master-DOC resources are
# relevant to the request.
#
# It does NOT copy their implementation code.
# ============================================================

def select_master_doc_resources(
    request,
    roles
):

    selected = {}

    # --------------------------------------------------------
    # Core resources
    # --------------------------------------------------------

    for role in (
        "ingestion",
        "preprocessing",
        "statistics",
        "decoding",
        "visualization",
        "validation",
        "pipeline",
        "output",
        "connectivity",
        "signal_analysis",
    ):

        if role in roles:

            selected[
                role
            ] = roles[
                role
            ].__name__

    # --------------------------------------------------------
    # Generator is part of the compilation architecture.
    # --------------------------------------------------------

    if "generator" in roles:

        selected[
            "generator"
        ] = roles[
            "generator"
        ].__name__

    return selected


# ============================================================
# BUILD COMPONENT REQUEST
# ============================================================
#
# This object describes WHAT the Generator needs.
#
# It does not contain the final generated source code.
# ============================================================

def build_component_request(
    request
):

    components = {}

    # --------------------------------------------------------
    # Neural data
    # --------------------------------------------------------

    components[
        "neural_data"
    ] = request.get(
        "neural_data"
    )

    # --------------------------------------------------------
    # File format
    # --------------------------------------------------------

    components[
        "file_type"
    ] = request.get(
        "file_type"
    )

    # --------------------------------------------------------
    # Pipeline type
    # --------------------------------------------------------

    components[
        "pipeline_type"
    ] = request.get(
        "pipeline_type"
    )

    # --------------------------------------------------------
    # Preprocessing
    # --------------------------------------------------------

    components[
        "preprocessing"
    ] = request.get(
        "preprocessing",
        []
    )

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    components[
        "statistics"
    ] = request.get(
        "statistics",
        []
    )

    # --------------------------------------------------------
    # Features
    # --------------------------------------------------------

    components[
        "features"
    ] = request.get(
        "features",
        []
    )

    # --------------------------------------------------------
    # Decoder
    # --------------------------------------------------------

    components[
        "decoder"
    ] = request.get(
        "decoder"
    )

    # --------------------------------------------------------
    # Target
    # --------------------------------------------------------

    components[
        "target_type"
    ] = request.get(
        "target_type"
    )

    # --------------------------------------------------------
    # Visualization
    # --------------------------------------------------------

    components[
        "visualization"
    ] = request.get(
        "visualization",
        False
    )

    return components


# ============================================================
# BUILD COMPATIBILITY OBJECT
# ============================================================
#
# The actual compatibility rules belong in the Master-DOC
# library.
#
# At this stage analysis.py records the information needed by
# the Generator to perform compatibility resolution.
# ============================================================

def build_compatibility_context(
    request
):

    return {

        "neural_data":
            request.get(
                "neural_data"
            ),

        "file_type":
            request.get(
                "file_type"
            ),

        "pipeline_type":
            request.get(
                "pipeline_type"
            ),

        "preprocessing":
            request.get(
                "preprocessing",
                []
            ),

        "statistics":
            request.get(
                "statistics",
                []
            ),

        "features":
            request.get(
                "features",
                []
            ),

        "decoder":
            request.get(
                "decoder"
            ),

        "target_type":
            request.get(
                "target_type"
            ),

    }


# ============================================================
# BUILD GENERATION SPECIFICATION
# ============================================================
#
# THIS IS THE OBJECT THAT GETS HANDED TO generator.py.
#
# This is the critical boundary between analysis and
# generation.
# ============================================================

def build_generation_specification(
    request,
    roles
):

    master_doc_resources = (
        select_master_doc_resources(
            request,
            roles
        )
    )

    component_request = (
        build_component_request(
            request
        )
    )

    compatibility = (
        build_compatibility_context(
            request
        )
    )

    return {

        "type":
            "neural_pipeline_generation_specification",

        "version":
            "1.0",

        "request":
            dict(request),

        "components":
            component_request,

        "master_doc_resources":
            master_doc_resources,

        "compatibility":
            compatibility,

        "generation":
            {

                "source_generation":
                    True,

                "compile_master_doc_code":
                    True,

                "write_output":
                    False,

            },

    }


# ============================================================
# HAND OFF TO GENERATOR
# ============================================================
#
# This is deliberately isolated.
#
# analysis.py produces the object.
#
# generator.py receives the object.
#
# generator.py will eventually inspect it and compile the
# actual pipeline.
# ============================================================

def handoff_to_generator(
    generation_specification
):

    from generator import generate

    return generate(
        generation_specification
    )


# ============================================================
# ANALYZE
# ============================================================
#
# Main entry point used by ingestion.py.
# ============================================================

def analyze(
    parameters
):

    # --------------------------------------------------------
    # STEP 1
    # Receive parameter object.
    # --------------------------------------------------------

    request = (
        parameter_object_to_request(
            parameters
        )
    )

    # --------------------------------------------------------
    # STEP 2
    # Normalize into a predictable dictionary.
    # --------------------------------------------------------

    request = (
        normalize_request(
            request
        )
    )

    # --------------------------------------------------------
    # STEP 3
    # Load Master-DOC library.
    # --------------------------------------------------------

    master_doc_state = (
        load_master_docs()
    )

    # --------------------------------------------------------
    # STEP 4
    # Validate that the library itself is available.
    # --------------------------------------------------------

    library_validation = (
        validate_master_doc_library(
            master_doc_state
        )
    )

    if not library_validation[
        "valid"
    ]:

        raise RuntimeError(
            "Master-DOC compiler library is not ready:\n"
            +
            "\n".join(
                library_validation[
                    "errors"
                ]
            )
        )

    # --------------------------------------------------------
    # STEP 5
    # Retrieve logical Master-DOC roles.
    # --------------------------------------------------------

    roles = (
        library_validation[
            "roles"
        ]
    )

    # --------------------------------------------------------
    # STEP 6
    # Build the object that describes what the Generator
    # needs to compile.
    # --------------------------------------------------------

    generation_specification = (
        build_generation_specification(
            request,
            roles
        )
    )

    # --------------------------------------------------------
    # STEP 7
    # HANDOFF
    #
    # This is the point where analysis.py stops being the
    # construction layer and generator.py takes ownership.
    # --------------------------------------------------------

    generator_result = (
        handoff_to_generator(
            generation_specification
        )
    )

    # --------------------------------------------------------
    # STEP 8
    # Return Generator result to ingestion.py.
    # --------------------------------------------------------

    return generator_result


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
                "spectral_power",
                "dominant_frequency",
            ],

        "features":
            [],

        "target_type":
            None,

        "decoder":
            None,

        "visualization":
            False,
    }

    result = analyze(
        test_parameters
    )

    print()

    print(
        "ANALYSIS RESULT:"
    )

    print(
        result
    )
