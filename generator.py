# ============================================================
# PIPELINE GENERATOR
# ============================================================
#
# generator.py is the construction layer of the
# Neural Analysis Pipeline Generator.
#
# analysis.py produces the generation specification.
#
# generator.py then:
#
#     1. receives that specification
#     2. loads the Master-DOC library
#     3. uses Master-DOC-Generator as the authoritative
#        structural compiler
#     4. resolves the requested raw-material resources
#     5. retrieves the actual reusable functions
#     6. resolves function dependencies
#     7. assembles those functions into generated source code
#     8. writes generated_pipeline.py
#
# IMPORTANT:
#
# The generator does NOT invent scientific algorithms.
#
# The Master-DOCs remain the source of the scientific methods,
# compatibility rules, pipeline structure, and reusable code.
# ============================================================


# ============================================================
# IMPORTS
# ============================================================

from pathlib import Path
from importlib.machinery import SourceFileLoader
import ast
import importlib.util
import inspect
import re
import textwrap
from types import ModuleType


# ============================================================
# DIRECTORIES
# ============================================================

PROJECT_DIRECTORY = Path(__file__).resolve().parent

MASTER_DOC_DIRECTORY = (
    PROJECT_DIRECTORY /
    "Master-DOC's"
)

GENERATED_PIPELINE_PATH = (
    PROJECT_DIRECTORY /
    "generated_pipeline.py"
)


# ============================================================
# MASTER-DOC FILE ROLE PATTERNS
# ============================================================

MASTER_DOC_ROLE_PATTERNS = {

    "ingestion": "master-doc-ingestion",

    "preprocessing": "master-doc-preprocessing",

    "statistics": "master-doc-stats",

    "decoding": "master-doc-decoding",

    "visualization": "master-doc-visualization",

    "validation": "master-doc-validation",

    "pipeline": "master-doc-pipeline",

    "output": "master-doc-output",

    "connectivity": "master-doc-connectivity",

    "signal_analysis": "master-doc-signal_analysis",

    "generator": "master-doc-generator",
}


# ============================================================
# NORMALIZE DOCUMENT NAME
# ============================================================

def normalize_document_name(name):

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
        key=lambda path: path.name.lower()
    )


# ============================================================
# LOAD MASTER-DOC MODULE
# ============================================================

def load_master_doc(path):

    module_name = (
        path.stem
        .replace("-", "_")
        .replace(" ", "_")
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
            f"Unable to create module specification for {path.name}."
        )

    module = importlib.util.module_from_spec(
        spec
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

    for path in discover_master_docs():

        try:

            loaded[path.name] = load_master_doc(path)

        except Exception as error:

            errors[path.name] = error

    if errors:

        details = "\n".join(
            f"{name}: {type(error).__name__}: {error}"
            for name, error in errors.items()
        )

        raise RuntimeError(
            "One or more Master-DOCs failed to load:\n"
            f"{details}"
        )

    return loaded


# ============================================================
# IDENTIFY MASTER-DOC ROLES
# ============================================================

def identify_master_doc_roles(loaded):

    roles = {}

    for filename, module in loaded.items():

        normalized = normalize_document_name(
            filename
        )

        for role, pattern in MASTER_DOC_ROLE_PATTERNS.items():

            if (
                normalized == pattern
                or normalized.startswith(pattern)
            ):

                roles[role] = module
                break

    return roles


# ============================================================
# REQUIRE MASTER-DOC ROLE
# ============================================================

def require_role(roles, role):

    module = roles.get(role)

    if module is None:

        raise RuntimeError(
            "Required Master-DOC role is unavailable: "
            f"{role}"
        )

    return module


# ============================================================
# NORMALIZE RESOURCE NAME
# ============================================================
#
# GUI labels and Master-DOC registry keys are not always written
# identically.
#
# Examples:
#
#     Mean              -> mean
#     Standard Deviation -> standard_deviation
#     P-value           -> p_value
#     EEGLAB (.set)     -> EEGLAB
# ============================================================

def normalize_resource_name(value):

    if value is None:
        return None

    value = str(value).strip()

    value = re.sub(
        r"\([^)]*\)",
        "",
        value
    )

    value = value.lower().strip()

    value = re.sub(
        r"[^a-z0-9]+",
        "_",
        value
    )

    return value.strip("_")


# ============================================================
# NORMALIZE FILE TYPE
# ============================================================

def normalize_file_type(value):

    if value is None:
        return None

    text = str(value).strip()
    lowered = text.lower()

    if "eeglab" in lowered or lowered.endswith(".set"):
        return "EEGLAB"

    if "csv" in lowered or lowered.endswith(".csv"):
        return "CSV"

    return text


# ============================================================
# CALL MASTER-DOC GENERATOR
# ============================================================
#
# Master-DOC-Generator.py is the authoritative structural layer.
#
# generator.py does not replace its rules. It executes them.
# ============================================================

def build_authoritative_specification(
    handoff,
    roles
):

    request = dict(
        handoff.get(
            "request",
            {}
        )
    )

    generator_module = require_role(
        roles,
        "generator"
    )

    validation_module = require_role(
        roles,
        "validation"
    )

    normalize_function = getattr(
        generator_module,
        "normalize_request",
        None
    )

    build_function = getattr(
        generator_module,
        "build_generator_specification",
        None
    )

    safety_function = getattr(
        generator_module,
        "generator_safety_check",
        None
    )

    ready_function = getattr(
        generator_module,
        "ready_for_generation",
        None
    )

    validation_function = getattr(
        validation_module,
        "validate_pipeline_configuration",
        None
    )

    required = {
        "normalize_request": normalize_function,
        "build_generator_specification": build_function,
        "generator_safety_check": safety_function,
        "ready_for_generation": ready_function,
        "validate_pipeline_configuration": validation_function,
    }

    missing = [
        name
        for name, function in required.items()
        if not callable(function)
    ]

    if missing:

        raise AttributeError(
            "Master-DOC compiler is missing required functions: "
            + ", ".join(missing)
        )

    normalized = normalize_function(
        request
    )

    specification = build_function(
        normalized,
        validation_function
    )

    safety = safety_function(
        specification
    )

    ready = bool(
        ready_function(
            specification
        )
    )

    if not safety.get(
        "safe",
        False
    ):

        raise RuntimeError(
            "Master-DOC Generator rejected the pipeline:\n"
            + "\n".join(
                safety.get(
                    "errors",
                    []
                )
            )
        )

    if not ready:

        raise RuntimeError(
            "Master-DOC Generator did not mark the pipeline "
            "ready for generation."
        )

    return specification


# ============================================================
# RESOURCE LOOKUP HELPER
# ============================================================

def lookup_resource(
    module,
    lookup_function_name,
    *arguments
):

    lookup_function = getattr(
        module,
        lookup_function_name,
        None
    )

    if not callable(lookup_function):

        raise AttributeError(
            f"Master-DOC '{module.__name__}' does not expose "
            f"'{lookup_function_name}'."
        )

    return lookup_function(
        *arguments
    )


# ============================================================
# RESOLVE RAW MATERIALS
# ============================================================
#
# This is the point where the generator moves from:
#
#     "what should be generated?"
#
# to:
#
#     "which actual Master-DOC resources will be compiled?"
# ============================================================

def resolve_raw_materials(
    specification,
    roles
):

    request = specification[
        "request"
    ]

    ingestion_module = require_role(
        roles,
        "ingestion"
    )

    preprocessing_module = require_role(
        roles,
        "preprocessing"
    )

    statistics_module = require_role(
        roles,
        "statistics"
    )

    decoding_module = require_role(
        roles,
        "decoding"
    )

    output_module = require_role(
        roles,
        "output"
    )

    resources = {
        "ingestion": None,
        "preprocessing": [],
        "statistics": [],
        "features": [],
        "decoders": [],
        "output": [],
    }

    # --------------------------------------------------------
    # INGESTION
    # --------------------------------------------------------

    neural_data = request[
        "neural_data"
    ]

    file_type = normalize_file_type(
        request[
            "file_type"
        ]
    )

    resources[
        "ingestion"
    ] = lookup_resource(
        ingestion_module,
        "get_ingestion_resource",
        neural_data,
        file_type
    )

    # --------------------------------------------------------
    # PREPROCESSING
    # --------------------------------------------------------

    for operation in request.get(
        "preprocessing",
        []
    ):

        operation_key = normalize_resource_name(
            operation
        )

        resources[
            "preprocessing"
        ].append(
            lookup_resource(
                preprocessing_module,
                "get_preprocessing_resource",
                operation_key,
                neural_data
            )
        )

    # --------------------------------------------------------
    # STATISTICS
    # --------------------------------------------------------

    for statistic in request.get(
        "statistics",
        []
    ):

        statistic_key = normalize_resource_name(
            statistic
        )

        resources[
            "statistics"
        ].append(
            lookup_resource(
                statistics_module,
                "get_statistical_resource",
                statistic_key
            )
        )

    # --------------------------------------------------------
    # FEATURES
    # --------------------------------------------------------

    for feature in request.get(
        "features",
        []
    ):

        feature_key = normalize_resource_name(
            feature
        )

        resources[
            "features"
        ].append(
            lookup_resource(
                decoding_module,
                "get_feature_resource",
                feature_key
            )
        )

    # --------------------------------------------------------
    # DECODER
    # --------------------------------------------------------

    decoder = request.get(
        "decoder"
    )

    if decoder:

        decoder_key = normalize_resource_name(
            decoder
        )

        resources[
            "decoders"
        ].append(
            lookup_resource(
                decoding_module,
                "get_decoder_resource",
                decoder_key
            )
        )

    # --------------------------------------------------------
    # OUTPUT RESOURCES
    # --------------------------------------------------------
    #
    # The output Master-DOC is itself a reusable function library.
    # The generated pipeline uses its terminal-report functions.
    #
    # We select the complete pipeline output function rather than
    # inventing a new reporting implementation.
    # --------------------------------------------------------

    output_function = getattr(
        output_module,
        "print_pipeline_results",
        None
    )

    if callable(output_function):

        resources[
            "output"
        ].append(
            output_function
        )

    return resources


# ============================================================
# EXTRACT FUNCTION DEPENDENCY GRAPH
# ============================================================
#
# Master-DOC functions frequently depend on helper functions in
# the same Master-DOC.
#
# Example:
#
#     calculate_mean()
#             |
#             v
#     validate_numeric_data()
#
# The generator therefore includes the dependency closure rather
# than copying only the top-level requested function.
# ============================================================

def build_function_index(
    module
):

    return {
        name: value
        for name, value in vars(module).items()
        if inspect.isfunction(value)
    }


def referenced_names(function):

    try:
        source = inspect.getsource(function)

    except (OSError, TypeError):
        return set()

    try:
        tree = ast.parse(
            textwrap.dedent(source)
        )

    except SyntaxError:
        return set()

    names = set()

    for node in ast.walk(tree):

        if isinstance(node, ast.Name):
            names.add(node.id)

    return names


def collect_function_dependencies(
    function,
    module,
    collected=None
):

    if collected is None:
        collected = {}

    key = (
        module.__name__,
        function.__name__
    )

    if key in collected:
        return collected

    collected[
        key
    ] = function

    function_index = build_function_index(
        module
    )

    for name in referenced_names(function):

        dependency = function_index.get(
            name
        )

        if dependency is None:
            continue

        collect_function_dependencies(
            dependency,
            module,
            collected
        )

    return collected


# ============================================================
# COLLECT IMPORTS
# ============================================================

def collect_module_imports(
    module
):

    try:
        source = inspect.getsource(
            module
        )

    except (OSError, TypeError):
        return []

    try:
        tree = ast.parse(
            source
        )

    except SyntaxError:
        return []

    imports = []

    for node in tree.body:

        if isinstance(
            node,
            (ast.Import, ast.ImportFrom)
        ):

            imports.append(
                ast.get_source_segment(
                    source,
                    node
                )
            )

    return [
        value
        for value in imports
        if value
    ]


# ============================================================
# SOURCE EXTRACTION
# ============================================================

def extract_function_source(
    functions
):

    ordered = list(
        functions.values()
    )

    # --------------------------------------------------------
    # Put dependencies before functions that use them.
    # --------------------------------------------------------

    result = []
    visited = set()

    function_lookup = {
        (
            function.__module__,
            function.__name__
        ): function
        for function in ordered
    }

    def visit(function):

        key = (
            function.__module__,
            function.__name__
        )

        if key in visited:
            return

        visited.add(key)

        for name in referenced_names(function):

            dependency = function_lookup.get(
                (
                    function.__module__,
                    name
                )
            )

            if dependency is not None:
                visit(dependency)

        try:
            source = inspect.getsource(
                function
            )

        except (OSError, TypeError):
            return

        result.append(
            textwrap.dedent(
                source
            ).strip()
        )

    for function in ordered:
        visit(function)

    return "\n\n\n".join(
        result
    )


# ============================================================
# BUILD SOURCE MATERIAL
# ============================================================

def build_source_material(
    resources,
    roles
):

    selected_functions = {}
    imports = set()
    source_modules = []

    # --------------------------------------------------------
    # Function-bearing Master-DOCs
    # --------------------------------------------------------

    function_modules = {
        "preprocessing": roles[
            "preprocessing"
        ],
        "statistics": roles[
            "statistics"
        ],
        "decoding": roles[
            "decoding"
        ],
        "output": roles[
            "output"
        ],
    }

    for role, module in function_modules.items():

        selected = []

        if role == "preprocessing":

            selected = resources[
                "preprocessing"
            ]

        elif role == "statistics":

            selected = resources[
                "statistics"
            ]

        elif role == "decoding":

            selected = (
                resources[
                    "features"
                ]
                +
                resources[
                    "decoders"
                ]
            )

        elif role == "output":

            selected = resources[
                "output"
            ]

        if not selected:
            continue

        source_modules.append(
            module.__name__
        )

        for resource in selected:

            function = resource

            if isinstance(
                resource,
                dict
            ):

                function = resource.get(
                    "function"
                )

            if not inspect.isfunction(
                function
            ):
                continue

            dependencies = (
                collect_function_dependencies(
                    function,
                    module
                )
            )

            for key, dependency in dependencies.items():

                selected_functions[
                    key
                ] = dependency

        imports.update(
            collect_module_imports(
                module
            )
        )

    return {
        "functions": selected_functions,
        "imports": sorted(imports),
        "modules": source_modules,
    }


# ============================================================
# BUILD GENERATED INGESTION FUNCTION
# ============================================================
#
# The ingestion Master-DOC stores reader specifications rather
# than one universal ingestion function. The generator therefore
# translates that Master-DOC specification into the generated
# ingestion function.
#
# No unsupported reader is invented here.
# ============================================================

def build_ingestion_source(
    ingestion_resource
):

    modality = ingestion_resource[
        "modality"
    ]

    file_type = ingestion_resource[
        "file_type"
    ]

    reader = ingestion_resource[
        "reader"
    ]

    reader_function = reader[
        "function"
    ]

    dependencies = ingestion_resource.get(
        "dependencies",
        []
    )

    dependency_imports = []

    for dependency in dependencies:

        if dependency == "numpy":
            dependency_imports.append(
                "import numpy as np"
            )

        elif dependency == "pandas":
            dependency_imports.append(
                "import pandas as pd"
            )

        elif dependency == "mne":
            dependency_imports.append(
                "import mne"
            )

    if reader_function == "mne.io.read_raw_eeglab":

        body = '''

def load_neural_data(file_path):
    """Load an EEGLAB dataset using the Master-DOC reader."""

    raw = mne.io.read_raw_eeglab(
        file_path,
        preload=True
    )

    data = raw.get_data()

    return {
        "data": data,
        "sampling_rate": raw.info["sfreq"],
        "timestamps": raw.times,
        "channels": raw.ch_names,
        "channel_locations": None,
        "metadata": raw.info,
        "modality": "EEG",
        "file_type": "EEGLAB",
        "source_file": str(file_path)
    }
'''

    elif reader_function == "pandas.read_csv":

        body = f'''

def load_neural_data(file_path):
    """Load a CSV neural dataset using the Master-DOC reader."""

    dataframe = pd.read_csv(
        file_path
    )

    numeric = dataframe.select_dtypes(
        include=["number"]
    )

    if numeric.empty:
        raise ValueError(
            "The selected CSV contains no numeric signal columns."
        )

    data = numeric.to_numpy().T

    return {{
        "data": data,
        "sampling_rate": None,
        "timestamps": None,
        "channels": list(numeric.columns),
        "channel_locations": None,
        "metadata": {{
            "columns": list(dataframe.columns)
        }},
        "modality": {modality!r},
        "file_type": {file_type!r},
        "source_file": str(file_path)
    }}
'''

    else:

        raise RuntimeError(
            "Master-DOC ingestion resource uses an unsupported "
            "reader: "
            f"{reader_function}"
        )

    return {
        "imports": dependency_imports,
        "source": textwrap.dedent(body).strip(),
    }


# ============================================================
# BUILD EXECUTION PLAN
# ============================================================
#
# The execution plan does not invent arguments that the user did
# not provide.
#
# Operations whose Master-DOC function signatures require extra
# scientific parameters remain explicitly unresolved.
# ============================================================

def build_execution_plan(
    specification,
    resources
):

    request = specification[
        "request"
    ]

    operations = []
    unresolved = []

    # --------------------------------------------------------
    # Preprocessing
    # --------------------------------------------------------

    for resource in resources[
        "preprocessing"
    ]:

        function = resource.get(
            "function"
        )

        if not inspect.isfunction(function):
            continue

        signature = inspect.signature(
            function
        )

        required = [
            parameter.name
            for parameter in signature.parameters.values()
            if (
                parameter.default is inspect.Parameter.empty
                and parameter.name not in {
                    "data"
                }
            )
        ]

        missing = [
            name
            for name in required
            if name not in {
                "sampling_rate"
            }
            and name not in request
        ]

        if missing:

            unresolved.append({
                "stage": "preprocessing",
                "component": function.__name__,
                "missing_parameters": missing,
            })

            continue

        arguments = [
            "data"
        ]

        for parameter in signature.parameters.values():

            if parameter.name == "data":
                continue

            if parameter.name == "sampling_rate":

                arguments.append(
                    "pipeline_data[\"sampling_rate\"]"
                )

            elif parameter.name in request:

                arguments.append(
                    repr(
                        request[
                            parameter.name
                        ]
                    )
                )

        operations.append({
            "stage": "preprocessing",
            "function": function.__name__,
            "arguments": arguments,
        })

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    for resource in resources[
        "statistics"
    ]:

        function = resource.get(
            "function"
        )

        if not inspect.isfunction(function):
            continue

        signature = inspect.signature(
            function
        )

        required = [
            parameter.name
            for parameter in signature.parameters.values()
            if parameter.default is inspect.Parameter.empty
        ]

        unsupported = [
            name
            for name in required
            if name not in {
                "data"
            }
        ]

        if unsupported:

            unresolved.append({
                "stage": "statistics",
                "component": function.__name__,
                "missing_parameters": unsupported,
            })

            continue

        operations.append({
            "stage": "statistics",
            "function": function.__name__,
            "arguments": [
                "pipeline_data[\"data\"]"
            ],
        })

    return {
        "operations": operations,
        "unresolved": unresolved,
    }


# ============================================================
# BUILD GENERATED PIPELINE SOURCE
# ============================================================

def build_generated_source(
    specification,
    resources,
    source_material,
    execution_plan
):

    ingestion_source = build_ingestion_source(
        resources[
            "ingestion"
        ]
    )

    imports = set(
        source_material[
            "imports"
        ]
    )

    imports.update(
        ingestion_source[
            "imports"
        ]
    )

    imports = sorted(
        imports
    )

    source = []

    source.append(
        "# ============================================================\n"
        "# GENERATED NEURAL ANALYSIS PIPELINE\n"
        "# ============================================================\n"
        "#\n"
        "# This file was assembled by generator.py from the\n"
        "# Master-DOC raw-material library.\n"
        "#\n"
        "# The generator did not invent the scientific functions.\n"
        "# Selected reusable functions were retrieved from the\n"
        "# corresponding Master-DOC modules.\n"
        "# ============================================================\n"
    )

    source.append(
        "# ============================================================\n"
        "# PIPELINE SPECIFICATION\n"
        "# ============================================================\n"
        f"PIPELINE_SPECIFICATION = {specification!r}\n"
    )

    source.append(
        "# ============================================================\n"
        "# IMPORTS FROM SELECTED MASTER-DOCs\n"
        "# ============================================================\n"
        + "\n".join(imports)
    )

    source.append(
        "# ============================================================\n"
        "# INGESTION CODE COMPILED FROM MASTER-DOC INGESTION\n"
        "# ============================================================\n"
        + ingestion_source[
            "source"
        ]
    )

    function_source = extract_function_source(
        source_material[
            "functions"
        ]
    )

    if function_source:

        source.append(
            "# ============================================================\n"
            "# SELECTED MASTER-DOC FUNCTIONS\n"
            "# ============================================================\n"
            + function_source
        )

    # --------------------------------------------------------
    # Generated execution wrapper
    # --------------------------------------------------------

    source.append(
        "# ============================================================\n"
        "# GENERATED PIPELINE EXECUTION\n"
        "# ============================================================\n"
    )

    source.append(
        "def run_pipeline(file_path):\n"
        "    \"\"\"Execute the generated pipeline.\"\"\"\n"
        "\n"
        "    pipeline_data = load_neural_data(file_path)\n"
        "    data = pipeline_data[\"data\"]\n"
        "\n"
    )

    for operation in execution_plan[
        "operations"
    ]:

        if operation[
            "stage"
        ] == "preprocessing":

            function_name = operation[
                "function"
            ]

            arguments = operation[
                "arguments"
            ]

            argument_text = ", ".join(
                arguments
            )

            source.append(
                "    data = "
                f"{function_name}({argument_text})\n"
            )

            source.append(
                "    pipeline_data[\"data\"] = data\n"
            )

        elif operation[
            "stage"
        ] == "statistics":

            function_name = operation[
                "function"
            ]

            source.append(
                "    result_"
                f"{len(source)}"
                " = "
                f"{function_name}(pipeline_data[\"data\"])\n"
            )

            source.append(
                "    print("
                f"\"{function_name}:\", "
                f"result_{len(source) - 1}"
                ")\n"
            )

    source.append(
        "\n"
        "    return pipeline_data\n"
    )

    source.append(
        "\n"
        "# ============================================================\n"
        "# DIRECT EXECUTION\n"
        "# ============================================================\n"
        "#\n"
        "# The generated pipeline is intentionally not executed on\n"
        "# import. The caller supplies the actual input file.\n"
        "# ============================================================\n"
    )

    return "\n\n".join(
        source
    ).rstrip() + "\n"


# ============================================================
# WRITE GENERATED PIPELINE
# ============================================================

def write_generated_pipeline(
    source_code
):

    GENERATED_PIPELINE_PATH.write_text(
        source_code,
        encoding="utf-8"
    )

    return GENERATED_PIPELINE_PATH


# ============================================================
# GENERATOR ENTRY POINT
# ============================================================

def generate(
    generation_specification
):
    """
    Receive analysis.py's generation specification and compile
    the requested pipeline from the Master-DOC library.
    """

    if generation_specification is None:

        raise ValueError(
            "Generator received no generation specification."
        )

    if not isinstance(
        generation_specification,
        dict
    ):

        raise TypeError(
            "Generator expects the analysis handoff object "
            "to be a dictionary."
        )

    print()
    print("=" * 70)
    print("PIPELINE GENERATOR")
    print("=" * 70)
    print(
        "GENERATION SPECIFICATION RECEIVED"
    )

    # --------------------------------------------------------
    # STEP 1 — LOAD MASTER-DOC LIBRARY
    # --------------------------------------------------------

    loaded = load_master_docs()

    roles = identify_master_doc_roles(
        loaded
    )

    # --------------------------------------------------------
    # STEP 2 — RUN AUTHORITATIVE MASTER-DOC GENERATOR LOGIC
    # --------------------------------------------------------

    specification = build_authoritative_specification(
        generation_specification,
        roles
    )

    # --------------------------------------------------------
    # STEP 3 — RESOLVE REQUESTED RAW MATERIALS
    # --------------------------------------------------------

    resources = resolve_raw_materials(
        specification,
        roles
    )

    # --------------------------------------------------------
    # STEP 4 — RETRIEVE ACTUAL FUNCTION SOURCE
    # --------------------------------------------------------

    source_material = build_source_material(
        resources,
        roles
    )

    # --------------------------------------------------------
    # STEP 5 — BUILD EXECUTION PLAN
    # --------------------------------------------------------

    execution_plan = build_execution_plan(
        specification,
        resources
    )

    # --------------------------------------------------------
    # STEP 6 — COMPILE SOURCE CODE
    # --------------------------------------------------------

    source_code = build_generated_source(
        specification,
        resources,
        source_material,
        execution_plan
    )

    # --------------------------------------------------------
    # STEP 7 — WRITE GENERATED PIPELINE
    # --------------------------------------------------------

    output_path = write_generated_pipeline(
        source_code
    )

    # --------------------------------------------------------
    # STEP 8 — REPORT
    # --------------------------------------------------------

    print()
    print(
        "MASTER-DOC RESOURCES RESOLVED"
    )

    print(
        f"  Ingestion: "
        f"{resources['ingestion'].get('id')}"
    )

    print(
        f"  Preprocessing: "
        f"{len(resources['preprocessing'])}"
    )

    print(
        f"  Statistics: "
        f"{len(resources['statistics'])}"
    )

    print(
        f"  Features: "
        f"{len(resources['features'])}"
    )

    print(
        f"  Decoders: "
        f"{len(resources['decoders'])}"
    )

    print()
    print(
        "PIPELINE SOURCE COMPILED"
    )

    print(
        f"  Functions compiled: "
        f"{len(source_material['functions'])}"
    )

    print(
        f"  Output file: "
        f"{output_path}"
    )

    if execution_plan[
        "unresolved"
    ]:

        print()
        print(
            "UNRESOLVED COMPONENT PARAMETERS"
        )

        for item in execution_plan[
            "unresolved"
        ]:

            print(
                "  - "
                f"{item['component']}: "
                f"missing {item['missing_parameters']}"
            )

        print()
        print(
            "Those components were not inserted into the "
            "execution plan because the supplied parameters "
            "did not define their required scientific arguments."
        )

    print()
    print("=" * 70)
    print(
        "GENERATOR COMPLETED"
    )
    print("=" * 70)

    return {
        "status": "GENERATED",
        "generation_specification": generation_specification,
        "pipeline_specification": specification,
        "master_doc_roles": roles,
        "resources": resources,
        "source_material": {
            "function_count": len(
                source_material[
                    "functions"
                ]
            ),
            "modules": source_material[
                "modules"
            ],
        },
        "execution_plan": execution_plan,
        "source_code": source_code,
        "output_path": str(
            output_path
        ),
    }


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 70)
    print("PIPELINE GENERATOR")
    print("=" * 70)
    print()
    print(
        "Generator is ready to receive a generation specification."
    )
    print()
    print(
        f"Master-DOC directory: {MASTER_DOC_DIRECTORY}"
    )
    print(
        f"Generated pipeline: {GENERATED_PIPELINE_PATH}"
    )
    print()
    print("=" * 70)
