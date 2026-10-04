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
#          +----> load Master-DOCs
#          |
#          +----> identify Master-DOC roles
#          |
#          +----> acquire resources
#          |
#          +----> resolve dependencies
#          |
#          +----> assemble source
#          |
#          v
#     generated/generated_pipeline.py
#
# IMPORTANT:
#
# generator.py does NOT invent scientific algorithms.
#
# It acquires resources from the designated Master-DOCs.
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

from typing import Any
import ast
import importlib.util
import inspect
import re
import sys
import textwrap


# ============================================================
# PATHS
# ============================================================

BASE_DIRECTORY = (
    Path(__file__).resolve().parent
)

MASTER_DOC_DIRECTORY = (
    BASE_DIRECTORY /
    "Master-DOC's"
)

GENERATED_DIRECTORY = (
    BASE_DIRECTORY /
    "generated"
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

    # --------------------------------------------------------
    # STATISTICS
    # --------------------------------------------------------

    "mean": (
        "mean",
        "calculate_mean",
        "compute_mean",
        "extract_mean_features",
    ),

    "std": (
        "std",
        "standard_deviation",
        "calculate_standard_deviation",
        "calculate_std",
        "compute_standard_deviation",
        "extract_std_features",
    ),

    "variance": (
        "variance",
        "calculate_variance",
        "compute_variance",
        "extract_variance_features",
    ),

    "rms": (
        "rms",
        "calculate_rms",
        "compute_rms",
        "root_mean_square",
        "extract_rms_features",
    ),

    "median": (
        "median",
        "calculate_median",
        "compute_median",
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

    "dominant_frequency": (
        "dominant_frequency",
        "calculate_dominant_frequency",
        "compute_dominant_frequency",
        "find_dominant_frequency",
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
# RESOURCE OBJECT
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

    value = str(
        value
    )

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

    return value.strip(
        "_"
    )


# ============================================================
# NORMALIZE ROLE
# ============================================================

def normalize_role(
    value: Any
) -> str:

    value = normalize_name(
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
        value,
        value
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

        if name.startswith(
            "_"
        ):

            continue

        try:

            value = getattr(
                specification,
                name
            )

        except Exception:

            continue

        if callable(
            value
        ):

            continue

        result[
            name
        ] = value

    return result


# ============================================================
# FIND MASTER-DOC ROOT
# ============================================================
#
# Supports:
#
#     PIPELINE-GENERATOR/
#         Master-DOC's/
#
# and:
#
#     PIPELINE-GENERATOR/
#         Master-DOC's/
#             Master-DOC's/
#
# without changing the Master-DOC architecture.
# ============================================================

def find_master_doc_root() -> Path:

    candidates = [

        BASE_DIRECTORY /
        "Master-DOC's",

        BASE_DIRECTORY /
        "Master-DOC's" /
        "Master-DOC's",

    ]

    for candidate in candidates:

        if not candidate.is_dir():

            continue

        files = list(
            candidate.rglob(
                "*.py"
            )
        )

        if any(
            "master-doc-generator"
            in normalize_name(
                path.stem
            )
            for path in files
        ):

            return candidate

    # --------------------------------------------------------
    # Recursive fallback
    # --------------------------------------------------------

    for directory in (
        BASE_DIRECTORY.rglob(
            "*"
        )
    ):

        if not directory.is_dir():

            continue

        if (
            directory.name.lower()
            != "master-doc's"
        ):

            continue

        files = list(
            directory.rglob(
                "*.py"
            )
        )

        if any(
            "master-doc-generator"
            in normalize_name(
                path.stem
            )
            for path in files
        ):

            return directory

    raise FileNotFoundError(
        "Could not locate the Master-DOC library."
    )


# ============================================================
# DISCOVER MASTER-DOC FILES
# ============================================================

def discover_master_docs() -> list[Path]:

    root = (
        find_master_doc_root()
    )

    paths = sorted(
        (
            path
            for path
            in root.rglob(
                "*.py"
            )
            if (
                path.is_file()
                and
                not path.name.startswith(
                    "."
                )
                and
                "__pycache__"
                not in path.parts
            )
        ),
        key=lambda path:
            str(path).lower()
    )

    if not paths:

        raise FileNotFoundError(
            "Master-DOC directory exists, "
            "but no Python Master-DOC files were found."
        )

    return paths


# ============================================================
# LOAD ONE MASTER-DOC
# ============================================================
#
# CRITICAL:
#
# Register the dynamically created module in sys.modules
# BEFORE exec_module().
#
# This prevents the Python 3.14 dataclass failure.
# ============================================================

def load_master_doc(
    path: Path
) -> ModuleType:

    module_name = (
        "pipeline_master_doc_"
        +
        re.sub(
            r"[^A-Za-z0-9_]",
            "_",
            path.stem
        )
    )

    # Prevent collisions if nested directories contain
    # identically named files.
    module_name += (
        "_"
        +
        str(
            abs(
                hash(
                    str(path)
                )
            )
        )
    )

    loader = SourceFileLoader(
        module_name,
        str(path)
    )

    specification = (
        importlib.util.spec_from_loader(
            module_name,
            loader
        )
    )

    if specification is None:

        raise ImportError(
            f"Could not create module specification "
            f"for {path}"
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
        module_name
    ] = module

    try:

        loader.exec_module(
            module
        )

    except Exception:

        sys.modules.pop(
            module_name,
            None
        )

        raise

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
                "      ✗ failed: "
                f"{type(error).__name__}: "
                f"{error}"
            )

    return (
        loaded,
        errors
    )


# ============================================================
# IDENTIFY MASTER-DOC ROLES
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
                    or
                    normalized_pattern
                    in normalized_document
                ):

                    roles[
                        role
                    ] = module

                    break

            if role in roles:

                break

    return roles


# ============================================================
# GET RESOURCE ALIASES
# ============================================================

def get_aliases(
    requested_name: str
) -> set[str]:

    normalized = normalize_name(
        requested_name
    )

    aliases = {
        normalize_name(
            alias
        )
        for alias
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
# SOURCE FILE
# ============================================================

def module_source(
    module: ModuleType
) -> str:

    path = getattr(
        module,
        "__file__",
        None
    )

    if not path:

        return ""

    try:

        return Path(
            path
        ).read_text(
            encoding="utf-8"
        )

    except Exception:

        return ""


# ============================================================
# SOURCE OF OBJECT
# ============================================================

def source_of_object(
    obj: Any
) -> str:

    if inspect.isfunction(
        obj
    ) or inspect.isclass(
        obj
    ):

        try:

            return textwrap.dedent(
                inspect.getsource(
                    obj
                )
            )

        except (
            OSError,
            TypeError
        ):

            return ""

    return ""


# ============================================================
# RECURSIVE RESOURCE SEARCH
# ============================================================
#
# Search a Master-DOC's module namespace.
#
# The search understands:
#
#     functions
#     dictionaries
#     lists
#     tuples
#     structured resource definitions
#
# It NEVER searches another role.
# ============================================================

def find_resource_in_module(
    module: ModuleType,
    requested_name: str
):

    aliases = get_aliases(
        requested_name
    )

    visited = set()

    # --------------------------------------------------------
    # DIRECT MODULE ATTRIBUTES
    # --------------------------------------------------------

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

        result = inspect_resource_value(
            value,
            attribute_name,
            aliases,
            visited
        )

        if result is not None:

            return result

    return None


# ============================================================
# INSPECT RESOURCE VALUE
# ============================================================

def inspect_resource_value(
    value: Any,
    object_name: str,
    aliases: set[str],
    visited: set[int]
):

    identity = id(
        value
    )

    if identity in visited:

        return None

    visited.add(
        identity
    )

    normalized_object_name = (
        normalize_name(
            object_name
        )
    )

    # --------------------------------------------------------
    # FUNCTION
    # --------------------------------------------------------

    if callable(
        value
    ):

        if (
            normalized_object_name
            in aliases
        ):

            source = source_of_object(
                value
            )

            if source:

                return {
                    "resource_type":
                        "function",

                    "resolved_name":
                        object_name,

                    "function_name":
                        getattr(
                            value,
                            "__name__",
                            object_name
                        ),

                    "source_code":
                        source,

                    "metadata":
                        {},
                }

        return None

    # --------------------------------------------------------
    # DICTIONARY
    # --------------------------------------------------------

    if isinstance(
        value,
        dict
    ):

        # First check whether the dictionary itself is a
        # named resource.
        dictionary_names = []

        for key in (
            "name",
            "id",
            "resource",
            "resource_name",
            "type",
            "kind",
            "key",
        ):

            if key in value:

                dictionary_names.append(
                    value[key]
                )

        dictionary_names.append(
            object_name
        )

        normalized_names = {
            normalize_name(
                name
            )
            for name in dictionary_names
            if name is not None
        }

        if normalized_names & aliases:

            return {
                "resource_type":
                    "resource_definition",

                "resolved_name":
                    object_name,

                "function_name":
                    None,

                "source_code":
                    format_resource_definition(
                        object_name,
                        value
                    ),

                "metadata":
                    dict(
                        value
                    ),
            }

        # Search dictionary keys.
        for key, nested_value in (
            value.items()
        ):

            normalized_key = (
                normalize_name(
                    key
                )
            )

            if normalized_key in aliases:

                source = (
                    source_of_object(
                        nested_value
                    )
                )

                if source:

                    return {
                        "resource_type":
                            "function",

                        "resolved_name":
                            str(key),

                        "function_name":
                            getattr(
                                nested_value,
                                "__name__",
                                str(key)
                            ),

                        "source_code":
                            source,

                        "metadata":
                            {},
                    }

                if isinstance(
                    nested_value,
                    dict
                ):

                    return {
                        "resource_type":
                            "resource_definition",

                        "resolved_name":
                            str(key),

                        "function_name":
                            None,

                        "source_code":
                            format_resource_definition(
                                str(key),
                                nested_value
                            ),

                        "metadata":
                            dict(
                                nested_value
                            ),
                    }

            nested_result = (
                inspect_resource_value(
                    nested_value,
                    str(key),
                    aliases,
                    visited
                )
            )

            if nested_result is not None:

                return nested_result

        return None

    # --------------------------------------------------------
    # LIST / TUPLE / SET
    # --------------------------------------------------------

    if isinstance(
        value,
        (
            list,
            tuple,
            set
        )
    ):

        for index, nested_value in enumerate(
            value
        ):

            result = (
                inspect_resource_value(
                    nested_value,
                    f"{object_name}_{index}",
                    aliases,
                    visited
                )
            )

            if result is not None:

                return result

    return None


# ============================================================
# FORMAT RESOURCE DEFINITION
# ============================================================

def format_resource_definition(
    name: str,
    definition: dict
) -> str:

    lines = [
        "# ====================================================",
        f"# RESOURCE: {name}",
        "# ====================================================",
        "",
        f"RESOURCE_DEFINITION = {definition!r}",
        "",
    ]

    return "\n".join(
        lines
    )


# ============================================================
# RESOLVE ONE RESOURCE
# ============================================================

def resolve_resource(
    role: str,
    requested_name: str,
    module: ModuleType,
    master_doc_name: str
):

    result = find_resource_in_module(
        module,
        requested_name
    )

    if result is None:

        return None

    return ResolvedResource(

        requested_name=
            requested_name,

        resolved_name=
            result[
                "resolved_name"
            ],

        role=
            role,

        master_doc=
            master_doc_name,

        resource_type=
            result[
                "resource_type"
            ],

        source_code=
            result[
                "source_code"
            ],

        function_name=
            result.get(
                "function_name"
            ),

        metadata=
            result.get(
                "metadata",
                {}
            ),
    )


# ============================================================
# REQUESTED RESOURCES
# ============================================================

def requested_resources(
    specification: dict[str, Any]
):

    result = []

    # --------------------------------------------------------
    # ingestion
    # --------------------------------------------------------

    neural_data = (
        specification.get(
            "neural_data"
        )
    )

    if neural_data:

        result.append(
            (
                "ingestion",
                neural_data
            )
        )

    # --------------------------------------------------------
    # file type is NOT itself a resource
    # --------------------------------------------------------
    #
    # .edf is a compatibility requirement.
    # It should not be sent into resource acquisition as though
    # it were a Master-DOC algorithm.
    #
    # --------------------------------------------------------

    # --------------------------------------------------------
    # preprocessing
    # --------------------------------------------------------

    for resource in (
        specification.get(
            "preprocessing",
            []
        )
        or []
    ):

        result.append(
            (
                "preprocessing",
                resource
            )
        )

    # --------------------------------------------------------
    # statistics
    # --------------------------------------------------------

    for resource in (
        specification.get(
            "statistics",
            []
        )
        or []
    ):

        result.append(
            (
                "statistics",
                resource
            )
        )

    # --------------------------------------------------------
    # signal analysis
    # --------------------------------------------------------

    for resource in (
        specification.get(
            "signal_analysis",
            []
        )
        or []
    ):

        result.append(
            (
                "signal_analysis",
                resource
            )
        )

    # --------------------------------------------------------
    # decoder
    # --------------------------------------------------------

    decoder = (
        specification.get(
            "decoder"
        )
    )

    if decoder:

        result.append(
            (
                "decoding",
                decoder
            )
        )

    # --------------------------------------------------------
    # visualization
    # --------------------------------------------------------

    visualization = (
        specification.get(
            "visualization"
        )
    )

    if isinstance(
        visualization,
        str
    ):

        result.append(
            (
                "visualization",
                visualization
            )
        )

    return result


# ============================================================
# RESOLVE ALL RESOURCES
# ============================================================

def resolve_resources(
    specification,
    roles
):

    resolved = []

    unresolved = []

    print()
    print(
        "Resolving requested resources..."
    )

    for role, requested_name in (
        requested_resources(
            specification
        )
    ):

        normalized_role = normalize_role(
            role
        )

        module = roles.get(
            normalized_role
        )

        print()

        print(
            f"  Searching role "
            f"'{normalized_role}'"
        )

        if module is None:

            print(
                "    ✗ No designated "
                "Master-DOC exists."
            )

            unresolved.append(
                {
                    "role":
                        normalized_role,

                    "requested":
                        requested_name,

                    "reason":
                        "Designated Master-DOC "
                        "does not exist.",
                }
            )

            continue

        master_doc_name = Path(
            module.__file__
        ).name

        print(
            f"    Primary Master-DOC: "
            f"{master_doc_name}"
        )

        print(
            f"    Requested resource: "
            f"{requested_name}"
        )

        aliases = get_aliases(
            requested_name
        )

        print(
            "    Aliases: "
            +
            ", ".join(
                sorted(
                    aliases
                )
            )
        )

        resource = resolve_resource(
            normalized_role,
            requested_name,
            module,
            master_doc_name
        )

        if resource is None:

            print(
                "    ✗ Resource was not "
                "acquired from its "
                "designated Master-DOC."
            )

            unresolved.append(
                {
                    "role":
                        normalized_role,

                    "requested":
                        requested_name,

                    "reason":
                        "Resource was not exposed "
                        "by designated Master-DOC.",
                }
            )

            continue

        print(
            f"    ✓ Acquired source: "
            f"{resource.resolved_name}"
        )

        print(
            f"      type: "
            f"{resource.resource_type}"
        )

        resolved.append(
            resource
        )

    return (
        resolved,
        unresolved
    )


# ============================================================
# CHECK INGESTION FILE COMPATIBILITY
# ============================================================

def check_ingestion_compatibility(
    specification,
    resolved_resources
):

    errors = []

    file_type = specification.get(
        "file_type"
    )

    if not file_type:

        return errors

    file_type = str(
        file_type
    ).lower().strip()

    ingestion_resources = [
        resource
        for resource
        in resolved_resources
        if resource.role ==
        "ingestion"
    ]

    if not ingestion_resources:

        return errors

    # --------------------------------------------------------
    # Look at the acquired ingestion resource definitions.
    # --------------------------------------------------------

    supported_formats = set()

    for resource in ingestion_resources:

        metadata = resource.metadata

        for key in (
            "file_type",
            "file_types",
            "extensions",
            "supported_formats",
            "formats",
        ):

            value = metadata.get(
                key
            )

            if isinstance(
                value,
                str
            ):

                supported_formats.add(
                    value.lower()
                )

            elif isinstance(
                value,
                (
                    list,
                    tuple,
                    set
                )
            ):

                supported_formats.update(
                    str(item).lower()
                    for item in value
                )

    # --------------------------------------------------------
    # If Master-DOC exposes no format metadata, do not invent
    # compatibility.
    # --------------------------------------------------------

    if not supported_formats:

        return errors

    normalized_formats = {
        format_value.lower()
        for format_value
        in supported_formats
    }

    if file_type not in normalized_formats:

        errors.append(
            "EEG ingestion does not currently "
            f"support '{file_type}'. "
            "The designated ingestion Master-DOC "
            "does not expose this file type."
        )

    return errors


# ============================================================
# ASSEMBLE SOURCE
# ============================================================

def assemble_pipeline_source(
    specification,
    resolved_resources
):

    imports = set()

    source_sections = []

    for resource in resolved_resources:

        source = (
            resource.source_code
        ).strip()

        if not source:

            continue

        # ----------------------------------------------------
        # Extract imports from acquired source.
        # ----------------------------------------------------

        try:

            tree = ast.parse(
                source
            )

            for node in tree.body:

                if isinstance(
                    node,
                    (
                        ast.Import,
                        ast.ImportFrom
                    )
                ):

                    imports.add(
                        ast.unparse(
                            node
                        )
                    )

        except SyntaxError:

            pass

        # ----------------------------------------------------
        # Store actual Master-DOC source.
        # ----------------------------------------------------

        source_sections.append(

            "\n".join(
                [
                    "",
                    "# ====================================================",
                    f"# ACQUIRED RESOURCE: "
                    f"{resource.requested_name}",
                    f"# ROLE: "
                    f"{resource.role}",
                    f"# MASTER-DOC: "
                    f"{resource.master_doc}",
                    "# ====================================================",
                    "",
                    source,
                    "",
                ]
            )
        )

    # --------------------------------------------------------
    # Generated pipeline header
    # --------------------------------------------------------

    header = """
# ============================================================
# GENERATED NEURAL PIPELINE
# ============================================================
#
# This file was assembled by generator.py.
#
# Scientific source code was acquired from the Master-DOCs.
#
# generator.py did not invent the scientific algorithms.
# ============================================================

from __future__ import annotations

"""

    # --------------------------------------------------------
    # Specification
    # --------------------------------------------------------

    specification_literal = repr(
        specification
    )

    specification_block = (
        "# ============================================================\n"
        "# GENERATION SPECIFICATION\n"
        "# ============================================================\n\n"
        f"GENERATION_SPECIFICATION = "
        f"{specification_literal}\n"
    )

    # --------------------------------------------------------
    # Main pipeline placeholder
    # --------------------------------------------------------

    pipeline_function = """
# ============================================================
# PIPELINE ENTRY POINT
# ============================================================

def run_pipeline(data):
    """
 
    """

    current_data = data

    return current_data
"""

    return (
        header
        +
        "\n".join(
            sorted(
                imports
            )
        )
        +
        "\n\n"
        +
        specification_block
        +
        "\n"
        +
        "\n".join(
            source_sections
        )
        +
        "\n"
        +
        pipeline_function
    )


# ============================================================
# WRITE GENERATED PIPELINE
# ============================================================

def write_generated_pipeline(
    source: str
):

    GENERATED_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True
    )

    GENERATED_FILE.write_text(
        source,
        encoding="utf-8"
    )

    return GENERATED_FILE


# ============================================================
# GENERATION
# ============================================================

def generate(
    specification: Any
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
    # OBJECT HANDOFF
    # --------------------------------------------------------

    print()
    print(
        "OBJECT RECEIVED"
    )

    print()

    specification = (
        specification_to_dict(
            specification
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
    # LOAD MASTER-DOC LIBRARY
    # --------------------------------------------------------

    print()
    print(
        "Loading Master-DOC library..."
    )

    loaded_docs, load_errors = (
        load_master_docs()
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

    for role in sorted(
        roles
    ):

        module = roles[
            role
        ]

        print(
            f"  ✓ "
            f"{Path(module.__file__).stem}"
            f" -> "
            f"{role}"
        )

    # --------------------------------------------------------
    # MASTER-DOC LOAD FAILURE
    # --------------------------------------------------------

    if load_errors:

        print()

        print(
            "Master-DOC load errors:"
        )

        for name, error in (
            load_errors.items()
        ):

            print(
                f"  ✗ {name}: "
                f"{type(error).__name__}: "
                f"{error}"
            )

    # --------------------------------------------------------
    # REQUIRED ROLES
    # --------------------------------------------------------

    required_roles = set()

    for role, _ in requested_resources(
        specification
    ):

        required_roles.add(
            role
        )

    missing_roles = [
        role
        for role in sorted(
            required_roles
        )
        if role not in roles
    ]

    if missing_roles:

        errors = [
            f"Required Master-DOC role "
            f"'{role}' was not found."
            for role in missing_roles
        ]

        return {
            "status":
                "REJECTED",

            "specification":
                specification,

            "master_docs":
                loaded_docs,

            "master_doc_roles":
                roles,

            "resolved_resources":
                [],

            "unresolved_resources":
                [],

            "errors":
                errors,

            "output":
                None,
        }

    # --------------------------------------------------------
    # RESOLVE RESOURCES
    # --------------------------------------------------------

    resolved_resources, unresolved = (
        resolve_resources(
            specification,
            roles
        )
    )

    # --------------------------------------------------------
    # DISPLAY RESOLUTION
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
        f"{len(resolved_resources)}"
    )

    for resource in (
        resolved_resources
    ):

        print(
            f"  ✓ "
            f"{resource.requested_name} "
            f"-> "
            f"{resource.master_doc} "
            f"-> "
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

        for item in unresolved:

            print(
                f"  ✗ "
                f"{item['role']}: "
                f"{item['requested']}"
            )

    # --------------------------------------------------------
    # INGESTION COMPATIBILITY
    # --------------------------------------------------------

    compatibility_errors = (
        check_ingestion_compatibility(
            specification,
            resolved_resources
        )
    )

    # --------------------------------------------------------
    # STOP IF RESOURCES ARE MISSING
    # --------------------------------------------------------

    errors = []

    for item in unresolved:

        errors.append(
            f"{item['role']}: "
            f"{item['requested']} "
            f"could not be acquired from "
            f"its designated Master-DOC."
        )

    errors.extend(
        compatibility_errors
    )

    if errors:

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

        for error in errors:

            print(
                f"  - {error}"
            )

        return {

            "status":
                "REJECTED",

            "specification":
                specification,

            "master_docs":
                loaded_docs,

            "master_doc_roles":
                roles,

            "resolved_resources":
                resolved_resources,

            "unresolved_resources":
                unresolved,

            "errors":
                errors,

            "output":
                None,
        }

    # --------------------------------------------------------
    # ASSEMBLE
    # --------------------------------------------------------

    print()
    print(
        "Assembling pipeline source..."
    )

    source = (
        assemble_pipeline_source(
            specification,
            resolved_resources
        )
    )

    output_path = (
        write_generated_pipeline(
            source
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
        "Generated file:"
    )

    print(
        f"  {output_path}"
    )

    print()

    print(
        f"Resources: "
        f"{len(resolved_resources)}"
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
        "Status: GENERATED"
    )

    print(
        f"Output: {output_path}"
    )

    return {

        "status":
            "GENERATED",

        "specification":
            specification,

        "master_docs":
            loaded_docs,

        "master_doc_roles":
            roles,

        "resolved_resources":
            resolved_resources,

        "unresolved_resources":
            [],

        "errors":
            [],

        "output":
            str(output_path),
    }


# ============================================================
# COMPATIBILITY ALIAS
# ============================================================
#
# Some older analysis.py versions may call:
#
#     generate_pipeline()
#
# Keep this alias so the handoff remains compatible.
# ============================================================

def generate_pipeline(
    specification
):

    return generate(
        specification
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

    generate(
        test_specification
    )
