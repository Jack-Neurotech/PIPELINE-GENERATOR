
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
#          +----> acquire requested resources
#          |
#          +----> resolve dependencies
#          |
#          +----> apply compatibility/order
#          |
#          +----> acquire source code
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
# Scientific implementations come from the Master-DOC library.
#
# The generator selects, organizes, and assembles those existing
# resources into a pipeline.
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
    GENERATED_DIRECTORY / "generated_pipeline.py"
)


# ============================================================
# MASTER-DOC ROLE PATTERNS
# ============================================================
#
# These are intentionally broader than the previous version.
#
# The generator should not fail merely because a Master-DOC
# filename uses a slightly different spelling.
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
# PARAMETER → FUNCTION ALIASES
# ============================================================

RESOURCE_ALIASES = {

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
    ),

    "median": (
        "median",
        "calculate_median",
        "compute_median",
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
    ),

    "std": (
        "std",
        "standard_deviation",
        "calculate_standard_deviation",
        "calculate_std",
        "compute_standard_deviation",
    ),

    "rms": (
        "rms",
        "calculate_rms",
        "compute_rms",
        "root_mean_square",
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

        "signal_analysis":
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

            for path
            in MASTER_DOC_DIRECTORY.iterdir()

            if (
                path.is_file()
                and
                path.suffix.lower() == ".py"
                and
                not path.name.startswith(".")
                and
                "__pycache__" not in path.parts
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
# LOAD COMPLETE MASTER-DOC LIBRARY
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

        normalized_pattern = (
            normalize_name(
                pattern
            )
        )

        if (
            normalized_document
            ==
            normalized_pattern
        ):

            return True

        if normalized_pattern in normalized_document:

            return True

        if normalized_document in normalized_pattern:

            return True

    return False


# ============================================================
# CONTENT-BASED ROLE DETECTION
# ============================================================
#
# Filename matching is the primary method.
#
# Content matching is the fallback.
#
# This is important because the generator should not depend
# upon a single exact filename spelling.
# ============================================================

def infer_role_from_module(
    document_name: str,
    module: ModuleType
) -> str | None:

    normalized_document = normalize_name(
        Path(
            document_name
        ).stem
    )

    # --------------------------------------------------------
    # FIRST: filename evidence
    # --------------------------------------------------------

    for role in MASTER_DOC_ROLE_PATTERNS:

        if role_matches_document(
            role,
            document_name
        ):

            return role

    # --------------------------------------------------------
    # SECOND: function-name evidence
    # --------------------------------------------------------

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

    # Preprocessing evidence.

    preprocessing_terms = (
        "bandpass",
        "band_pass",
        "notch",
        "lowpass",
        "low_pass",
        "highpass",
        "high_pass",
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

    # Statistics evidence.

    statistics_terms = (
        "calculate_mean",
        "calculate_median",
        "calculate_variance",
        "calculate_std",
        "calculate_standard_deviation",
        "calculate_rms",
        "calculate_skewness",
        "calculate_kurtosis",
    )

    if any(
        term in function_text
        for term in statistics_terms
    ):

        return "statistics"

    # Signal analysis evidence.

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

    # Ingestion evidence.

    ingestion_terms = (
        "load_eeg",
        "read_eeg",
        "ingest",
        "load_data",
        "read_data",
        "edf",
        "eeglab",
        "eeg",
    )

    if any(
        term in (
            normalized_document
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

            # Do not overwrite a more specific match
            # with a later fallback match.

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

    if normalized not in aliases:

        aliases.append(
            normalized
        )

    return aliases


# ============================================================
# FUNCTION CANDIDATE LIST
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

            functions.append(
                name
            )

    return sorted(
        functions,
        key=str.lower
    )


# ============================================================
# DIAGNOSTIC FUNCTION SEARCH
# ============================================================

def diagnostic_function_search(
    module: ModuleType,
    requested_name: str
) -> list[str]:

    aliases = {
        normalize_name(
            value
        )
        for value
        in get_resource_aliases(
            requested_name
        )
    }

    candidates = []

    for function_name in list_module_functions(
        module
    ):

        normalized_function = (
            normalize_name(
                function_name
            )
        )

        for alias in aliases:

            if (
                normalized_function == alias
                or
                alias in normalized_function
                or
                normalized_function in alias
            ):

                candidates.append(
                    function_name
                )

                break

    return sorted(
        set(candidates),
        key=str.lower
    )


# ============================================================
# FIND FUNCTION BY ALIASES
# ============================================================

def find_function_by_aliases(
    module: ModuleType,
    requested_name: str
):

    aliases = get_resource_aliases(
        requested_name
    )

    normalized_aliases = [
        normalize_name(
            alias
        )
        for alias
        in aliases
    ]

    # --------------------------------------------------------
    # EXACT NORMALIZED MATCH
    # --------------------------------------------------------

    for function_name in list_module_functions(
        module
    ):

        normalized_function = normalize_name(
            function_name
        )

        if normalized_function in normalized_aliases:

            return getattr(
                module,
                function_name
            )

    # --------------------------------------------------------
    # CONTAINMENT MATCH
    # --------------------------------------------------------

    for function_name in list_module_functions(
        module
    ):

        normalized_function = normalize_name(
            function_name
        )

        for alias in normalized_aliases:

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
# FIND RESOURCE IN MODULE
# ============================================================

def find_named_resource(
    module: ModuleType | None,
    requested_name: str
):

    if module is None:

        return None

    aliases = get_resource_aliases(
        requested_name
    )

    normalized_aliases = {
        normalize_name(
            alias
        )
        for alias
        in aliases
    }

    # --------------------------------------------------------
    # DIRECT FUNCTION / ATTRIBUTE SEARCH
    # --------------------------------------------------------

    for attribute_name in dir(module):

        if attribute_name.startswith("__"):

            continue

        normalized_attribute = (
            normalize_name(
                attribute_name
            )
        )

        if normalized_attribute not in normalized_aliases:

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
    # FUNCTION ALIAS SEARCH
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
    # RESOURCE DICTIONARIES
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

            if normalized_key in normalized_aliases:

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

                    metadata_value = (
                        value.get(
                            metadata_key
                        )
                    )

                    if metadata_value is None:

                        continue

                    if (
                        normalize_name(
                            metadata_value
                        )
                        in
                        normalized_aliases
                    ):

                        return (
                            str(key),
                            value
                        )

    return None


# ============================================================
# RESOURCE SOURCE
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

    source_code = get_resource_source(
        resource
    )

    function_name = None

    if callable(resource):

        function_name = getattr(
            resource,
            "__name__",
            None
        )

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
        }
    )


# ============================================================
# SEARCH ENTIRE MASTER-DOC LIBRARY
# ============================================================
#
# This is the critical fallback.
#
# The generator first searches the Master-DOC associated with
# the requested role.
#
# If the role-specific Master-DOC does not expose the requested
# resource, the generator searches the entire loaded library.
#
# This prevents exact filename/role assumptions from blocking
# otherwise valid resources.
# ============================================================

def resolve_resource_across_library(
    role: str,
    requested_name: str,
    roles: dict[str, ModuleType],
    loaded_docs: dict[str, ModuleType]
):

    # --------------------------------------------------------
    # PRIMARY SEARCH
    # --------------------------------------------------------

    primary_module = roles.get(
        role
    )

    primary_name = (
        role.replace(
            "_",
            "-"
        )
        .title()
    )

    print(
        f"  Searching role '{role}'"
    )

    if primary_module is not None:

        print(
            f"    Primary Master-DOC: "
            f"{primary_module.__name__}"
        )

        print(
            f"    Requested resource: "
            f"{requested_name}"
        )

        aliases = get_resource_aliases(
            requested_name
        )

        print(
            f"    Aliases: "
            f"{', '.join(aliases)}"
        )

        resource = resolve_resource(
            primary_module,
            role,
            requested_name,
            primary_name
        )

        if resource is not None:

            print(
                f"    ✓ Found in primary "
                f"Master-DOC: "
                f"{resource.resolved_name}"
            )

            return resource

        print(
            "    ✗ Not found in primary "
            "Master-DOC."
        )

        candidates = (
            diagnostic_function_search(
                primary_module,
                requested_name
            )
        )

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
                "    Candidate functions: "
                "none"
            )

    else:

        print(
            f"    ✗ No Master-DOC role "
            f"resolved for '{role}'."
        )

    # --------------------------------------------------------
    # LIBRARY-WIDE FALLBACK
    # --------------------------------------------------------

    print(
        "    Searching complete "
        "Master-DOC library..."
    )

    for document_name, module in (
        loaded_docs.items()
    ):

        if (
            primary_module is not None
            and
            module is primary_module
        ):

            continue

        resource = resolve_resource(
            module,
            role,
            requested_name,
            Path(
                document_name
            ).stem
        )

        if resource is not None:

            print(
                f"    ✓ Found in fallback "
                f"Master-DOC: "
                f"{document_name}"
            )

            return resource

    print(
        "    ✗ Resource not found "
        "anywhere in Master-DOC library."
    )

    return None


# ============================================================
# RESOLVE INGESTION
# ============================================================

def resolve_ingestion(
    specification: dict[str, Any],
    roles: dict[str, ModuleType],
    loaded_docs: dict[str, ModuleType]
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

    # --------------------------------------------------------
    # Explicit candidates
    # --------------------------------------------------------

    for candidate in candidates:

        resource = (
            resolve_resource_across_library(
                "ingestion",
                candidate,
                roles,
                loaded_docs
            )
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
    roles: dict[str, ModuleType],
    loaded_docs: dict[str, ModuleType]
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
            or
            requested_name is False
        ):

            continue

        if isinstance(
            requested_name,
            bool
        ):

            continue

        resource = (
            resolve_resource_across_library(
                role,
                str(requested_name),
                roles,
                loaded_docs
            )
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
    roles: dict[str, ModuleType],
    loaded_docs: dict[str, ModuleType]
):

    resolved = []

    unresolved = []

    # --------------------------------------------------------
    # INGESTION
    # --------------------------------------------------------

    ingestion_resources = (
        resolve_ingestion(
            specification,
            roles,
            loaded_docs
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

    # --------------------------------------------------------
    # COMPONENT ROLES
    # --------------------------------------------------------

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
                roles,
                loaded_docs
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

    # --------------------------------------------------------
    # DEPENDENCY ORDER
    # --------------------------------------------------------

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
            # This file was assembled by generator.py.
            #
            # Scientific implementations originate from the
            # PIPELINE-GENERATOR Master-DOC library.
            #
            # ============================================================
            """
        ).strip()
    )

    # --------------------------------------------------------
    # IMPORTS
    # --------------------------------------------------------

    import_lines = []

    for dependency in dependencies:

        if dependency.startswith(
            "__"
        ):

            continue

        import_lines.append(
            f"import {dependency}"
        )

    if import_lines:

        sections.append(
            "\n".join(
                [
                    "# ============================================================",
                    "# IMPORTS ACQUIRED FROM MASTER-DOC RESOURCES",
                    "# ============================================================",
                    *sorted(
                        set(
                            import_lines
                        )
                    ),
                ]
            )
        )

    # --------------------------------------------------------
    # RESOURCE SOURCE
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # PIPELINE CONFIGURATION
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # EXECUTION SHELL
    # --------------------------------------------------------

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

    # ========================================================
    # STEP 1 — RECEIVE OBJECT
    # ========================================================

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

    # ========================================================
    # STEP 2 — LOAD MASTER-DOC LIBRARY
    # ========================================================

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

            status=
                "FAILED",

            specification=
                generation_specification,

            errors=[
                str(error)
            ]
        )

    # ========================================================
    # STEP 3 — IDENTIFY ROLES
    # ========================================================

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

    # ========================================================
    # STEP 4 — RESOURCE RESOLUTION
    # ========================================================

    print()

    print(
        "Resolving requested resources..."
    )

    resources, unresolved = (
        resolve_all_resources(
            specification,
            roles,
            loaded_docs
        )
    )

    # ========================================================
    # STEP 5 — MASTER-DOC LOAD ERRORS
    # ========================================================

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

    # ========================================================
    # STEP 6 — DEPENDENCIES
    # ========================================================

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

    # ========================================================
    # STEP 7 — ORDER
    # ========================================================

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

    # ========================================================
    # STEP 8 — COMPATIBILITY
    # ========================================================

    compatibility = (
        check_compatibility(
            specification,
            resources
        )
    )

    # ========================================================
    # STEP 9 — RESOLUTION REPORT
    # ========================================================

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
            f"{bool(resource.source_code)}"
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

    # ========================================================
    # STEP 10 — STOP IF RESOURCE RESOLUTION FAILED
    # ========================================================

    if unresolved:

        return GenerationResult(

            status=
                "PARTIAL",

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

            errors=[
                f"{role}: {name}"
                for role, name
                in unresolved
            ]
        )

    # ========================================================
    # STEP 11 — COMPATIBILITY
    # ========================================================

    if not compatibility[
        "compatible"
    ]:

        return GenerationResult(

            status=
                "REJECTED",

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

    # ========================================================
    # STEP 12 — ASSEMBLE SOURCE
    # ========================================================

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

    # ========================================================
    # STEP 13 — VALIDATE SOURCE
    # ========================================================

    source_validation = (
        validate_generated_source(
            source_code
        )
    )

    if not source_validation[
        "valid"
    ]:

        return GenerationResult(

            status=
                "REJECTED",

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

    # ========================================================
    # STEP 14 — WRITE PIPELINE
    # ========================================================

    generated_file = (
        write_generated_pipeline(
            source_code,
            output_path
        )
    )

    # ========================================================
    # STEP 15 — SUCCESS
    # ========================================================

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

        status=
            "GENERATED",

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
# COMPATIBILITY ENTRY POINT
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

