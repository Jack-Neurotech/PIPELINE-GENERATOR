
# ============================================================
# PIPELINE GENERATOR
# ============================================================
#
# generator.py is the construction layer of the
# Neural Analysis Pipeline Generator.
#
# analysis.py produces a generation specification.
#
# generator.py:
#
#     1. receives the specification
#     2. loads the Master-DOC library
#     3. identifies the requested pipeline components
#     4. resolves those components against the Master-DOCs
#     5. retrieves the actual reusable functions/resources
#     6. returns the resolved raw materials
#
# THIS VERSION DOES NOT YET GENERATE THE FINAL PIPELINE.
#
# The purpose of this stage is to prove:
#
#     analysis.py
#          |
#          v
#     generation specification
#          |
#          v
#     generator.py
#          |
#          v
#     actual Master-DOC resources
#
# Scientific algorithms remain inside the Master-DOCs.
# generator.py does not invent them.
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
# MASTER-DOC ROLE PATTERNS
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
# RESOURCE ALIASES
# ============================================================
#
# The user-facing parameter object may use a logical name
# that differs slightly from the canonical Master-DOC name.
#
# Aliases are handled here.
#
# The actual implementation remains in the Master-DOC.
# ============================================================

RESOURCE_ALIASES = {

    "bandpass_filter":
        "band_pass_filter",

    "band-pass-filter":
        "band_pass_filter",

    "notch_filter":
        "notch_filter",

    "spectral-power":
        "spectral_power",

    "dominant-frequency":
        "dominant_frequency",

    "spectral-entropy":
        "spectral_entropy",

    "peak-alpha-frequency":
        "peak_alpha_frequency",

    "spectral-edge":
        "spectral_edge",

    "band-power-ratios":
        "band_power_ratios"

}


# ============================================================
# NORMALIZE NAME
# ============================================================

def normalize_name(
    value: Any
) -> str:

    if value is None:

        return ""

    return (
        str(value)
        .strip()
        .lower()
        .replace("-", "_")
        .replace(" ", "_")
    )


# ============================================================
# APPLY RESOURCE ALIAS
# ============================================================

def canonical_resource_name(
    value: Any
) -> str:

    normalized = normalize_name(
        value
    )

    return RESOURCE_ALIASES.get(
        normalized,
        normalized
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
# LOAD MASTER-DOC LIBRARY
# ============================================================

def load_master_docs():

    loaded = {}

    errors = {}

    for document_path in discover_master_docs():

        try:

            loaded[
                document_path.name
            ] = load_master_doc(
                document_path
            )

        except Exception as error:

            errors[
                document_path.name
            ] = error

    return {
        "loaded": loaded,
        "errors": errors
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
            Path(document_name)
            .stem
            .lower()
            .replace("_", "-")
            .replace(" ", "-")
        )

        matched_role = None

        for role, patterns in (
            MASTER_DOC_ROLE_PATTERNS.items()
        ):

            for pattern in patterns:

                if (
                    normalized_name == pattern
                    or
                    normalized_name.startswith(pattern)
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
# FIND FUNCTION
# ============================================================

def find_function(
    module: ModuleType,
    function_name: str
):

    function = getattr(
        module,
        function_name,
        None
    )

    if callable(function):

        return function

    return None


# ============================================================
# FIND RESOURCE REGISTRY
# ============================================================
#
# Master-DOCs may expose resources through registries.
#
# This function searches common registry names without
# replacing the Master-DOC's own architecture.
# ============================================================

def find_registry(
    module: ModuleType
):

    registry_names = (

        "INGESTION_RESOURCES",

        "PREPROCESSING_RESOURCES",

        "STATISTICAL_RESOURCES",

        "STATISTICS_RESOURCES",

        "DECODING_RESOURCES",

        "VISUALIZATION_RESOURCES",

        "SIGNAL_ANALYSIS_RESOURCES",

        "RESOURCE_REGISTRY",

        "RESOURCES",

        "REGISTRY"

    )

    for registry_name in registry_names:

        registry = getattr(
            module,
            registry_name,
            None
        )

        if isinstance(
            registry,
            dict
        ):

            return registry

    return None


# ============================================================
# RESOLVE RESOURCE THROUGH MASTER-DOC
# ============================================================
#
# We first look for the Master-DOC's explicit resource
# accessor.
#
# This is preferable to directly reaching into internal
# implementation details.
# ============================================================

def resolve_resource(
    module: ModuleType,
    resource_name: str
):

    canonical_name = (
        canonical_resource_name(
            resource_name
        )
    )

    # --------------------------------------------------------
    # EXPLICIT RESOURCE ACCESSORS
    # --------------------------------------------------------

    accessor_names = (

        "get_ingestion_resource",

        "get_preprocessing_resource",

        "get_statistical_resource",

        "get_statistics_resource",

        "get_decoding_resource",

        "get_visualization_resource",

        "get_signal_analysis_resource",

        "get_resource"

    )

    for accessor_name in accessor_names:

        accessor = getattr(
            module,
            accessor_name,
            None
        )

        if not callable(accessor):

            continue

        try:

            result = accessor(
                canonical_name
            )

            if result is not None:

                return {
                    "name":
                        canonical_name,

                    "resource":
                        result,

                    "source":
                        module.__name__,

                    "accessor":
                        accessor_name
                }

        except TypeError:

            # ------------------------------------------------
            # Some accessors require additional information
            # such as modality.
            #
            # The registry resolution below may still work.
            # ------------------------------------------------

            continue

    # --------------------------------------------------------
    # RESOURCE REGISTRY
    # --------------------------------------------------------

    registry = find_registry(
        module
    )

    if registry is not None:

        # Direct lookup.

        if canonical_name in registry:

            return {
                "name":
                    canonical_name,

                "resource":
                    registry[
                        canonical_name
                    ],

                "source":
                    module.__name__,

                "accessor":
                    "registry"
            }

        # Normalized lookup.

        for key, value in registry.items():

            if (
                canonical_resource_name(key)
                ==
                canonical_name
            ):

                return {
                    "name":
                        canonical_name,

                    "resource":
                        value,

                    "source":
                        module.__name__,

                    "accessor":
                        "registry"
                }

    # --------------------------------------------------------
    # DIRECT FUNCTION LOOKUP
    # --------------------------------------------------------

    direct_function = find_function(
        module,
        canonical_name
    )

    if direct_function is not None:

        return {
            "name":
                canonical_name,

            "resource":
                direct_function,

            "source":
                module.__name__,

            "accessor":
                "direct_function"
        }

    return None


# ============================================================
# RESOURCE REQUEST EXTRACTION
# ============================================================
#
# Extract the logical resources requested by the generation
# specification.
#
# The specification may contain lists, dictionaries, or
# nested resource objects.
# ============================================================

def extract_requested_resources(
    specification
):

    requested = {

        "ingestion":
            [],

        "preprocessing":
            [],

        "statistics":
            [],

        "decoding":
            [],

        "visualization":
            [],

        "signal_analysis":
            [],

        "output":
            []

    }

    if not isinstance(
        specification,
        dict
    ):

        return requested

    # --------------------------------------------------------
    # DIRECT COMPONENT FIELDS
    # --------------------------------------------------------

    field_role_map = {

        "ingestion":
            "ingestion",

        "preprocessing":
            "preprocessing",

        "statistics":
            "statistics",

        "features":
            "statistics",

        "decoding":
            "decoding",

        "decoder":
            "decoding",

        "visualization":
            "visualization",

        "signal_analysis":
            "signal_analysis",

        "output":
            "output"

    }

    for field_name, role in (
        field_role_map.items()
    ):

        value = specification.get(
            field_name
        )

        if value is None:

            continue

        if isinstance(
            value,
            (list, tuple, set)
        ):

            requested[
                role
            ].extend(
                value
            )

        else:

            requested[
                role
            ].append(
                value
            )

    return requested


# ============================================================
# RESOLVE RAW MATERIALS
# ============================================================
#
# THIS IS THE FIRST REAL GENERATOR OPERATION.
#
# The generation specification tells us WHAT is needed.
#
# The Master-DOCs tell us WHERE the implementation lives.
#
# This function connects those two worlds.
# ============================================================

def resolve_raw_materials(
    generation_specification
):

    # --------------------------------------------------------
    # LOAD LIBRARY
    # --------------------------------------------------------

    master_doc_state = (
        load_master_docs()
    )

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

    # --------------------------------------------------------
    # IDENTIFY ROLES
    # --------------------------------------------------------

    role_state = (
        identify_master_doc_roles(
            loaded_docs
        )
    )

    roles = (
        role_state[
            "roles"
        ]
    )

    # --------------------------------------------------------
    # EXTRACT REQUESTS
    # --------------------------------------------------------

    requested = (
        extract_requested_resources(
            generation_specification
        )
    )

    # --------------------------------------------------------
    # RESOLUTION RESULT
    # --------------------------------------------------------

    resolved = {

        "ingestion":
            [],

        "preprocessing":
            [],

        "statistics":
            [],

        "decoding":
            [],

        "visualization":
            [],

        "signal_analysis":
            [],

        "output":
            []

    }

    unresolved = []

    # --------------------------------------------------------
    # RESOLVE EACH REQUESTED RESOURCE
    # --------------------------------------------------------

    for role, resource_names in (
        requested.items()
    ):

        if not resource_names:

            continue

        module = roles.get(
            role
        )

        if module is None:

            for resource_name in resource_names:

                unresolved.append({

                    "role":
                        role,

                    "name":
                        resource_name,

                    "reason":
                        "Master-DOC role unavailable"

                })

            continue

        for resource_name in resource_names:

            # --------------------------------------------
            # Ignore empty configuration values.
            # --------------------------------------------

            if resource_name in (
                None,
                "",
                False
            ):

                continue

            # --------------------------------------------
            # Resource may already be a callable.
            # --------------------------------------------

            if callable(
                resource_name
            ):

                resolved[
                    role
                ].append({

                    "name":
                        getattr(
                            resource_name,
                            "__name__",
                            str(
                                resource_name
                            )
                        ),

                    "resource":
                        resource_name,

                    "source":
                        module.__name__,

                    "accessor":
                        "provided_callable"

                })

                continue

            # --------------------------------------------
            # Resolve through Master-DOC.
            # --------------------------------------------

            resource = resolve_resource(
                module,
                resource_name
            )

            if resource is None:

                unresolved.append({

                    "role":
                        role,

                    "name":
                        resource_name,

                    "reason":
                        (
                            "Resource was not found "
                            "in the corresponding "
                            "Master-DOC."
                        )

                })

                continue

            resolved[
                role
            ].append(
                resource
            )

    # --------------------------------------------------------
    # RETURN RESOURCE PACKAGE
    # --------------------------------------------------------

    return {

        "status":
            (
                "RESOLVED"
                if not unresolved
                else "PARTIAL"
            ),

        "specification":
            generation_specification,

        "requested":
            requested,

        "resolved":
            resolved,

        "unresolved":
            unresolved,

        "master_docs":
            loaded_docs,

        "master_doc_roles":
            roles,

        "load_errors":
            load_errors

    }


# ============================================================
# GENERATOR ENTRY POINT
# ============================================================
#
# This is the function analysis.py hands its object to.
#
# At this stage the generator:
#
#     receives
#     resolves
#     reports
#
# It does NOT yet generate source code.
# ============================================================

def generate(
    generation_specification
):

    if generation_specification is None:

        raise ValueError(
            "Generator received no generation specification."
        )

    result = resolve_raw_materials(
        generation_specification
    )

    return result


# ============================================================
# GENERATOR REPORT
# ============================================================

def print_generator_report(
    result
):

    print()

    print(
        "=" * 70
    )

    print(
        "PIPELINE GENERATOR"
    )

    print(
        "=" * 70
    )

    print(
        "RAW MATERIAL RESOLUTION"
    )

    print(
        "=" * 70
    )

    print()

    print(
        f"Status: "
        f"{result.get('status')}"
    )

    print()

    # --------------------------------------------------------
    # REQUESTED
    # --------------------------------------------------------

    print(
        "Requested resources:"
    )

    requested = (
        result.get(
            "requested",
            {}
        )
    )

    for role, resources in (
        requested.items()
    ):

        if not resources:

            continue

        print(
            f"  {role}:"
        )

        for resource in resources:

            print(
                f"    - {resource}"
            )

    print()

    # --------------------------------------------------------
    # RESOLVED
    # --------------------------------------------------------

    print(
        "Resolved resources:"
    )

    resolved = (
        result.get(
            "resolved",
            {}
        )
    )

    for role, resources in (
        resolved.items()
    ):

        if not resources:

            continue

        print(
            f"  {role}:"
        )

        for resource in resources:

            print(
                f"    - {resource.get('name')}"
                f" "
                f"[{resource.get('source')}]"
            )

    print()

    # --------------------------------------------------------
    # UNRESOLVED
    # --------------------------------------------------------

    unresolved = (
        result.get(
            "unresolved",
            []
        )
    )

    if unresolved:

        print(
            "Unresolved resources:"
        )

        for item in unresolved:

            print(
                f"  - "
                f"{item.get('role')}: "
                f"{item.get('name')} "
                f"-> "
                f"{item.get('reason')}"
            )

    else:

        print(
            "Unresolved resources: NONE"
        )

    print()

    print(
        "=" * 70
    )


# ============================================================
# DIRECT TEST
# ============================================================
#
# This allows:
#
#     python generator.py
#
# to test the generator independently.
#
# In the actual application:
#
#     analysis.py
#          |
#          v
#     generate(specification)
#
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # TEST SPECIFICATION
    # --------------------------------------------------------
    #
    # This represents the type of specification that
    # analysis.py hands to the generator.
    # --------------------------------------------------------

    test_generation_specification = {

        "neural_data":
            "EEG",

        "file_type":
            ".edf",

        "pipeline_type":
            "EEG",

        "ingestion":
            [
                "EEG"
            ],

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

        "decoder":
            None,

        "visualization":
            False,

        "output":
            []

    }


    # --------------------------------------------------------
    # RUN GENERATOR
    # --------------------------------------------------------

    generator_result = generate(
        test_generation_specification
    )


    # --------------------------------------------------------
    # DISPLAY RESULT
    # --------------------------------------------------------

    print_generator_report(
        generator_result
    )
