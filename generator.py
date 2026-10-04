
# ============================================================
# PIPELINE GENERATOR
# ============================================================
#
# generator.py is the factory/compiler layer of the
# PIPELINE-GENERATOR system.
#
# ARCHITECTURE
#
#     ingestion.py
#          |
#          v
#     analysis.py
#          |
#          v
#     generation specification object
#          |
#          v
#     generator.py
#          |
#          +----> read specification
#          |
#          +----> locate Master-DOCs
#          |
#          +----> identify Master-DOC roles
#          |
#          +----> resolve requested resources
#          |
#          +----> acquire ACTUAL source code
#          |
#          +----> resolve dependencies
#          |
#          +----> apply compatibility/order
#          |
#          +----> assemble pipeline
#          |
#          +----> validate generated source
#          |
#          v
#     generated_pipeline.py
#
# IMPORTANT
#
# generator.py does NOT invent scientific algorithms.
#
# Scientific implementations must come from the Master-DOC
# library.
#
# generator.py selects, acquires, organizes, and assembles
# those implementations.
#
# A resource is NOT considered resolved merely because a
# matching name was found.
#
# A resource is resolved only when actual reusable source
# material has been acquired.
#
# There is NO library-wide role fallback.
#
# preprocessing resources MUST come from preprocessing.
# statistics resources MUST come from statistics.
# signal-analysis resources MUST come from signal_analysis.
# ============================================================


# ============================================================
# IMPORTS
# ============================================================

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from types import ModuleType
from importlib.machinery import SourceFileLoader

import ast
import importlib.util
import inspect
import re
import textwrap

from typing import Any


# ============================================================
# PATHS
# ============================================================

BASE_DIRECTORY = Path(__file__).resolve().parent

MASTER_DOC_DIRECTORY = (
    BASE_DIRECTORY / "Master-DOC's"
)

GENERATED_DIRECTORY = (
    BASE_DIRECTORY / "generated"
)

DEFAULT_GENERATED_FILE = (
    GENERATED_DIRECTORY /
    "generated_pipeline.py"
)


# ============================================================
# MASTER-DOC ROLE PATTERNS
# ============================================================

MASTER_DOC_ROLE_PATTERNS = {

    "ingestion": (
        "master-doc-ingestion",
        "master-doc-input",
        "master-doc-data",
        "ingestion",
        "input",
    ),

    "preprocessing": (
        "master-doc-preprocessing",
        "master-doc-preprocess",
        "preprocessing",
        "preprocess",
    ),

    "statistics": (
        "master-doc-stats",
        "master-doc-statistics",
        "statistics",
        "stats",
    ),

    "signal_analysis": (
        "master-doc-signal-analysis",
        "master-doc-signal_analysis",
        "master-doc-signalanalysis",
        "signal-analysis",
        "signal_analysis",
        "signal",
        "spectral",
    ),

    "decoding": (
        "master-doc-decoding",
        "master-doc-decoder",
        "decoding",
        "decoder",
    ),

    "visualization": (
        "master-doc-visualization",
        "master-doc-visualizatiom",
        "visualization",
        "visualisation",
        "plot",
        "visual",
    ),

    "validation": (
        "master-doc-validation",
        "validation",
        "validator",
    ),

    "pipeline": (
        "master-doc-pipeline",
        "pipeline",
    ),

    "output": (
        "master-doc-output",
        "output",
    ),

    "connectivity": (
        "master-doc-connectivity",
        "connectivity",
        "connection",
    ),

    "generator": (
        "master-doc-generator",
        "generator",
    ),
}


# ============================================================
# RESOURCE ALIASES
# ============================================================

RESOURCE_ALIASES = {

    # --------------------------------------------------------
    # INGESTION
    # --------------------------------------------------------

    "eeg": (
        "eeg",
        "EEG",
        "load_eeg",
        "read_eeg",
        "ingest_eeg",
    ),

    # --------------------------------------------------------
    # PREPROCESSING
    # --------------------------------------------------------

    "bandpass_filter": (
        "bandpass_filter",
        "band_pass_filter",
        "apply_bandpass_filter",
        "apply_band_pass_filter",
        "bandpass",
        "band_pass",
    ),

    "notch_filter": (
        "notch_filter",
        "apply_notch_filter",
        "notch",
    ),

    "lowpass_filter": (
        "lowpass_filter",
        "low_pass_filter",
        "apply_lowpass_filter",
        "apply_low_pass_filter",
    ),

    "highpass_filter": (
        "highpass_filter",
        "high_pass_filter",
        "apply_highpass_filter",
        "apply_high_pass_filter",
    ),

    "bandstop_filter": (
        "bandstop_filter",
        "band_stop_filter",
        "apply_bandstop_filter",
        "apply_band_stop_filter",
    ),

    "remove_invalid_samples": (
        "remove_invalid_samples",
        "remove_nan_samples",
        "remove_nans",
        "clean_invalid_samples",
    ),

    "remove_dc_offset": (
        "remove_dc_offset",
        "dc_offset_removal",
    ),

    "detrend": (
        "detrend",
        "detrend_signal",
        "remove_trend",
    ),

    "baseline_correction": (
        "baseline_correction",
        "baseline_correct",
        "correct_baseline",
    ),

    "resample": (
        "resample",
        "resample_signal",
        "resampling",
    ),

    "common_average_reference": (
        "common_average_reference",
        "car",
        "apply_common_average_reference",
    ),

    "select_channels": (
        "select_channels",
        "choose_channels",
        "channel_selection",
    ),

    # --------------------------------------------------------
    # STATISTICS
    # --------------------------------------------------------

    "mean": (
        "mean",
        "calculate_mean",
        "compute_mean",
        "extract_mean_features",
    ),

    "median": (
        "median",
        "calculate_median",
        "compute_median",
        "extract_median_features",
    ),

    "mode": (
        "mode",
        "calculate_mode",
        "compute_mode",
    ),

    "minimum": (
        "minimum",
        "min",
        "calculate_minimum",
        "calculate_min",
        "compute_minimum",
    ),

    "maximum": (
        "maximum",
        "max",
        "calculate_maximum",
        "calculate_max",
        "compute_maximum",
    ),

    "variance": (
        "variance",
        "calculate_variance",
        "compute_variance",
        "extract_variance_features",
    ),

    "std": (
        "std",
        "standard_deviation",
        "calculate_standard_deviation",
        "calculate_std",
        "compute_standard_deviation",
        "extract_std_features",
    ),

    "rms": (
        "rms",
        "calculate_rms",
        "compute_rms",
        "root_mean_square",
        "extract_rms_features",
    ),

    "range": (
        "range",
        "calculate_range",
        "compute_range",
    ),

    "skewness": (
        "skewness",
        "calculate_skewness",
        "compute_skewness",
    ),

    "kurtosis": (
        "kurtosis",
        "calculate_kurtosis",
        "compute_kurtosis",
    ),

    # --------------------------------------------------------
    # SIGNAL ANALYSIS
    # --------------------------------------------------------

    "spectral_power": (
        "spectral_power",
        "calculate_spectral_power",
        "compute_spectral_power",
        "power_spectral_density",
        "calculate_power_spectral_density",
        "compute_power_spectral_density",
        "psd",
    ),

    "total_spectral_power": (
        "total_spectral_power",
        "calculate_total_spectral_power",
        "compute_total_spectral_power",
    ),

    "band_power": (
        "band_power",
        "calculate_band_power",
        "compute_band_power",
    ),

    "relative_band_power": (
        "relative_band_power",
        "calculate_relative_band_power",
        "compute_relative_band_power",
    ),

    "dominant_frequency": (
        "dominant_frequency",
        "calculate_dominant_frequency",
        "compute_dominant_frequency",
        "find_dominant_frequency",
    ),

    "peak_frequency": (
        "peak_frequency",
        "calculate_peak_frequency",
        "compute_peak_frequency",
        "find_peak_frequency",
    ),

    "spectral_entropy": (
        "spectral_entropy",
        "calculate_spectral_entropy",
        "compute_spectral_entropy",
    ),

    "spectral_edge": (
        "spectral_edge",
        "spectral_edge_frequency",
        "calculate_spectral_edge",
        "calculate_spectral_edge_frequency",
    ),
}


# ============================================================
# PIPELINE STAGE ORDER
# ============================================================

PIPELINE_STAGE_ORDER = (
    "ingestion",
    "preprocessing",
    "statistics",
    "signal_analysis",
    "decoding",
    "visualization",
    "output",
)


# ============================================================
# RESOLVED RESOURCE
# ============================================================

@dataclass
class ResolvedResource:

    requested_name: str

    resolved_name: str

    role: str

    master_doc: str

    source_code: str = ""

    function_name: str | None = None

    dependencies: list[str] = field(
        default_factory=list
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    @property
    def source_acquired(self) -> bool:

        return bool(
            self.source_code.strip()
        )

    @property
    def qualified_name(self) -> str:

        return (
            f"{self.master_doc}:"
            f"{self.resolved_name}"
        )


# ============================================================
# GENERATION RESULT
# ============================================================

@dataclass
class GenerationResult:

    status: str

    specification: Any

    resolved_resources: list[
        ResolvedResource
    ] = field(
        default_factory=list
    )

    unresolved_resources: list[str] = field(
        default_factory=list
    )

    dependencies: list[str] = field(
        default_factory=list
    )

    stages: list[str] = field(
        default_factory=list
    )

    compatibility: dict[str, Any] = field(
        default_factory=dict
    )

    source_code: str = ""

    generated_file: Path | None = None

    errors: list[str] = field(
        default_factory=list
    )


# ============================================================
# NORMALIZE NAME
# ============================================================

def normalize_name(
    value: Any
) -> str:

    if value is None:

        return ""

    value = str(value)

    value = (
        value
        .strip()
        .lower()
        .replace("-", "_")
        .replace(" ", "_")
    )

    value = re.sub(
        r"[^a-z0-9_]",
        "_",
        value
    )

    value = re.sub(
        r"_+",
        "_",
        value
    )

    return value.strip("_")


# ============================================================
# NORMALIZE ROLE
# ============================================================

def normalize_role_name(
    value: Any
) -> str:

    normalized = normalize_name(
        value
    )

    aliases = {

        "stats":
            "statistics",

        "stat":
            "statistics",

        "preprocess":
            "preprocessing",

        "signal":
            "signal_analysis",

        "signalanalysis":
            "signal_analysis",

        "visualisation":
            "visualization",
    }

    return aliases.get(
        normalized,
        normalized
    )


# ============================================================
# SPECIFICATION → DICTIONARY
# ============================================================

def specification_to_dict(
    specification: Any
) -> dict[str, Any]:

    if specification is None:

        return {}

    if isinstance(
        specification,
        dict
    ):

        return dict(
            specification
        )

    for method_name in (
        "to_dict",
        "model_dump",
    ):

        method = getattr(
            specification,
            method_name,
            None
        )

        if callable(method):

            result = method()

            if isinstance(
                result,
                dict
            ):

                return dict(
                    result
                )

    result = {}

    for name in dir(
        specification
    ):

        if name.startswith("_"):

            continue

        try:

            value = getattr(
                specification,
                name
            )

        except Exception:

            continue

        if callable(value):

            continue

        result[name] = value

    return result


# ============================================================
# DISCOVER MASTER-DOC FILES
# ============================================================

def discover_master_docs() -> list[Path]:

    if not MASTER_DOC_DIRECTORY.exists():

        raise FileNotFoundError(
            "Master-DOC directory not found:\n"
            f"{MASTER_DOC_DIRECTORY}\n\n"
            "The Master-DOC library must exist locally "
            "beside generator.py."
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
                and path.suffix.lower() == ".py"
                and not path.name.startswith(".")
                and "__pycache__" not in path.parts
            )
        ),
        key=lambda path:
            path.name.lower()
    )


# ============================================================
# LOAD MASTER-DOC
# ============================================================

def load_master_doc(
    path: Path
) -> ModuleType:

    module_name = re.sub(
        r"[^A-Za-z0-9_]",
        "_",
        path.stem
    )

    loader = SourceFileLoader(
        module_name,
        str(path)
    )

    spec = (
        importlib.util.spec_from_loader(
            module_name,
            loader
        )
    )

    if spec is None:

        raise ImportError(
            "Unable to create module specification "
            f"for {path.name}"
        )

    module = (
        importlib.util.module_from_spec(
            spec
        )
    )

    loader.exec_module(
        module
    )

    return module


# ============================================================
# LOAD MASTER-DOC LIBRARY
# ============================================================

def load_master_doc_library():

    loaded = {}

    errors = {}

    paths = discover_master_docs()

    print(
        f"  Master-DOC files discovered: "
        f"{len(paths)}"
    )

    for path in paths:

        print(
            f"    Loading: {path.name}"
        )

        try:

            loaded[
                path.name
            ] = load_master_doc(
                path
            )

            print(
                "      ✓ loaded"
            )

        except Exception as error:

            errors[
                path.name
            ] = error

            print(
                "      ✗ FAILED"
            )

            print(
                f"        {type(error).__name__}: "
                f"{error}"
            )

    return (
        loaded,
        errors
    )


# ============================================================
# ROLE MATCHING
# ============================================================

def role_matches_document(
    role: str,
    document_name: str
) -> bool:

    normalized_document = normalize_name(
        Path(
            document_name
        ).stem
    )

    patterns = (
        MASTER_DOC_ROLE_PATTERNS.get(
            role,
            ()
        )
    )

    for pattern in patterns:

        normalized_pattern = normalize_name(
            pattern
        )

        if normalized_document == normalized_pattern:
            return True

        if normalized_pattern in normalized_document:
            return True

    return False


# ============================================================
# CONTENT-BASED ROLE DETECTION
# ============================================================

def infer_role_from_module(
    document_name: str,
    module: ModuleType
) -> str | None:

    for role in MASTER_DOC_ROLE_PATTERNS:

        if role_matches_document(
            role,
            document_name
        ):

            return role

    function_names = []

    for name in dir(module):

        if name.startswith("_"):
            continue

        try:
            value = getattr(
                module,
                name
            )
        except Exception:
            continue

        if callable(value):
            function_names.append(
                normalize_name(name)
            )

    function_text = " ".join(
        function_names
    )

    preprocessing_terms = (
        "bandpass",
        "band_pass",
        "notch",
        "lowpass",
        "highpass",
        "detrend",
        "baseline",
        "resample",
        "preprocess",
    )

    if any(
        term in function_text
        for term in preprocessing_terms
    ):
        return "preprocessing"

    statistics_terms = (
        "calculate_mean",
        "calculate_median",
        "calculate_variance",
        "calculate_std",
        "calculate_standard_deviation",
        "calculate_rms",
        "extract_mean",
        "extract_std",
        "extract_variance",
        "extract_rms",
    )

    if any(
        term in function_text
        for term in statistics_terms
    ):
        return "statistics"

    signal_terms = (
        "spectral",
        "power_spectral",
        "spectral_power",
        "dominant_frequency",
        "peak_frequency",
        "band_power",
        "entropy",
    )

    if any(
        term in function_text
        for term in signal_terms
    ):
        return "signal_analysis"

    ingestion_terms = (
        "load_eeg",
        "read_eeg",
        "ingest",
        "load_data",
        "read_data",
        "eeglab",
        "edf",
    )

    if any(
        term in (
            normalize_name(
                document_name
            )
            + " "
            + function_text
        )
        for term in ingestion_terms
    ):
        return "ingestion"

    return None


# ============================================================
# IDENTIFY MASTER-DOC ROLES
# ============================================================

def identify_master_doc_roles(
    loaded_docs: dict[str, ModuleType]
):

    roles = {}

    diagnostics = {}

    for document_name, module in (
        loaded_docs.items()
    ):

        role = infer_role_from_module(
            document_name,
            module
        )

        diagnostics[
            document_name
        ] = role

        if role is not None:

            if role not in roles:

                roles[
                    role
                ] = module

    return (
        roles,
        diagnostics
    )


# ============================================================
# REQUEST LIST
# ============================================================

def get_request_list(
    specification: dict[str, Any],
    key: str
) -> list[Any]:

    value = specification.get(
        key,
        []
    )

    if value is None:
        return []

    if isinstance(
        value,
        (list, tuple, set)
    ):
        return list(value)

    return [value]


# ============================================================
# RESOURCE ALIASES
# ============================================================

def get_resource_aliases(
    requested_name: str
) -> list[str]:

    normalized = normalize_name(
        requested_name
    )

    aliases = list(
        RESOURCE_ALIASES.get(
            normalized,
            ()
        )
    )

    if normalized not in [
        normalize_name(alias)
        for alias in aliases
    ]:
        aliases.append(
            normalized
        )

    return aliases


# ============================================================
# LIST FUNCTIONS
# ============================================================

def list_module_functions(
    module: ModuleType
) -> list[str]:

    functions = []

    for name in dir(module):

        if name.startswith("_"):
            continue

        try:
            value = getattr(
                module,
                name
            )
        except Exception:
            continue

        if callable(value):
            functions.append(name)

    return sorted(
        functions,
        key=str.lower
    )


# ============================================================
# FIND FUNCTION
# ============================================================

def find_function_by_aliases(
    module: ModuleType,
    requested_name: str
):

    aliases = {
        normalize_name(alias)
        for alias
        in get_resource_aliases(
            requested_name
        )
    }

    functions = (
        list_module_functions(
            module
        )
    )

    # Exact match first.
    for function_name in functions:

        if normalize_name(
            function_name
        ) in aliases:

            return getattr(
                module,
                function_name
            )

    # Containment match second.
    for function_name in functions:

        normalized_function = normalize_name(
            function_name
        )

        for alias in aliases:

            if (
                alias in normalized_function
                or
                normalized_function in alias
            ):

                return getattr(
                    module,
                    function_name
                )

    return None


# ============================================================
# SOURCE FROM FUNCTION
# ============================================================

def get_function_source(
    function
) -> str:

    try:

        return inspect.getsource(
            function
        )

    except (
        OSError,
        TypeError
    ):

        return ""


# ============================================================
# AST SOURCE EXTRACTION
# ============================================================
#
# This is the important correction.
#
# A Master-DOC does not have to expose a function as a module
# attribute in order for generator.py to acquire its source.
#
# We inspect the actual Master-DOC source file and locate:
#
#     def function(...)
#     class ...
#     assignments containing resource definitions
#
# This allows the generator to acquire reusable source instead
# of merely finding a name.
# ============================================================

def get_ast_nodes_for_name(
    source_text: str,
    aliases: set[str]
):

    try:

        tree = ast.parse(
            source_text
        )

    except SyntaxError:

        return []

    matches = []

    for node in tree.body:

        node_name = getattr(
            node,
            "name",
            None
        )

        if node_name is not None:

            normalized_node_name = normalize_name(
                node_name
            )

            if (
                normalized_node_name in aliases
                or
                any(
                    alias in normalized_node_name
                    or
                    normalized_node_name in alias
                    for alias in aliases
                )
            ):

                matches.append(
                    node
                )

                continue

        if isinstance(
            node,
            ast.Assign
        ):

            for target in node.targets:

                target_name = getattr(
                    target,
                    "id",
                    None
                )

                if target_name is None:
                    continue

                normalized_target = normalize_name(
                    target_name
                )

                if normalized_target in aliases:

                    matches.append(
                        node
                    )

    return matches


def get_ast_node_source(
    source_text: str,
    node
) -> str:

    try:

        return ast.get_source_segment(
            source_text,
            node
        ) or ""

    except Exception:

        return ""


# ============================================================
# SOURCE FROM RESOURCE
# ============================================================

def get_resource_source(
    resource
) -> str:

    if callable(resource):

        return get_function_source(
            resource
        )

    if isinstance(
        resource,
        str
    ):

        return resource

    if isinstance(
        resource,
        dict
    ):

        for key in (
            "source_code",
            "code",
            "source",
            "implementation",
        ):

            value = resource.get(
                key
            )

            if isinstance(
                value,
                str
            ):

                return value

    return ""


# ============================================================
# READ MASTER-DOC SOURCE
# ============================================================

def read_module_source(
    module: ModuleType
) -> str:

    module_file = getattr(
        module,
        "__file__",
        None
    )

    if not module_file:

        return ""

    try:

        return Path(
            module_file
        ).read_text(
            encoding="utf-8"
        )

    except (
        OSError,
        UnicodeDecodeError
    ):

        return ""


# ============================================================
# FIND RESOURCE IN ONE MASTER-DOC
# ============================================================

def find_named_resource(
    module: ModuleType | None,
    requested_name: str
):

    if module is None:

        return None

    aliases = {
        normalize_name(alias)
        for alias
        in get_resource_aliases(
            requested_name
        )
    }

    # --------------------------------------------------------
    # 1. DIRECT ATTRIBUTE
    # --------------------------------------------------------

    for attribute_name in dir(module):

        if attribute_name.startswith("__"):
            continue

        normalized_attribute = normalize_name(
            attribute_name
        )

        if normalized_attribute not in aliases:
            continue

        try:

            resource = getattr(
                module,
                attribute_name
            )

        except Exception:

            continue

        return (
            attribute_name,
            resource
        )

    # --------------------------------------------------------
    # 2. FUNCTION SEARCH
    # --------------------------------------------------------

    function = find_function_by_aliases(
        module,
        requested_name
    )

    if function is not None:

        return (
            function.__name__,
            function
        )

    # --------------------------------------------------------
    # 3. RESOURCE DICTIONARIES
    # --------------------------------------------------------

    for attribute_name in dir(module):

        if attribute_name.startswith("__"):
            continue

        try:

            container = getattr(
                module,
                attribute_name
            )

        except Exception:

            continue

        if not isinstance(
            container,
            dict
        ):
            continue

        for key, value in container.items():

            normalized_key = normalize_name(
                key
            )

            if normalized_key in aliases:

                return (
                    str(key),
                    value
                )

            if isinstance(
                value,
                dict
            ):

                for metadata_key in (
                    "id",
                    "name",
                    "key",
                    "identifier",
                    "resource",
                    "function",
                ):

                    metadata_value = value.get(
                        metadata_key
                    )

                    if metadata_value is None:
                        continue

                    if normalize_name(
                        metadata_value
                    ) in aliases:

                        return (
                            str(key),
                            value
                        )

    return None


# ============================================================
# ACQUIRE ACTUAL SOURCE
# ============================================================

def acquire_resource_source(
    module: ModuleType,
    requested_name: str,
    resource_name: str,
    resource: Any
) -> tuple[str, str | None]:

    # --------------------------------------------------------
    # First attempt: runtime source
    # --------------------------------------------------------

    source_code = clean_source(
        get_resource_source(
            resource
        )
    )

    if source_code:

        function_name = None

        if callable(resource):

            function_name = getattr(
                resource,
                "__name__",
                None
            )

        return (
            source_code,
            function_name
        )

    # --------------------------------------------------------
    # Second attempt: source-file AST
    # --------------------------------------------------------

    source_text = read_module_source(
        module
    )

    if not source_text:

        return (
            "",
            None
        )

    aliases = {
        normalize_name(
            alias
        )
        for alias
        in get_resource_aliases(
            requested_name
        )
    }

    aliases.add(
        normalize_name(
            resource_name
        )
    )

    nodes = get_ast_nodes_for_name(
        source_text,
        aliases
    )

    if not nodes:

        return (
            "",
            None
        )

    source_parts = []

    function_name = None

    for node in nodes:

        node_source = clean_source(
            get_ast_node_source(
                source_text,
                node
            )
        )

        if not node_source:
            continue

        source_parts.append(
            node_source
        )

        node_name = getattr(
            node,
            "name",
            None
        )

        if node_name:

            function_name = node_name

    if not source_parts:

        return (
            "",
            None
        )

    return (
        "\n\n".join(
            source_parts
        ),
        function_name
    )


# ============================================================
# EXTRACT DEPENDENCIES
# ============================================================

def extract_dependencies(
    source_code: str
) -> list[str]:

    if not source_code:

        return []

    dependencies = []

    try:

        tree = ast.parse(
            source_code
        )

    except SyntaxError:

        return dependencies

    for node in ast.walk(tree):

        if isinstance(
            node,
            ast.Import
        ):

            for alias in node.names:

                dependencies.append(
                    alias.name
                )

        elif isinstance(
            node,
            ast.ImportFrom
        ):

            if node.module:

                dependencies.append(
                    node.module
                )

    return dependencies


# ============================================================
# RESOLVE ONE RESOURCE
# ============================================================

def resolve_resource(
    module: ModuleType | None,
    role: str,
    requested_name: Any,
    master_doc_name: str
) -> ResolvedResource | None:

    if module is None:
        return None

    if requested_name is None:
        return None

    requested_name = str(
        requested_name
    )

    found = find_named_resource(
        module,
        requested_name
    )

    if found is None:
        return None

    resolved_name, resource = found

    source_code, function_name = (
        acquire_resource_source(
            module,
            requested_name,
            str(resolved_name),
            resource
        )
    )

    # --------------------------------------------------------
    # CRITICAL:
    #
    # A matching name without actual source is NOT resolved.
    # --------------------------------------------------------

    if not source_code.strip():

        return None

    dependencies = (
        extract_dependencies(
            source_code
        )
    )

    return ResolvedResource(

        requested_name=
            requested_name,

        resolved_name=
            str(resolved_name),

        role=
            role,

        master_doc=
            master_doc_name,

        source_code=
            source_code,

        function_name=
            function_name,

        dependencies=
            dependencies,

        metadata={
            "aliases":
                get_resource_aliases(
                    requested_name
                ),

            "resource_type":
                type(resource).__name__,

            "source_acquired":
                True,
        }
    )


# ============================================================
# RESOLVE RESOURCE — STRICT ROLE OWNERSHIP
# ============================================================
#
# IMPORTANT:
#
# There is intentionally NO complete-library fallback here.
#
# The analysis object specifies the role.
#
# Therefore:
#
# preprocessing -> preprocessing Master-DOC
# statistics -> statistics Master-DOC
# signal_analysis -> signal_analysis Master-DOC
#
# If the designated Master-DOC cannot provide actual source,
# the resource remains unresolved.
# ============================================================

def resolve_resource_strict(
    role: str,
    requested_name: str,
    roles: dict[str, ModuleType]
):

    print(
        f"  Searching role '{role}'"
    )

    primary_module = roles.get(
        role
    )

    if primary_module is None:

        print(
            f"    ✗ No Master-DOC assigned "
            f"to role '{role}'."
        )

        return None

    print(
        f"    Primary Master-DOC: "
        f"{primary_module.__name__}"
    )

    print(
        f"    Requested resource: "
        f"{requested_name}"
    )

    print(
        f"    Aliases: "
        f"{', '.join(get_resource_aliases(requested_name))}"
    )

    resource = resolve_resource(
        primary_module,
        role,
        requested_name,
        primary_module.__name__
    )

    if resource is None:

        candidates = []

        try:

            candidates = (
                diagnostic_function_search(
                    primary_module,
                    requested_name
                )
            )

        except Exception:

            candidates = []

        if candidates:

            print(
                "    Candidate functions:"
            )

            for candidate in candidates:

                print(
                    f"      - {candidate}"
                )

        else:

            print(
                "    Candidate executable "
                "resources: none"
            )

        print(
            "    ✗ Resource was not acquired "
            "from its designated Master-DOC."
        )

        return None

    print(
        f"    ✓ Acquired source from "
        f"{primary_module.__name__}: "
        f"{resource.resolved_name}"
    )

    return resource


# ============================================================
# RESOLVE INGESTION
# ============================================================

def resolve_ingestion(
    specification: dict[str, Any],
    roles: dict[str, ModuleType]
):

    resources = []

    neural_data = specification.get(
        "neural_data"
    )

    file_type = specification.get(
        "file_type"
    )

    candidates = []

    if neural_data:
        candidates.append(
            str(neural_data)
        )

    if file_type:
        candidates.append(
            str(file_type)
        )

    for candidate in candidates:

        resource = resolve_resource_strict(
            "ingestion",
            candidate,
            roles
        )

        if resource is not None:

            resources.append(
                resource
            )

            return resources

    return resources


# ============================================================
# RESOLVE COMPONENT LIST
# ============================================================

def resolve_component_list(
    specification: dict[str, Any],
    role: str,
    roles: dict[str, ModuleType]
):

    resources = []

    unresolved = []

    key_map = {

        "preprocessing":
            "preprocessing",

        "statistics":
            "statistics",

        "signal_analysis":
            "signal_analysis",

        "decoding":
            "decoder",

        "visualization":
            "visualization",

        "output":
            "output",
    }

    key = key_map.get(
        role,
        role
    )

    requests = get_request_list(
        specification,
        key
    )

    for requested_name in requests:

        if (
            requested_name is None
            or requested_name is False
        ):
            continue

        if isinstance(
            requested_name,
            bool
        ):
            continue

        resource = resolve_resource_strict(
            role,
            str(requested_name),
            roles
        )

        if resource is None:

            unresolved.append(
                (
                    role,
                    str(requested_name)
                )
            )

        else:

            resources.append(
                resource
            )

    return (
        resources,
        unresolved
    )


# ============================================================
# RESOLVE ALL REQUESTED RESOURCES
# ============================================================

def resolve_all_resources(
    specification: dict[str, Any],
    roles: dict[str, ModuleType]
):

    resolved = []

    unresolved = []

    ingestion_resources = (
        resolve_ingestion(
            specification,
            roles
        )
    )

    if ingestion_resources:

        resolved.extend(
            ingestion_resources
        )

    else:

        unresolved.append(
            (
                "ingestion",
                (
                    specification.get(
                        "neural_data"
                    )
                    or
                    specification.get(
                        "file_type"
                    )
                    or
                    "unknown"
                )
            )
        )

    for role in (
        "preprocessing",
        "statistics",
        "signal_analysis",
        "decoding",
        "visualization",
        "output",
    ):

        resources, missing = (
            resolve_component_list(
                specification,
                role,
                roles
            )
        )

        resolved.extend(
            resources
        )

        unresolved.extend(
            missing
        )

    return (
        resolved,
        unresolved
    )


# ============================================================
# RESOLVE DEPENDENCIES
# ============================================================

def resolve_dependencies(
    resources: list[ResolvedResource]
) -> list[str]:

    dependencies = []

    for resource in resources:

        for dependency in (
            resource.dependencies
        ):

            if dependency not in dependencies:

                dependencies.append(
                    dependency
                )

    return dependencies


# ============================================================
# ORDER RESOURCES
# ============================================================

def order_resources(
    resources: list[ResolvedResource]
) -> list[ResolvedResource]:

    stage_index = {

        role: index

        for index, role
        in enumerate(
            PIPELINE_STAGE_ORDER
        )
    }

    return sorted(

        resources,

        key=lambda resource: (
            stage_index.get(
                resource.role,
                999
            ),

            resource.resolved_name.lower()
        )
    )


# ============================================================
# COMPATIBILITY CHECK
# ============================================================

def check_compatibility(
    specification: dict[str, Any],
    resources: list[ResolvedResource]
):

    errors = []

    roles_present = {
        resource.role
        for resource in resources
    }

    stage_keys = {

        "preprocessing":
            "preprocessing",

        "statistics":
            "statistics",

        "signal_analysis":
            "signal_analysis",

        "decoding":
            "decoder",

        "visualization":
            "visualization",

        "output":
            "output",
    }

    for role, key in (
        stage_keys.items()
    ):

        requested = [

            value

            for value

            in get_request_list(
                specification,
                key
            )

            if (
                value is not None
                and
                value is not False
                and
                not isinstance(
                    value,
                    bool
                )
            )
        ]

        if (
            requested
            and
            role not in roles_present
        ):

            errors.append(
                f"Requested {role} resources "
                f"were not resolved."
            )

    if (
        "preprocessing"
        in roles_present
        and
        "ingestion"
        not in roles_present
    ):

        errors.append(
            "Preprocessing requires "
            "an ingestion stage."
        )

    if (
        "statistics"
        in roles_present
        and
        "ingestion"
        not in roles_present
    ):

        errors.append(
            "Statistics requires "
            "an ingestion stage."
        )

    if (
        "signal_analysis"
        in roles_present
        and
        "ingestion"
        not in roles_present
    ):

        errors.append(
            "Signal analysis requires "
            "an ingestion stage."
        )

    return {

        "compatible":
            len(errors) == 0,

        "errors":
            errors,
    }


# ============================================================
# EXTRACT STAGES
# ============================================================

def extract_stage_names(
    resources: list[ResolvedResource]
) -> list[str]:

    stages = []

    for resource in resources:

        if resource.role not in stages:

            stages.append(
                resource.role
            )

    return stages


# ============================================================
# DEDUPLICATE IMPORTS
# ============================================================

def deduplicate_imports(
    dependencies: list[str]
) -> list[str]:

    result = []

    for dependency in dependencies:

        if dependency not in result:

            result.append(
                dependency
            )

    return result


# ============================================================
# CLEAN SOURCE
# ============================================================

def clean_source(
    source: str
) -> str:

    if not source:
        return ""

    return textwrap.dedent(
        source
    ).strip()


# ============================================================
# ASSEMBLE SOURCE
# ============================================================

def assemble_source(
    specification: dict[str, Any],
    resources: list[ResolvedResource],
    dependencies: list[str]
) -> str:

    sections = []

    sections.append(
        textwrap.dedent(
            """
            # ============================================================
            # GENERATED NEURAL PIPELINE
            # ============================================================
            #
            # Generated by PIPELINE-GENERATOR.
            #
            # Scientific implementations were acquired from the
            # designated Master-DOCs.
            #
            # ============================================================
            """
        ).strip()
    )

    import_lines = []

    for dependency in dependencies:

        if dependency.startswith("__"):
            continue

        if "." in dependency:

            import_lines.append(
                f"import {dependency}"
            )

        else:

            import_lines.append(
                f"import {dependency}"
            )

    if import_lines:

        sections.append(
            "\n".join(
                [
                    "# ============================================================",
                    "# IMPORTS",
                    "# ============================================================",
                    *sorted(
                        set(
                            import_lines
                        )
                    ),
                ]
            )
        )

    for resource in resources:

        source = clean_source(
            resource.source_code
        )

        if not source:
            continue

        sections.append(
            "\n".join(
                [
                    "# ============================================================",
                    f"# {resource.role.upper()}",
                    f"# RESOURCE: {resource.requested_name}",
                    f"# MASTER-DOC: {resource.master_doc}",
                    "# ============================================================",
                    source,
                ]
            )
        )

    sections.append(
        "\n".join(
            [
                "# ============================================================",
                "# PIPELINE CONFIGURATION",
                "# ============================================================",
                "",
                "PIPELINE_CONFIGURATION = "
                + repr(
                    specification
                ),
                "",
            ]
        )
    )

    execution = [

        "# ============================================================",
        "# PIPELINE EXECUTION",
        "# ============================================================",
        "",
        "def run_pipeline(data=None):",
        "    current_data = data",
        "",
    ]

    for resource in resources:

        if not resource.function_name:
            continue

        execution.extend(
            [
                f"    # {resource.role}: "
                f"{resource.requested_name}",

                f"    # Master-DOC: "
                f"{resource.master_doc}",

                f"    current_data = "
                f"{resource.function_name}"
                f"(current_data)",

                "",
            ]
        )

    execution.append(
        "    return current_data"
    )

    sections.append(
        "\n".join(
            execution
        )
    )

    return (
        "\n\n".join(
            sections
        )
        + "\n"
    )


# ============================================================
# VALIDATE GENERATED SOURCE
# ============================================================

def validate_generated_source(
    source_code: str
):

    if not source_code.strip():

        return {

            "valid":
                False,

            "errors": [
                "Generated source is empty."
            ],
        }

    try:

        ast.parse(
            source_code
        )

    except SyntaxError as error:

        return {

            "valid":
                False,

            "errors": [
                (
                    "Generated source contains "
                    f"SyntaxError: {error}"
                )
            ],
        }

    return {

        "valid":
            True,

        "errors":
            [],
    }


# ============================================================
# WRITE GENERATED PIPELINE
# ============================================================

def write_generated_pipeline(
    source_code: str,
    output_path: Path | None = None
) -> Path:

    if output_path is None:

        output_path = (
            DEFAULT_GENERATED_FILE
        )

    output_path = Path(
        output_path
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path.write_text(
        source_code,
        encoding="utf-8"
    )

    return output_path


# ============================================================
# MAIN GENERATOR
# ============================================================

def generate(
    generation_specification: Any,
    output_path: Path | None = None
) -> GenerationResult:

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

    print()

    print(
        "OBJECT RECEIVED"
    )

    print()

    specification = (
        specification_to_dict(
            generation_specification
        )
    )

    print(
        "Generation specification read."
    )

    print()

    print(
        "Specification contents:"
    )

    for key, value in (
        specification.items()
    ):

        print(
            f"  {key}: {value}"
        )

    # --------------------------------------------------------
    # LOAD LIBRARY
    # --------------------------------------------------------

    print()

    print(
        "Loading Master-DOC library..."
    )

    try:

        loaded_docs, load_errors = (
            load_master_doc_library()
        )

    except Exception as error:

        return GenerationResult(

            status="FAILED",

            specification=
                generation_specification,

            errors=[
                str(error)
            ]
        )

    # --------------------------------------------------------
    # ROLE MAP
    # --------------------------------------------------------

    print()

    print(
        "Resolving Master-DOC roles..."
    )

    roles, role_diagnostics = (
        identify_master_doc_roles(
            loaded_docs
        )
    )

    print()

    print(
        f"Master-DOCs loaded: "
        f"{len(loaded_docs)}"
    )

    print(
        f"Master-DOC roles resolved: "
        f"{len(roles)}"
    )

    print()

    print(
        "Master-DOC role map:"
    )

    for document_name, role in (
        role_diagnostics.items()
    ):

        if role is None:

            print(
                f"  ? {document_name}"
                f" -> role not identified"
            )

        else:

            print(
                f"  ✓ {document_name}"
                f" -> {role}"
            )

    # --------------------------------------------------------
    # REQUIRED ROLE CHECK
    # --------------------------------------------------------

    required_roles = set()

    if specification.get(
        "neural_data"
    ) or specification.get(
        "file_type"
    ):

        required_roles.add(
            "ingestion"
        )

    for role, key in (
        (
            "preprocessing",
            "preprocessing"
        ),
        (
            "statistics",
            "statistics"
        ),
        (
            "signal_analysis",
            "signal_analysis"
        ),
        (
            "decoding",
            "decoder"
        ),
        (
            "visualization",
            "visualization"
        ),
        (
            "output",
            "output"
        ),
    ):

        requested = get_request_list(
            specification,
            key
        )

        if any(
            value is not None
            and value is not False
            and not isinstance(
                value,
                bool
            )
            for value in requested
        ):

            required_roles.add(
                role
            )

    missing_roles = [
        role
        for role
        in sorted(
            required_roles
        )
        if role not in roles
    ]

    if missing_roles:

        errors = [
            (
                f"Required Master-DOC role "
                f"'{role}' is unavailable."
            )
            for role in missing_roles
        ]

        return GenerationResult(

            status="REJECTED",

            specification=
                generation_specification,

            errors=errors
        )

    # --------------------------------------------------------
    # RESOURCE RESOLUTION
    # --------------------------------------------------------

    print()

    print(
        "Resolving requested resources..."
    )

    resources, unresolved = (
        resolve_all_resources(
            specification,
            roles
        )
    )

    # --------------------------------------------------------
    # LOAD ERRORS
    # --------------------------------------------------------

    if load_errors:

        print()

        print(
            "Master-DOC load errors:"
        )

        for document_name, error in (
            load_errors.items()
        ):

            print(
                f"  ✗ {document_name}"
            )

            print(
                f"    {type(error).__name__}: "
                f"{error}"
            )

    # --------------------------------------------------------
    # DEPENDENCIES
    # --------------------------------------------------------

    dependencies = (
        resolve_dependencies(
            resources
        )
    )

    dependencies = (
        deduplicate_imports(
            dependencies
        )
    )

    # --------------------------------------------------------
    # ORDER
    # --------------------------------------------------------

    resources = (
        order_resources(
            resources
        )
    )

    stages = (
        extract_stage_names(
            resources
        )
    )

    # --------------------------------------------------------
    # COMPATIBILITY
    # --------------------------------------------------------

    compatibility = (
        check_compatibility(
            specification,
            resources
        )
    )

    # --------------------------------------------------------
    # RESOLUTION REPORT
    # --------------------------------------------------------

    print()

    print(
        "=" * 70
    )

    print(
        "RESOURCE RESOLUTION"
    )

    print(
        "=" * 70
    )

    print()

    print(
        f"Resolved resources: "
        f"{len(resources)}"
    )

    for resource in resources:

        print(
            f"  ✓ "
            f"{resource.requested_name}"
            f" -> "
            f"{resource.master_doc}"
            f" -> "
            f"{resource.resolved_name}"
        )

        if resource.function_name:

            print(
                f"      function: "
                f"{resource.function_name}"
            )

        print(
            f"      source acquired: "
            f"{resource.source_acquired}"
        )

    if unresolved:

        print()

        print(
            "Unresolved resources:"
        )

        for role, name in unresolved:

            print(
                f"  ✗ "
                f"{role}: "
                f"{name}"
            )

    # --------------------------------------------------------
    # HARD SOURCE-ACQUISITION GATE
    # --------------------------------------------------------
    #
    # This is the critical correction.
    #
    # A resource without source cannot enter the generator.
    # --------------------------------------------------------

    resources_without_source = [

        resource

        for resource
        in resources

        if not resource.source_acquired
    ]

    if resources_without_source:

        for resource in resources_without_source:

            unresolved.append(
                (
                    resource.role,
                    resource.requested_name
                )
            )

        unresolved = list(
            dict.fromkeys(
                unresolved
            )
        )

    if unresolved:

        errors = [

            (
                f"{role}: {name} "
                f"could not be acquired from its "
                f"designated Master-DOC."
            )

            for role, name
            in unresolved
        ]

        return GenerationResult(

            status="REJECTED",

            specification=
                generation_specification,

            resolved_resources=
                resources,

            unresolved_resources=[
                f"{role}: {name}"
                for role, name
                in unresolved
            ],

            dependencies=
                dependencies,

            stages=
                stages,

            compatibility=
                compatibility,

            errors=
                errors
        )

    # --------------------------------------------------------
    # COMPATIBILITY GATE
    # --------------------------------------------------------

    if not compatibility[
        "compatible"
    ]:

        return GenerationResult(

            status="REJECTED",

            specification=
                generation_specification,

            resolved_resources=
                resources,

            dependencies=
                dependencies,

            stages=
                stages,

            compatibility=
                compatibility,

            errors=
                compatibility[
                    "errors"
                ]
        )

    # --------------------------------------------------------
    # ASSEMBLY
    # --------------------------------------------------------

    print()

    print(
        "Assembling pipeline source..."
    )

    source_code = (
        assemble_source(
            specification,
            resources,
            dependencies
        )
    )

    # --------------------------------------------------------
    # SOURCE VALIDATION
    # --------------------------------------------------------

    source_validation = (
        validate_generated_source(
            source_code
        )
    )

    if not source_validation[
        "valid"
    ]:

        return GenerationResult(

            status="REJECTED",

            specification=
                generation_specification,

            resolved_resources=
                resources,

            dependencies=
                dependencies,

            stages=
                stages,

            compatibility=
                compatibility,

            source_code=
                source_code,

            errors=
                source_validation[
                    "errors"
                ]
        )

    # --------------------------------------------------------
    # WRITE
    # --------------------------------------------------------

    generated_file = (
        write_generated_pipeline(
            source_code,
            output_path
        )
    )

    # --------------------------------------------------------
    # SUCCESS
    # --------------------------------------------------------

    print()

    print(
        "=" * 70
    )

    print(
        "PIPELINE GENERATED"
    )

    print(
        "=" * 70
    )

    print()

    print(
        f"Generated file:"
    )

    print(
        f"  {generated_file}"
    )

    print()

    print(
        f"Resources: "
        f"{len(resources)}"
    )

    print(
        f"Dependencies: "
        f"{len(dependencies)}"
    )

    print(
        f"Stages: "
        f"{', '.join(stages)}"
    )

    print()

    return GenerationResult(

        status="GENERATED",

        specification=
            generation_specification,

        resolved_resources=
            resources,

        dependencies=
            dependencies,

        stages=
            stages,

        compatibility=
            compatibility,

        source_code=
            source_code,

        generated_file=
            generated_file
    )


# ============================================================
# PUBLIC ENTRY POINT
# ============================================================

def generate_pipeline(
    generation_specification: Any,
    output_path: Path | None = None
) -> GenerationResult:

    return generate(
        generation_specification,
        output_path
    )


# ============================================================
# OBJECT RECEIVER
# ============================================================

def receive_generation_specification(
    generation_specification: Any
) -> GenerationResult:

    return generate(
        generation_specification
    )


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    test_specification = {

        "neural_data":
            "EEG",

        "file_type":
            ".edf",

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
        ],

        "signal_analysis": [

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

    result = generate(
        test_specification
    )

    print()

    print(
        "=" * 70
    )

    print(
        "GENERATION RESULT"
    )

    print(
        "=" * 70
    )

    print()

    print(
        f"Status: "
        f"{result.status}"
    )

    if result.generated_file:

        print(
            f"Output: "
            f"{result.generated_file}"
        )

    if result.errors:

        print()

        print(
            "Errors:"
        )

        for error in result.errors:

            print(
                f"  - {error}"
            )

    print()


