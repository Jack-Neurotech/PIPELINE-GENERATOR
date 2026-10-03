"""
====================================================================
MASTER-DOC-VALIDATION.PY
====================================================================

PURPOSE
-------
Master raw-material library for validating pipeline combinations.

This document provides the Pipeline Generator with rules that answer:

    "Can these selected components actually be assembled together?"

The generator can use this document to validate combinations of:

    neural data type
    file type
    pipeline type
    preprocessing
    statistics
    decoding
    visualization
    output

IMPORTANT
---------
This document is a VALIDATION / COMPATIBILITY LIBRARY.

It does not perform the actual neural-data analysis.

It does not generate popup reports.

Results are intended to be displayed in the terminal.

The generator should reject incompatible combinations rather than
attempting to generate code that cannot work.

====================================================================
"""


# ==================================================================
# 1. VALIDATION RESULT
# ==================================================================

def validation_result(
    valid,
    message,
    errors=None,
    warnings=None
):
    """
    Create a standardized validation result.
    """

    return {
        "valid": bool(valid),
        "message": message,
        "errors": errors or [],
        "warnings": warnings or []
    }


# ==================================================================
# 2. SUPPORTED NEURAL DATA TYPES
# ==================================================================

SUPPORTED_NEURAL_DATA_TYPES = {

    "EEG",
    "ECoG",
    "LFP",
    "intracortical",
    "MEG"

}


# ==================================================================
# 3. SUPPORTED PIPELINE TYPES
# ==================================================================

SUPPORTED_PIPELINE_TYPES = {

    "EEG",
    "ECoG",
    "LFP",
    "intracortical",
    "MEG",

    "neural_decoding",
    "BCI_decoding",
    "intracortical_decoding"

}


# ==================================================================
# 4. FILE TYPE COMPATIBILITY
# ==================================================================

FILE_TYPE_COMPATIBILITY = {

    "EEG": {

        ".edf",
        ".bdf",
        ".set",
        ".fif",
        ".vhdr",
        ".cnt",
        ".csv",
        ".txt",
        ".npy"

    },

    "ECoG": {

        ".edf",
        ".fif",
        ".mat",
        ".npy",
        ".csv",
        ".txt"

    },

    "LFP": {

        ".npy",
        ".mat",
        ".csv",
        ".txt",
        ".fif"

    },

    "intracortical": {

        ".npy",
        ".mat",
        ".csv",
        ".txt"

    },

    "MEG": {

        ".fif",
        ".ds",
        ".con",
        ".sqd",
        ".csv",
        ".npy"

    }

}


# ==================================================================
# 5. PIPELINE / NEURAL-DATA COMPATIBILITY
# ==================================================================

PIPELINE_DATA_COMPATIBILITY = {

    "EEG": {

        "EEG"

    },

    "ECoG": {

        "ECoG"

    },

    "LFP": {

        "LFP"

    },

    "intracortical": {

        "intracortical"

    },

    "MEG": {

        "MEG"

    },

    "neural_decoding": {

        "EEG",
        "ECoG",
        "LFP",
        "intracortical",
        "MEG"

    },

    "BCI_decoding": {

        "EEG",
        "ECoG",
        "LFP",
        "intracortical",
        "MEG"

    },

    "intracortical_decoding": {

        "intracortical",
        "LFP"

    }

}


# ==================================================================
# 6. PREPROCESSING COMPATIBILITY
# ==================================================================

PREPROCESSING_COMPATIBILITY = {

    "filtering": {

        "EEG",
        "ECoG",
        "LFP",
        "intracortical",
        "MEG"

    },

    "bandpass_filter": {

        "EEG",
        "ECoG",
        "LFP",
        "intracortical",
        "MEG"

    },

    "highpass_filter": {

        "EEG",
        "ECoG",
        "LFP",
        "intracortical",
        "MEG"

    },

    "lowpass_filter": {

        "EEG",
        "ECoG",
        "LFP",
        "intracortical",
        "MEG"

    },

    "notch_filter": {

        "EEG",
        "ECoG",
        "LFP",
        "intracortical",
        "MEG"

    },

    "standardization": {

        "EEG",
        "ECoG",
        "LFP",
        "intracortical",
        "MEG"

    },

    "normalization": {

        "EEG",
        "ECoG",
        "LFP",
        "intracortical",
        "MEG"

    },

    "detrending": {

        "EEG",
        "ECoG",
        "LFP",
        "intracortical",
        "MEG"

    }

}


# ==================================================================
# 7. STATISTICAL ANALYSIS COMPATIBILITY
# ==================================================================

STATISTICS_COMPATIBILITY = {

    "mean": {

        "EEG",
        "ECoG",
        "LFP",
        "intracortical",
        "MEG"

    },

    "std": {

        "EEG",
        "ECoG",
        "LFP",
        "intracortical",
        "MEG"

    },

    "variance": {

        "EEG",
        "ECoG",
        "LFP",
        "intracortical",
        "MEG"

    },

    "rms": {

        "EEG",
        "ECoG",
        "LFP",
        "intracortical",
        "MEG"

    },

    "minimum": {

        "EEG",
        "ECoG",
        "LFP",
        "intracortical",
        "MEG"

    },

    "maximum": {

        "EEG",
        "ECoG",
        "LFP",
        "intracortical",
        "MEG"

    },

    "peak": {

        "EEG",
        "ECoG",
        "LFP",
        "intracortical",
        "MEG"

    },

    "spectral_power": {

        "EEG",
        "ECoG",
        "LFP",
        "MEG"

    },

    "dominant_frequency": {

        "EEG",
        "ECoG",
        "LFP",
        "MEG"

    },

    "peak_alpha_frequency": {

        "EEG",
        "ECoG",
        "MEG"

    },

    "spectral_entropy": {

        "EEG",
        "ECoG",
        "LFP",
        "MEG"

    },

    "spectral_edge": {

        "EEG",
        "ECoG",
        "LFP",
        "MEG"

    },

    "band_power": {

        "EEG",
        "ECoG",
        "LFP",
        "MEG"

    },

    "band_power_ratio": {

        "EEG",
        "ECoG",
        "LFP",
        "MEG"

    }

}


# ==================================================================
# 8. DECODING COMPATIBILITY
# ==================================================================

DECODING_COMPATIBILITY = {

    "neural_decoding": {

        "EEG",
        "ECoG",
        "LFP",
        "intracortical",
        "MEG"

    },

    "BCI_decoding": {

        "EEG",
        "ECoG",
        "LFP",
        "intracortical",
        "MEG"

    },

    "intracortical_decoding": {

        "intracortical",
        "LFP"

    }

}


# ==================================================================
# 9. DECODER / TARGET COMPATIBILITY
# ==================================================================

DECODER_TARGET_COMPATIBILITY = {

    "linear_regression": {

        "continuous"

    },

    "logistic_regression": {

        "binary",
        "multiclass"

    },

    "svm": {

        "binary",
        "multiclass"

    },

    "knn": {

        "binary",
        "multiclass"

    }

}


# ==================================================================
# 10. FEATURE COMPATIBILITY
# ==================================================================

FEATURE_COMPATIBILITY = {

    "raw": {

        "EEG",
        "ECoG",
        "LFP",
        "intracortical",
        "MEG"

    },

    "mean": {

        "EEG",
        "ECoG",
        "LFP",
        "intracortical",
        "MEG"

    },

    "std": {

        "EEG",
        "ECoG",
        "LFP",
        "intracortical",
        "MEG"

    },

    "variance": {

        "EEG",
        "ECoG",
        "LFP",
        "intracortical",
        "MEG"

    },

    "rms": {

        "EEG",
        "ECoG",
        "LFP",
        "intracortical",
        "MEG"

    },

    "peak": {

        "EEG",
        "ECoG",
        "LFP",
        "intracortical",
        "MEG"

    },

    "minimum": {

        "EEG",
        "ECoG",
        "LFP",
        "intracortical",
        "MEG"

    },

    "maximum": {

        "EEG",
        "ECoG",
        "LFP",
        "intracortical",
        "MEG"

    },

    "frequency": {

        "EEG",
        "ECoG",
        "LFP",
        "intracortical",
        "MEG"

    },

    "band_power": {

        "EEG",
        "ECoG",
        "LFP",
        "MEG"

    }

}


# ==================================================================
# 11. REQUIRED INPUTS
# ==================================================================

REQUIRED_COMPONENTS = {

    "file_ingestion": {

        "required": True

    },

    "preprocessing": {

        "required": False

    },

    "statistics": {

        "required": False

    },

    "features": {

        "required": False

    },

    "targets": {

        "required": False

    },

    "decoder": {

        "required": False

    },

    "evaluation": {

        "required": False

    },

    "visualization": {

        "required": False

    },

    "terminal_output": {

        "required": True

    }

}


# ==================================================================
# 12. DECODING REQUIRED COMPONENTS
# ==================================================================

DECODING_REQUIRED_COMPONENTS = {

    "features": True,

    "targets": True,

    "train_test_split": True,

    "decoder": True,

    "prediction": True,

    "evaluation": True,

    "terminal_output": True

}


# ==================================================================
# 13. OUTPUT RULES
# ==================================================================

OUTPUT_RULES = {

    "terminal_output": True,

    "popup_report": False,

    "popup_required": False,

    "terminal_required": True

}


# ==================================================================
# 14. VALIDATE NEURAL DATA TYPE
# ==================================================================

def validate_neural_data_type(
    neural_data
):
    """
    Validate neural-data type.
    """

    if neural_data not in SUPPORTED_NEURAL_DATA_TYPES:

        return validation_result(
            False,
            f"Unsupported neural data type: {neural_data}",
            [
                f"{neural_data} is not in the supported "
                "neural-data library."
            ]
        )

    return validation_result(
        True,
        f"Neural data type '{neural_data}' is supported."
    )


# ==================================================================
# 15. VALIDATE FILE TYPE
# ==================================================================

def validate_file_type(
    neural_data,
    file_type
):
    """
    Validate whether a file type can be used with
    the selected neural-data type.
    """

    if neural_data not in SUPPORTED_NEURAL_DATA_TYPES:

        return validation_result(
            False,
            "Unknown neural data type."
        )

    if file_type.startswith(".") is False:

        file_type = "." + file_type

    compatible_files = (
        FILE_TYPE_COMPATIBILITY[
            neural_data
        ]
    )

    if file_type not in compatible_files:

        return validation_result(
            False,
            f"File type '{file_type}' is not compatible "
            f"with '{neural_data}'.",
            [
                f"Compatible file types: "
                f"{sorted(compatible_files)}"
            ]
        )

    return validation_result(
        True,
        f"File type '{file_type}' is compatible "
        f"with '{neural_data}'."
    )


# ==================================================================
# 16. VALIDATE PIPELINE
# ==================================================================

def validate_pipeline(
    neural_data,
    pipeline_type
):
    """
    Validate pipeline / neural-data compatibility.
    """

    if pipeline_type not in PIPELINE_DATA_COMPATIBILITY:

        return validation_result(
            False,
            f"Unsupported pipeline type: {pipeline_type}"
        )

    compatible_data = (
        PIPELINE_DATA_COMPATIBILITY[
            pipeline_type
        ]
    )

    if neural_data not in compatible_data:

        return validation_result(
            False,
            f"Pipeline '{pipeline_type}' cannot use "
            f"'{neural_data}' data.",
            [
                f"Compatible neural data: "
                f"{sorted(compatible_data)}"
            ]
        )

    return validation_result(
        True,
        f"Pipeline '{pipeline_type}' is compatible "
        f"with '{neural_data}'."
    )


# ==================================================================
# 17. VALIDATE PREPROCESSING
# ==================================================================

def validate_preprocessing(
    neural_data,
    preprocessing
):
    """
    Validate preprocessing compatibility.
    """

    if preprocessing not in PREPROCESSING_COMPATIBILITY:

        return validation_result(
            False,
            f"Unsupported preprocessing method: "
            f"{preprocessing}"
        )

    if neural_data not in (
        PREPROCESSING_COMPATIBILITY[
            preprocessing
        ]
    ):

        return validation_result(
            False,
            f"Preprocessing '{preprocessing}' "
            f"is not compatible with '{neural_data}'."
        )

    return validation_result(
        True,
        f"Preprocessing '{preprocessing}' is compatible."
    )


# ==================================================================
# 18. VALIDATE STATISTICS
# ==================================================================

def validate_statistic(
    neural_data,
    statistic
):
    """
    Validate statistical-analysis compatibility.
    """

    if statistic not in STATISTICS_COMPATIBILITY:

        return validation_result(
            False,
            f"Unsupported statistic: {statistic}"
        )

    if neural_data not in (
        STATISTICS_COMPATIBILITY[
            statistic
        ]
    ):

        return validation_result(
            False,
            f"Statistic '{statistic}' is not compatible "
            f"with '{neural_data}'."
        )

    return validation_result(
        True,
        f"Statistic '{statistic}' is compatible."
    )


# ==================================================================
# 19. VALIDATE FEATURE
# ==================================================================

def validate_feature(
    neural_data,
    feature
):
    """
    Validate decoding-feature compatibility.
    """

    if feature not in FEATURE_COMPATIBILITY:

        return validation_result(
            False,
            f"Unsupported feature: {feature}"
        )

    if neural_data not in (
        FEATURE_COMPATIBILITY[
            feature
        ]
    ):

        return validation_result(
            False,
            f"Feature '{feature}' is not compatible "
            f"with '{neural_data}'."
        )

    return validation_result(
        True,
        f"Feature '{feature}' is compatible."
    )


# ==================================================================
# 20. VALIDATE DECODER
# ==================================================================

def validate_decoder(
    decoder,
    target_type
):
    """
    Validate decoder / target compatibility.
    """

    if decoder not in DECODER_TARGET_COMPATIBILITY:

        return validation_result(
            False,
            f"Unsupported decoder: {decoder}"
        )

    compatible_targets = (
        DECODER_TARGET_COMPATIBILITY[
            decoder
        ]
    )

    if target_type not in compatible_targets:

        return validation_result(
            False,
            f"Decoder '{decoder}' cannot use "
            f"target type '{target_type}'.",
            [
                f"Compatible target types: "
                f"{sorted(compatible_targets)}"
            ]
        )

    return validation_result(
        True,
        f"Decoder '{decoder}' is compatible "
        f"with target type '{target_type}'."
    )


# ==================================================================
# 21. VALIDATE COMPLETE DECODING CONFIGURATION
# ==================================================================

def validate_decoding_configuration(
    neural_data,
    pipeline_type,
    features,
    decoder,
    target_type
):
    """
    Validate the entire decoding configuration.
    """

    errors = []

    pipeline_check = validate_pipeline(
        neural_data,
        pipeline_type
    )

    if not pipeline_check["valid"]:

        errors.extend(
            pipeline_check["errors"]
        )

    for feature in features:

        feature_check = validate_feature(
            neural_data,
            feature
        )

        if not feature_check["valid"]:

            errors.append(
                feature_check["message"]
            )

    decoder_check = validate_decoder(
        decoder,
        target_type
    )

    if not decoder_check["valid"]:

        errors.extend(
            decoder_check["errors"]
        )

    if errors:

        return validation_result(
            False,
            "Decoding configuration is not valid.",
            errors
        )

    return validation_result(
        True,
        "Decoding configuration is valid."
    )


# ==================================================================
# 22. VALIDATE COMPLETE PIPELINE CONFIGURATION
# ==================================================================

def validate_pipeline_configuration(
    neural_data,
    file_type,
    pipeline_type,
    preprocessing=None,
    statistics=None,
    features=None,
    decoder=None,
    target_type=None
):
    """
    Validate an entire proposed pipeline.

    This is the primary validation function that the
    Pipeline Generator should call before generating code.
    """

    errors = []
    warnings = []

    features = features or []
    statistics = statistics or []

    # --------------------------------------------------------------
    # Neural data
    # --------------------------------------------------------------

    check = validate_neural_data_type(
        neural_data
    )

    if not check["valid"]:

        errors.append(
            check["message"]
        )

    # --------------------------------------------------------------
    # File
    # --------------------------------------------------------------

    check = validate_file_type(
        neural_data,
        file_type
    )

    if not check["valid"]:

        errors.append(
            check["message"]
        )

    # --------------------------------------------------------------
    # Pipeline
    # --------------------------------------------------------------

    check = validate_pipeline(
        neural_data,
        pipeline_type
    )

    if not check["valid"]:

        errors.append(
            check["message"]
        )

    # --------------------------------------------------------------
    # Preprocessing
    # --------------------------------------------------------------

    if preprocessing is not None:

        if isinstance(
            preprocessing,
            str
        ):

            preprocessing = [
                preprocessing
            ]

        for method in preprocessing:

            check = validate_preprocessing(
                neural_data,
                method
            )

            if not check["valid"]:

                errors.append(
                    check["message"]
                )

    # --------------------------------------------------------------
    # Statistics
    # --------------------------------------------------------------

    for statistic in statistics:

        check = validate_statistic(
            neural_data,
            statistic
        )

        if not check["valid"]:

            errors.append(
                check["message"]
            )

    # --------------------------------------------------------------
    # Features
    # --------------------------------------------------------------

    for feature in features:

        check = validate_feature(
            neural_data,
            feature
        )

        if not check["valid"]:

            errors.append(
                check["message"]
            )

    # --------------------------------------------------------------
    # Decoding
    # --------------------------------------------------------------

    decoding_requested = (
        decoder is not None
        or
        target_type is not None
        or
        len(features) > 0
    )

    if decoding_requested:

        if decoder is None:

            errors.append(
                "Decoding requires a decoder."
            )

        if target_type is None:

            errors.append(
                "Decoding requires a target type."
            )

        if not features:

            errors.append(
                "Decoding requires at least "
                "one feature."
            )

        if (
            decoder is not None
            and
            target_type is not None
            and
            features
        ):

            decoding_check = (
                validate_decoding_configuration(
                    neural_data,
                    pipeline_type,
                    features,
                    decoder,
                    target_type
                )
            )

            if not decoding_check["valid"]:

                errors.extend(
                    decoding_check["errors"]
                )

    # --------------------------------------------------------------
    # Output
    # --------------------------------------------------------------

    if OUTPUT_RULES[
        "terminal_required"
    ] is False:

        errors.append(
            "Terminal output must remain enabled."
        )

    if errors:

        return validation_result(
            False,
            "Pipeline configuration is NOT valid.",
            errors,
            warnings
        )

    return validation_result(
        True,
        "Pipeline configuration is valid.",
        [],
        warnings
    )


# ==================================================================
# 23. RETURN ALL COMPATIBLE FILE TYPES
# ==================================================================

def get_compatible_file_types(
    neural_data
):
    """
    Return all file types compatible with a neural-data type.
    """

    return sorted(
        FILE_TYPE_COMPATIBILITY.get(
            neural_data,
            set()
        )
    )


# ==================================================================
# 24. RETURN ALL COMPATIBLE PIPELINES
# ==================================================================

def get_compatible_pipelines(
    neural_data
):
    """
    Return all pipeline types compatible with a neural-data type.
    """

    return [

        pipeline

        for pipeline, data_types
        in PIPELINE_DATA_COMPATIBILITY.items()

        if neural_data in data_types

    ]


# ==================================================================
# 25. RETURN ALL COMPATIBLE STATISTICS
# ==================================================================

def get_compatible_statistics(
    neural_data
):
    """
    Return all statistics compatible with a neural-data type.
    """

    return [

        statistic

        for statistic, data_types
        in STATISTICS_COMPATIBILITY.items()

        if neural_data in data_types

    ]


# ==================================================================
# 26. RETURN ALL COMPATIBLE PREPROCESSING
# ==================================================================

def get_compatible_preprocessing(
    neural_data
):
    """
    Return all preprocessing methods compatible with
    a neural-data type.
    """

    return [

        method

        for method, data_types
        in PREPROCESSING_COMPATIBILITY.items()

        if neural_data in data_types

    ]


# ==================================================================
# 27. RETURN ALL COMPATIBLE FEATURES
# ==================================================================

def get_compatible_features(
    neural_data
):
    """
    Return all decoding features compatible with
    a neural-data type.
    """

    return [

        feature

        for feature, data_types
        in FEATURE_COMPATIBILITY.items()

        if neural_data in data_types

    ]


# ==================================================================
# 28. RETURN ALL COMPATIBLE DECODERS
# ==================================================================

def get_compatible_decoders(
    target_type
):
    """
    Return decoders compatible with a target type.
    """

    return [

        decoder

        for decoder, target_types
        in DECODER_TARGET_COMPATIBILITY.items()

        if target_type in target_types

    ]


# ==================================================================
# 29. GENERATOR COMPATIBILITY MATRIX
# ==================================================================

def get_compatibility_matrix(
    neural_data
):
    """
    Return all compatible generator components for a neural-data type.
    """

    if neural_data not in SUPPORTED_NEURAL_DATA_TYPES:

        raise ValueError(
            f"Unsupported neural data type: "
            f"{neural_data}"
        )

    return {

        "neural_data":
            neural_data,

        "file_types":
            get_compatible_file_types(
                neural_data
            ),

        "pipelines":
            get_compatible_pipelines(
                neural_data
            ),

        "preprocessing":
            get_compatible_preprocessing(
                neural_data
            ),

        "statistics":
            get_compatible_statistics(
                neural_data
            ),

        "features":
            get_compatible_features(
                neural_data
            )

    }


# ==================================================================
# 30. GENERATOR RULE
# ==================================================================

def can_generate_pipeline(
    **configuration
):
    """
    Final boolean gate for the Pipeline Generator.

    Returns True only when the proposed configuration passes
    all validation rules.
    """

    result = validate_pipeline_configuration(
        **configuration
    )

    return result["valid"]


# ==================================================================
# 31. VALIDATION SUMMARY
# ==================================================================

VALIDATION_RULES = {

    "reject_unknown_neural_data":
        True,

    "reject_unknown_file_type":
        True,

    "reject_incompatible_file":
        True,

    "reject_incompatible_pipeline":
        True,

    "reject_incompatible_preprocessing":
        True,

    "reject_incompatible_statistics":
        True,

    "reject_incompatible_features":
        True,

    "reject_incompatible_decoder":
        True,

    "require_targets_for_decoding":
        True,

    "require_features_for_decoding":
        True,

    "require_decoder_for_decoding":
        True,

    "require_evaluation_for_decoding":
        True,

    "terminal_output":
        True,

    "popup_report":
        False,

    "generate_only_valid_pipelines":
        True

}


# ==================================================================
# 32. DIRECT TEST
# ==================================================================

if __name__ == "__main__":

    print("=" * 70)

    print(
        "MASTER-DOC-VALIDATION"
    )

    print("=" * 70)

    print()

    print(
        "Supported neural data:"
    )

    for item in sorted(
        SUPPORTED_NEURAL_DATA_TYPES
    ):

        print(
            f"  {item}"
        )

    print()

    print(
        "Validation rules loaded:"
    )

    for rule, enabled in VALIDATION_RULES.items():

        print(
            f"  {rule}: {enabled}"
        )

    print()

    # --------------------------------------------------------------
    # Example valid configuration
    # --------------------------------------------------------------

    result = validate_pipeline_configuration(

        neural_data="EEG",

        file_type=".edf",

        pipeline_type="EEG",

        preprocessing=[
            "bandpass_filter",
            "notch_filter"
        ],

        statistics=[
            "mean",
            "std",
            "spectral_power"
        ],

        features=[
            "mean",
            "std",
            "band_power"
        ]

    )

    print(
        "Example validation:"
    )

    print(
        f"Valid: {result['valid']}"
    )

    print(
        f"Message: {result['message']}"
    )

    if result["errors"]:

        print(
            "Errors:"
        )

        for error in result["errors"]:

            print(
                f"  - {error}"
            )

    print()

    print(
        "Popup report:"
    )

    print(
        "  DISABLED"
    )

    print()

    print(
        "Terminal output:"
    )

    print(
        "  ENABLED"
    )

    print()

    print(
        "Master-DOC-validation loaded successfully."
    )

    print("=" * 70)