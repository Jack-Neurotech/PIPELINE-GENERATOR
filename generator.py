
# ============================================================
# PIPELINE GENERATOR
# ============================================================
#
# generator.py receives the validated generation specification
# from analysis.py and resolves that specification into the
# ACTUAL reusable resources contained in the Master-DOCs.
#
# The architecture is:
#
#     Ingestion.py
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
#          +----> Master-DOC-Ingestion
#          +----> Master-DOC-Preprocessing
#          +----> Master-DOC-Stats
#          +----> Master-DOC-Decoding
#          +----> Master-DOC-Visualization
#          +----> Master-DOC-Output
#          |
#          v
#     resolved raw materials
#
# IMPORTANT:
#
# generator.py does NOT invent scientific algorithms.
#
# The actual scientific implementations remain inside the
# Master-DOCs.
#
# generator.py determines WHICH Master-DOC resource belongs
# to each requested parameter.
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
# PARAMETER → MASTER-DOC FUNCTION MAPPINGS
# ============================================================
#
# These mappings connect the logical parameter names used by
# the generation specification to the ACTUAL functions inside
# the Master-DOCs.
#
# We do not recreate those functions here.
#
# We only tell the generator where to look.
# ============================================================

PREPROCESSING_FUNCTIONS = {

    "bandpass_filter":
        "band_pass_filter",

    "band_pass_filter":
        "band_pass_filter",

    "notch_filter":
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

    "remove_invalid_samples":
        "remove_invalid_samples",

    "remove_dc_offset":
        "remove_dc_offset",

    "detrend":
        "detrend_signal",

    "detrend_signal":
        "detrend_signal",

    "baseline_correction":
        "baseline_correct",

    "baseline_correct":
        "baseline_correct",

    "resample":
        "resample_signal",

    "resample_signal":
        "resample_signal",

    "common_average_reference":
        "common_average_reference",

    "select_channels":
        "select_channels"

}


STATISTICS_FUNCTIONS = {

    "mean":
        "calculate_mean",

    "median":
        "calculate_median",

    "mode":
        "calculate_mode",

    "minimum":
        "calculate_minimum",

    "min":
        "calculate_minimum",

    "maximum":
        "calculate_maximum",

    "max":
        "calculate_maximum",

    "range":
        "calculate_range",

    "variance":
        "calculate_variance",

    "std":
        "calculate_standard_deviation",

    "standard_deviation":
        "calculate_standard_deviation",

    "standard_error":
        "calculate_standard_error",

    "rms":
        "calculate_rms",

    "coefficient_of_variation":
        "calculate_coefficient_of_variation",

    "skewness":
        "calculate_skewness",

    "kurtosis":
        "calculate_kurtosis",

    "shapiro_wilk":
        "shapiro_wilk_test",

    "kolmogorov_smirnov":
        "kolmogorov_smirnov_test",

    "independent_t_test":
        "independent_t_test",

    "paired_t_test":
        "paired_t_test",

    "one_way_anova":
        "one_way_anova",

    "repeated_measures_anova":
        "repeated_measures_anova",

    "mann_whitney_u":
        "mann_whitney_u",

    "wilcoxon_signed_rank":
        "wilcoxon_signed_rank"

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
# CANONICAL PREPROCESSING NAME
# ============================================================

def canonical_preprocessing_name(
    value
):

    normalized = normalize_name(
        value
    )

    return PREPROCESSING_FUNCTIONS.get(
        normalized,
        normalized
    )


# ============================================================
# CANONICAL STATISTICS NAME
# ============================================================

def canonical_statistics_name(
    value
):

    normalized = normalize_name(
        value
    )

    return STATISTICS_FUNCTIONS.get(
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

        key=lambda path:
            path.name.lower()

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

    specification = (
        importlib.util.spec_from_loader(
            module_name,
            loader
        )
    )

    if specification is None:

        raise ImportError(
            "Unable to create module specification for "
            f"{document_path.name}"
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
# LOAD MASTER-DOC LIBRARY
# ============================================================

def load_master_docs():

    loaded = {}

    errors = {}

    for document_path in (
        discover_master_docs()
    ):

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

        "loaded":
            loaded,

        "errors":
            errors

    }


# ============================================================
# IDENTIFY MASTER-DOC ROLES
# ============================================================

def identify_master_doc_roles(
    loaded_docs
):

    roles = {}

    unmatched = {}

    for document_name, module in (
        loaded_docs.items()
    ):

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

        "roles":
            roles,

        "unmatched":
            unmatched

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
# RESOLVE FUNCTION
# ============================================================

def resolve_function(
    module,
    requested_name,
    canonical_name
):

    function = find_function(
        module,
        canonical_name
    )

    if function is None:

        return None

    return {

        "requested_name":
            requested_name,

        "resolved_name":
            canonical_name,

        "resource":
            function,

        "source":
            module.__name__,

        "type":
            "function"

    }


# ============================================================
# FIND DICTIONARY RESOURCES
# ============================================================
#
# Master-DOCs use dictionaries heavily for raw-material
# specifications.
#
# We inspect module-level dictionaries for matching resources.
# ============================================================

def find_dictionary_resource(
    module,
    requested_name
):

    normalized_requested = normalize_name(
        requested_name
    )

    for attribute_name in dir(
        module
    ):

        if attribute_name.startswith("_"):

            continue

        try:

            value = getattr(
                module,
                attribute_name
            )

        except Exception:

            continue

        if not isinstance(
            value,
            dict
        ):

            continue

        # ----------------------------------------------------
        # Direct key.
        # ----------------------------------------------------

        for key in value.keys():

            if normalize_name(
                key
            ) == normalized_requested:

                return {

                    "requested_name":
                        requested_name,

                    "resolved_name":
                        key,

                    "resource":
                        value[key],

                    "source":
                        module.__name__,

                    "container":
                        attribute_name,

                    "type":
                        "dictionary_resource"

                }

        # ----------------------------------------------------
        # Nested resource.
        # ----------------------------------------------------

        for key, item in (
            value.items()
        ):

            if not isinstance(
                item,
                dict
            ):

                continue

            resource_id = item.get(
                "id"
            )

            if resource_id is not None:

                if normalize_name(
                    resource_id
                ) == normalized_requested:

                    return {

                        "requested_name":
                            requested_name,

                        "resolved_name":
                            resource_id,

                        "resource":
                            item,

                        "source":
                            module.__name__,

                        "container":
                            attribute_name,

                        "type":
                            "dictionary_resource"

                    }

    return None


# ============================================================
# RESOLVE INGESTION RESOURCE
# ============================================================
#
# Ingestion is different from preprocessing/statistics.
#
# "EEG" is not itself a function.
#
# The ingestion resource is selected from:
#
#     neural_data + file_type
#
# The Master-DOC explicitly defines ingestion combinations.
# ============================================================

def resolve_ingestion_resource(
    module,
    specification
):

    neural_data = (
        specification.get(
            "neural_data"
        )
    )

    file_type = (
        specification.get(
            "file_type"
        )
    )

    if neural_data is None:

        return None, {

            "reason":
                "neural_data was not provided."

        }

    if file_type is None:

        return None, {

            "reason":
                "file_type was not provided."

        }

    neural_data_normalized = normalize_name(
        neural_data
    )

    file_type_normalized = normalize_name(
        file_type
    )

    # --------------------------------------------------------
    # Direct tuple-key lookup.
    # --------------------------------------------------------

    for attribute_name in dir(
        module
    ):

        if attribute_name.startswith("_"):

            continue

        try:

            value = getattr(
                module,
                attribute_name
            )

        except Exception:

            continue

        if not isinstance(
            value,
            dict
        ):

            continue

        for key, resource in (
            value.items()
        ):

            if not isinstance(
                key,
                tuple
            ):

                continue

            if len(key) != 2:

                continue

            key_modality = normalize_name(
                key[0]
            )

            key_file_type = normalize_name(
                key[1]
            )

            if (
                key_modality ==
                neural_data_normalized
                and
                key_file_type ==
                file_type_normalized
            ):

                return {

                    "requested_name":
                        f"{neural_data}/{file_type}",

                    "resolved_name":
                        resource.get(
                            "id",
                            f"{neural_data}/{file_type}"
                        )
                        if isinstance(
                            resource,
                            dict
                        )
                        else
                        f"{neural_data}/{file_type}",

                    "resource":
                        resource,

                    "source":
                        module.__name__,

                    "container":
                        attribute_name,

                    "type":
                        "ingestion_resource"

                }, None

    # --------------------------------------------------------
    # Search dictionaries for resource metadata.
    # --------------------------------------------------------

    for attribute_name in dir(
        module
    ):

        if attribute_name.startswith("_"):

            continue

        try:

            value = getattr(
                module,
                attribute_name
            )

        except Exception:

            continue

        if not isinstance(
            value,
            dict
        ):

            continue

        resource_id = value.get(
            "id"
        )

        modality = value.get(
            "modality"
        )

        resource_file_type = value.get(
            "file_type"
        )

        if (
            resource_id is None
            or modality is None
            or resource_file_type is None
        ):

            continue

        if (
            normalize_name(modality)
            ==
            neural_data_normalized
            and
            normalize_name(resource_file_type)
            ==
            file_type_normalized
        ):

            return {

                "requested_name":
                    f"{neural_data}/{file_type}",

                "resolved_name":
                    resource_id,

                "resource":
                    value,

                "source":
                    module.__name__,

                "container":
                    attribute_name,

                "type":
                    "ingestion_resource"

            }, None

    return None, {

        "reason":
            (
                "No ingestion resource exists for "
                f"{neural_data}/{file_type} "
                "in the Ingestion Master-DOC."
            )

    }


# ============================================================
# EXTRACT REQUESTED RESOURCES
# ============================================================

def extract_requested_resources(
    specification
):

    requested = {

        "preprocessing":
            [],

        "statistics":
            [],

        "decoding":
            [],

        "visualization":
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
    # PREPROCESSING
    # --------------------------------------------------------

    preprocessing = specification.get(
        "preprocessing",
        []
    )

    if isinstance(
        preprocessing,
        str
    ):

        preprocessing = [
            preprocessing
        ]

    requested[
        "preprocessing"
    ].extend(
        preprocessing or []
    )

    # --------------------------------------------------------
    # STATISTICS
    # --------------------------------------------------------

    statistics = specification.get(
        "statistics",
        []
    )

    if isinstance(
        statistics,
        str
    ):

        statistics = [
            statistics
        ]

    requested[
        "statistics"
    ].extend(
        statistics or []
    )

    # --------------------------------------------------------
    # DECODING
    # --------------------------------------------------------

    decoder = specification.get(
        "decoder"
    )

    if decoder not in (
        None,
        "",
        False
    ):

        requested[
            "decoding"
        ].append(
            decoder
        )

    features = specification.get(
        "features",
        []
    )

    if isinstance(
        features,
        str
    ):

        features = [
            features
        ]

    requested[
        "decoding"
    ].extend(
        features or []
    )

    # --------------------------------------------------------
    # VISUALIZATION
    # --------------------------------------------------------

    visualization = specification.get(
        "visualization"
    )

    if visualization not in (
        None,
        "",
        False
    ):

        if isinstance(
            visualization,
            str
        ):

            requested[
                "visualization"
            ].append(
                visualization
            )

        else:

            requested[
                "visualization"
            ].append(
                True
            )

    return requested


# ============================================================
# RESOLVE STANDARD COMPONENT
# ============================================================

def resolve_standard_component(
    module,
    requested_name,
    role
):

    if role == "preprocessing":

        canonical_name = (
            canonical_preprocessing_name(
                requested_name
            )
        )

    elif role == "statistics":

        canonical_name = (
            canonical_statistics_name(
                requested_name
            )
        )

    else:

        canonical_name = normalize_name(
            requested_name
        )

    # --------------------------------------------------------
    # First: direct function lookup.
    # --------------------------------------------------------

    function_result = resolve_function(
        module,
        requested_name,
        canonical_name
    )

    if function_result is not None:

        return function_result

    # --------------------------------------------------------
    # Second: dictionary resource lookup.
    # --------------------------------------------------------

    dictionary_result = (
        find_dictionary_resource(
            module,
            canonical_name
        )
    )

    if dictionary_result is not None:

        return dictionary_result

    return None


# ============================================================
# RESOLVE RAW MATERIALS
# ============================================================

def resolve_raw_materials(
    generation_specification
):

    if not isinstance(
        generation_specification,
        dict
    ):

        raise TypeError(
            "generation_specification must be a dictionary."
        )

    # --------------------------------------------------------
    # LOAD MASTER-DOC LIBRARY
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
    # RESULT OBJECT
    # --------------------------------------------------------

    result = {

        "status":
            "RESOLVING",

        "specification":
            generation_specification,

        "resolved":
            {

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

                "output":
                    []

            },

        "unresolved":
            [],

        "master_doc_roles":
            roles,

        "load_errors":
            load_errors

    }

    # ========================================================
    # INGESTION
    # ========================================================

    ingestion_module = roles.get(
        "ingestion"
    )

    if ingestion_module is None:

        result[
            "unresolved"
        ].append({

            "role":
                "ingestion",

            "reason":
                "Ingestion Master-DOC unavailable."

        })

    else:

        resource, error = (
            resolve_ingestion_resource(
                ingestion_module,
                generation_specification
            )
        )

        if resource is not None:

            result[
                "resolved"
            ][
                "ingestion"
            ].append(
                resource
            )

        else:

            result[
                "unresolved"
            ].append({

                "role":
                    "ingestion",

                "requested":
                    (
                        f"{generation_specification.get('neural_data')}"
                        f"/"
                        f"{generation_specification.get('file_type')}"
                    ),

                "reason":
                    error.get(
                        "reason"
                    )

            })

    # ========================================================
    # STANDARD COMPONENTS
    # ========================================================

    requested = (
        extract_requested_resources(
            generation_specification
        )
    )

    role_to_module = {

        "preprocessing":
            "preprocessing",

        "statistics":
            "statistics",

        "decoding":
            "decoding",

        "visualization":
            "visualization",

        "output":
            "output"

    }

    for role, resource_names in (
        requested.items()
    ):

        if not resource_names:

            continue

        module = roles.get(
            role_to_module.get(
                role,
                role
            )
        )

        if module is None:

            for resource_name in resource_names:

                result[
                    "unresolved"
                ].append({

                    "role":
                        role,

                    "requested":
                        resource_name,

                    "reason":
                        "Master-DOC role unavailable."

                })

            continue

        for resource_name in resource_names:

            if resource_name in (
                None,
                "",
                False
            ):

                continue

            resolved = (
                resolve_standard_component(
                    module,
                    resource_name,
                    role
                )
            )

            if resolved is None:

                result[
                    "unresolved"
                ].append({

                    "role":
                        role,

                    "requested":
                        resource_name,

                    "reason":
                        (
                            "No matching function or "
                            "resource was found in "
                            f"{module.__name__}."
                        )

                })

            else:

                result[
                    "resolved"
                ][
                    role
                ].append(
                    resolved
                )

    # ========================================================
    # FINAL STATUS
    # ========================================================

    if result[
        "unresolved"
    ]:

        result[
            "status"
        ] = "PARTIAL"

    else:

        result[
            "status"
        ] = "RESOLVED"

    return result


# ============================================================
# GENERATOR ENTRY POINT
# ============================================================

def generate(
    generation_specification
):

    if generation_specification is None:

        raise ValueError(
            "Generator received no generation specification."
        )

    return resolve_raw_materials(
        generation_specification
    )


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
        "MASTER-DOC RAW MATERIAL RESOLUTION"
    )

    print(
        "=" * 70
    )

    print()

    print(
        f"Status: {result.get('status')}"
    )

    print()

    # --------------------------------------------------------
    # RESOLVED
    # --------------------------------------------------------

    print(
        "RESOLVED:"
    )

    resolved = result.get(
        "resolved",
        {}
    )

    any_resolved = False

    for role, resources in (
        resolved.items()
    ):

        if not resources:

            continue

        any_resolved = True

        print()

        print(
            f"  {role}:"
        )

        for resource in resources:

            print(
                f"    requested: "
                f"{resource.get('requested_name')}"
            )

            print(
                f"    resolved:   "
                f"{resource.get('resolved_name')}"
            )

            print(
                f"    source:     "
                f"{resource.get('source')}"
            )

            print(
                f"    type:       "
                f"{resource.get('type')}"
            )

    if not any_resolved:

        print(
            "  NONE"
        )

    print()

    # --------------------------------------------------------
    # UNRESOLVED
    # --------------------------------------------------------

    print(
        "UNRESOLVED:"
    )

    unresolved = result.get(
        "unresolved",
        []
    )

    if not unresolved:

        print(
            "  NONE"
        )

    else:

        for item in unresolved:

            print(
                f"  role:      "
                f"{item.get('role')}"
            )

            if item.get(
                "requested"
            ) is not None:

                print(
                    f"  requested: "
                    f"{item.get('requested')}"
                )

            print(
                f"  reason:    "
                f"{item.get('reason')}"
            )

            print()

    # --------------------------------------------------------
    # MASTER-DOC LOAD ERRORS
    # --------------------------------------------------------

    load_errors = result.get(
        "load_errors",
        {}
    )

    if load_errors:

        print(
            "MASTER-DOC LOAD ERRORS:"
        )

        for name, error in (
            load_errors.items()
        ):

            print(
                f"  {name}: "
                f"{type(error).__name__}: "
                f"{error}"
            )

        print()

    print(
        "=" * 70
    )


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    test_generation_specification = {

        "neural_data":
            "EEG",

        "file_type":
            ".set",

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

        "decoder":
            None,

        "target_type":
            None,

        "visualization":
            False

    }

    result = generate(
        test_generation_specification
    )

    print_generator_report(
        result
    )

