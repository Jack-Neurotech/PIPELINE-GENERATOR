"""
============================================================
MASTER-DATA-INGESTION.PY
============================================================

PURPOSE
-------
Master raw-material library for the Neural Analysis Pipeline
Generator's DATA INGESTION layer.

This file does NOT represent every neural-data format that
exists in the world.

It contains ONLY the ingestion combinations currently exposed
by Ingestion.py and supported by the current project:

    EEG
        ├── EEGLAB (.set)
        └── CSV

    IONM
        └── CSV

    Intracortical / Extracellular
        └── CSV

The generator can use this document to determine:

    1. Which reader to use
    2. Which dependencies are required
    3. How the file should be validated
    4. What information should be extracted
    5. What standardized object should be produced
    6. What downstream pipeline stages can consume it
    7. How the ingestion component should be assembled

IMPORTANT
---------
This is a RESOURCE LIBRARY.

It is not the GUI.
It is not the pipeline generator.
It is not analysis.py.

analysis.py will eventually use these resources to construct
the actual ingestion code required by the user's parameters.
============================================================
"""


# ============================================================
# 1. STANDARDIZED INGESTION CONTRACT
# ============================================================
#
# Every ingestion method must ultimately produce the same
# conceptual structure.
#
# This allows preprocessing, signal analysis, statistics, etc.
# to operate on the resulting neural data without needing to
# know how the original file was stored.
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
        "description": "Channel spatial/location metadata when available",
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
#
# These requirements apply to every supported ingestion method.
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
#
# Supported file:
#
#     .set
#
# Primary reader:
#
#     MNE-Python
#     mne.io.read_raw_eeglab()
#
# The generated ingestion code should load the EEGLAB file,
# extract the EEG signal and associated metadata, and convert
# the result into the standardized ingestion structure.
# ============================================================

EEG_EEGLAB = {

    "id": "eeg_eeglab",

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
            "Load the EEGLAB dataset into an MNE Raw object."
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

        "metadata": {
            "method": "raw.info",
            "output": "dictionary-like metadata"
        },

        "timestamps": {
            "method": "raw.times",
            "output": "numpy.ndarray"
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
# 4. EEG → CSV
# ============================================================
#
# CSV is treated as a generic structured-data input.
#
# Because CSV files can have many different layouts, the
# generated pipeline must validate the structure rather than
# assuming every CSV represents the same EEG organization.
# ============================================================

EEG_CSV = {

    "id": "eeg_csv",

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
# 5. IONM → CSV
# ============================================================
#
# IONM CSV files can contain multiple signal types and channels.
#
# Therefore the ingestion layer should preserve the raw
# structured signal information rather than making assumptions
# about one particular IONM device/vendor.
# ============================================================

IONM_CSV = {

    "id": "ionm_csv",

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
# 6. INTRACORTICAL / EXTRACELLULAR → CSV
# ============================================================
#
# CSV may contain sampled voltage traces, spike/event data,
# channel/unit identifiers, timestamps, or other structured
# extracellular recordings.
#
# The ingestion layer should preserve the structure so the
# downstream spike-analysis / population-analysis modules can
# determine how to interpret it.
# ============================================================

INTRACORTICAL_CSV = {

    "id": "intracortical_csv",

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
# 7. INGESTION RESOURCE REGISTRY
# ============================================================
#
# This is the main lookup table that analysis.py can eventually
# use to retrieve the correct ingestion resource.
#
# KEY:
#
#     (neural_data, file_type)
#
# VALUE:
#
#     corresponding raw-material specification
# ============================================================

INGESTION_RESOURCES = {

    ("EEG", "EEGLAB"): EEG_EEGLAB,

    ("EEG", "CSV"): EEG_CSV,

    ("IONM", "CSV"): IONM_CSV,

    ("Intracortical / Extracellular", "CSV"):
        INTRACORTICAL_CSV

}


# ============================================================
# 8. SUPPORTED NEURAL-DATA OPTIONS
# ============================================================
#
# This must remain synchronized with Ingestion.py.
# ============================================================

SUPPORTED_NEURAL_DATA = {

    "EEG": [
        "EEGLAB",
        "CSV"
    ],

    "IONM": [
        "CSV"
    ],

    "Intracortical / Extracellular": [
        "CSV"
    ]

}


# ============================================================
# 9. COMPATIBILITY CHECK
# ============================================================
#
# Prevents analysis.py from requesting an ingestion combination
# that does not exist in this Master Document.
# ============================================================

def is_supported(neural_data, file_type):
    """
    Determine whether a neural-data/file-type combination has
    a corresponding ingestion resource.
    """

    return (
        neural_data,
        file_type
    ) in INGESTION_RESOURCES


# ============================================================
# 10. RETRIEVE INGESTION RESOURCE
# ============================================================

def get_ingestion_resource(neural_data, file_type):
    """
    Return the complete raw-material specification for the
    requested neural-data/file-type combination.

    Raises:
        ValueError
            If the combination is not supported.
    """

    key = (
        neural_data,
        file_type
    )

    if key not in INGESTION_RESOURCES:

        raise ValueError(
            f"Unsupported ingestion combination: "
            f"{neural_data} + {file_type}"
        )

    return INGESTION_RESOURCES[key]


# ============================================================
# 11. LIST ALL SUPPORTED INGESTION COMBINATIONS
# ============================================================

def list_supported_ingestion():
    """
    Return every currently supported neural-data/file-type
    combination.
    """

    return list(
        INGESTION_RESOURCES.keys()
    )


# ============================================================
# 12. VALIDATE STANDARDIZED OUTPUT
# ============================================================

def validate_standardized_output(data_object):
    """
    Verify that the generated ingestion result contains the
    minimum required standardized fields.
    """

    required_fields = [

        "data",

        "modality",

        "file_type",

        "source_file"

    ]

    missing = [

        field

        for field in required_fields

        if field not in data_object

    ]

    if missing:

        raise ValueError(
            "Missing standardized ingestion fields: "
            + ", ".join(missing)
        )

    return True


# ============================================================
# 13. RESOURCE SUMMARY
# ============================================================

MASTER_DOCUMENT_SUMMARY = {

    "document": "Master-Data-Ingestion",

    "purpose":
        "Raw materials for neural-data file ingestion",

    "supported_modalities": [

        "EEG",

        "IONM",

        "Intracortical / Extracellular"

    ],

    "supported_combinations": len(
        INGESTION_RESOURCES
    ),

    "standardized_output": STANDARDIZED_OUTPUT,

    "resource_registry":
        "INGESTION_RESOURCES",

    "generator_interface":
        "get_ingestion_resource()"

}


# ============================================================
# 14. DIRECT TEST
# ============================================================
#
# Running this file directly does NOT ingest a real file.
# It simply verifies that the Master Document is internally
# consistent.
# ============================================================

if __name__ == "__main__":

    print("=" * 60)

    print("MASTER-DATA-INGESTION")

    print("=" * 60)

    print()

    print("Supported ingestion combinations:")

    for modality, file_type in list_supported_ingestion():

        print(
            f"  {modality} → {file_type}"
        )

    print()

    print(
        "Total supported combinations:",
        len(INGESTION_RESOURCES)
    )

    print()

    print("Master Document loaded successfully.")

    print("=" * 60)