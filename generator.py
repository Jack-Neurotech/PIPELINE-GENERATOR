
# ============================================================
# PIPELINE GENERATOR
# ============================================================
#
# generator.py is the raw-material resolution and pipeline
# compilation layer.
#
# The architecture is:
#
#     analysis.py
#          |
#          v
#     generation specification
#          |
#          v
#     generator.py
#          |
#          +----> Master-DOC Ingestion
#          +----> Master-DOC Preprocessing
#          +----> Master-DOC Stats
#          +----> Master-DOC Signal Analysis
#          +----> Master-DOC Decoding
#          +----> Master-DOC Visualization
#          +----> Master-DOC Output
#          |
#          v
#     resolved raw materials
#          |
#          v
#     future source-code compilation
#
# IMPORTANT:
#
# generator.py does NOT invent scientific algorithms.
#
# It resolves requested resources against the Master-DOC
# library and prepares those resources for later compilation.
# ============================================================


# ============================================================
# IMPORTS
# ============================================================

from pathlib import Path
import importlib.util
from importlib.machinery import SourceFileLoader
from types import ModuleType


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
    ),
}


# ============================================================
# PARAMETER → MASTER-DOC FUNCTION MAPPINGS
# ============================================================
#
# These mappings translate the logical names used by the
# parameter object into the actual function names contained
# in the Master-DOCs.
# ============================================================


# ============================================================
# PREPROCESSING
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
        "select_channels",
}


# ============================================================
# STATISTICS
# ============================================================

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
        "wilcoxon_signed_rank",
}


# ============================================================
# SIGNAL ANALYSIS
# ============================================================
#
# Spectral/frequency-domain operations belong to the Signal
# Analysis Master-DOC rather than the Statistics Master-DOC.
# ============================================================

SIGNAL_ANALYSIS_FUNCTIONS = {

    "spectral_power":
        "calculate_power_spectral_density",

    "power_spectral_density":
        "calculate_power_spectral_density",

    "total_spectral_power":
        "calculate_total_spectral_power",

    "band_power":
        "calculate_band_power",

    "relative_band_power":
        "calculate_relative_band_power",

    "dominant_frequency":
        "calculate_dominant_frequency",

    "peak_frequency":
        "calculate_peak_frequency",

    "spectral_entropy":
        "calculate_spectral_entropy",

    "spectral_edge":
        "calculate_spectral_edge_frequency",

    "spectral_edge_frequency":
        "calculate_spectral_edge_frequency",
}


# ============================================================
# SIGNAL ANALYSIS REQUEST NAMES
# ============================================================

SIGNAL_ANALYSIS_REQUESTS = {

    "spectral_power",

    "power_spectral_density",

    "total_spectral_power",

    "band_power",

    "relative_band_power",

    "dominant_frequency",

    "peak_frequency",

    "spectral_entropy",

    "spectral_edge",

    "spectral_edge_frequency",
}


# ============================================================
# NORMALIZE NAME
# ============================================================

def normalize_name(
    value
):

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
# NORMALIZE FILE TYPE
# ============================================================
#
# The ingestion Master-DOC may identify a format logically:
#
#     EEGLAB
#
# while the parameter object may provide its physical
# extension:
#
#     .set
#
# These two identifiers therefore need to resolve to the same
# ingestion resource.
# ============================================================

def normalize_file_type(
    file_type
):

    if file_type is None:

        return ""

    value = (
        str(file_type)
        .strip()
        .lower()
    )

    aliases = {

        ".set":
            "eeglab",

        "set":
            "eeglab",

        "eeglab":
            "eeglab",

        ".edf":
            "edf",

        "edf":
            "edf",

        ".csv":
            "csv",

        "csv":
            "csv",
    }

    return aliases.get(
        value,
        value
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
            if path.is_file()
            and not path.name.startswith(".")
            and path.suffix.lower() == ".py"
            and "__pycache__" not in path.parts
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
        .replace("'", "")
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

    document_paths = (
        discover_master_docs()
    )

    loaded = {}

    errors = {}

    for document_path in document_paths:

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
        "discovered":
            document_paths,

        "loaded":
            loaded,

        "errors":
            errors,
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

        normalized_name = normalize_name(
            Path(
                document_name
            ).stem
        )

        matched_role = None

        for role, patterns in (
            MASTER_DOC_ROLE_PATTERNS.items()
        ):

            for pattern in patterns:

                normalized_pattern = normalize_name(
                    pattern
                )

                if (
                    normalized_name
                    ==
                    normalized_pattern
                    or
                    normalized_name.startswith(
                        normalized_pattern
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
            unmatched,
    }


# ============================================================
# GET MASTER-DOC ROLE
# ============================================================

def get_master_doc(
    roles,
    role
):

    return roles.get(
        role
    )


# ============================================================
# FIND FUNCTIONS
# ============================================================

def find_function(
    module,
    function_name
):

    if module is None:

        return None

    function = getattr(
        module,
        function_name,
        None
    )

    if callable(function):

        return function

    return None


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
# CANONICAL SIGNAL ANALYSIS NAME
# ============================================================

def canonical_signal_analysis_name(
    value
):

    normalized = normalize_name(
        value
    )

    return SIGNAL_ANALYSIS_FUNCTIONS.get(
        normalized,
        normalized
    )


# ============================================================
# FIND DICTIONARY RESOURCE
# ============================================================
#
# Some Master-DOCs store resources as dictionaries rather than
# functions.
#
# Example:
#
#     EEG_EEGLAB = {
#         ...
#     }
#
# The generator must be able to discover these resources.
# ============================================================

def find_dictionary_resource(
    module,
    requested_name
):

    if module is None:

        return None

    requested_normalized = normalize_name(
        requested_name
    )

    for attribute_name in dir(
        module
    ):

        if attribute_name.startswith(
            "__"
        ):

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

        attribute_normalized = normalize_name(
            attribute_name
        )

        if (
            attribute_normalized
            ==
            requested_normalized
        ):

            return {

                "requested_name":
                    requested_name,

                "resolved_name":
                    attribute_name,

                "resource":
                    value,

                "source":
                    module.__name__,

                "container":
                    attribute_name,

                "type":
                    "dictionary_resource",
            }

        resource_id = value.get(
            "id"
        )

        if (
            resource_id is not None
            and
            normalize_name(
                resource_id
            )
            ==
            requested_normalized
        ):

            return {

                "requested_name":
                    requested_name,

                "resolved_name":
                    resource_id,

                "resource":
                    value,

                "source":
                    module.__name__,

                "container":
                    attribute_name,

                "type":
                    "dictionary_resource",
            }

    return None


# ============================================================
# RESOLVE STANDARD COMPONENT
# ============================================================

def resolve_standard_component(
    module,
    requested_name,
    role
):

    if module is None:

        return None

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

    elif role == "signal_analysis":

        canonical_name = (
            canonical_signal_analysis_name(
                requested_name
            )
        )

    else:

        canonical_name = normalize_name(
            requested_name
        )

    # --------------------------------------------------------
    # TRY CANONICAL FUNCTION
    # --------------------------------------------------------

    function = find_function(
        module,
        canonical_name
    )

    if function is not None:

        return {

            "requested_name":
                requested_name,

            "resolved_name":
                canonical_name,

            "resource":
                function,

            "source":
                module.__name__,

            "container":
                canonical_name,

            "type":
                "function",
        }

    # --------------------------------------------------------
    # TRY ORIGINAL FUNCTION NAME
    # --------------------------------------------------------

    function = find_function(
        module,
        requested_name
    )

    if function is not None:

        return {

            "requested_name":
                requested_name,

            "resolved_name":
                requested_name,

            "resource":
                function,

            "source":
                module.__name__,

            "container":
                requested_name,

            "type":
                "function",
        }

    # --------------------------------------------------------
    # TRY DICTIONARY RESOURCE
    # --------------------------------------------------------

    dictionary_resource = (
        find_dictionary_resource(
            module,
            canonical_name
        )
    )

    if dictionary_resource is not None:

        return dictionary_resource

    return None


# ============================================================
# RESOLVE INGESTION RESOURCE
# ============================================================
#
# Ingestion is different from preprocessing/statistics.
#
# The ingestion Master-DOC contains structured resources.
#
# Example:
#
#     EEG_EEGLAB
#
# with:
#
#     modality = EEG
#     file_type = EEGLAB
#     extensions = [".set"]
#
# Therefore:
#
#     EEG + .set
#
# must resolve to:
#
#     EEG_EEGLAB
# ============================================================

def resolve_ingestion_resource(
    module,
    specification
):

    if module is None:

        return None, {
            "reason":
                "Ingestion Master-DOC is unavailable."
        }

    neural_data = specification.get(
        "neural_data"
    )

    file_type = specification.get(
        "file_type"
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

    requested_file_type = normalize_file_type(
        file_type
    )

    # --------------------------------------------------------
    # SEARCH STRUCTURED MASTER-DOC RESOURCES
    # --------------------------------------------------------

    for attribute_name in dir(
        module
    ):

        if attribute_name.startswith(
            "__"
        ):

            continue

        try:

            resource = getattr(
                module,
                attribute_name
            )

        except Exception:

            continue

        if not isinstance(
            resource,
            dict
        ):

            continue

        modality = resource.get(
            "modality"
        )

        resource_file_type = resource.get(
            "file_type"
        )

        extensions = resource.get(
            "extensions",
            []
        )

        if modality is None:

            continue

        if resource_file_type is None:

            continue

        modality_matches = (
            normalize_name(
                modality
            )
            ==
            neural_data_normalized
        )

        logical_type_matches = (
            normalize_file_type(
                resource_file_type
            )
            ==
            requested_file_type
        )

        extension_matches = any(
            normalize_file_type(
                extension
            )
            ==
            requested_file_type

            for extension in (
                extensions or []
            )
        )

        if (
            modality_matches
            and
            (
                logical_type_matches
                or
                extension_matches
            )
        ):

            return {

                "requested_name":
                    f"{neural_data}/{file_type}",

                "resolved_name":
                    resource.get(
                        "id",
                        attribute_name
                    ),

                "resource":
                    resource,

                "source":
                    module.__name__,

                "container":
                    attribute_name,

                "type":
                    "ingestion_resource",
            }, None

    return None, {

        "reason":
            "Resource was not found in the "
            "corresponding Master-DOC.",

        "neural_data":
            neural_data,

        "file_type":
            file_type,
    }


# ============================================================
# EXTRACT REQUESTED RESOURCES
# ============================================================
#
# The analysis layer may place spectral requests inside the
# statistics collection because the original parameter object
# treats them as requested measurements.
#
# The generator classifies them correctly before resolution.
# ============================================================

def extract_requested_resources(
    specification
):

    requested = {

        "preprocessing":
            [],

        "statistics":
            [],

        "signal_analysis":
            [],

        "decoding":
            [],

        "visualization":
            [],

        "output":
            [],
    }

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

    for statistic in (
        statistics or []
    ):

        normalized_statistic = normalize_name(
            statistic
        )

        if (
            normalized_statistic
            in
            SIGNAL_ANALYSIS_REQUESTS
        ):

            requested[
                "signal_analysis"
            ].append(
                statistic
            )

        else:

            requested[
                "statistics"
            ].append(
                statistic
            )

    # --------------------------------------------------------
    # EXPLICIT SIGNAL ANALYSIS
    # --------------------------------------------------------

    signal_analysis = specification.get(
        "signal_analysis",
        []
    )

    if isinstance(
        signal_analysis,
        str
    ):

        signal_analysis = [
            signal_analysis
        ]

    requested[
        "signal_analysis"
    ].extend(
        signal_analysis or []
    )

    # --------------------------------------------------------
    # DECODING
    # --------------------------------------------------------

    decoding = specification.get(
        "decoder",
        []
    )

    if isinstance(
        decoding,
        str
    ):

        decoding = [
            decoding
        ]

    if decoding:

        requested[
            "decoding"
        ].extend(
            decoding
        )

    # --------------------------------------------------------
    # VISUALIZATION
    # --------------------------------------------------------

    visualization = specification.get(
        "visualization",
        []
    )

    if (
        visualization
        and
        visualization is not False
    ):

        if isinstance(
            visualization,
            str
        ):

            visualization = [
                visualization
            ]

        requested[
            "visualization"
        ].extend(
            visualization
        )

    # --------------------------------------------------------
    # OUTPUT
    # --------------------------------------------------------

    output = specification.get(
        "output",
        []
    )

    if isinstance(
        output,
        str
    ):

        output = [
            output
        ]

    requested[
        "output"
    ].extend(
        output or []
    )

    return requested


# ============================================================
# RESOLVE RAW MATERIALS
# ============================================================
#
# This is the primary generator resolution operation.
# ============================================================

def resolve_raw_materials(
    generation_specification
):

    # --------------------------------------------------------
    # USE NESTED COMPONENTS WHEN PRESENT
    # --------------------------------------------------------

    components = (
        generation_specification.get(
            "components",
            generation_specification
        )
    )

    if not isinstance(
        components,
        dict
    ):

        raise TypeError(
            "Generation specification contains "
            "an invalid components object."
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

    # --------------------------------------------------------
    # IDENTIFY MASTER-DOC ROLES
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
    # GET MODULES
    # --------------------------------------------------------

    ingestion_module = get_master_doc(
        roles,
        "ingestion"
    )

    preprocessing_module = get_master_doc(
        roles,
        "preprocessing"
    )

    statistics_module = get_master_doc(
        roles,
        "statistics"
    )

    signal_analysis_module = get_master_doc(
        roles,
        "signal_analysis"
    )

    decoding_module = get_master_doc(
        roles,
        "decoding"
    )

    visualization_module = get_master_doc(
        roles,
        "visualization"
    )

    output_module = get_master_doc(
        roles,
        "output"
    )

    # --------------------------------------------------------
    # REQUESTED RESOURCES
    # --------------------------------------------------------

    requested = (
        extract_requested_resources(
            components
        )
    )

    resolved = {

        "ingestion":
            [],

        "preprocessing":
            [],

        "statistics":
            [],

        "signal_analysis":
            [],

        "decoding":
            [],

        "visualization":
            [],

        "output":
            [],
    }

    unresolved = []

    # ========================================================
    # INGESTION
    # ========================================================

    ingestion_resource, ingestion_error = (
        resolve_ingestion_resource(
            ingestion_module,
            components
        )
    )

    if ingestion_resource is not None:

        resolved[
            "ingestion"
        ].append(
            ingestion_resource
        )

    elif ingestion_error is not None:

        unresolved.append({

            "role":
                "ingestion",

            "requested":
                (
                    f"{components.get('neural_data')}"
                    f"/"
                    f"{components.get('file_type')}"
                ),

            "reason":
                ingestion_error.get(
                    "reason"
                ),
        })

    # ========================================================
    # PREPROCESSING
    # ========================================================

    for requested_name in (
        requested[
            "preprocessing"
        ]
    ):

        result = (
            resolve_standard_component(
                preprocessing_module,
                requested_name,
                "preprocessing"
            )
        )

        if result is not None:

            resolved[
                "preprocessing"
            ].append(
                result
            )

        else:

            unresolved.append({

                "role":
                    "preprocessing",

                "requested":
                    requested_name,

                "reason":
                    (
                        "Resource was not found "
                        "in the corresponding "
                        "Master-DOC."
                    ),
            })

    # ========================================================
    # STATISTICS
    # ========================================================

    for requested_name in (
        requested[
            "statistics"
        ]
    ):

        result = (
            resolve_standard_component(
                statistics_module,
                requested_name,
                "statistics"
            )
        )

        if result is not None:

            resolved[
                "statistics"
            ].append(
                result
            )

        else:

            unresolved.append({

                "role":
                    "statistics",

                "requested":
                    requested_name,

                "reason":
                    (
                        "Resource was not found "
                        "in the corresponding "
                        "Master-DOC."
                    ),
            })

    # ========================================================
    # SIGNAL ANALYSIS
    # ========================================================

    for requested_name in (
        requested[
            "signal_analysis"
        ]
    ):

        result = (
            resolve_standard_component(
                signal_analysis_module,
                requested_name,
                "signal_analysis"
            )
        )

        if result is not None:

            resolved[
                "signal_analysis"
            ].append(
                result
            )

        else:

            unresolved.append({

                "role":
                    "signal_analysis",

                "requested":
                    requested_name,

                "reason":
                    (
                        "Resource was not found "
                        "in the corresponding "
                        "Master-DOC."
                    ),
            })

    # ========================================================
    # DECODING
    # ========================================================

    for requested_name in (
        requested[
            "decoding"
        ]
    ):

        result = (
            resolve_standard_component(
                decoding_module,
                requested_name,
                "decoding"
            )
        )

        if result is not None:

            resolved[
                "decoding"
            ].append(
                result
            )

        else:

            unresolved.append({

                "role":
                    "decoding",

                "requested":
                    requested_name,

                "reason":
                    (
                        "Resource was not found "
                        "in the corresponding "
                        "Master-DOC."
                    ),
            })

    # ========================================================
    # VISUALIZATION
    # ========================================================

    for requested_name in (
        requested[
            "visualization"
        ]
    ):

        result = (
            resolve_standard_component(
                visualization_module,
                requested_name,
                "visualization"
            )
        )

        if result is not None:

            resolved[
                "visualization"
            ].append(
                result
            )

        else:

            unresolved.append({

                "role":
                    "visualization",

                "requested":
                    requested_name,

                "reason":
                    (
                        "Resource was not found "
                        "in the corresponding "
                        "Master-DOC."
                    ),
            })

    # ========================================================
    # OUTPUT
    # ========================================================

    for requested_name in (
        requested[
            "output"
        ]
    ):

        result = (
            resolve_standard_component(
                output_module,
                requested_name,
                "output"
            )
        )

        if result is not None:

            resolved[
                "output"
            ].append(
                result
            )

        else:

            unresolved.append({

                "role":
                    "output",

                "requested":
                    requested_name,

                "reason":
                    (
                        "Resource was not found "
                        "in the corresponding "
                        "Master-DOC."
                    ),
            })

    # ========================================================
    # STATUS
    # ========================================================

    if not unresolved:

        status = "RESOLVED"

    elif resolved:

        status = "PARTIAL"

    else:

        status = "FAILED"

    return {

        "status":
            status,

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
            master_doc_state[
                "errors"
            ],
    }


# ============================================================
# BUILD COMPILATION PLAN
# ============================================================
#
# This converts resolved raw materials into an ordered
# representation for the future source-code compiler.
#
# It does NOT execute the scientific functions yet.
# ============================================================

def build_compilation_plan(
    resolution
):

    plan = []

    stage_order = (

        "ingestion",

        "preprocessing",

        "statistics",

        "signal_analysis",

        "decoding",

        "visualization",

        "output",
    )

    for stage in stage_order:

        for resource in resolution[
            "resolved"
        ].get(
            stage,
            []
        ):

            plan.append({

                "stage":
                    stage,

                "requested":
                    resource.get(
                        "requested_name"
                    ),

                "resolved":
                    resource.get(
                        "resolved_name"
                    ),

                "source":
                    resource.get(
                        "source"
                    ),

                "container":
                    resource.get(
                        "container"
                    ),

                "type":
                    resource.get(
                        "type"
                    ),

                "resource":
                    resource.get(
                        "resource"
                    ),
            })

    return plan


# ============================================================
# RECEIVE GENERATION SPECIFICATION
# ============================================================
#
# This is the public handoff function.
#
# analysis.py calls:
#
#     generator.receive_generation_specification(
#         specification
#     )
#
# The generator receives the object and immediately resolves
# its raw materials against the Master-DOC library.
# ============================================================

def receive_generation_specification(
    generation_specification
):

    if generation_specification is None:

        raise ValueError(
            "Generator received no generation "
            "specification."
        )

    if not isinstance(
        generation_specification,
        dict
    ):

        raise TypeError(
            "Generator expected the generation "
            "specification to be a dictionary."
        )

    resolution = (
        resolve_raw_materials(
            generation_specification
        )
    )

    compilation_plan = (
        build_compilation_plan(
            resolution
        )
    )

    return {

        "status":
            resolution[
                "status"
            ],

        "generation_specification":
            generation_specification,

        "raw_material_resolution":
            resolution,

        "compilation_plan":
            compilation_plan,

        "ready_for_compilation":
            (
                resolution[
                    "status"
                ]
                ==
                "RESOLVED"
            ),
    }


# ============================================================
# GENERATOR ENTRY POINT
# ============================================================

def generate(
    generation_specification
):

    return receive_generation_specification(
        generation_specification
    )


# ============================================================
# PRINT RAW MATERIAL RESOLUTION
# ============================================================

def print_resolution_report(
    generator_state
):

    resolution = (
        generator_state[
            "raw_material_resolution"
        ]
    )

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
        f"Status: "
        f"{resolution.get('status')}"
    )

    print()

    # --------------------------------------------------------
    # REQUESTED
    # --------------------------------------------------------

    print(
        "Requested resources:"
    )

    for role, resources in (
        resolution[
            "requested"
        ].items()
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

    any_resolved = False

    for role, resources in (
        resolution[
            "resolved"
        ].items()
    ):

        for resource in resources:

            any_resolved = True

            print(
                f"  - {role}: "
                f"{resource.get('requested_name')}"
                f" -> "
                f"{resource.get('resolved_name')}"
                f" "
                f"[{resource.get('source')}]"
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
        "Unresolved resources:"
    )

    unresolved = (
        resolution[
            "unresolved"
        ]
    )

    if not unresolved:

        print(
            "  NONE"
        )

    else:

        for item in unresolved:

            print(
                f"  - "
                f"{item.get('role')}: "
                f"{item.get('requested')} "
                f"-> "
                f"{item.get('reason')}"
            )

    print()

    # --------------------------------------------------------
    # COMPILATION PLAN
    # --------------------------------------------------------

    print(
        "Compilation plan:"
    )

    compilation_plan = (
        generator_state.get(
            "compilation_plan",
            []
        )
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
        "Ready for compilation:"
    )

    print(
        f"  "
        f"{generator_state.get('ready_for_compilation')}"
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
#     python generator.py
#
# tests the generator independently of ingestion.py.
#
# This test intentionally uses the same logical parameter
# structure passed through the analysis → generator handoff.
# ============================================================

if __name__ == "__main__":

    test_generation_specification = {

        "components": {

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
    }

    generator_state = generate(
        test_generation_specification
    )

    print_resolution_report(
        generator_state
    )

