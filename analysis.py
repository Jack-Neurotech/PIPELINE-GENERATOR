# ============================================================
# NEURAL ANALYSIS / PIPELINE COMPILATION SYSTEM
# ============================================================
#
# analysis.py is the orchestration and compilation layer of
# the Neural Analysis Pipeline Generator.
#
# INGESTION.py
#       |
#       v
# parameter object
#       |
#       v
# analysis.py
#       |
#       +----> Master-DOC library
#       |
#       +----> Generator Master-DOC
#       |
#       +----> Validation Master-DOC
#       |
#       v
# validated generation specification
#       |
#       v
# future source-code generator
#
# IMPORTANT:
#
# analysis.py does NOT invent scientific algorithms.
#
# The scientific methods, compatibility rules, pipeline stages,
# and generator rules come from the Master-DOC library.
#
# analysis.py coordinates those resources.
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
#
# The Master-DOC library lives beside analysis.py:
#
# PIPELINE-GENERATOR/
#
#     analysis.py
#
#     Master-DOC's/
#         Master-DOC-Ingestion.py
#         Master-DOC-Preprocessing.py
#         Master-DOC-Stats.py
#         Master-DOC-Decoding.py
#         Master-DOC-Visualization.py
#         Master-DOC-Validation.py
#         Master-DOC-Pipeline.py
#         Master-DOC-Output.py
#         Master-DOC-Connectivity.py
#         Master-DOC-Generator.py
#         Master-DOC-Signal_Analysis.py
#
# The directory is discovered relative to this file so that
# the program does not depend on the user's current terminal
# location.
# ============================================================

MASTER_DOC_DIRECTORY = (
    Path(__file__).resolve().parent /
    "Master-DOC's"
)


# ============================================================
# MASTER-DOC IDENTIFIERS
# ============================================================
#
# These are the logical roles used by the compiler.
#
# The physical filenames are discovered dynamically.
#
# This prevents analysis.py from depending on the exact
# capitalization or punctuation of the filenames.
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
    )

}


# ============================================================
# NORMALIZE FILE NAME
# ============================================================
#
# Converts a physical Master-DOC filename into a predictable
# comparison form.
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
#
# Every file in Master-DOC's is considered a potential
# executable Python resource.
#
# We intentionally do NOT hard-code a list of only 5 or 8
# Master-DOCs.
#
# This means newly added Master-DOCs are automatically
# discovered.
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
            if path.is_file()
            and not path.name.startswith(".")
            and path.suffix.lower() != ".pyc"
            and "__pycache__" not in path.parts
        ),
        key=lambda path: path.name.lower()
    )


# ============================================================
# LOAD ONE MASTER-DOC
# ============================================================
#
# The Master-DOCs are executable Python source files.
#
# SourceFileLoader allows analysis.py to execute them even
# when the physical filename contains hyphens.
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
#
# This is the central resource-loading operation.
#
# ALL discovered Master-DOCs are executed.
#
# A failed Master-DOC is recorded rather than silently
# disappearing.
#
# The compiler can therefore distinguish:
#
#     loaded successfully
#
# from
#
#     discovered but failed
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
        "errors": errors
    }


# ============================================================
# IDENTIFY MASTER-DOC ROLES
# ============================================================
#
# The generator does not need to know the physical filename
# of every document.
#
# It needs to know which loaded module performs which role.
#
# Example:
#
#     Master-DOC-Validation.py
#
# becomes:
#
#     validation
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
        "unmatched": unmatched
    }


# ============================================================
# FIND REQUIRED MASTER-DOC
# ============================================================
#
# The Generator Master-DOC and Validation Master-DOC are
# fundamental to compilation.
#
# We fail explicitly if either is unavailable.
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
            f"Required Master-DOC role is unavailable: "
            f"{role}"
        )

    return module


# ============================================================
# FIND FUNCTION
# ============================================================
#
# Master-DOCs contain executable functions.
#
# This helper retrieves a required function from the correct
# Master-DOC without duplicating its implementation.
# ============================================================

def require_function(
    module: ModuleType,
    function_name: str
):

    function = getattr(
        module,
        function_name,
        None
    )

    if not callable(function):

        raise AttributeError(
            f"Master-DOC "
            f"'{module.__name__}' does not expose "
            f"required function '{function_name}'."
        )

    return function


# ============================================================
# VALIDATE MASTER-DOC LIBRARY
# ============================================================
#
# Before compiling a user pipeline we verify that the critical
# compiler resources actually exist.
#
# This is different from validating the user's requested
# pipeline.
#
# This validates the COMPILER itself.
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
                f"Master-DOC failed to execute: "
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
    # REQUIRED COMPILER ROLES
    # --------------------------------------------------------

    required_roles = (
        "generator",
        "validation"
    )

    for role in required_roles:

        if role not in roles:

            errors.append(
                f"Required Master-DOC role missing: "
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
        )
    }


# ============================================================
# CONVERT PARAMETER OBJECT TO REQUEST DICTIONARY
# ============================================================
#
# Ingestion.py supplies the parameter object.
#
# The Generator Master-DOC operates on a request dictionary.
#
# We therefore adapt the object without changing its contents.
#
# Supported input forms:
#
#     dictionary
#
#     dataclass/object with attributes
#
#     object exposing to_dict()
#
#     object exposing model_dump()
#
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
# NORMALIZE REQUEST USING GENERATOR MASTER-DOC
# ============================================================
#
# The Generator Master-DOC already owns the request-normalizing
# logic.
#
# analysis.py therefore calls that function instead of
# duplicating the rules.
# ============================================================

def normalize_request(
    request,
    generator_module
):

    function = require_function(
        generator_module,
        "normalize_request"
    )

    return function(
        request
    )


# ============================================================
# RUN MASTER-DOC VALIDATION
# ============================================================
#
# Validation is performed by Master-DOC-Validation.
#
# The Generator Master-DOC itself also performs structural
# validation, so both layers are preserved:
#
#     analysis
#         |
#         +--> Validation Master-DOC
#         |
#         +--> Generator Master-DOC
# ============================================================

def validate_request(
    request,
    validation_module
):

    validation_function = require_function(
        validation_module,
        "validate_pipeline_configuration"
    )

    return validation_function(
        neural_data=request.get(
            "neural_data"
        ),

        file_type=request.get(
            "file_type"
        ),

        pipeline_type=request.get(
            "pipeline_type"
        ),

        preprocessing=request.get(
            "preprocessing"
        ),

        statistics=request.get(
            "statistics"
        ),

        features=request.get(
            "features"
        ),

        decoder=request.get(
            "decoder"
        ),

        target_type=request.get(
            "target_type"
        )
    )


# ============================================================
# BUILD GENERATION SPECIFICATION
# ============================================================
#
# This is the central compilation operation.
#
# We deliberately use the actual Generator Master-DOC's
# build_generator_specification() function.
#
# analysis.py does not recreate that algorithm.
# ============================================================

def compile_generation_specification(
    request,
    generator_module,
    validation_module
):

    validation_function = require_function(
        validation_module,
        "validate_pipeline_configuration"
    )

    generator_function = require_function(
        generator_module,
        "build_generator_specification"
    )

    specification = generator_function(
        request,
        validation_function
    )

    return specification


# ============================================================
# RUN GENERATOR SAFETY GATE
# ============================================================
#
# The Generator Master-DOC defines the final safety gate.
#
# Invalid specifications must never proceed toward source
# generation.
# ============================================================

def run_generator_safety_gate(
    specification,
    generator_module
):

    safety_function = require_function(
        generator_module,
        "generator_safety_check"
    )

    return safety_function(
        specification
    )


# ============================================================
# CHECK GENERATION READINESS
# ============================================================

def check_generation_readiness(
    specification,
    generator_module
):

    readiness_function = require_function(
        generator_module,
        "ready_for_generation"
    )

    return bool(
        readiness_function(
            specification
        )
    )


# ============================================================
# BUILD COMPLETE COMPILER STATE
# ============================================================
#
# This function performs the entire analysis stage.
#
# It does NOT generate arbitrary scientific code.
#
# It compiles a validated generation specification using the
# actual Master-DOC Generator and Validation libraries.
# ============================================================

def analyze(
    parameters
):

    # --------------------------------------------------------
    # STEP 1
    # RECEIVE PARAMETER OBJECT
    # --------------------------------------------------------

    request = (
        parameter_object_to_request(
            parameters
        )
    )


    # --------------------------------------------------------
    # STEP 2
    # LOAD COMPLETE MASTER-DOC LIBRARY
    # --------------------------------------------------------

    master_doc_state = (
        load_master_docs()
    )


    # --------------------------------------------------------
    # STEP 3
    # VERIFY MASTER-DOC LIBRARY
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
    # STEP 4
    # IDENTIFY MASTER-DOC ROLES
    # --------------------------------------------------------

    roles = (
        library_validation[
            "roles"
        ]
    )


    # --------------------------------------------------------
    # STEP 5
    # GET GENERATOR MASTER-DOC
    # --------------------------------------------------------

    generator_module = (
        require_master_doc_role(
            roles,
            "generator"
        )
    )


    # --------------------------------------------------------
    # STEP 6
    # GET VALIDATION MASTER-DOC
    # --------------------------------------------------------

    validation_module = (
        require_master_doc_role(
            roles,
            "validation"
        )
    )


    # --------------------------------------------------------
    # STEP 7
    # NORMALIZE USER REQUEST
    # --------------------------------------------------------
    #
    # This uses the actual Generator Master-DOC.
    # --------------------------------------------------------

    normalized_request = (
        normalize_request(
            request,
            generator_module
        )
    )


    # --------------------------------------------------------
    # STEP 8
    # VALIDATE REQUEST
    # --------------------------------------------------------
    #
    # This uses the actual Validation Master-DOC.
    # --------------------------------------------------------

    validation_result = (
        validate_request(
            normalized_request,
            validation_module
        )
    )


    # --------------------------------------------------------
    # STEP 9
    # STOP INVALID REQUESTS
    # --------------------------------------------------------

    if not validation_result.get(
        "valid",
        False
    ):

        return {

            "status":
                "INVALID",

            "parameters":
                parameters,

            "request":
                normalized_request,

            "master_docs":
                master_doc_state[
                    "loaded"
                ],

            "master_doc_roles":
                roles,

            "validation":
                validation_result,

            "specification":
                None,

            "safety":
                None,

            "ready_for_generation":
                False

        }


    # --------------------------------------------------------
    # STEP 10
    # COMPILE GENERATION SPECIFICATION
    # --------------------------------------------------------
    #
    # The Generator Master-DOC now determines:
    #
    #     required components
    #     required stages
    #     decoding requirements
    #     data connections
    #     output configuration
    #
    # according to the request.
    # --------------------------------------------------------

    specification = (
        compile_generation_specification(
            normalized_request,
            generator_module,
            validation_module
        )
    )


    # --------------------------------------------------------
    # STEP 11
    # RUN FINAL GENERATOR SAFETY CHECK
    # --------------------------------------------------------

    safety = (
        run_generator_safety_gate(
            specification,
            generator_module
        )
    )


    # --------------------------------------------------------
    # STEP 12
    # DETERMINE GENERATION READINESS
    # --------------------------------------------------------

    ready = False

    if safety.get(
        "safe",
        False
    ):

        ready = (
            check_generation_readiness(
                specification,
                generator_module
            )
        )


    # --------------------------------------------------------
    # STEP 13
    # RETURN COMPLETE COMPILER STATE
    # --------------------------------------------------------

    return {

        "status":
            (
                "READY"
                if ready
                else "REJECTED"
            ),

        "parameters":
            parameters,

        "request":
            normalized_request,

        "master_docs":
            master_doc_state[
                "loaded"
            ],

        "master_doc_roles":
            roles,

        "validation":
            validation_result,

        "specification":
            specification,

        "safety":
            safety,

        "ready_for_generation":
            ready

    }


# ============================================================
# PRINT COMPILER REPORT
# ============================================================
#
# This is intentionally terminal-based.
#
# The Master-DOC Generator explicitly defines terminal output
# and disables popup reports.
# ============================================================

def print_compiler_report(
    compiler_state
):

    print()

    print(
        "=" * 70
    )

    print(
        "NEURAL PIPELINE COMPILER"
    )

    print(
        "=" * 70
    )

    print()

    print(
        f"Status: "
        f"{compiler_state.get('status')}"
    )

    print()


    # --------------------------------------------------------
    # MASTER-DOC STATUS
    # --------------------------------------------------------

    print(
        "Master-DOCs loaded:"
    )

    print(
        f"  "
        f"{len(compiler_state.get('master_docs', {}))}"
    )

    print()


    # --------------------------------------------------------
    # REQUEST
    # --------------------------------------------------------

    request = (
        compiler_state.get(
            "request",
            {}
        )
    )

    print(
        "Normalized request:"
    )

    for key, value in request.items():

        print(
            f"  {key}: {value}"
        )

    print()


    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    validation = (
        compiler_state.get(
            "validation"
        )
    )

    if validation is not None:

        print(
            "Validation:"
        )

        print(
            f"  Valid: "
            f"{validation.get('valid')}"
        )

        print(
            f"  Message: "
            f"{validation.get('message')}"
        )

        for error in validation.get(
            "errors",
            []
        ):

            print(
                f"  ERROR: {error}"
            )

        print()


    # --------------------------------------------------------
    # SPECIFICATION
    # --------------------------------------------------------

    specification = (
        compiler_state.get(
            "specification"
        )
    )

    if specification is not None:

        print(
            "Pipeline stages:"
        )

        for number, stage in enumerate(
            specification.get(
                "stages",
                []
            ),
            start=1
        ):

            print(
                f"  {number}. {stage}"
            )

        print()


        print(
            "Data connections:"
        )

        for connection in specification.get(
            "connections",
            []
        ):

            print(
                f"  "
                f"{connection.get('from')}"
                f" -> "
                f"{connection.get('to')}"
            )

        print()


    # --------------------------------------------------------
    # SAFETY
    # --------------------------------------------------------

    safety = (
        compiler_state.get(
            "safety"
        )
    )

    if safety is not None:

        print(
            "Generator safety:"
        )

        print(
            f"  Safe: "
            f"{safety.get('safe')}"
        )

        for error in safety.get(
            "errors",
            []
        ):

            print(
                f"  ERROR: {error}"
            )

        print()


    # --------------------------------------------------------
    # GENERATION READINESS
    # --------------------------------------------------------

    print(
        "Ready for source generation:"
    )

    print(
        f"  "
        f"{compiler_state.get('ready_for_generation')}"
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
# verifies the complete compilation layer independently.
#
# It uses a test parameter object.
#
# In the real application, Ingestion.py calls:
#
#     analyze(parameters)
#
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # TEST PARAMETER OBJECT
    # --------------------------------------------------------
    #
    # This mirrors the parameter structure already defined
    # by the Generator Master-DOC.
    # --------------------------------------------------------

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
                "notch_filter"
            ],

        "statistics":
            [
                "mean",
                "std",
                "variance",
                "rms",
                "spectral_power",
                "dominant_frequency"
            ],

        "features":
            [],

        "target_type":
            None,

        "decoder":
            None,

        "visualization":
            False

    }


    # --------------------------------------------------------
    # RUN ANALYSIS / COMPILATION
    # --------------------------------------------------------

    compiler_state = analyze(
        test_parameters
    )


    # --------------------------------------------------------
    # DISPLAY RESULT
    # --------------------------------------------------------

    print_compiler_report(
        compiler_state
    )

