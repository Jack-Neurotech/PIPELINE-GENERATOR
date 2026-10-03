"""
====================================================================
MASTER-DOC-OUTPUT.PY
====================================================================

PURPOSE
-------
Master raw-material library for terminal-based pipeline output.

The generated pipeline performs the analysis and then presents the
results directly in the terminal window.

NO POPUP REPORTS ARE USED.

This document defines:

    - terminal output structure
    - section formatting
    - ingestion summaries
    - preprocessing summaries
    - statistical results
    - feature results
    - decoding results
    - evaluation results
    - pipeline completion information
    - error reporting
    - warning reporting

This document does NOT perform the actual analysis.

It provides reusable output functions and rules for the Pipeline
Generator.

====================================================================
"""


# ==================================================================
# 1. OUTPUT CONFIGURATION
# ==================================================================

OUTPUT_CONFIG = {

    "destination": "terminal",

    "popup_report": False,

    "file_report": False,

    "html_report": False,

    "terminal_required": True,

    "show_pipeline_header": True,

    "show_ingestion": True,

    "show_preprocessing": True,

    "show_statistics": True,

    "show_features": True,

    "show_decoding": True,

    "show_evaluation": True,

    "show_visualization_status": True,

    "show_completion": True,

    "show_errors": True,

    "show_warnings": True

}


# ==================================================================
# 2. OUTPUT SECTIONS
# ==================================================================

OUTPUT_SECTIONS = [

    "pipeline",

    "configuration",

    "ingestion",

    "validation",

    "preprocessing",

    "statistics",

    "features",

    "decoding",

    "evaluation",

    "visualization",

    "completion",

    "errors",

    "warnings"

]


# ==================================================================
# 3. TERMINAL FORMAT
# ==================================================================

LINE_LENGTH = 70

SEPARATOR = "=" * LINE_LENGTH

SUBSEPARATOR = "-" * LINE_LENGTH


# ==================================================================
# 4. SAFE VALUE FORMATTER
# ==================================================================

def format_value(
    value
):
    """
    Convert a result into a readable terminal string.
    """

    if value is None:

        return "None"

    if isinstance(
        value,
        float
    ):

        return f"{value:.6f}"

    if isinstance(
        value,
        bool
    ):

        return (
            "True"
            if value
            else
            "False"
        )

    if isinstance(
        value,
        (list, tuple)
    ):

        return str(
            list(value)
        )

    if isinstance(
        value,
        dict
    ):

        return str(
            value
        )

    return str(
        value
    )


# ==================================================================
# 5. PRINT HEADER
# ==================================================================

def print_header(
    title
):
    """
    Print a major terminal section.
    """

    print()

    print(
        SEPARATOR
    )

    print(
        title
    )

    print(
        SEPARATOR
    )


# ==================================================================
# 6. PRINT SUBHEADER
# ==================================================================

def print_subheader(
    title
):
    """
    Print a smaller terminal section.
    """

    print()

    print(
        SUBSEPARATOR
    )

    print(
        title
    )

    print(
        SUBSEPARATOR
    )


# ==================================================================
# 7. PRINT KEY-VALUE
# ==================================================================

def print_value(
    name,
    value
):
    """
    Print a named result.
    """

    print(
        f"{name}: {format_value(value)}"
    )


# ==================================================================
# 8. PRINT LIST
# ==================================================================

def print_list(
    title,
    values
):
    """
    Print a collection of values.
    """

    print_subheader(
        title
    )

    if not values:

        print(
            "None"
        )

        return

    for value in values:

        print(
            f"  - {format_value(value)}"
        )


# ==================================================================
# 9. PIPELINE HEADER
# ==================================================================

def print_pipeline_header(
    pipeline_name=None
):
    """
    Print the beginning of a generated pipeline report.
    """

    print()

    print(
        SEPARATOR
    )

    print(
        "NEURAL DATA PIPELINE"
    )

    print(
        SEPARATOR
    )

    if pipeline_name is not None:

        print_value(
            "Pipeline",
            pipeline_name
        )

    print_value(
        "Output",
        "Terminal"
    )

    print_value(
        "Popup report",
        False
    )


# ==================================================================
# 10. CONFIGURATION OUTPUT
# ==================================================================

def print_configuration(
    configuration
):
    """
    Print the pipeline configuration.
    """

    print_subheader(
        "PIPELINE CONFIGURATION"
    )

    if not configuration:

        print(
            "No configuration supplied."
        )

        return

    for name, value in (
        configuration.items()
    ):

        print_value(
            name,
            value
        )


# ==================================================================
# 11. INGESTION OUTPUT
# ==================================================================

def print_ingestion_results(
    results
):
    """
    Print file-ingestion information.
    """

    print_subheader(
        "FILE INGESTION"
    )

    if not results:

        print(
            "No ingestion results."
        )

        return

    fields = [

        "file",

        "file_type",

        "data_type",

        "sampling_rate",

        "channels",

        "samples",

        "duration",

        "shape"

    ]

    for field in fields:

        if field in results:

            print_value(
                field,
                results[field]
            )

    additional = {

        key: value

        for key, value
        in results.items()

        if key not in fields

    }

    for key, value in additional.items():

        print_value(
            key,
            value
        )


# ==================================================================
# 12. VALIDATION OUTPUT
# ==================================================================

def print_validation_results(
    results
):
    """
    Print validation status.
    """

    print_subheader(
        "VALIDATION"
    )

    if not results:

        print(
            "No validation results."
        )

        return

    if isinstance(
        results,
        dict
    ):

        if "valid" in results:

            print_value(
                "Valid",
                results["valid"]
            )

        if "message" in results:

            print_value(
                "Message",
                results["message"]
            )

        errors = results.get(
            "errors",
            []
        )

        warnings = results.get(
            "warnings",
            []
        )

        if errors:

            print(
                "Errors:"
            )

            for error in errors:

                print(
                    f"  - {error}"
                )

        if warnings:

            print(
                "Warnings:"
            )

            for warning in warnings:

                print(
                    f"  - {warning}"
                )

    else:

        print(
            format_value(
                results
            )
        )


# ==================================================================
# 13. PREPROCESSING OUTPUT
# ==================================================================

def print_preprocessing_results(
    results
):
    """
    Print preprocessing information.
    """

    print_subheader(
        "PREPROCESSING"
    )

    if not results:

        print(
            "No preprocessing requested."
        )

        return

    if isinstance(
        results,
        dict
    ):

        for name, value in (
            results.items()
        ):

            print_value(
                name,
                value
            )

    else:

        if isinstance(
            results,
            (list, tuple)
        ):

            for method in results:

                print(
                    f"  - {method}"
                )

        else:

            print(
                format_value(
                    results
                )
            )


# ==================================================================
# 14. STATISTICAL OUTPUT
# ==================================================================

def print_statistical_results(
    results
):
    """
    Print statistical-analysis results.

    This is the primary replacement for the former popup report.
    """

    print_subheader(
        "STATISTICAL ANALYSIS"
    )

    if not results:

        print(
            "No statistical analysis requested."
        )

        return

    if isinstance(
        results,
        dict
    ):

        for name, value in (
            results.items()
        ):

            print_value(
                name,
                value
            )

        return

    if isinstance(
        results,
        (list, tuple)
    ):

        for result in results:

            print(
                f"  - {format_value(result)}"
            )

        return

    print(
        format_value(
            results
        )
    )


# ==================================================================
# 15. FEATURE OUTPUT
# ==================================================================

def print_feature_results(
    results
):
    """
    Print extracted feature values.
    """

    print_subheader(
        "FEATURE EXTRACTION"
    )

    if not results:

        print(
            "No features requested."
        )

        return

    if isinstance(
        results,
        dict
    ):

        for name, value in (
            results.items()
        ):

            print_value(
                name,
                value
            )

    elif isinstance(
        results,
        (list, tuple)
    ):

        for feature in results:

            print(
                f"  - {format_value(feature)}"
            )

    else:

        print(
            format_value(
                results
            )
        )


# ==================================================================
# 16. DECODING OUTPUT
# ==================================================================

def print_decoding_results(
    results
):
    """
    Print neural-decoding results.
    """

    print_subheader(
        "NEURAL DECODING"
    )

    if not results:

        print(
            "No decoding requested."
        )

        return

    if isinstance(
        results,
        dict
    ):

        for name, value in (
            results.items()
        ):

            print_value(
                name,
                value
            )

    else:

        print(
            format_value(
                results
            )
        )


# ==================================================================
# 17. EVALUATION OUTPUT
# ==================================================================

def print_evaluation_results(
    results
):
    """
    Print decoder/model evaluation results.
    """

    print_subheader(
        "EVALUATION"
    )

    if not results:

        print(
            "No evaluation requested."
        )

        return

    if isinstance(
        results,
        dict
    ):

        for name, value in (
            results.items()
        ):

            print_value(
                name,
                value
            )

    else:

        print(
            format_value(
                results
            )
        )


# ==================================================================
# 18. VISUALIZATION OUTPUT
# ==================================================================

def print_visualization_status(
    results=None
):
    """
    Print visualization status.

    Visualization itself is handled by the visualization layer.
    """

    print_subheader(
        "VISUALIZATION"
    )

    if results is None:

        print(
            "No visualization requested."
        )

        return

    if isinstance(
        results,
        dict
    ):

        for name, value in (
            results.items()
        ):

            print_value(
                name,
                value
            )

    else:

        print(
            format_value(
                results
            )
        )


# ==================================================================
# 19. ERROR OUTPUT
# ==================================================================

def print_errors(
    errors
):
    """
    Print pipeline errors.
    """

    if not errors:

        return

    print_subheader(
        "ERRORS"
    )

    for error in errors:

        print(
            f"  - {error}"
        )


# ==================================================================
# 20. WARNING OUTPUT
# ==================================================================

def print_warnings(
    warnings
):
    """
    Print pipeline warnings.
    """

    if not warnings:

        return

    print_subheader(
        "WARNINGS"
    )

    for warning in warnings:

        print(
            f"  - {warning}"
        )


# ==================================================================
# 21. COMPLETION OUTPUT
# ==================================================================

def print_completion(
    success=True
):
    """
    Print final pipeline status.
    """

    print()

    print(
        SEPARATOR
    )

    if success:

        print(
            "PIPELINE COMPLETED"
        )

    else:

        print(
            "PIPELINE FAILED"
        )

    print(
        SEPARATOR
    )

    print()

    print_value(
        "Terminal output",
        True
    )

    print_value(
        "Popup report",
        False
    )


# ==================================================================
# 22. COMPLETE STATISTICAL TERMINAL REPORT
# ==================================================================

def print_statistics_report(
    results,
    pipeline_name=None
):
    """
    Print a complete terminal-based statistical report.

    This is intentionally NOT a popup.
    """

    print_pipeline_header(
        pipeline_name
    )

    print_statistical_results(
        results
    )

    print_completion(
        success=True
    )


# ==================================================================
# 23. COMPLETE DECODING TERMINAL REPORT
# ==================================================================

def print_decoding_report(
    results,
    pipeline_name=None
):
    """
    Print a complete terminal-based decoding report.
    """

    print_pipeline_header(
        pipeline_name
    )

    print_decoding_results(
        results
    )

    print_completion(
        success=True
    )


# ==================================================================
# 24. COMPLETE PIPELINE OUTPUT
# ==================================================================

def print_pipeline_results(
    results,
    pipeline_name=None
):
    """
    Print every available result section.

    The generator can pass the final pipeline results here.
    """

    print_pipeline_header(
        pipeline_name
    )

    if not isinstance(
        results,
        dict
    ):

        print(
            format_value(
                results
            )
        )

        print_completion(
            success=True
        )

        return

    if "configuration" in results:

        print_configuration(
            results[
                "configuration"
            ]
        )

    if "ingestion" in results:

        print_ingestion_results(
            results[
                "ingestion"
            ]
        )

    if "validation" in results:

        print_validation_results(
            results[
                "validation"
            ]
        )

    if "preprocessing" in results:

        print_preprocessing_results(
            results[
                "preprocessing"
            ]
        )

    if "statistics" in results:

        print_statistical_results(
            results[
                "statistics"
            ]
        )

    if "features" in results:

        print_feature_results(
            results[
                "features"
            ]
        )

    if "decoding" in results:

        print_decoding_results(
            results[
                "decoding"
            ]
        )

    if "evaluation" in results:

        print_evaluation_results(
            results[
                "evaluation"
            ]
        )

    if "visualization" in results:

        print_visualization_status(
            results[
                "visualization"
            ]
        )

    if "warnings" in results:

        print_warnings(
            results[
                "warnings"
            ]
        )

    if "errors" in results:

        print_errors(
            results[
                "errors"
            ]
        )

    success = not bool(
        results.get(
            "errors"
        )
    )

    print_completion(
        success=success
    )


# ==================================================================
# 25. TERMINAL OUTPUT RULES
# ==================================================================

TERMINAL_OUTPUT_RULES = {

    "output_destination":
        "terminal",

    "popup":
        False,

    "popup_report":
        False,

    "gui_report":
        False,

    "file_report":
        False,

    "terminal_statistics":
        True,

    "terminal_features":
        True,

    "terminal_decoding":
        True,

    "terminal_evaluation":
        True,

    "terminal_errors":
        True,

    "terminal_warnings":
        True,

    "pipeline_completion":
        True

}


# ==================================================================
# 26. RESULT CATEGORIES
# ==================================================================

RESULT_CATEGORIES = {

    "ingestion": {

        "enabled":
            True,

        "destination":
            "terminal"

    },

    "preprocessing": {

        "enabled":
            True,

        "destination":
            "terminal"

    },

    "statistics": {

        "enabled":
            True,

        "destination":
            "terminal"

    },

    "features": {

        "enabled":
            True,

        "destination":
            "terminal"

    },

    "decoding": {

        "enabled":
            True,

        "destination":
            "terminal"

    },

    "evaluation": {

        "enabled":
            True,

        "destination":
            "terminal"

    },

    "visualization": {

        "enabled":
            True,

        "destination":
            "terminal"

    }

}


# ==================================================================
# 27. GENERATOR OUTPUT INTERFACE
# ==================================================================

def send_to_terminal(
    section,
    results
):
    """
    Generator-facing interface.

    Routes a result section to the appropriate terminal formatter.
    """

    if section == "ingestion":

        print_ingestion_results(
            results
        )

    elif section == "validation":

        print_validation_results(
            results
        )

    elif section == "preprocessing":

        print_preprocessing_results(
            results
        )

    elif section == "statistics":

        print_statistical_results(
            results
        )

    elif section == "features":

        print_feature_results(
            results
        )

    elif section == "decoding":

        print_decoding_results(
            results
        )

    elif section == "evaluation":

        print_evaluation_results(
            results
        )

    elif section == "visualization":

        print_visualization_status(
            results
        )

    elif section == "errors":

        print_errors(
            results
        )

    elif section == "warnings":

        print_warnings(
            results
        )

    else:

        print_subheader(
            section.upper()
        )

        print(
            format_value(
                results
            )
        )


# ==================================================================
# 28. OUTPUT VALIDATION
# ==================================================================

def validate_output_configuration():
    """
    Verify that terminal output remains the active output system.
    """

    errors = []

    if OUTPUT_CONFIG[
        "terminal_required"
    ] is not True:

        errors.append(
            "Terminal output must be enabled."
        )

    if OUTPUT_CONFIG[
        "popup_report"
    ] is True:

        errors.append(
            "Popup reports must remain disabled."
        )

    if OUTPUT_CONFIG[
        "file_report"
    ] is True:

        errors.append(
            "File reports are not part of this output layer."
        )

    return {

        "valid":
            len(errors) == 0,

        "errors":
            errors

    }


# ==================================================================
# 29. MASTER DOCUMENT SUMMARY
# ==================================================================

MASTER_DOCUMENT_SUMMARY = {

    "document":
        "Master-DOC-output",

    "purpose":
        "Terminal result presentation",

    "output_destination":
        "terminal",

    "popup_reports":
        False,

    "file_reports":
        False,

    "sections":
        OUTPUT_SECTIONS,

    "statistics":
        "terminal",

    "decoding":
        "terminal",

    "evaluation":
        "terminal",

    "errors":
        "terminal",

    "warnings":
        "terminal"

}


# ==================================================================
# 30. DIRECT TEST
# ==================================================================

if __name__ == "__main__":

    print_header(
        "MASTER-DOC-OUTPUT"
    )

    print(
        "Testing terminal output system..."
    )

    print()

    validation = (
        validate_output_configuration()
    )

    print_subheader(
        "OUTPUT CONFIGURATION"
    )

    print_value(
        "Valid",
        validation["valid"]
    )

    if validation["errors"]:

        print(
            "Errors:"
        )

        for error in validation["errors"]:

            print(
                f"  - {error}"
            )

    # --------------------------------------------------------------
    # Example statistical results
    # --------------------------------------------------------------

    statistics = {

        "mean":
            12.483921,

        "std":
            2.384921,

        "variance":
            5.688849,

        "rms":
            12.709182,

        "dominant_frequency":
            10.0,

        "spectral_power":
            142.8124,

        "peak_alpha_frequency":
            10.0,

        "spectral_entropy":
            0.7821,

        "spectral_edge":
            24.7

    }

    print_statistics_report(
        statistics,
        pipeline_name="EEG Statistical Pipeline"
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
        "Master-DOC-output loaded successfully."
    )

    print(
        "=" * LINE_LENGTH
    )