# ============================================================
# PIPELINE GENERATOR
# ============================================================
#
# generator.py is the factory/compiler layer.
#
# ARCHITECTURE
#
#     Ingestion.py
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
#          +----> load Master-DOCs
#          |
#          +----> identify Master-DOC roles
#          |
#          +----> acquire requested resources
#          |
#          +----> resolve dependencies
#          |
#          +----> check compatibility
#          |
#          +----> assemble pipeline
#          |
#          v
#     generated/generated_pipeline.py
#
# IMPORTANT
#
# generator.py does NOT invent scientific algorithms.
#
# It acquires the actual resources defined by the Master-DOCs.
#
# Master-DOC resources may be:
#
#     1. functions
#     2. dictionaries
#     3. named constants
#     4. structured resource definitions
#
# Therefore a resource such as:
#
#     EEG
#
# does NOT have to be a Python function called EEG.
#
# In Master-DOC-Ingestion.py, EEG is represented through
# resource definitions such as EEG_EEGLAB and EEG_CSV.
#
# Likewise:
#
#     bandpass_filter
#
# maps to the actual Master-DOC function:
#
#     band_pass_filter
#
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

GENERATED_FILE = (
    GENERATED_DIRECTORY /
    "generated_pipeline.py"
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

    "signal_analysis": (
        "master-doc-signal-analysis",
        "master-doc-signal_analysis",
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

    "generator": (
        "master-doc-generator",
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
        "eeg_eeglab",
        "eeg_csv",
    ),

    "edf": (
        "edf",
        "eeg_edf",
    ),

    "set": (
        "set",
        "eeg_eeglab",
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
# PIPELINE ORDER
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

    resource_type: str

    source_code: str

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

def normalize_role(
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
# DISCOVER MASTER-DOCS
# ============================================================

def discover_master_docs() -> list[Path]:

    if not MASTER_DOC_DIRECTORY.exists():

        raise FileNotFoundError(
            "Master-DOC directory not found:\n"
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

    spec = importlib.util.spec_from_loader(
        module_name,
        loader
    )

    if spec is None:

        raise ImportError(
            f"Could not create module specification "
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

def load_master_docs():

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

            loaded[path.name] = (
                load_master_doc(
                    path
                )
            )

            print(
                "      ✓ loaded"
            )

        except Exception as error:

            errors[path.name] = error

            print(
                "      ✗ failed: "
                f"{type(error).__name__}: "
                f"{error}"
            )

    return (
        loaded,
        errors
    )


# ============================================================
# ROLE DETECTION
# ============================================================

def identify_roles(
    loaded_docs
):

    roles = {}

    for document_name, module in (
        loaded_docs.items()
    ):

        normalized_document = (
            normalize_name(
                Path(
                    document_name
                ).stem
            )
        )

        for role, patterns in (
            MASTER_DOC_ROLE_PATTERNS.items()
        ):

            matched = False

            for pattern in patterns:

                normalized_pattern = (
                    normalize_name(
                        pattern
                    )
                )

                if (
                    normalized_document ==
                    normalized_pattern
                    or
                    normalized_pattern
                    in normalized_document
                ):

                    matched = True
                    break

            if matched:

                roles[role] = module
                break

    return roles


# ============================================================
# RESOURCE ALIASES
# ============================================================

def get_aliases(
    requested_name: str
) -> set[str]:

    normalized = normalize_name(
        requested_name
    )

    aliases = {
        normalize_name(
            value
        )
        for value
        in RESOURCE_ALIASES.get(
            normalized,
            ()
        )
    }

    aliases.add(
        normalized
    )

    return aliases


# ============================================================
# READ SOURCE
# ============================================================

def read_source(
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
# AST PARSE
# ============================================================

def parse_source(
    source: str
):

    try:

        return ast.parse(
            source
        )

    except SyntaxError:

        return None


# ============================================================
# AST NODE NAME
# ============================================================

def ast_node_name(
    node
):

    if isinstance(
        node,
        (
            ast.FunctionDef,
            ast.AsyncFunctionDef,
            ast.ClassDef
        )
    ):

        return node.name

    return None


# ============================================================
# MATCH AST NODE
# ============================================================

def node_matches(
    node,
    aliases: set[str]
) -> bool:

    node_name = ast_node_name(
        node
    )

    if node_name:

        normalized = normalize_name(
            node_name
        )

        if normalized in aliases:
            return True

        for alias in aliases:

            if (
                alias in normalized
                or
                normalized in alias
            ):

                return True

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

            if not target_name:
                continue

            normalized = normalize_name(
                target_name
            )

            if normalized in aliases:
                return True

    return False


# ============================================================
# SOURCE SEGMENT
# ============================================================

def source_segment(
    source: str,
    node
) -> str:

    try:

        return textwrap.dedent(
            ast.get_source_segment(
                source,
                node
            ) or ""
        ).strip()

    except Exception:

        return ""


# ============================================================
# ACQUIRE RESOURCE FROM MASTER-DOC
# ============================================================
#
# This is the central correction.
#
# We do NOT require the resource to be a callable.
#
# We inspect:
#
#     functions
#     dictionaries
#     constants
#     resource definitions
#
# directly from the Master-DOC source.
# ============================================================

def acquire_resource(
    module: ModuleType,
    requested_name: str
):

    source = read_source(
        module
    )

    if not source:
        return None

    tree = parse_source(
        source
    )

    if tree is None:
        return None

    aliases = get_aliases(
        requested_name
    )

    # --------------------------------------------------------
    # PASS 1
    # Exact function / assignment match.
    # --------------------------------------------------------

    exact_matches = []

    for node in tree.body:

        node_name = ast_node_name(
            node
        )

        if node_name:

            if normalize_name(
                node_name
            ) in aliases:

                exact_matches.append(
                    node
                )

        elif isinstance(
            node,
            ast.Assign
        ):

            for target in node.targets:

                target_name = getattr(
                    target,
                    "id",
                    None
                )

                if not target_name:
                    continue

                if normalize_name(
                    target_name
                ) in aliases:

                    exact_matches.append(
                        node
                    )

    # --------------------------------------------------------
    # PASS 2
    # Semantic/alias match.
    # --------------------------------------------------------

    if not exact_matches:

        for node in tree.body:

            if node_matches(
                node,
                aliases
            ):

                exact_matches.append(
                    node
                )

    if exact_matches:

        node = exact_matches[0]

        source_code = (
            source_segment(
                source,
                node
            )
        )

        if source_code:

            node_name = ast_node_name(
                node
            )

            resource_type = (
                "function"
                if isinstance(
                    node,
                    (
                        ast.FunctionDef,
                        ast.AsyncFunctionDef
                    )
                )
                else
                "resource_definition"
            )

            return {
                "requested_name":
                    requested_name,

                "resolved_name":
                    node_name
                    or
                    requested_name,

                "resource_type":
                    resource_type,

                "source_code":
                    source_code,

                "function_name":
                    node_name,

                "master_doc":
                    module.__name__,

                "source_file":
                    getattr(
                        module,
                        "__file__",
                        None
                    ),
            }

    # --------------------------------------------------------
    # PASS 3
    # INGESTION MODALITY RESOLUTION.
    #
    # "EEG" is a conceptual modality.
    #
    # The ingestion Master-DOC defines concrete resources
    # such as EEG_EEGLAB and EEG_CSV.
    # --------------------------------------------------------

    if normalize_name(
        requested_name
    ) == "eeg":

        eeg_candidates = (
            "EEG_EEGLAB",
            "EEG_CSV",
        )

        for candidate in eeg_candidates:

            candidate_aliases = {
                normalize_name(
                    candidate
                )
            }

            for node in tree.body:

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

                        if not target_name:
                            continue

                        if normalize_name(
                            target_name
                        ) not in candidate_aliases:
                            continue

                        source_code = (
                            source_segment(
                                source,
                                node
                            )
                        )

                        if source_code:

                            return {
                                "requested_name":
                                    requested_name,

                                "resolved_name":
                                    target_name,

                                "resource_type":
                                    "ingestion_definition",

                                "source_code":
                                    source_code,

                                "function_name":
                                    None,

                                "master_doc":
                                    module.__name__,

                                "source_file":
                                    getattr(
                                        module,
                                        "__file__",
                                        None
                                    ),
                            }

    return None


# ============================================================
# EXTRACT IMPORTS FROM MASTER-DOC
# ============================================================

def extract_imports(
    source: str
) -> list[str]:

    tree = parse_source(
        source
    )

    if tree is None:
        return []

    imports = []

    for node in tree.body:

        if isinstance(
            node,
            ast.Import
        ):

            for alias in node.names:

                imports.append(
                    f"import {alias.name}"
                )

        elif isinstance(
            node,
            ast.ImportFrom
        ):

            module = node.module

            if not module:
                continue

            names = ", ".join(
                alias.name
                for alias in node.names
            )

            imports.append(
                f"from {module} import {names}"
            )

    return imports


# ============================================================
# EXTRACT DEPENDENCIES
# ============================================================

def extract_dependencies(
    source: str
) -> list[str]:

    tree = parse_source(
        source
    )

    if tree is None:
        return []

    dependencies = []

    for node in ast.walk(
        tree
    ):

        if isinstance(
            node,
            ast.Import
        ):

            for alias in node.names:

                if alias.name not in dependencies:

                    dependencies.append(
                        alias.name
                    )

        elif isinstance(
            node,
            ast.ImportFrom
        ):

            if (
                node.module
                and
                node.module not in dependencies
            ):

                dependencies.append(
                    node.module
                )

    return dependencies


# ============================================================
# RESOLVE ONE RESOURCE
# ============================================================

def resolve_one(
    role: str,
    requested_name: str,
    roles
):

    module = roles.get(
        role
    )

    if module is None:

        print(
            f"    ✗ No Master-DOC for role "
            f"'{role}'"
        )

        return None

    print(
        f"  Searching role '{role}'"
    )

    print(
        f"    Primary Master-DOC: "
        f"{module.__name__}"
    )

    print(
        f"    Requested resource: "
        f"{requested_name}"
    )

    print(
        f"    Aliases: "
        f"{', '.join(get_aliases(requested_name))}"
    )

    acquired = acquire_resource(
        module,
        requested_name
    )

    if acquired is None:

        print(
            "    ✗ Resource was not acquired "
            "from its designated Master-DOC."
        )

        return None

    source_code = acquired[
        "source_code"
    ]

    dependencies = extract_dependencies(
        source_code
    )

    resource = ResolvedResource(

        requested_name=
            requested_name,

        resolved_name=
            acquired[
                "resolved_name"
            ],

        role=
            role,

        master_doc=
            acquired[
                "master_doc"
            ],

        resource_type=
            acquired[
                "resource_type"
            ],

        source_code=
            source_code,

        function_name=
            acquired[
                "function_name"
            ],

        dependencies=
            dependencies,

        metadata={
            "source_acquired":
                True,

            "source_file":
                acquired[
                    "source_file"
                ],
        }
    )

    print(
        f"    ✓ Acquired source: "
        f"{resource.resolved_name}"
    )

    print(
        f"      type: "
        f"{resource.resource_type}"
    )

    return resource


# ============================================================
# REQUEST LIST
# ============================================================

def request_list(
    specification,
    key
):

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

        return list(
            value
        )

    return [value]


# ============================================================
# RESOLVE ALL RESOURCES
# ============================================================

def resolve_all_resources(
    specification,
    roles
):

    resolved = []

    unresolved = []

    # --------------------------------------------------------
    # INGESTION
    # --------------------------------------------------------

    neural_data = specification.get(
        "neural_data"
    )

    file_type = specification.get(
        "file_type"
    )

    if neural_data:

        resource = resolve_one(
            "ingestion",
            str(neural_data),
            roles
        )

        if resource:

            resolved.append(
                resource
            )

        else:

            unresolved.append(
                (
                    "ingestion",
                    str(neural_data)
                )
            )

    # --------------------------------------------------------
    # PREPROCESSING
    # --------------------------------------------------------

    for requested in request_list(
        specification,
        "preprocessing"
    ):

        resource = resolve_one(
            "preprocessing",
            str(requested),
            roles
        )

        if resource:

            resolved.append(
                resource
            )

        else:

            unresolved.append(
                (
                    "preprocessing",
                    str(requested)
                )
            )

    # --------------------------------------------------------
    # STATISTICS
    # --------------------------------------------------------

    for requested in request_list(
        specification,
        "statistics"
    ):

        resource = resolve_one(
            "statistics",
            str(requested),
            roles
        )

        if resource:

            resolved.append(
                resource
            )

        else:

            unresolved.append(
                (
                    "statistics",
                    str(requested)
                )
            )

    # --------------------------------------------------------
    # SIGNAL ANALYSIS
    # --------------------------------------------------------

    for requested in request_list(
        specification,
        "signal_analysis"
    ):

        resource = resolve_one(
            "signal_analysis",
            str(requested),
            roles
        )

        if resource:

            resolved.append(
                resource
            )

        else:

            unresolved.append(
                (
                    "signal_analysis",
                    str(requested)
                )
            )

    # --------------------------------------------------------
    # DECODING
    # --------------------------------------------------------

    for requested in request_list(
        specification,
        "decoder"
    ):

        if requested in (
            None,
            False
        ):

            continue

        resource = resolve_one(
            "decoding",
            str(requested),
            roles
        )

        if resource:

            resolved.append(
                resource
            )

        else:

            unresolved.append(
                (
                    "decoding",
                    str(requested)
                )
            )

    # --------------------------------------------------------
    # VISUALIZATION
    # --------------------------------------------------------

    visualization = specification.get(
        "visualization"
    )

    if (
        visualization
        and
        not isinstance(
            visualization,
            bool
        )
    ):

        for requested in request_list(
            specification,
            "visualization"
        ):

            resource = resolve_one(
                "visualization",
                str(requested),
                roles
            )

            if resource:

                resolved.append(
                    resource
                )

            else:

                unresolved.append(
                    (
                        "visualization",
                        str(requested)
                    )
                )

    return (
        resolved,
        unresolved
    )


# ============================================================
# ORDER RESOURCES
# ============================================================

def order_resources(
    resources
):

    order = {
        role: index
        for index, role
        in enumerate(
            PIPELINE_STAGE_ORDER
        )
    }

    return sorted(
        resources,
        key=lambda resource: (
            order.get(
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
    specification,
    resolved,
    unresolved
):

    errors = []

    # --------------------------------------------------------
    # Missing requested resources
    # --------------------------------------------------------

    for role, name in unresolved:

        errors.append(
            f"{role}: {name} could not be "
            "acquired from its designated Master-DOC."
        )

    # --------------------------------------------------------
    # File-type compatibility
    # --------------------------------------------------------
    #
    # EEG ingestion definitions currently expose:
    #
    #     .set
    #     .csv
    #
    # The current specification says .edf.
    #
    # Do not silently pretend EDF is supported.
    # --------------------------------------------------------

    neural_data = normalize_name(
        specification.get(
            "neural_data"
        )
    )

    file_type = normalize_name(
        specification.get(
            "file_type"
        )
    )

    if neural_data == "eeg":

        supported_eeg_extensions = {
            "set",
            "csv"
        }

        if file_type.startswith("."):

            file_type = file_type[1:]

        if (
            file_type
            and
            file_type not in supported_eeg_extensions
        ):

            errors.append(
                "EEG ingestion does not currently "
                f"support '.{file_type}'. "
                "The Master-DOC currently defines "
                "EEG ingestion for .set and .csv."
            )

    # --------------------------------------------------------
    # Downstream stages require ingestion.
    # --------------------------------------------------------

    resolved_roles = {
        resource.role
        for resource in resolved
    }

    if (
        "preprocessing"
        in resolved_roles
        and
        "ingestion"
        not in resolved_roles
    ):

        errors.append(
            "Preprocessing requires "
            "an ingestion stage."
        )

    if (
        "statistics"
        in resolved_roles
        and
        "ingestion"
        not in resolved_roles
    ):

        errors.append(
            "Statistics requires "
            "an ingestion stage."
        )

    if (
        "signal_analysis"
        in resolved_roles
        and
        "ingestion"
        not in resolved_roles
    ):

        errors.append(
            "Signal analysis requires "
            "an ingestion stage."
        )

    return {
        "compatible":
            not errors,

        "errors":
            errors
    }


# ============================================================
# ASSEMBLE SOURCE
# ============================================================

def assemble_source(
    specification,
    resources
):

    imports = []

    # --------------------------------------------------------
    # Acquire imports from the Master-DOC source files.
    # --------------------------------------------------------

    seen_imports = set()

    for resource in resources:

        source_file = resource.metadata.get(
            "source_file"
        )

        if not source_file:
            continue

        try:

            master_source = Path(
                source_file
            ).read_text(
                encoding="utf-8"
            )

        except Exception:

            continue

        for import_line in extract_imports(
            master_source
        ):

            if import_line not in seen_imports:

                seen_imports.add(
                    import_line
                )

                imports.append(
                    import_line
                )

    sections = []

    sections.append(
        "# ============================================================\n"
        "# GENERATED NEURAL PIPELINE\n"
        "# ============================================================\n"
        "#\n"
        "# Generated by PIPELINE-GENERATOR.\n"
        "#\n"
        "# Scientific resources were acquired from the designated\n"
        "# Master-DOCs. No scientific algorithm was invented here.\n"
        "# ============================================================\n"
    )

    if imports:

        sections.append(
            "\n".join(
                imports
            )
        )

    # --------------------------------------------------------
    # Add acquired source.
    # --------------------------------------------------------

    added = set()

    for resource in resources:

        source = resource.source_code.strip()

        if not source:
            continue

        identity = (
            resource.master_doc,
            resource.resolved_name
        )

        if identity in added:
            continue

        added.add(
            identity
        )

        sections.append(
            "\n"
            "# ============================================================\n"
            f"# SOURCE: {resource.master_doc}\n"
            f"# RESOURCE: {resource.resolved_name}\n"
            f"# ROLE: {resource.role}\n"
            "# ============================================================\n"
        )

        sections.append(
            source
        )

    # --------------------------------------------------------
    # Add a manifest describing the assembled pipeline.
    # --------------------------------------------------------

    manifest = {

        "neural_data":
            specification.get(
                "neural_data"
            ),

        "file_type":
            specification.get(
                "file_type"
            ),

        "pipeline_type":
            specification.get(
                "pipeline_type"
            ),

        "resources": [

            {
                "requested":
                    resource.requested_name,

                "resolved":
                    resource.resolved_name,

                "role":
                    resource.role,

                "master_doc":
                    resource.master_doc,

                "resource_type":
                    resource.resource_type,

            }

            for resource
            in resources
        ]
    }

    sections.append(
        "\n"
        "# ============================================================\n"
        "# PIPELINE MANIFEST\n"
        "# ============================================================\n"
        f"PIPELINE_MANIFEST = {manifest!r}\n"
    )

    return "\n\n".join(
        sections
    )


# ============================================================
# VALIDATE GENERATED SOURCE
# ============================================================

def validate_generated_source(
    source_code
):

    try:

        ast.parse(
            source_code
        )

        return {
            "valid":
                True,

            "error":
                None
        }

    except SyntaxError as error:

        return {
            "valid":
                False,

            "error":
                (
                    f"{type(error).__name__}: "
                    f"{error}"
                )
        }


# ============================================================
# WRITE GENERATED PIPELINE
# ============================================================

def write_generated_pipeline(
    source_code
):

    GENERATED_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True
    )

    GENERATED_FILE.write_text(
        source_code,
        encoding="utf-8"
    )

    return GENERATED_FILE


# ============================================================
# RECEIVE OBJECT
# ============================================================

def receive_generation_specification(
    specification
):

    print()

    print(
        "OBJECT RECEIVED"
    )

    print()

    normalized = specification_to_dict(
        specification
    )

    print(
        "Generation specification read."
    )

    print()

    print(
        "Specification contents:"
    )

    for key, value in normalized.items():

        print(
            f"  {key}: {value}"
        )

    return normalized


# ============================================================
# GENERATE PIPELINE
# ============================================================

def generate_pipeline(
    specification
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

    # --------------------------------------------------------
    # 1. RECEIVE OBJECT
    # --------------------------------------------------------

    specification = (
        receive_generation_specification(
            specification
        )
    )

    # --------------------------------------------------------
    # 2. LOAD MASTER-DOCS
    # --------------------------------------------------------

    print()
    print(
        "Loading Master-DOC library..."
    )

    loaded_docs, load_errors = (
        load_master_docs()
    )

    if load_errors:

        print()
        print(
            "Master-DOC loading errors:"
        )

        for name, error in (
            load_errors.items()
        ):

            print(
                f"  ✗ {name}: "
                f"{type(error).__name__}: "
                f"{error}"
            )

    print()
    print(
        "Resolving Master-DOC roles..."
    )

    roles = identify_roles(
        loaded_docs
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

    for role, module in sorted(
        roles.items()
    ):

        print(
            f"  ✓ {module.__name__} "
            f"-> {role}"
        )

    # --------------------------------------------------------
    # 3. RESOLVE RESOURCES
    # --------------------------------------------------------

    print()
    print(
        "Resolving requested resources..."
    )

    resolved, unresolved = (
        resolve_all_resources(
            specification,
            roles
        )
    )

    resolved = order_resources(
        resolved
    )

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
        f"{len(resolved)}"
    )

    for resource in resolved:

        print(
            f"  ✓ "
            f"{resource.requested_name}"
            f" -> "
            f"{resource.master_doc}"
            f" -> "
            f"{resource.resolved_name}"
        )

        print(
            f"      type: "
            f"{resource.resource_type}"
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
                f"  ✗ {role}: {name}"
            )

    # --------------------------------------------------------
    # 4. COMPATIBILITY
    # --------------------------------------------------------

    compatibility = (
        check_compatibility(
            specification,
            resolved,
            unresolved
        )
    )

    if not compatibility[
        "compatible"
    ]:

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
            "Status: REJECTED"
        )

        print()
        print(
            "Errors:"
        )

        for error in compatibility[
            "errors"
        ]:

            print(
                f"  - {error}"
            )

        return {
            "status":
                "REJECTED",

            "specification":
                specification,

            "resolved_resources":
                resolved,

            "unresolved_resources":
                unresolved,

            "compatibility":
                compatibility,

            "generated_file":
                None
        }

    # --------------------------------------------------------
    # 5. ASSEMBLE
    # --------------------------------------------------------

    print()
    print(
        "Assembling pipeline source..."
    )

    source_code = assemble_source(
        specification,
        resolved
    )

    # --------------------------------------------------------
    # 6. VALIDATE SOURCE
    # --------------------------------------------------------

    validation = (
        validate_generated_source(
            source_code
        )
    )

    if not validation[
        "valid"
    ]:

        print()
        print(
            "Generated source failed "
            "Python syntax validation."
        )

        print(
            validation[
                "error"
            ]
        )

        return {
            "status":
                "REJECTED",

            "specification":
                specification,

            "resolved_resources":
                resolved,

            "unresolved_resources":
                unresolved,

            "compatibility":
                compatibility,

            "generated_file":
                None,

            "error":
                validation[
                    "error"
                ]
        }

    # --------------------------------------------------------
    # 7. WRITE
    # --------------------------------------------------------

    generated_file = (
        write_generated_pipeline(
            source_code
        )
    )

    # --------------------------------------------------------
    # 8. SUCCESS
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
        "Generated file:"
    )

    print(
        f"  {generated_file}"
    )

    print()

    print(
        f"Resources: "
        f"{len(resolved)}"
    )

    print(
        "Stages: "
        +
        ", ".join(
            dict.fromkeys(
                resource.role
                for resource in resolved
            )
        )
    )

    print()
    print(
        "=" * 70
    )

    return {
        "status":
            "GENERATED",

        "specification":
            specification,

        "resolved_resources":
            resolved,

        "unresolved_resources":
            unresolved,

        "compatibility":
            compatibility,

        "source_code":
            source_code,

        "generated_file":
            generated_file
    }


# ============================================================
# OBJECT HANDOFF
# ============================================================
#
# analysis.py is the producer.
#
# If analysis.py exposes analyze(), generator.py can receive
# its returned object directly.
# ============================================================

def receive_from_analysis(
    parameters
):

    analysis_path = (
        BASE_DIRECTORY /
        "analysis.py"
    )

    if not analysis_path.exists():

        raise FileNotFoundError(
            f"analysis.py not found at "
            f"{analysis_path}"
        )

    loader = SourceFileLoader(
        "pipeline_analysis",
        str(analysis_path)
    )

    spec = importlib.util.spec_from_loader(
        "pipeline_analysis",
        loader
    )

    if spec is None:

        raise ImportError(
            "Could not load analysis.py"
        )

    module = (
        importlib.util.module_from_spec(
            spec
        )
    )

    loader.exec_module(
        module
    )

    analyze = getattr(
        module,
        "analyze",
        None
    )

    if not callable(analyze):

        raise AttributeError(
            "analysis.py does not expose "
            "analyze(parameters)."
        )

    return analyze(
        parameters
    )


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # TEST OBJECT
    # --------------------------------------------------------
    #
    # This is only used when generator.py is run directly.
    #
    # The real application receives the object from analysis.py.
    # --------------------------------------------------------

    test_specification = {

        "neural_data":
            "EEG",

        "file_type":
            ".edf",

        "pipeline_type":
            "EEG",

        "preprocessing": [
            "bandpass_filter",
            "notch_filter"
        ],

        "statistics": [
            "mean",
            "std",
            "variance",
            "rms"
        ],

        "signal_analysis": [
            "spectral_power",
            "dominant_frequency"
        ],

        "decoder":
            None,

        "visualization":
            False,

        "output":
            None
    }

    generate_pipeline(
        test_specification
    )
