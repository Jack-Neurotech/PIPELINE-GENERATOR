
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
# The generator's job is to select, organize, and assemble
# those existing resources into a coherent pipeline.
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
        "master-doc-signal_analysis",
        "master-doc-signal-analysis",
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
# PARAMETER → MASTER-DOC FUNCTION MAPPINGS
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
# RESOURCE OBJECT
# ============================================================

@dataclass
class ResolvedResource:
    """
    One concrete resource acquired from a Master-DOC.
    """

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
    """
    Final result returned by the generator.
    """

    status: str

    specification: Any

    resolved_resources: list[ResolvedResource] = field(
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

def normalize_file_type(
    value: Any
) -> str:

    if value is None:
        return ""

    value = (
        str(value)
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
# SPECIFICATION EXTRACTION
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
        return dict(specification)

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

                return dict(result)

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

    module_name = (
        re.sub(
            r"[^A-Za-z0-9_]",
            "_",
            path.stem
        )
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
            f"Unable to create module specification "
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

    for path in discover_master_docs():

        try:

            loaded[
                path.name
            ] = load_master_doc(
                path
            )

        except Exception as error:

            errors[
                path.name
            ] = error

    return (
        loaded,
        errors
    )


# ============================================================
# IDENTIFY MASTER-DOC ROLES
# ============================================================

def identify_master_doc_roles(
    loaded_docs: dict[str, ModuleType]
):

    roles = {}

    for document_name, module in (
        loaded_docs.items()
    ):

        normalized = normalize_name(
            Path(
                document_name
            ).stem
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
                    normalized == normalized_pattern
                    or
                    normalized.startswith(
                        normalized_pattern
                    )
                ):

                    roles[role] = module

                    break

            if role in roles:
                break

    return roles


# ============================================================
# GET REQUEST LIST
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
# FIND FUNCTION
# ============================================================

def find_function(
    module: ModuleType | None,
    function_name: str
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
# CANONICAL RESOURCE NAME
# ============================================================

def canonical_resource_name(
    role: str,
    requested_name: Any
) -> str:

    normalized = normalize_name(
        requested_name
    )

    if role == "preprocessing":

        return PREPROCESSING_FUNCTIONS.get(
            normalized,
            normalized
        )

    if role == "statistics":

        return STATISTICS_FUNCTIONS.get(
            normalized,
            normalized
        )

    if role == "signal_analysis":

        return SIGNAL_ANALYSIS_FUNCTIONS.get(
            normalized,
            normalized
        )

    return normalized


# ============================================================
# FIND RESOURCE BY NAME
# ============================================================

def find_named_resource(
    module: ModuleType | None,
    requested_name: str,
    canonical_name: str
):

    if module is None:
        return None

    candidates = [
        requested_name,
        canonical_name,
        normalize_name(requested_name),
        normalize_name(canonical_name),
    ]

    normalized_candidates = {
        normalize_name(
            candidate
        )
        for candidate in candidates
        if candidate
    }

    # --------------------------------------------------------
    # DIRECT ATTRIBUTE SEARCH
    # --------------------------------------------------------

    for attribute_name in dir(
        module
    ):

        if attribute_name.startswith("__"):
            continue

        normalized_attribute = normalize_name(
            attribute_name
        )

        if (
            normalized_attribute
            not in
            normalized_candidates
        ):
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
    # SEARCH RESOURCE DICTIONARIES
    # --------------------------------------------------------

    for attribute_name in dir(
        module
    ):

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

        # Dictionary key.

        for key, value in (
            container.items()
        ):

            if normalize_name(
                key
            ) in normalized_candidates:

                return (
                    str(key),
                    value
                )

            # Dictionary entry with metadata.

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
                ):

                    metadata_value = (
                        value.get(
                            metadata_key
                        )
                    )

                    if (
                        metadata_value is not None
                        and
                        normalize_name(
                            metadata_value
                        )
                        in normalized_candidates
                    ):

                        return (
                            str(key),
                            value
                        )

    return None


# ============================================================
# SOURCE OF FUNCTION
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
# SOURCE OF RESOURCE
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
# EXTRACT DEPENDENCIES FROM SOURCE
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

    for node in (
        ast.walk(tree)
    ):

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
# RESOLVE RESOURCE
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

    canonical_name = (
        canonical_resource_name(
            role,
            requested_name
        )
    )

    found = find_named_resource(
        module,
        requested_name,
        canonical_name
    )

    if found is None:
        return None

    resolved_name, resource = found

    source_code = get_resource_source(
        resource
    )

    function_name = None

    if callable(resource):
        function_name = (
            getattr(
                resource,
                "__name__",
                None
            )
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
            resolved_name,

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
            "canonical_name":
                canonical_name,

            "resource_type":
                type(resource).__name__,
        }
    )


# ============================================================
# RESOLVE INGESTION
# ============================================================

def resolve_ingestion(
    specification: dict[str, Any],
    module: ModuleType | None,
    master_doc_name: str
):

    resources = []

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
    # First try explicit resource names.
    # --------------------------------------------------------

    for candidate in candidates:

        resource = resolve_resource(
            module,
            "ingestion",
            candidate,
            master_doc_name
        )

        if resource is not None:

            resources.append(
                resource
            )

            return resources

    # --------------------------------------------------------
    # Try common ingestion accessor functions.
    # --------------------------------------------------------

    accessors = (

        "get_ingestion_resource",

        "get_data_ingestion_resource",

        "resolve_ingestion_resource",

        "get_ingestion_method",

    )

    for accessor_name in accessors:

        accessor = find_function(
            module,
            accessor_name
        )

        if accessor is None:
            continue

        for candidate in candidates:

            try:

                result = accessor(
                    candidate
                )

            except TypeError:

                try:

                    result = accessor(
                        neural_data,
                        file_type
                    )

                except Exception:
                    continue

            except Exception:
                continue

            if result is None:
                continue

            source_code = (
                get_resource_source(
                    result
                )
            )

            if (
                source_code
                or
                isinstance(
                    result,
                    dict
                )
            ):

                resources.append(
                    ResolvedResource(

                        requested_name=
                            candidate,

                        resolved_name=
                            candidate,

                        role=
                            "ingestion",

                        master_doc=
                            master_doc_name,

                        source_code=
                            source_code,

                        function_name=(
                            getattr(
                                result,
                                "__name__",
                                None
                            )
                            if callable(result)
                            else None
                        ),

                        dependencies=
                            extract_dependencies(
                                source_code
                            ),

                        metadata={
                            "accessor":
                                accessor_name
                        }
                    )
                )

                return resources

    return resources


# ============================================================
# RESOLVE COMPONENT LIST
# ============================================================

def resolve_component_list(
    specification: dict[str, Any],
    role: str,
    module: ModuleType | None,
    master_doc_name: str
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
            requested_name is False
            or
            requested_name is None
        ):
            continue

        if isinstance(
            requested_name,
            bool
        ):
            continue

        resource = resolve_resource(
            module,
            role,
            requested_name,
            master_doc_name
        )

        if resource is None:

            unresolved.append(
                (
                    role,
                    str(requested_name)
                )
            )

            continue

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

    # --------------------------------------------------------
    # INGESTION
    # --------------------------------------------------------

    ingestion_module = roles.get(
        "ingestion"
    )

    if ingestion_module is not None:

        ingestion_name = (
            "Master-DOC-Ingestion"
        )

        ingestion_resources = (
            resolve_ingestion(
                specification,
                ingestion_module,
                ingestion_name
            )
        )

        if ingestion_resources:

            resolved.extend(
                ingestion_resources
            )

        else:

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

            unresolved.append(
                (
                    "ingestion",
                    (
                        neural_data
                        or
                        file_type
                        or
                        "unknown"
                    )
                )
            )

    else:

        unresolved.append(
            (
                "ingestion",
                "Master-DOC-Ingestion unavailable"
            )
        )

    # --------------------------------------------------------
    # STANDARD ROLES
    # --------------------------------------------------------

    for role in (
        "preprocessing",
        "statistics",
        "signal_analysis",
        "decoding",
        "visualization",
        "output",
    ):

        module = roles.get(
            role
        )

        if module is None:
            continue

        master_doc_name = (
            role
            .replace("_", "-")
            .title()
        )

        resources, missing = (
            resolve_component_list(
                specification,
                role,
                module,
                master_doc_name
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
        for index, role in enumerate(
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

    # --------------------------------------------------------
    # Every nonempty requested stage must have resources.
    # --------------------------------------------------------

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

    for role, key in stage_keys.items():

        requested = get_request_list(
            specification,
            key
        )

        requested = [
            value
            for value in requested
            if value is not False
            and value is not None
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
    # Basic ordering constraints.
    # --------------------------------------------------------

    if (
        "statistics" in roles_present
        and
        "ingestion" not in roles_present
    ):

        errors.append(
            "Statistics require an ingestion stage."
        )

    if (
        "preprocessing" in roles_present
        and
        "ingestion" not in roles_present
    ):

        errors.append(
            "Preprocessing requires an ingestion stage."
        )

    if (
        "signal_analysis" in roles_present
        and
        "ingestion" not in roles_present
    ):

        errors.append(
            "Signal analysis requires an "
            "ingestion stage."
        )

    if (
        "decoding" in roles_present
        and
        not (
            "signal_analysis" in roles_present
            or
            "statistics" in roles_present
            or
            "preprocessing" in roles_present
        )
    ):

        errors.append(
            "Decoding requires an upstream "
            "analysis stage."
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

    source = textwrap.dedent(
        source
    ).strip()

    return source


# ============================================================
# ASSEMBLE SOURCE
# ============================================================

def assemble_source(
    specification: dict[str, Any],
    resources: list[ResolvedResource],
    dependencies: list[str]
) -> str:

    sections = []

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    sections.append(
        "\n".join([
            "# ============================================================",
            "# GENERATED NEURAL PIPELINE",
            "# ============================================================",
            "#",
            "# This file was assembled by generator.py.",
            "#",
            "# Scientific implementations originate from the",
            "# PIPELINE-GENERATOR Master-DOC library.",
            "#",
            "# Do not edit generated source as the canonical scientific",
            "# implementation. Modify the corresponding Master-DOC.",
            "# ============================================================",
            "",
        ])
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

        if "." in dependency:

            root = dependency.split(
                ".",
                1
            )[0]

        else:

            root = dependency

        if root in (
            "typing",
            "dataclasses",
            "pathlib",
            "inspect",
            "ast",
            "re",
        ):
            continue

        import_lines.append(
            f"import {root}"
        )

    import_lines = sorted(
        set(import_lines)
    )

    if import_lines:

        sections.append(
            "\n".join([
                "# ============================================================",
                "# IMPORTS ACQUIRED FROM MASTER-DOC RESOURCES",
                "# ============================================================",
                *import_lines,
                "",
            ])
        )

    # --------------------------------------------------------
    # RESOURCE DEFINITIONS
    # --------------------------------------------------------

    for resource in resources:

        source = clean_source(
            resource.source_code
        )

        if not source:
            continue

        sections.append(
            "\n".join([
                "# ============================================================",
                f"# {resource.role.upper()}",
                f"# RESOURCE: {resource.requested_name}",
                f"# MASTER-DOC: {resource.master_doc}",
                "# ============================================================",
                source,
                "",
            ])
        )

    # --------------------------------------------------------
    # PIPELINE EXECUTION SHELL
    # --------------------------------------------------------

    sections.append(
        "\n".join([
            "# ============================================================",
            "# GENERATED PIPELINE CONFIGURATION",
            "# ============================================================",
            "",
            "PIPELINE_CONFIGURATION = ",
            repr(specification),
            "",
            "",
            "def run_pipeline(data=None):",
            '    """Run the assembled pipeline."""',
            "",
            "    current_data = data",
            "",
        ])
    )

    # --------------------------------------------------------
    # EXECUTION ORDER
    # --------------------------------------------------------

    executable_resources = [
        resource
        for resource in resources
        if resource.function_name
    ]

    for resource in executable_resources:

        function_name = (
            resource.function_name
        )

        if not function_name:
            continue

        sections.append(
            "\n".join([
                f"    # {resource.role}: "
                f"{resource.requested_name}",
                f"    # Master-DOC: "
                f"{resource.master_doc}",
                f"    current_data = "
                f"{function_name}(current_data)",
                "",
            ])
        )

    sections.append(
        "\n".join([
            "    return current_data",
            "",
        ])
    )

    return "\n".join(
        sections
    ).rstrip() + "\n"


# ============================================================
# VALIDATE GENERATED SOURCE
# ============================================================

def validate_generated_source(
    source_code: str
):

    if not source_code.strip():

        return {
            "valid": False,
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
            "valid": False,
            "errors": [
                (
                    "Generated source contains "
                    f"SyntaxError: {error}"
                )
            ],
        }

    return {
        "valid": True,
        "errors": [],
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

    # --------------------------------------------------------
    # STEP 1 — RECEIVE OBJECT
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("PIPELINE GENERATOR")
    print("=" * 70)
    print()
    print("OBJECT RECEIVED")
    print()

    specification = (
        specification_to_dict(
            generation_specification
        )
    )

    print(
        "Generation specification read."
    )

    # --------------------------------------------------------
    # STEP 2 — LOAD MASTER-DOC LIBRARY
    # --------------------------------------------------------

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
    # STEP 3 — IDENTIFY ROLES
    # --------------------------------------------------------

    roles = (
        identify_master_doc_roles(
            loaded_docs
        )
    )

    print(
        f"Master-DOCs loaded: "
        f"{len(loaded_docs)}"
    )

    print(
        f"Master-DOC roles resolved: "
        f"{len(roles)}"
    )

    # --------------------------------------------------------
    # STEP 4 — RESOLVE RESOURCES
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

    # Include Master-DOC execution errors.

    for document_name, error in (
        load_errors.items()
    ):

        unresolved.append(
            (
                "master_doc",
                (
                    f"{document_name} -> "
                    f"{type(error).__name__}: "
                    f"{error}"
                )
            )
        )

    # --------------------------------------------------------
    # STEP 5 — RESOLVE DEPENDENCIES
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
    # STEP 6 — ORDER RESOURCES
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
    # STEP 7 — COMPATIBILITY
    # --------------------------------------------------------

    compatibility = (
        check_compatibility(
            specification,
            resources
        )
    )

    # --------------------------------------------------------
    # STEP 8 — REPORT RESOLUTION
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("RESOURCE RESOLUTION")
    print("=" * 70)
    print()

    print(
        f"Resolved resources: "
        f"{len(resources)}"
    )

    for resource in resources:

        print(
            f"  ✓ {resource.requested_name}"
            f" -> "
            f"{resource.master_doc}"
            f" -> "
            f"{resource.resolved_name}"
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
    # STEP 9 — STOP IF RESOURCE RESOLUTION FAILED
    # --------------------------------------------------------

    if unresolved:

        return GenerationResult(

            status="PARTIAL",

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
                (
                    f"{role}: {name}"
                )
                for role, name
                in unresolved
            ]
        )

    # --------------------------------------------------------
    # STEP 10 — STOP IF COMPATIBILITY FAILED
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
    # STEP 11 — ASSEMBLE SOURCE
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
    # STEP 12 — VALIDATE SOURCE
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
    # STEP 13 — WRITE PIPELINE
    # --------------------------------------------------------

    generated_file = (
        write_generated_pipeline(
            source_code,
            output_path
        )
    )

    # --------------------------------------------------------
    # STEP 14 — SUCCESS
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("PIPELINE GENERATED")
    print("=" * 70)
    print()
    print(
        f"Generated file:"
        f"\n  {generated_file}"
    )
    print()
    print(
        f"Resources:"
        f" {len(resources)}"
    )
    print(
        f"Dependencies:"
        f" {len(dependencies)}"
    )
    print(
        f"Stages:"
        f" {', '.join(stages)}"
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
# COMPATIBILITY ENTRY POINT
# ============================================================
#
# This alias makes it easy for ingestion.py or another caller
# to pass the generation object directly.
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
#
# Explicit handoff function.
#
# The object enters the generator here and then proceeds
# through the complete generation lifecycle.
# ============================================================

def receive_generation_specification(
    generation_specification: Any
) -> GenerationResult:

    return generate(
        generation_specification
    )


# ============================================================
# TEST OBJECT
# ============================================================
#
# This allows:
#
#     python generator.py
#
# to test the generator independently of ingestion.py.
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
    print("=" * 70)
    print("GENERATION RESULT")
    print("=" * 70)
    print()
    print(
        f"Status: {result.status}"
    )

    if result.generated_file:

        print(
            f"Output: "
            f"{result.generated_file}"
        )

    if result.errors:

        print()
        print("Errors:")

        for error in result.errors:

            print(
                f"  - {error}"
            )

    print()
