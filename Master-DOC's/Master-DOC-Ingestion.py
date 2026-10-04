
"""
============================================================
MASTER-DOC-INGESTION.PY
============================================================

PURPOSE
-------
Master raw-material library for the Neural Analysis Pipeline
Generator's DATA INGESTION layer.

This file is a RESOURCE LIBRARY.

It defines:

    - supported neural-data modalities
    - supported file formats
    - reader requirements
    - dependencies
    - extraction requirements
    - validation requirements
    - standardized output requirements
    - downstream compatibility
    - assembly rules

It does NOT:

    - provide the GUI
    - select files
    - execute the ingestion pipeline
    - generate the final pipeline
    - perform analysis.py orchestration

The generator acquires resources from this file.

IMPORTANT
---------
The resource-resolution interface at the bottom of this file
is part of the Master-DOC contract.

generator.py should ask this module:

    resolve_resource("EEG")

or:

    resolve_resource("eeg_edf")

rather than inspecting this file's internal dictionaries.
============================================================
"""


# ============================================================
# 1. STANDARDIZED INGESTION CONTRACT
# ============================================================

STANDARDIZED_OUTPUT = {

    "data": {
        "description": "Primary neural signal/data array",
        "required": True
    },

    "sampling_rate": {
        "description": "Sampling frequency in Hz when applicable",
        "required": False
    },

    "timestamps": {
        "description": "Time axis associated with the data",
        "required": False
    },

    "channels": {
        "description": "Channel/sensor/electrode identifiers",
        "required": False
    },

    "channel_locations": {
        "description": "Channel spatial/location metadata",
        "required": False
    },

    "metadata": {
        "description": "Additional source-file metadata",
        "required": False
    },

    "modality": {
        "description": "Neural-data modality",
        "required": True
    },

    "file_type": {
        "description": "Source file format",
        "required": True
    },

    "source_file": {
        "description": "Original input-file path",
        "required": True
    }
}


# ============================================================
# 2. COMMON INGESTION REQUIREMENTS
# ============================================================

COMMON_REQUIREMENTS = {

    "file_exists": True,

    "file_is_readable": True,

    "file_extension_matches_selection": True,

    "data_can_be_loaded": True,

    "data_is_not_empty": True,

    "data_structure_is_valid": True,

    "source_file_is_recorded": True,

    "modality_is_recorded": True,

    "file_type_is_recorded": True,

    "errors_are_reported": True
}


# ============================================================
# 3. EEG → EEGLAB
# ============================================================

EEG_EEGLAB = {

    "id": "eeg_eeglab",

    "name": "EEG",

    "modality": "EEG",

    "file_type": "EEGLAB",

    "extensions": [
        ".set"
    ],

    "reader": {
        "library": "mne",
        "function": "mne.io.read_raw_eeglab",
        "preload": True
    },

    "dependencies": [
        "mne",
        "numpy"
    ],

    "input_requirements": {

        "required_extension": ".set",

        "file_must_exist": True,

        "file_must_be_readable": True

    },

    "loading": {

        "method": "MNE EEGLAB reader",

        "preload": True,

        "description":
            "Load an EEGLAB dataset into an MNE Raw object."
    },

    "extraction": {

        "signal_data": {
            "method": "raw.get_data()",
            "output": "numpy.ndarray"
        },

        "sampling_rate": {
            "method": "raw.info['sfreq']",
            "output": "float"
        },

        "channels": {
            "method": "raw.ch_names",
            "output": "list"
        },

        "timestamps": {
            "method": "raw.times",
            "output": "numpy.ndarray"
        },

        "metadata": {
            "method": "raw.info",
            "output": "dictionary-like metadata"
        }
    },

    "validation": {

        "signal_data_not_empty": True,

        "sampling_rate_positive": True,

        "channel_list_available": True,

        "channel_count_matches_data": True,

        "data_contains_valid_numeric_values": True

    },

    "standardized_output": STANDARDIZED_OUTPUT,

    "compatible_downstream_stages": [

        "Preprocessing",

        "Signal Analysis",

        "Statistical Analysis",

        "Time-Series Analysis",

        "EEG Analysis",

        "Machine Learning",

        "Neural Decoding",

        "Visualization"

    ],

    "assembly_rules": {

        "reader": "mne.io.read_raw_eeglab",

        "load_with_preload": True,

        "extract_data": True,

        "extract_sampling_rate": True,

        "extract_channels": True,

        "extract_timestamps": True,

        "extract_metadata": True,

        "standardize_output": True

    }
}


# ============================================================
# 4. EEG → EDF
# ============================================================
#
# THIS RESOURCE FIXES THE CURRENT .edf FAILURE.
#
# The previous Master-DOC defined EEG for:
#
#     .set
#     .csv
#
# but the handoff object requests:
#
#     .edf
#
# EDF is a standard EEG/physiological recording format and
# MNE provides:
#
#     mne.io.read_raw_edf()
#
# ============================================================

EEG_EDF = {

    "id": "eeg_edf",

    "name": "EEG",

    "modality": "EEG",

    "file_type": "EDF",

    "extensions": [
        ".edf",
        ".EDF"
    ],

    "reader": {
        "library": "mne",
        "function": "mne.io.read_raw_edf",
        "preload": True
    },

    "dependencies": [
        "mne",
        "numpy"
    ],

    "input_requirements": {

        "required_extension": ".edf",

        "file_must_exist": True,

        "file_must_be_readable": True

    },

    "loading": {

        "method": "MNE EDF reader",

        "preload": True,

        "description":
            "Load an EDF/EDF+ recording into an MNE Raw object."
    },

    "extraction": {

        "signal_data": {
            "method": "raw.get_data()",
            "output": "numpy.ndarray"
        },

        "sampling_rate": {
            "method": "raw.info['sfreq']",
            "output": "float"
        },

        "channels": {
            "method": "raw.ch_names",
            "output": "list"
        },

        "timestamps": {
            "method": "raw.times",
            "output": "numpy.ndarray"
        },

        "metadata": {
            "method": "raw.info",
            "output": "dictionary-like metadata"
        },

        "channel_locations": {
            "method": "raw.get_montage()",
            "output": "montage metadata when available"
        }
    },

    "validation": {

        "signal_data_not_empty": True,

        "sampling_rate_positive": True,

        "channel_list_available": True,

        "channel_count_matches_data": True,

        "data_contains_valid_numeric_values": True

    },

    "standardized_output": STANDARDIZED_OUTPUT,

    "compatible_downstream_stages": [

        "Preprocessing",

        "Signal Analysis",

        "Statistical Analysis",

        "Time-Series Analysis",

        "EEG Analysis",

        "Machine Learning",

        "Neural Decoding",

        "Visualization"

    ],

    "assembly_rules": {

        "reader": "mne.io.read_raw_edf",

        "load_with_preload": True,

        "extract_data": True,

        "extract_sampling_rate": True,

        "extract_channels": True,

        "extract_timestamps": True,

        "extract_metadata": True,

        "extract_channel_locations_when_available": True,

        "standardize_output": True

    }
}


# ============================================================
# 5. EEG → CSV
# ============================================================

EEG_CSV = {

    "id": "eeg_csv",

    "name": "EEG",

    "modality": "EEG",

    "file_type": "CSV",

    "extensions": [
        ".csv"
    ],

    "reader": {
        "library": "pandas",
        "function": "pandas.read_csv"
    },

    "dependencies": [
        "pandas",
        "numpy"
    ],

    "input_requirements": {

        "required_extension": ".csv",

        "file_must_exist": True,

        "file_must_be_readable": True,

        "file_must_contain_structured_data": True

    },

    "loading": {

        "method": "pandas.read_csv",

        "description":
            "Load the CSV file into a pandas DataFrame."
    },

    "extraction": {

        "signal_data": {
            "method": "DataFrame numeric-column extraction",
            "output": "numpy.ndarray"
        },

        "channels": {
            "method": "CSV column names",
            "output": "list"
        },

        "sampling_rate": {
            "method":
                "Explicit metadata/configuration when available",
            "output": "float or None"
        },

        "timestamps": {
            "method":
                "Timestamp/time column when available",
            "output": "numpy.ndarray or None"
        },

        "metadata": {
            "method":
                "CSV structure and column metadata",
            "output": "dictionary"
        }
    },

    "validation": {

        "signal_data_not_empty": True,

        "numeric_signal_columns_required": True,

        "channel_count_matches_data": True,

        "data_contains_valid_numeric_values": True,

        "sampling_rate_must_be_verified_before_time_based_analysis":
            True

    },

    "standardized_output": STANDARDIZED_OUTPUT,

    "compatible_downstream_stages": [

        "Preprocessing",

        "Signal Analysis",

        "Statistical Analysis",

        "Time-Series Analysis",

        "EEG Analysis",

        "Machine Learning",

        "Neural Decoding",

        "Visualization"

    ],

    "assembly_rules": {

        "reader": "pandas.read_csv",

        "identify_numeric_columns": True,

        "identify_timestamp_column_when_available": True,

        "identify_channel_columns": True,

        "validate_signal_structure": True,

        "require_sampling_rate_for_frequency_analysis": True,

        "standardize_output": True

    }
}


# ============================================================
# 6. IONM → CSV
# ============================================================

IONM_CSV = {

    "id": "ionm_csv",

    "name": "IONM",

    "modality": "IONM",

    "file_type": "CSV",

    "extensions": [
        ".csv"
    ],

    "reader": {
        "library": "pandas",
        "function": "pandas.read_csv"
    },

    "dependencies": [
        "pandas",
        "numpy"
    ],

    "input_requirements": {

        "required_extension": ".csv",

        "file_must_exist": True,

        "file_must_be_readable": True,

        "file_must_contain_structured_data": True

    },

    "loading": {

        "method": "pandas.read_csv",

        "description":
            "Load the IONM CSV dataset into a structured table."
    },

    "extraction": {

        "signal_data": {
            "method": "DataFrame numeric-column extraction",
            "output": "numpy.ndarray"
        },

        "channels": {
            "method": "Signal column identification",
            "output": "list"
        },

        "timestamps": {
            "method":
                "Timestamp/time column when available",
            "output": "numpy.ndarray or None"
        },

        "sampling_rate": {
            "method":
                "Explicit dataset metadata/configuration",
            "output": "float or None"
        },

        "metadata": {
            "method":
                "CSV structure and column metadata",
            "output": "dictionary"
        },

        "signal_labels": {
            "method":
                "Column names / signal identifiers",
            "output": "list"
        }
    },

    "validation": {

        "signal_data_not_empty": True,

        "numeric_signal_columns_required": True,

        "data_contains_valid_numeric_values": True,

        "signal_labels_should_be_preserved": True,

        "sampling_rate_must_be_verified_before_time_based_analysis":
            True

    },

    "standardized_output": STANDARDIZED_OUTPUT,

    "compatible_downstream_stages": [

        "Preprocessing",

        "Signal Processing",

        "Statistical Analysis",

        "Time-Series Analysis",

        "IONM Analysis",

        "Visualization"

    ],

    "assembly_rules": {

        "reader": "pandas.read_csv",

        "identify_signal_columns": True,

        "preserve_signal_labels": True,

        "identify_timestamp_column_when_available": True,

        "validate_signal_structure": True,

        "require_sampling_rate_for_frequency_analysis": True,

        "standardize_output": True

    }
}


# ============================================================
# 7. INTRACORTICAL / EXTRACELLULAR → CSV
# ============================================================

INTRACORTICAL_CSV = {

    "id": "intracortical_csv",

    "name": "Intracortical / Extracellular",

    "modality": "Intracortical / Extracellular",

    "file_type": "CSV",

    "extensions": [
        ".csv"
    ],

    "reader": {
        "library": "pandas",
        "function": "pandas.read_csv"
    },

    "dependencies": [
        "pandas",
        "numpy"
    ],

    "input_requirements": {

        "required_extension": ".csv",

        "file_must_exist": True,

        "file_must_be_readable": True,

        "file_must_contain_structured_data": True

    },

    "loading": {

        "method": "pandas.read_csv",

        "description":
            "Load the extracellular/intracortical dataset."
    },

    "extraction": {

        "signal_data": {
            "method": "Numeric-column extraction",
            "output": "numpy.ndarray"
        },

        "timestamps": {
            "method":
                "Timestamp column when available",
            "output": "numpy.ndarray or None"
        },

        "channels": {
            "method":
                "Channel/electrode/unit identifiers",
            "output": "list or None"
        },

        "sampling_rate": {
            "method":
                "Explicit dataset metadata/configuration",
            "output": "float or None"
        },

        "metadata": {
            "method":
                "CSV structure and column metadata",
            "output": "dictionary"
        },

        "unit_identifiers": {
            "method":
                "Unit/neuron identifiers when present",
            "output": "list or None"
        }
    },

    "validation": {

        "signal_data_not_empty": True,

        "numeric_data_required": True,

        "data_contains_valid_numeric_values": True,

        "sampling_rate_must_be_verified_before_time_based_analysis":
            True

    },

    "standardized_output": STANDARDIZED_OUTPUT,

    "compatible_downstream_stages": [

        "Preprocessing",

        "Signal Processing",

        "Statistical Analysis",

        "Time-Series Analysis",

        "Spike Analysis",

        "Neural Population Analysis",

        "Neural Decoding",

        "Machine Learning",

        "Visualization"

    ],

    "assembly_rules": {

        "reader": "pandas.read_csv",

        "identify_numeric_signal_columns": True,

        "identify_timestamp_column_when_available": True,

        "identify_channel_identifiers_when_available": True,

        "identify_unit_identifiers_when_available": True,

        "validate_signal_structure": True,

        "require_sampling_rate_for_frequency_analysis": True,

        "standardize_output": True

    }
}


# ============================================================
# 8. MASTER INGESTION RESOURCE REGISTRY
# ============================================================
#
# This is the authoritative registry.
#
# Every resource is represented by its actual resource
# definition rather than merely by a string name.
# ============================================================

INGESTION_RESOURCES = {

    "eeg_eeglab": EEG_EEGLAB,

    "eeg_edf": EEG_EDF,

    "eeg_csv": EEG_CSV,

    "ionm_csv": IONM_CSV,

    "intracortical_csv": INTRACORTICAL_CSV

}


# ============================================================
# 9. RESOURCE ALIASES
# ============================================================
#
# The user's parameter object may use a human-friendly name
# rather than the canonical registry identifier.
#
# The generator should NOT need to know all of these aliases.
#
# The Master-DOC owns them.
# ============================================================

INGESTION_RESOURCE_ALIASES = {

    # --------------------------------------------------------
    # EEG
    # --------------------------------------------------------

    "eeg":
        "eeg_edf",

    "EEG":
        "eeg_edf",

    "eeg_edf":
        "eeg_edf",

    "edf":
        "eeg_edf",

    "eeg_eeglab":
        "eeg_eeglab",

    "eeglab":
        "eeg_eeglab",

    "set":
        "eeg_eeglab",

    "eeg_csv":
        "eeg_csv",

    # --------------------------------------------------------
    # IONM
    # --------------------------------------------------------

    "ionm":
        "ionm_csv",

    "ionm_csv":
        "ionm_csv",

    # --------------------------------------------------------
    # INTRACORTICAL
    # --------------------------------------------------------

    "intracortical":
        "intracortical_csv",

    "extracellular":
        "intracortical_csv",

    "intracortical_csv":
        "intracortical_csv"
}


# ============================================================
# 10. NORMALIZE RESOURCE NAME
# ============================================================

def normalize_resource_name(
    name
):

    if name is None:

        return ""

    return (
        str(name)
        .strip()
        .lower()
        .replace("-", "_")
        .replace(" ", "_")
    )


# ============================================================
# 11. RESOLVE RESOURCE
# ============================================================
#
# This is the primary interface used by generator.py.
#
# It returns the COMPLETE resource definition.
# ============================================================

def resolve_resource(
    name,
    file_type=None
):

    normalized_name = (
        normalize_resource_name(
            name
        )
    )

    normalized_file_type = (
        normalize_resource_name(
            file_type
        )
    )

    # --------------------------------------------------------
    # Explicit modality + file-format resolution
    # --------------------------------------------------------

    if normalized_name == "eeg":

        if normalized_file_type in {
            "edf",
            ".edf"
        }:

            return EEG_EDF

        if normalized_file_type in {
            "set",
            ".set",
            "eeglab"
        }:

            return EEG_EEGLAB

        if normalized_file_type in {
            "csv",
            ".csv"
        }:

            return EEG_CSV

        # Default EEG resource.
        #
        # EDF is the current project input target.
        return EEG_EDF

    # --------------------------------------------------------
    # Alias resolution
    # --------------------------------------------------------

    canonical_name = (
        INGESTION_RESOURCE_ALIASES.get(
            normalized_name
        )
    )

    if canonical_name is None:

        return None

    return INGESTION_RESOURCES.get(
        canonical_name
    )


# ============================================================
# 12. GET RESOURCE
# ============================================================
#
# Compatibility alias for generator.py / future modules.
# ============================================================

def get_resource(
    name,
    file_type=None
):

    return resolve_resource(
        name,
        file_type
    )


# ============================================================
# 13. LIST RESOURCES
# ============================================================

def list_resources():

    return dict(
        INGESTION_RESOURCES
    )


# ============================================================
# 14. RESOURCE EXISTS
# ============================================================

def resource_exists(
    name,
    file_type=None
):

    return (
        resolve_resource(
            name,
            file_type
        )
        is not None
    )


# ============================================================
# 15. GET RESOURCE ID
# ============================================================

def get_resource_id(
    name,
    file_type=None
):

    resource = resolve_resource(
        name,
        file_type
    )

    if resource is None:

        return None

    return resource.get(
        "id"
    )


# ============================================================
# 16. GET RESOURCE READER
# ============================================================

def get_resource_reader(
    name,
    file_type=None
):

    resource = resolve_resource(
        name,
        file_type
    )

    if resource is None:

        return None

    return resource.get(
        "reader"
    )


# ============================================================
# 17. GET RESOURCE DEPENDENCIES
# ============================================================

def get_resource_dependencies(
    name,
    file_type=None
):

    resource = resolve_resource(
        name,
        file_type
    )

    if resource is None:

        return []

    return list(
        resource.get(
            "dependencies",
            []
        )
    )


# ============================================================
# 18. GET RESOURCE ASSEMBLY RULES
# ============================================================

def get_resource_assembly_rules(
    name,
    file_type=None
):

    resource = resolve_resource(
        name,
        file_type
    )

    if resource is None:

        return {}

    return dict(
        resource.get(
            "assembly_rules",
            {}
        )
    )


# ============================================================
# 19. VALIDATE FILE TYPE FOR RESOURCE
# ============================================================

def supports_file_type(
    name,
    file_type
):

    resource = resolve_resource(
        name,
        file_type
    )

    if resource is None:

        return False

    normalized_extension = (
        normalize_resource_name(
            file_type
        )
    )

    extensions = [
        normalize_resource_name(
            extension
        )
        for extension in resource.get(
            "extensions",
            []
        )
    ]

    return (
        normalized_extension
        in extensions
    )


# ============================================================
# 20. MASTER-DOC INFORMATION
# ============================================================

MASTER_DOC = {

    "name":
        "Master-DOC-Ingestion",

    "role":
        "ingestion",

    "description":
        "Raw neural-data ingestion resource library",

    "resource_count":
        len(INGESTION_RESOURCES),

    "resources":
        list(
            INGESTION_RESOURCES.keys()
        ),

    "supports_resource_resolution":
        True,

    "supports_edf":
        True,

    "standardized_output":
        STANDARDIZED_OUTPUT
}


# ============================================================
# 21. DIRECT TEST
# ============================================================
#
# Running:
#
#     python Master-DOC-Ingestion.py
#
# should NOT start the GUI or ingest an EEG file.
#
# It simply verifies that the Master-DOC can resolve the
# resources required by the generator.
# ============================================================

if __name__ == "__main__":

    print(
        "=" * 70
    )

    print(
        "MASTER-DOC INGESTION RESOURCE TEST"
    )

    print(
        "=" * 70
    )

    print()

    print(
        "Available resources:"
    )

    for resource_id in INGESTION_RESOURCES:

        print(
            f"  ✓ {resource_id}"
        )

    print()

    print(
        "Resolution tests:"
    )

    tests = [

        ("EEG", ".edf"),

        ("EEG", ".set"),

        ("EEG", ".csv"),

        ("ionm", ".csv"),

        ("intracortical", ".csv")

    ]

    for resource_name, file_type in tests:

        resource = resolve_resource(
            resource_name,
            file_type
        )

        if resource is None:

            print(
                f"  ✗ {resource_name} "
                f"+ {file_type}"
            )

        else:

            print(
                f"  ✓ {resource_name} "
                f"+ {file_type}"
                f" -> "
                f"{resource['id']}"
            )

    print()

    print(
        "=" * 70
    )

