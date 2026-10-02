"""
====================================================================
MASTER-DOC-DECODING.PY
====================================================================

PURPOSE
-------
Master raw-material library for neural decoding pipelines.

This document contains reusable components that the Pipeline
Generator can assemble into plausible neural-decoding pipelines.

PRIMARY USE CASES
-----------------
    EEG
    ECoG
    LFP
    Intracortical neural recordings

DECODING FLOW
-------------
    Neural Data
        ↓
    Preprocessing
        ↓
    Feature Extraction
        ↓
    Target / Label Preparation
        ↓
    Train / Test Split
        ↓
    Decoder Training
        ↓
    Prediction
        ↓
    Evaluation
        ↓
    Terminal Results

IMPORTANT
---------
This is a RESOURCE LIBRARY.

It is not one finished decoder.

The generator selects compatible components based on:

    neural_data_type
    pipeline_type
    feature_type
    target_type
    decoder_type
    evaluation_type

STATISTICAL / DECODING RESULTS
------------------------------
Results are printed to the terminal.

No popup report is generated here.

Visualization is optional and belongs to the visualization layer.

====================================================================
"""


# ==================================================================
# 1. IMPORTS
# ==================================================================

import numpy as np

from scipy import signal

from sklearn.model_selection import (
    train_test_split
)

from sklearn.preprocessing import (
    StandardScaler
)

from sklearn.linear_model import (
    LinearRegression,
    LogisticRegression
)

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

from sklearn.neighbors import (
    KNeighborsClassifier
)

from sklearn.svm import (
    SVC
)


# ==================================================================
# 2. VALIDATION UTILITIES
# ==================================================================

def validate_numeric_array(
    data
):
    """
    Validate that data contains numerical values.
    """

    data = np.asarray(
        data
    )

    if data.size == 0:

        raise ValueError(
            "Input data is empty."
        )

    if not np.issubdtype(
        data.dtype,
        np.number
    ):

        raise ValueError(
            "Input data must be numerical."
        )

    return data.astype(
        float
    )


def validate_2d_features(
    features
):
    """
    Validate feature matrix.

    Expected shape:

        samples × features
    """

    features = validate_numeric_array(
        features
    )

    if features.ndim != 2:

        raise ValueError(
            "Features must be two-dimensional."
        )

    return features


def validate_targets(
    targets
):
    """
    Validate target array.
    """

    targets = np.asarray(
        targets
    )

    if targets.size == 0:

        raise ValueError(
            "Targets are empty."
        )

    return targets


# ==================================================================
# 3. FEATURE EXTRACTION — RAW SIGNAL
# ==================================================================

def extract_raw_features(
    data
):
    """
    Use the raw signal values as decoder features.

    Input:

        samples × features

    Output:

        samples × features
    """

    data = validate_2d_features(
        data
    )

    return data.copy()


# ==================================================================
# 4. FEATURE EXTRACTION — MEAN
# ==================================================================

def extract_mean_features(
    data
):
    """
    Calculate mean amplitude for each sample.
    """

    data = validate_numeric_array(
        data
    )

    if data.ndim == 1:

        return np.array([
            np.mean(data)
        ])

    return np.mean(
        data,
        axis=1,
        keepdims=True
    )


# ==================================================================
# 5. FEATURE EXTRACTION — STANDARD DEVIATION
# ==================================================================

def extract_std_features(
    data
):
    """
    Calculate standard deviation for each sample.
    """

    data = validate_numeric_array(
        data
    )

    if data.ndim == 1:

        return np.array([
            np.std(data)
        ])

    return np.std(
        data,
        axis=1,
        keepdims=True
    )


# ==================================================================
# 6. FEATURE EXTRACTION — VARIANCE
# ==================================================================

def extract_variance_features(
    data
):
    """
    Calculate variance for each sample.
    """

    data = validate_numeric_array(
        data
    )

    if data.ndim == 1:

        return np.array([
            np.var(data)
        ])

    return np.var(
        data,
        axis=1,
        keepdims=True
    )


# ==================================================================
# 7. FEATURE EXTRACTION — RMS
# ==================================================================

def extract_rms_features(
    data
):
    """
    Calculate root-mean-square amplitude.
    """

    data = validate_numeric_array(
        data
    )

    if data.ndim == 1:

        return np.array([
            np.sqrt(
                np.mean(
                    data ** 2
                )
            )
        ])

    return np.sqrt(
        np.mean(
            data ** 2,
            axis=1,
            keepdims=True
        )
    )


# ==================================================================
# 8. FEATURE EXTRACTION — PEAK
# ==================================================================

def extract_peak_features(
    data
):
    """
    Extract maximum absolute amplitude.
    """

    data = validate_numeric_array(
        data
    )

    if data.ndim == 1:

        return np.array([
            np.max(
                np.abs(data)
            )
        ])

    return np.max(
        np.abs(data),
        axis=1,
        keepdims=True
    )


# ==================================================================
# 9. FEATURE EXTRACTION — MINIMUM
# ==================================================================

def extract_min_features(
    data
):
    """
    Extract minimum amplitude.
    """

    data = validate_numeric_array(
        data
    )

    if data.ndim == 1:

        return np.array([
            np.min(data)
        ])

    return np.min(
        data,
        axis=1,
        keepdims=True
    )


# ==================================================================
# 10. FEATURE EXTRACTION — MAXIMUM
# ==================================================================

def extract_max_features(
    data
):
    """
    Extract maximum amplitude.
    """

    data = validate_numeric_array(
        data
    )

    if data.ndim == 1:

        return np.array([
            np.max(data)
        ])

    return np.max(
        data,
        axis=1,
        keepdims=True
    )


# ==================================================================
# 11. FEATURE EXTRACTION — FREQUENCY DOMAIN
# ==================================================================

def extract_frequency_features(
    data,
    sampling_rate
):
    """
    Calculate frequency-domain features using the periodogram.

    Returns frequency and power features for each input sample.
    """

    data = validate_numeric_array(
        data
    )

    if sampling_rate <= 0:

        raise ValueError(
            "Sampling rate must be greater than zero."
        )

    if data.ndim == 1:

        frequencies, power = (
            signal.periodogram(
                data,
                fs=sampling_rate
            )
        )

        return np.concatenate(
            [
                frequencies,
                power
            ]
        )

    feature_rows = []

    for row in data:

        frequencies, power = (
            signal.periodogram(
                row,
                fs=sampling_rate
            )
        )

        feature_rows.append(
            np.concatenate(
                [
                    frequencies,
                    power
                ]
            )
        )

    return np.asarray(
        feature_rows
    )


# ==================================================================
# 12. BAND-POWER FEATURE
# ==================================================================

def calculate_band_power(
    data,
    sampling_rate,
    low_frequency,
    high_frequency
):
    """
    Calculate power contained within a frequency band.
    """

    data = validate_numeric_array(
        data
    )

    if sampling_rate <= 0:

        raise ValueError(
            "Sampling rate must be greater than zero."
        )

    frequencies, power = (
        signal.periodogram(
            data,
            fs=sampling_rate
        )
    )

    mask = (
        (frequencies >= low_frequency)
        &
        (frequencies <= high_frequency)
    )

    if not np.any(mask):

        return 0.0

    return np.trapezoid(
        power[mask],
        frequencies[mask]
    )


# ==================================================================
# 13. MULTI-BAND FEATURES
# ==================================================================

def extract_band_power_features(
    data,
    sampling_rate,
    bands
):
    """
    Extract power from multiple frequency bands.

    bands format:

        {
            "alpha": (8, 13),
            "beta": (13, 30)
        }
    """

    data = validate_numeric_array(
        data
    )

    if data.ndim == 1:

        data = data.reshape(
            1,
            -1
        )

    features = []

    for row in data:

        row_features = []

        for low, high in bands.values():

            power = calculate_band_power(
                row,
                sampling_rate,
                low,
                high
            )

            row_features.append(
                power
            )

        features.append(
            row_features
        )

    return np.asarray(
        features
    )


# ==================================================================
# 14. FEATURE COMBINATION
# ==================================================================

def combine_features(
    *feature_sets
):
    """
    Horizontally combine multiple feature matrices.
    """

    validated = []

    for features in feature_sets:

        features = validate_2d_features(
            features
        )

        validated.append(
            features
        )

    if len(validated) == 0:

        raise ValueError(
            "No feature sets were supplied."
        )

    sample_counts = [
        features.shape[0]
        for features in validated
    ]

    if len(
        set(sample_counts)
    ) != 1:

        raise ValueError(
            "All feature sets must contain "
            "the same number of samples."
        )

    return np.hstack(
        validated
    )


# ==================================================================
# 15. STANDARDIZATION
# ==================================================================

def standardize_features(
    X_train,
    X_test
):
    """
    Standardize decoder features.

    The scaler is fitted only on training data.
    """

    X_train = validate_2d_features(
        X_train
    )

    X_test = validate_2d_features(
        X_test
    )

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(
        X_train
    )

    X_test_scaled = scaler.transform(
        X_test
    )

    return (
        X_train_scaled,
        X_test_scaled,
        scaler
    )


# ==================================================================
# 16. TRAIN / TEST SPLIT
# ==================================================================

def split_data(
    X,
    y,
    test_size=0.2,
    random_state=42
):
    """
    Split features and targets into training and testing sets.
    """

    X = validate_2d_features(
        X
    )

    y = validate_targets(
        y
    )

    if len(X) != len(y):

        raise ValueError(
            "X and y must contain "
            "the same number of samples."
        )

    return train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state
    )


# ==================================================================
# 17. LINEAR REGRESSION DECODER
# ==================================================================

def train_linear_regression(
    X_train,
    y_train
):
    """
    Train a linear regression decoder.
    """

    model = LinearRegression()

    model.fit(
        X_train,
        y_train
    )

    return model


# ==================================================================
# 18. LOGISTIC REGRESSION DECODER
# ==================================================================

def train_logistic_regression(
    X_train,
    y_train
):
    """
    Train a logistic regression classifier.
    """

    model = LogisticRegression(
        max_iter=1000
    )

    model.fit(
        X_train,
        y_train
    )

    return model


# ==================================================================
# 19. SUPPORT VECTOR MACHINE DECODER
# ==================================================================

def train_svm_classifier(
    X_train,
    y_train
):
    """
    Train an SVM classifier.
    """

    model = SVC()

    model.fit(
        X_train,
        y_train
    )

    return model


# ==================================================================
# 20. K-NEAREST NEIGHBOR DECODER
# ==================================================================

def train_knn_classifier(
    X_train,
    y_train,
    neighbors=5
):
    """
    Train a K-nearest-neighbor classifier.
    """

    model = KNeighborsClassifier(
        n_neighbors=neighbors
    )

    model.fit(
        X_train,
        y_train
    )

    return model


# ==================================================================
# 21. GENERIC MODEL PREDICTION
# ==================================================================

def predict(
    model,
    X
):
    """
    Generate predictions using a trained decoder.
    """

    X = validate_2d_features(
        X
    )

    return model.predict(
        X
    )


# ==================================================================
# 22. REGRESSION EVALUATION
# ==================================================================

def evaluate_regression(
    y_true,
    y_pred
):
    """
    Calculate regression decoder metrics.
    """

    y_true = validate_numeric_array(
        y_true
    )

    y_pred = validate_numeric_array(
        y_pred
    )

    if y_true.shape != y_pred.shape:

        raise ValueError(
            "True and predicted values "
            "must have matching shapes."
        )

    mse = mean_squared_error(
        y_true,
        y_pred
    )

    rmse = np.sqrt(
        mse
    )

    mae = mean_absolute_error(
        y_true,
        y_pred
    )

    r2 = r2_score(
        y_true,
        y_pred
    )

    return {

        "MSE":
            mse,

        "RMSE":
            rmse,

        "MAE":
            mae,

        "R2":
            r2

    }


# ==================================================================
# 23. CLASSIFICATION EVALUATION
# ==================================================================

def evaluate_classification(
    y_true,
    y_pred
):
    """
    Calculate classification decoder metrics.
    """

    y_true = validate_targets(
        y_true
    )

    y_pred = validate_targets(
        y_pred
    )

    accuracy = accuracy_score(
        y_true,
        y_pred
    )

    precision = precision_score(
        y_true,
        y_pred,
        average="weighted",
        zero_division=0
    )

    recall = recall_score(
        y_true,
        y_pred,
        average="weighted",
        zero_division=0
    )

    f1 = f1_score(
        y_true,
        y_pred,
        average="weighted",
        zero_division=0
    )

    matrix = confusion_matrix(
        y_true,
        y_pred
    )

    return {

        "accuracy":
            accuracy,

        "precision":
            precision,

        "recall":
            recall,

        "F1":
            f1,

        "confusion_matrix":
            matrix

    }


# ==================================================================
# 24. TERMINAL REGRESSION REPORT
# ==================================================================

def print_regression_results(
    results
):
    """
    Print regression decoder results to the terminal.
    """

    print()
    print("=" * 60)
    print("NEURAL DECODING — REGRESSION RESULTS")
    print("=" * 60)

    for name, value in results.items():

        print(
            f"{name}: {value}"
        )

    print("=" * 60)
    print()


# ==================================================================
# 25. TERMINAL CLASSIFICATION REPORT
# ==================================================================

def print_classification_results(
    results
):
    """
    Print classification decoder results to the terminal.
    """

    print()
    print("=" * 60)
    print("NEURAL DECODING — CLASSIFICATION RESULTS")
    print("=" * 60)

    print(
        f"Accuracy:  {results['accuracy']}"
    )

    print(
        f"Precision: {results['precision']}"
    )

    print(
        f"Recall:    {results['recall']}"
    )

    print(
        f"F1 Score:  {results['F1']}"
    )

    print()
    print(
        "Confusion Matrix:"
    )

    print(
        results[
            "confusion_matrix"
        ]
    )

    print("=" * 60)
    print()


# ==================================================================
# 26. COMPLETE REGRESSION DECODER
# ==================================================================

def run_regression_decoder(
    X,
    y,
    test_size=0.2,
    random_state=42,
    standardize=True
):
    """
    Complete regression decoding workflow.
    """

    X = validate_2d_features(
        X
    )

    y = validate_targets(
        y
    )

    (
        X_train,
        X_test,
        y_train,
        y_test
    ) = split_data(
        X,
        y,
        test_size,
        random_state
    )

    scaler = None

    if standardize:

        (
            X_train,
            X_test,
            scaler
        ) = standardize_features(
            X_train,
            X_test
        )

    model = train_linear_regression(
        X_train,
        y_train
    )

    predictions = predict(
        model,
        X_test
    )

    results = evaluate_regression(
        y_test,
        predictions
    )

    print_regression_results(
        results
    )

    return {

        "model":
            model,

        "predictions":
            predictions,

        "y_test":
            y_test,

        "results":
            results,

        "scaler":
            scaler

    }


# ==================================================================
# 27. COMPLETE CLASSIFICATION DECODER
# ==================================================================

def run_classification_decoder(
    X,
    y,
    decoder="logistic_regression",
    test_size=0.2,
    random_state=42,
    standardize=True
):
    """
    Complete classification decoding workflow.
    """

    X = validate_2d_features(
        X
    )

    y = validate_targets(
        y
    )

    (
        X_train,
        X_test,
        y_train,
        y_test
    ) = split_data(
        X,
        y,
        test_size,
        random_state
    )

    scaler = None

    if standardize:

        (
            X_train,
            X_test,
            scaler
        ) = standardize_features(
            X_train,
            X_test
        )

    if decoder == "logistic_regression":

        model = train_logistic_regression(
            X_train,
            y_train
        )

    elif decoder == "svm":

        model = train_svm_classifier(
            X_train,
            y_train
        )

    elif decoder == "knn":

        model = train_knn_classifier(
            X_train,
            y_train
        )

    else:

        raise ValueError(
            f"Unsupported classifier: {decoder}"
        )

    predictions = predict(
        model,
        X_test
    )

    results = evaluate_classification(
        y_test,
        predictions
    )

    print_classification_results(
        results
    )

    return {

        "model":
            model,

        "predictions":
            predictions,

        "y_test":
            y_test,

        "results":
            results,

        "scaler":
            scaler

    }


# ==================================================================
# 28. DECODER RESOURCE REGISTRY
# ==================================================================

DECODER_RESOURCES = {

    "linear_regression": {

        "function":
            train_linear_regression,

        "type":
            "regression",

        "compatible_targets":
            [
                "continuous"
            ]

    },

    "logistic_regression": {

        "function":
            train_logistic_regression,

        "type":
            "classification",

        "compatible_targets":
            [
                "binary",
                "multiclass"
            ]

    },

    "svm": {

        "function":
            train_svm_classifier,

        "type":
            "classification",

        "compatible_targets":
            [
                "binary",
                "multiclass"
            ]

    },

    "knn": {

        "function":
            train_knn_classifier,

        "type":
            "classification",

        "compatible_targets":
            [
                "binary",
                "multiclass"
            ]

    }

}


# ==================================================================
# 29. FEATURE RESOURCE REGISTRY
# ==================================================================

FEATURE_RESOURCES = {

    "raw": {

        "function":
            extract_raw_features,

        "requires":
            [
                "neural_signal"
            ]

    },

    "mean": {

        "function":
            extract_mean_features,

        "requires":
            [
                "neural_signal"
            ]

    },

    "std": {

        "function":
            extract_std_features,

        "requires":
            [
                "neural_signal"
            ]

    },

    "variance": {

        "function":
            extract_variance_features,

        "requires":
            [
                "neural_signal"
            ]

    },

    "rms": {

        "function":
            extract_rms_features,

        "requires":
            [
                "neural_signal"
            ]

    },

    "peak": {

        "function":
            extract_peak_features,

        "requires":
            [
                "neural_signal"
            ]

    },

    "minimum": {

        "function":
            extract_min_features,

        "requires":
            [
                "neural_signal"
            ]

    },

    "maximum": {

        "function":
            extract_max_features,

        "requires":
            [
                "neural_signal"
            ]

    },

    "frequency": {

        "function":
            extract_frequency_features,

        "requires":
            [
                "neural_signal",
                "sampling_rate"
            ]

    },

    "band_power": {

        "function":
            extract_band_power_features,

        "requires":
            [
                "neural_signal",
                "sampling_rate",
                "frequency_bands"
            ]

    }

}


# ==================================================================
# 30. TARGET TYPES
# ==================================================================

TARGET_TYPES = {

    "continuous": {

        "description":
            "Continuous behavioral or physiological variable",

        "decoder_type":
            "regression"

    },

    "binary": {

        "description":
            "Two-class target",

        "decoder_type":
            "classification"

    },

    "multiclass": {

        "description":
            "More than two discrete classes",

        "decoder_type":
            "classification"

    }

}


# ==================================================================
# 31. NEURAL-DATA COMPATIBILITY
# ==================================================================

DECODING_DATA_COMPATIBILITY = {

    "EEG": [

        "raw",
        "mean",
        "std",
        "variance",
        "rms",
        "peak",
        "minimum",
        "maximum",
        "frequency",
        "band_power"

    ],

    "ECoG": [

        "raw",
        "mean",
        "std",
        "variance",
        "rms",
        "peak",
        "minimum",
        "maximum",
        "frequency",
        "band_power"

    ],

    "LFP": [

        "raw",
        "mean",
        "std",
        "variance",
        "rms",
        "peak",
        "minimum",
        "maximum",
        "frequency",
        "band_power"

    ],

    "intracortical": [

        "raw",
        "mean",
        "std",
        "variance",
        "rms",
        "peak",
        "minimum",
        "maximum",
        "frequency",
        "band_power"

    ],

    "MEG": [

        "raw",
        "mean",
        "std",
        "variance",
        "rms",
        "peak",
        "minimum",
        "maximum",
        "frequency",
        "band_power"

    ]

}


# ==================================================================
# 32. PIPELINE COMPATIBILITY
# ==================================================================

DECODING_PIPELINE_COMPATIBILITY = {

    "neural_decoding": [

        "EEG",
        "ECoG",
        "LFP",
        "intracortical",
        "MEG"

    ],

    "BCI_decoding": [

        "EEG",
        "ECoG",
        "LFP",
        "intracortical",
        "MEG"

    ],

    "intracortical_decoding": [

        "intracortical",
        "LFP"

    ]

}


# ==================================================================
# 33. ASSEMBLY RULES
# ==================================================================

DECODING_ASSEMBLY_RULES = {

    "features_required":
        True,

    "targets_required":
        True,

    "train_test_split_required":
        True,

    "model_training_required":
        True,

    "prediction_required":
        True,

    "evaluation_required":
        True,

    "terminal_results":
        True,

    "popup_report":
        False,

    "visualization_optional":
        True,

    "training_data_must_not_leak_into_test_scaling":
        True,

    "continuous_target_requires_regression":
        True,

    "binary_target_requires_classification":
        True,

    "multiclass_target_requires_classification":
        True

}


# ==================================================================
# 34. RESOURCE LOOKUP
# ==================================================================

def get_decoder_resource(
    decoder_name
):
    """
    Retrieve a decoder resource.
    """

    if decoder_name not in DECODER_RESOURCES:

        raise ValueError(
            f"Unknown decoder: {decoder_name}"
        )

    return DECODER_RESOURCES[
        decoder_name
    ]


# ==================================================================
# 35. FEATURE LOOKUP
# ==================================================================

def get_feature_resource(
    feature_name
):
    """
    Retrieve a feature-extraction resource.
    """

    if feature_name not in FEATURE_RESOURCES:

        raise ValueError(
            f"Unknown feature: {feature_name}"
        )

    return FEATURE_RESOURCES[
        feature_name
    ]


# ==================================================================
# 36. LIST DECODERS
# ==================================================================

def list_decoders(
    decoder_type=None
):
    """
    List available decoders.
    """

    if decoder_type is None:

        return list(
            DECODER_RESOURCES.keys()
        )

    return [

        name

        for name, resource
        in DECODER_RESOURCES.items()

        if resource["type"] == decoder_type

    ]


# ==================================================================
# 37. LIST FEATURES
# ==================================================================

def list_features():
    """
    List available feature extraction methods.
    """

    return list(
        FEATURE_RESOURCES.keys()
    )


# ==================================================================
# 38. CHECK FEATURE COMPATIBILITY
# ==================================================================

def is_feature_compatible(
    neural_data,
    feature_name
):
    """
    Check whether a feature is compatible with a neural-data type.
    """

    return (
        feature_name
        in
        DECODING_DATA_COMPATIBILITY.get(
            neural_data,
            []
        )
    )


# ==================================================================
# 39. GET COMPATIBLE FEATURES
# ==================================================================

def get_compatible_features(
    neural_data
):
    """
    Return all compatible decoding features.
    """

    return DECODING_DATA_COMPATIBILITY.get(
        neural_data,
        []
    )


# ==================================================================
# 40. CHECK PIPELINE COMPATIBILITY
# ==================================================================

def is_decoding_pipeline_compatible(
    pipeline_type,
    neural_data
):
    """
    Check whether a neural-data type can be used with
    a decoding pipeline.
    """

    return (
        neural_data
        in
        DECODING_PIPELINE_COMPATIBILITY.get(
            pipeline_type,
            []
        )
    )


# ==================================================================
# 41. BUILD DECODING PLAN
# ==================================================================

def build_decoding_plan(
    neural_data,
    pipeline_type,
    feature_names,
    decoder_name,
    target_type
):
    """
    Construct a validated decoding plan.

    This is the interface that the future generator can use
    when assembling a decoder.
    """

    if not is_decoding_pipeline_compatible(
        pipeline_type,
        neural_data
    ):

        raise ValueError(
            f"Neural data '{neural_data}' "
            f"is not compatible with "
            f"pipeline '{pipeline_type}'."
        )

    for feature_name in feature_names:

        if not is_feature_compatible(
            neural_data,
            feature_name
        ):

            raise ValueError(
                f"Feature '{feature_name}' "
                f"is not compatible with "
                f"neural data '{neural_data}'."
            )

    decoder = get_decoder_resource(
        decoder_name
    )

    if target_type not in (
        decoder[
            "compatible_targets"
        ]
    ):

        raise ValueError(
            f"Decoder '{decoder_name}' "
            f"is not compatible with "
            f"target type '{target_type}'."
        )

    return {

        "neural_data":
            neural_data,

        "pipeline_type":
            pipeline_type,

        "features":
            [
                get_feature_resource(
                    feature
                )
                for feature
                in feature_names
            ],

        "decoder":
            decoder,

        "target_type":
            target_type,

        "assembly_rules":
            DECODING_ASSEMBLY_RULES

    }


# ==================================================================
# 42. MASTER DOCUMENT SUMMARY
# ==================================================================

MASTER_DOCUMENT_SUMMARY = {

    "document":
        "Master-DOC-decoding",

    "feature_resources":
        list(
            FEATURE_RESOURCES.keys()
        ),

    "decoder_resources":
        list(
            DECODER_RESOURCES.keys()
        ),

    "target_types":
        list(
            TARGET_TYPES.keys()
        ),

    "supported_neural_data":
        list(
            DECODING_DATA_COMPATIBILITY.keys()
        ),

    "supported_pipeline_types":
        list(
            DECODING_PIPELINE_COMPATIBILITY.keys()
        ),

    "popup_report":
        False,

    "terminal_results":
        True,

    "visualization":
        "optional"

}


# ==================================================================
# 43. DIRECT TEST
# ==================================================================

if __name__ == "__main__":

    print("=" * 70)

    print(
        "MASTER-DOC-DECODING"
    )

    print("=" * 70)

    print()

    print(
        "Feature resources:"
    )

    for feature in FEATURE_RESOURCES:

        print(
            f"  {feature}"
        )

    print()

    print(
        "Decoder resources:"
    )

    for decoder in DECODER_RESOURCES:

        print(
            f"  {decoder}"
        )

    print()

    print(
        "Target types:"
    )

    for target in TARGET_TYPES:

        print(
            f"  {target}"
        )

    print()

    print(
        "Supported neural data:"
    )

    for data_type in DECODING_DATA_COMPATIBILITY:

        print(
            f"  {data_type}"
        )

    print()

    print(
        "Pipeline results:"
    )

    print(
        "  TERMINAL OUTPUT"
    )

    print()

    print(
        "Popup report:"
    )

    print(
        "  DISABLED / NOT USED"
    )

    print()

    print(
        "Master-DOC-decoding loaded successfully."
    )

    print("=" * 70)