"""
====================================================================
MASTER-DOC-VISUALIZATION.PY
====================================================================

PURPOSE
-------
Master raw-material library for visualization in the Neural Analysis
Pipeline Generator.

This document contains reusable visualization functions that
analysis.py can select and assemble into generated neural-analysis
pipelines.

IMPORTANT
---------
This is a RESOURCE LIBRARY.

It is NOT one finished visualization pipeline.

The generator selects the appropriate visualization components based
on:

    neural_data
    pipeline_type
    analysis_type
    available data
    requested visualization
    compatibility rules

STATISTICAL RESULTS
-------------------
Statistical results are NOT displayed through a popup or GUI report.

The generated pipeline prints numerical/statistical results directly
to the terminal.

Visualization functions in this document are responsible only for
visual representations of neural data and analysis results.

====================================================================
"""


# ==================================================================
# 1. IMPORTS
# ==================================================================

import numpy as np
import matplotlib.pyplot as plt

from scipy import signal


# ==================================================================
# 2. STANDARD VALIDATION
# ==================================================================

def validate_signal(data):
    """
    Validate a numerical signal.
    """

    data = np.asarray(data)

    if data.size == 0:
        raise ValueError(
            "Signal is empty."
        )

    if not np.issubdtype(
        data.dtype,
        np.number
    ):
        raise ValueError(
            "Signal must contain numerical values."
        )

    return data.astype(float)


def validate_sampling_rate(
    sampling_rate
):
    """
    Validate sampling rate.
    """

    if sampling_rate <= 0:
        raise ValueError(
            "Sampling rate must be greater than zero."
        )

    return float(
        sampling_rate
    )


def validate_multichannel_data(
    data
):
    """
    Validate channels × samples data.
    """

    data = validate_signal(
        data
    )

    if data.ndim != 2:
        raise ValueError(
            "Expected channels × samples data."
        )

    return data


# ==================================================================
# 3. TIME VECTOR
# ==================================================================

def create_time_vector(
    number_of_samples,
    sampling_rate
):
    """
    Create a time vector for a signal.
    """

    sampling_rate = validate_sampling_rate(
        sampling_rate
    )

    return np.arange(
        number_of_samples
    ) / sampling_rate


# ==================================================================
# 4. SINGLE SIGNAL TIME-SERIES PLOT
# ==================================================================

def plot_time_series(
    data,
    sampling_rate,
    title="Neural Signal",
    channel_name=None,
    show=True
):
    """
    Plot a single neural signal against time.
    """

    data = validate_signal(
        data
    )

    sampling_rate = validate_sampling_rate(
        sampling_rate
    )

    time = create_time_vector(
        len(data),
        sampling_rate
    )

    figure, axis = plt.subplots()

    axis.plot(
        time,
        data
    )

    axis.set_xlabel(
        "Time (s)"
    )

    axis.set_ylabel(
        "Amplitude"
    )

    axis.set_title(
        title
    )

    if channel_name is not None:

        axis.legend(
            [channel_name]
        )

    figure.tight_layout()

    if show:
        plt.show()

    return figure, axis


# ==================================================================
# 5. MULTI-CHANNEL TIME-SERIES PLOT
# ==================================================================

def plot_multichannel_time_series(
    data,
    sampling_rate,
    channel_names=None,
    title="Multichannel Neural Signals",
    show=True
):
    """
    Plot multiple channels against time.

    Expected shape:

        channels × samples
    """

    data = validate_multichannel_data(
        data
    )

    sampling_rate = validate_sampling_rate(
        sampling_rate
    )

    number_of_channels = data.shape[0]

    time = create_time_vector(
        data.shape[1],
        sampling_rate
    )

    figure, axis = plt.subplots()

    for channel_index in range(
        number_of_channels
    ):

        label = None

        if (
            channel_names is not None
            and
            channel_index < len(channel_names)
        ):
            label = channel_names[
                channel_index
            ]

        if label is None:
            label = (
                f"Channel {channel_index + 1}"
            )

        axis.plot(
            time,
            data[channel_index],
            label=label
        )

    axis.set_xlabel(
        "Time (s)"
    )

    axis.set_ylabel(
        "Amplitude"
    )

    axis.set_title(
        title
    )

    axis.legend()

    figure.tight_layout()

    if show:
        plt.show()

    return figure, axis


# ==================================================================
# 6. STACKED CHANNEL PLOT
# ==================================================================

def plot_stacked_channels(
    data,
    sampling_rate,
    channel_names=None,
    title="Stacked Neural Channels",
    show=True
):
    """
    Display channels vertically with independent offsets.
    """

    data = validate_multichannel_data(
        data
    )

    sampling_rate = validate_sampling_rate(
        sampling_rate
    )

    number_of_channels = data.shape[0]

    time = create_time_vector(
        data.shape[1],
        sampling_rate
    )

    figure, axis = plt.subplots(
        figsize=(
            10,
            max(
                4,
                number_of_channels * 1.5
            )
        )
    )

    scale = np.max(
        np.abs(data)
    )

    if scale == 0:
        scale = 1

    spacing = scale * 2

    for channel_index in range(
        number_of_channels
    ):

        offset = (
            channel_index *
            spacing
        )

        label = None

        if (
            channel_names is not None
            and
            channel_index < len(channel_names)
        ):
            label = channel_names[
                channel_index
            ]
        else:
            label = (
                f"Channel {channel_index + 1}"
            )

        axis.plot(
            time,
            data[channel_index] + offset
        )

        axis.text(
            time[0],
            offset,
            label
        )

    axis.set_xlabel(
        "Time (s)"
    )

    axis.set_ylabel(
        "Channels"
    )

    axis.set_title(
        title
    )

    figure.tight_layout()

    if show:
        plt.show()

    return figure, axis


# ==================================================================
# 7. PSD / POWER SPECTRAL DENSITY
# ==================================================================

def plot_power_spectral_density(
    data,
    sampling_rate,
    title="Power Spectral Density",
    maximum_frequency=None,
    show=True
):
    """
    Calculate and display power spectral density.
    """

    data = validate_signal(
        data
    )

    sampling_rate = validate_sampling_rate(
        sampling_rate
    )

    frequencies, power = signal.periodogram(
        data,
        fs=sampling_rate
    )

    if maximum_frequency is not None:

        mask = (
            frequencies <=
            maximum_frequency
        )

        frequencies = frequencies[
            mask
        ]

        power = power[
            mask
        ]

    figure, axis = plt.subplots()

    axis.plot(
        frequencies,
        power
    )

    axis.set_xlabel(
        "Frequency (Hz)"
    )

    axis.set_ylabel(
        "Power"
    )

    axis.set_title(
        title
    )

    figure.tight_layout()

    if show:
        plt.show()

    return figure, axis


# ==================================================================
# 8. MULTI-CHANNEL PSD
# ==================================================================

def plot_multichannel_psd(
    data,
    sampling_rate,
    channel_names=None,
    maximum_frequency=None,
    title="Multichannel Power Spectral Density",
    show=True
):
    """
    Display PSD for multiple channels.
    """

    data = validate_multichannel_data(
        data
    )

    sampling_rate = validate_sampling_rate(
        sampling_rate
    )

    figure, axis = plt.subplots()

    for channel_index in range(
        data.shape[0]
    ):

        frequencies, power = (
            signal.periodogram(
                data[channel_index],
                fs=sampling_rate
            )
        )

        if maximum_frequency is not None:

            mask = (
                frequencies <=
                maximum_frequency
            )

            frequencies = frequencies[
                mask
            ]

            power = power[
                mask
            ]

        if (
            channel_names is not None
            and
            channel_index < len(channel_names)
        ):

            label = channel_names[
                channel_index
            ]

        else:

            label = (
                f"Channel {channel_index + 1}"
            )

        axis.plot(
            frequencies,
            power,
            label=label
        )

    axis.set_xlabel(
        "Frequency (Hz)"
    )

    axis.set_ylabel(
        "Power"
    )

    axis.set_title(
        title
    )

    axis.legend()

    figure.tight_layout()

    if show:
        plt.show()

    return figure, axis


# ==================================================================
# 9. SPECTROGRAM
# ==================================================================

def plot_spectrogram(
    data,
    sampling_rate,
    title="Neural Signal Spectrogram",
    maximum_frequency=None,
    show=True
):
    """
    Display time-frequency representation of a signal.
    """

    data = validate_signal(
        data
    )

    sampling_rate = validate_sampling_rate(
        sampling_rate
    )

    frequencies, times, power = (
        signal.spectrogram(
            data,
            fs=sampling_rate
        )
    )

    if maximum_frequency is not None:

        mask = (
            frequencies <=
            maximum_frequency
        )

        frequencies = frequencies[
            mask
        ]

        power = power[
            mask,
            :
        ]

    figure, axis = plt.subplots()

    mesh = axis.pcolormesh(
        times,
        frequencies,
        power,
        shading="auto"
    )

    figure.colorbar(
        mesh,
        ax=axis,
        label="Power"
    )

    axis.set_xlabel(
        "Time (s)"
    )

    axis.set_ylabel(
        "Frequency (Hz)"
    )

    axis.set_title(
        title
    )

    figure.tight_layout()

    if show:
        plt.show()

    return figure, axis


# ==================================================================
# 10. FREQUENCY BAND PLOT
# ==================================================================

def plot_frequency_band(
    frequencies,
    values,
    low_frequency,
    high_frequency,
    title="Frequency Band",
    ylabel="Power",
    show=True
):
    """
    Display a selected frequency range.
    """

    frequencies = validate_signal(
        frequencies
    )

    values = validate_signal(
        values
    )

    if frequencies.size != values.size:
        raise ValueError(
            "Frequency and value arrays must have equal length."
        )

    mask = (
        (frequencies >= low_frequency)
        &
        (frequencies <= high_frequency)
    )

    figure, axis = plt.subplots()

    axis.plot(
        frequencies[mask],
        values[mask]
    )

    axis.set_xlabel(
        "Frequency (Hz)"
    )

    axis.set_ylabel(
        ylabel
    )

    axis.set_title(
        title
    )

    figure.tight_layout()

    if show:
        plt.show()

    return figure, axis


# ==================================================================
# 11. BAND POWER BAR PLOT
# ==================================================================

def plot_band_power(
    band_names,
    band_values,
    title="Band Power",
    ylabel="Power",
    show=True
):
    """
    Display numerical values for multiple frequency bands.
    """

    values = validate_signal(
        band_values
    )

    if len(band_names) != len(values):
        raise ValueError(
            "Band names and values must have equal length."
        )

    figure, axis = plt.subplots()

    axis.bar(
        band_names,
        values
    )

    axis.set_xlabel(
        "Frequency Band"
    )

    axis.set_ylabel(
        ylabel
    )

    axis.set_title(
        title
    )

    figure.tight_layout()

    if show:
        plt.show()

    return figure, axis


# ==================================================================
# 12. CONNECTIVITY MATRIX
# ==================================================================

def plot_connectivity_matrix(
    matrix,
    channel_names=None,
    title="Connectivity Matrix",
    show=True
):
    """
    Display a connectivity matrix.
    """

    matrix = validate_signal(
        matrix
    )

    if matrix.ndim != 2:
        raise ValueError(
            "Connectivity matrix must be two-dimensional."
        )

    figure, axis = plt.subplots()

    image = axis.imshow(
        matrix,
        aspect="auto",
        interpolation="nearest"
    )

    figure.colorbar(
        image,
        ax=axis,
        label="Connectivity"
    )

    if channel_names is not None:

        axis.set_xticks(
            np.arange(
                len(channel_names)
            )
        )

        axis.set_yticks(
            np.arange(
                len(channel_names)
            )
        )

        axis.set_xticklabels(
            channel_names,
            rotation=90
        )

        axis.set_yticklabels(
            channel_names
        )

    axis.set_xlabel(
        "Channel"
    )

    axis.set_ylabel(
        "Channel"
    )

    axis.set_title(
        title
    )

    figure.tight_layout()

    if show:
        plt.show()

    return figure, axis


# ==================================================================
# 13. COHERENCE PLOT
# ==================================================================

def plot_coherence(
    frequencies,
    coherence,
    title="Coherence",
    maximum_frequency=None,
    show=True
):
    """
    Display coherence as a function of frequency.
    """

    frequencies = validate_signal(
        frequencies
    )

    coherence = validate_signal(
        coherence
    )

    if frequencies.size != coherence.size:
        raise ValueError(
            "Frequency and coherence arrays must have equal length."
        )

    if maximum_frequency is not None:

        mask = (
            frequencies <=
            maximum_frequency
        )

        frequencies = frequencies[
            mask
        ]

        coherence = coherence[
            mask
        ]

    figure, axis = plt.subplots()

    axis.plot(
        frequencies,
        coherence
    )

    axis.set_xlabel(
        "Frequency (Hz)"
    )

    axis.set_ylabel(
        "Coherence"
    )

    axis.set_title(
        title
    )

    figure.tight_layout()

    if show:
        plt.show()

    return figure, axis


# ==================================================================
# 14. CROSS-CORRELATION PLOT
# ==================================================================

def plot_cross_correlation(
    lags,
    correlation,
    title="Cross-Correlation",
    show=True
):
    """
    Display cross-correlation against lag.
    """

    lags = validate_signal(
        lags
    )

    correlation = validate_signal(
        correlation
    )

    if lags.size != correlation.size:
        raise ValueError(
            "Lag and correlation arrays must have equal length."
        )

    figure, axis = plt.subplots()

    axis.plot(
        lags,
        correlation
    )

    axis.set_xlabel(
        "Lag"
    )

    axis.set_ylabel(
        "Correlation"
    )

    axis.set_title(
        title
    )

    figure.tight_layout()

    if show:
        plt.show()

    return figure, axis


# ==================================================================
# 15. PHASE DIFFERENCE PLOT
# ==================================================================

def plot_phase_difference(
    time,
    phase_difference,
    title="Phase Difference",
    show=True
):
    """
    Display phase difference over time.
    """

    time = validate_signal(
        time
    )

    phase_difference = validate_signal(
        phase_difference
    )

    if time.size != phase_difference.size:
        raise ValueError(
            "Time and phase arrays must have equal length."
        )

    figure, axis = plt.subplots()

    axis.plot(
        time,
        phase_difference
    )

    axis.set_xlabel(
        "Time (s)"
    )

    axis.set_ylabel(
        "Phase Difference (radians)"
    )

    axis.set_title(
        title
    )

    figure.tight_layout()

    if show:
        plt.show()

    return figure, axis


# ==================================================================
# 16. SPIKE RASTER PLOT
# ==================================================================

def plot_spike_raster(
    spike_times,
    neuron_ids=None,
    title="Spike Raster",
    show=True
):
    """
    Display spike events as a raster plot.

    spike_times may be:

        list of arrays

    where each array contains spike times for one neuron/channel.
    """

    if len(spike_times) == 0:
        raise ValueError(
            "Spike-time collection is empty."
        )

    figure, axis = plt.subplots()

    if neuron_ids is None:

        neuron_ids = range(
            len(spike_times)
        )

    for index, times in enumerate(
        spike_times
    ):

        times = validate_signal(
            times
        )

        y = np.full(
            times.shape,
            index
        )

        axis.scatter(
            times,
            y,
            marker="|"
        )

    axis.set_xlabel(
        "Time (s)"
    )

    axis.set_ylabel(
        "Neuron / Channel"
    )

    axis.set_title(
        title
    )

    if neuron_ids is not None:

        axis.set_yticks(
            np.arange(
                len(neuron_ids)
            )
        )

        axis.set_yticklabels(
            neuron_ids
        )

    figure.tight_layout()

    if show:
        plt.show()

    return figure, axis


# ==================================================================
# 17. FIRING RATE PLOT
# ==================================================================

def plot_firing_rate(
    time,
    firing_rate,
    title="Firing Rate",
    show=True
):
    """
    Display firing rate over time.
    """

    time = validate_signal(
        time
    )

    firing_rate = validate_signal(
        firing_rate
    )

    if time.size != firing_rate.size:
        raise ValueError(
            "Time and firing-rate arrays must have equal length."
        )

    figure, axis = plt.subplots()

    axis.plot(
        time,
        firing_rate
    )

    axis.set_xlabel(
        "Time (s)"
    )

    axis.set_ylabel(
        "Firing Rate (Hz)"
    )

    axis.set_title(
        title
    )

    figure.tight_layout()

    if show:
        plt.show()

    return figure, axis


# ==================================================================
# 18. ERP / EVOKED RESPONSE
# ==================================================================

def plot_evoked_response(
    time,
    response,
    title="Evoked Response",
    show=True
):
    """
    Display an evoked/ERP response.
    """

    time = validate_signal(
        time
    )

    response = validate_signal(
        response
    )

    if time.size != response.size:
        raise ValueError(
            "Time and response arrays must have equal length."
        )

    figure, axis = plt.subplots()

    axis.plot(
        time,
        response
    )

    axis.axvline(
        0,
        linestyle="--"
    )

    axis.set_xlabel(
        "Time"
    )

    axis.set_ylabel(
        "Amplitude"
    )

    axis.set_title(
        title
    )

    figure.tight_layout()

    if show:
        plt.show()

    return figure, axis


# ==================================================================
# 19. DISTRIBUTION HISTOGRAM
# ==================================================================

def plot_distribution(
    data,
    title="Distribution",
    xlabel="Value",
    bins=30,
    show=True
):
    """
    Display a numerical distribution.
    """

    data = validate_signal(
        data
    )

    figure, axis = plt.subplots()

    axis.hist(
        data,
        bins=bins
    )

    axis.set_xlabel(
        xlabel
    )

    axis.set_ylabel(
        "Count"
    )

    axis.set_title(
        title
    )

    figure.tight_layout()

    if show:
        plt.show()

    return figure, axis


# ==================================================================
# 20. BOXPLOT
# ==================================================================

def plot_boxplot(
    datasets,
    labels=None,
    title="Distribution Comparison",
    show=True
):
    """
    Compare multiple numerical distributions.
    """

    figure, axis = plt.subplots()

    axis.boxplot(
        datasets,
        labels=labels
    )

    axis.set_title(
        title
    )

    figure.tight_layout()

    if show:
        plt.show()

    return figure, axis


# ==================================================================
# 21. SCATTER PLOT
# ==================================================================

def plot_scatter(
    x,
    y,
    title="Signal Relationship",
    xlabel="Signal A",
    ylabel="Signal B",
    show=True
):
    """
    Display relationship between two variables/signals.
    """

    x = validate_signal(
        x
    )

    y = validate_signal(
        y
    )

    if x.size != y.size:
        raise ValueError(
            "X and Y must have equal length."
        )

    figure, axis = plt.subplots()

    axis.scatter(
        x,
        y
    )

    axis.set_xlabel(
        xlabel
    )

    axis.set_ylabel(
        ylabel
    )

    axis.set_title(
        title
    )

    figure.tight_layout()

    if show:
        plt.show()

    return figure, axis


# ==================================================================
# 22. DECODING ACCURACY
# ==================================================================

def plot_decoding_accuracy(
    x_values,
    accuracy,
    title="Decoding Accuracy",
    xlabel="Sample / Trial",
    show=True
):
    """
    Display decoding accuracy.
    """

    x_values = validate_signal(
        x_values
    )

    accuracy = validate_signal(
        accuracy
    )

    if x_values.size != accuracy.size:
        raise ValueError(
            "X values and accuracy arrays must have equal length."
        )

    figure, axis = plt.subplots()

    axis.plot(
        x_values,
        accuracy
    )

    axis.set_xlabel(
        xlabel
    )

    axis.set_ylabel(
        "Accuracy"
    )

    axis.set_title(
        title
    )

    figure.tight_layout()

    if show:
        plt.show()

    return figure, axis


# ==================================================================
# 23. CONFUSION MATRIX
# ==================================================================

def plot_confusion_matrix(
    matrix,
    class_names=None,
    title="Confusion Matrix",
    show=True
):
    """
    Display classification confusion matrix.
    """

    matrix = validate_signal(
        matrix
    )

    if matrix.ndim != 2:
        raise ValueError(
            "Confusion matrix must be two-dimensional."
        )

    figure, axis = plt.subplots()

    image = axis.imshow(
        matrix,
        interpolation="nearest"
    )

    figure.colorbar(
        image,
        ax=axis
    )

    if class_names is not None:

        axis.set_xticks(
            np.arange(
                len(class_names)
            )
        )

        axis.set_yticks(
            np.arange(
                len(class_names)
            )
        )

        axis.set_xticklabels(
            class_names,
            rotation=90
        )

        axis.set_yticklabels(
            class_names
        )

    axis.set_xlabel(
        "Predicted"
    )

    axis.set_ylabel(
        "Actual"
    )

    axis.set_title(
        title
    )

    figure.tight_layout()

    if show:
        plt.show()

    return figure, axis


# ==================================================================
# 24. GENERIC LINE PLOT
# ==================================================================

def plot_line(
    x,
    y,
    title="Analysis Result",
    xlabel="X",
    ylabel="Y",
    show=True
):
    """
    Generic line visualization for generated pipelines.
    """

    x = validate_signal(
        x
    )

    y = validate_signal(
        y
    )

    if x.size != y.size:
        raise ValueError(
            "X and Y must have equal length."
        )

    figure, axis = plt.subplots()

    axis.plot(
        x,
        y
    )

    axis.set_xlabel(
        xlabel
    )

    axis.set_ylabel(
        ylabel
    )

    axis.set_title(
        title
    )

    figure.tight_layout()

    if show:
        plt.show()

    return figure, axis


# ==================================================================
# 25. GENERIC BAR PLOT
# ==================================================================

def plot_bar(
    labels,
    values,
    title="Analysis Result",
    xlabel="Category",
    ylabel="Value",
    show=True
):
    """
    Generic bar visualization for generated pipelines.
    """

    values = validate_signal(
        values
    )

    if len(labels) != len(values):
        raise ValueError(
            "Labels and values must have equal length."
        )

    figure, axis = plt.subplots()

    axis.bar(
        labels,
        values
    )

    axis.set_xlabel(
        xlabel
    )

    axis.set_ylabel(
        ylabel
    )

    axis.set_title(
        title
    )

    figure.tight_layout()

    if show:
        plt.show()

    return figure, axis


# ==================================================================
# 26. SAVE FIGURE
# ==================================================================

def save_figure(
    figure,
    output_path,
    dpi=300
):
    """
    Save a generated visualization to disk.
    """

    figure.savefig(
        output_path,
        dpi=dpi,
        bbox_inches="tight"
    )

    return output_path


# ==================================================================
# 27. CLOSE FIGURE
# ==================================================================

def close_figure(
    figure=None
):
    """
    Close one figure or all matplotlib figures.
    """

    if figure is None:

        plt.close(
            "all"
        )

    else:

        plt.close(
            figure
        )


# ==================================================================
# 28. STANDARD FREQUENCY BANDS
# ==================================================================

STANDARD_FREQUENCY_BANDS = {

    "delta": (
        0.5,
        4.0
    ),

    "theta": (
        4.0,
        8.0
    ),

    "alpha": (
        8.0,
        13.0
    ),

    "beta": (
        13.0,
        30.0
    ),

    "gamma": (
        30.0,
        100.0
    )

}


# ==================================================================
# 29. VISUALIZATION RESOURCE REGISTRY
# ==================================================================

VISUALIZATION_RESOURCES = {

    "time_series": {

        "function":
            plot_time_series,

        "category":
            "time_domain",

        "requires":
            [
                "signal",
                "sampling_rate"
            ]

    },

    "multichannel_time_series": {

        "function":
            plot_multichannel_time_series,

        "category":
            "time_domain",

        "requires":
            [
                "multichannel_signal",
                "sampling_rate"
            ]

    },

    "stacked_channels": {

        "function":
            plot_stacked_channels,

        "category":
            "time_domain",

        "requires":
            [
                "multichannel_signal",
                "sampling_rate"
            ]

    },

    "power_spectral_density": {

        "function":
            plot_power_spectral_density,

        "category":
            "frequency_domain",

        "requires":
            [
                "signal",
                "sampling_rate"
            ]

    },

    "multichannel_psd": {

        "function":
            plot_multichannel_psd,

        "category":
            "frequency_domain",

        "requires":
            [
                "multichannel_signal",
                "sampling_rate"
            ]

    },

    "spectrogram": {

        "function":
            plot_spectrogram,

        "category":
            "time_frequency",

        "requires":
            [
                "signal",
                "sampling_rate"
            ]

    },

    "frequency_band": {

        "function":
            plot_frequency_band,

        "category":
            "frequency_domain",

        "requires":
            [
                "frequencies",
                "values",
                "frequency_band"
            ]

    },

    "band_power": {

        "function":
            plot_band_power,

        "category":
            "frequency_domain",

        "requires":
            [
                "band_names",
                "band_values"
            ]

    },

    "connectivity_matrix": {

        "function":
            plot_connectivity_matrix,

        "category":
            "connectivity",

        "requires":
            [
                "connectivity_matrix"
            ]

    },

    "coherence": {

        "function":
            plot_coherence,

        "category":
            "connectivity",

        "requires":
            [
                "frequencies",
                "coherence"
            ]

    },

    "cross_correlation": {

        "function":
            plot_cross_correlation,

        "category":
            "connectivity",

        "requires":
            [
                "lags",
                "correlation"
            ]

    },

    "phase_difference": {

        "function":
            plot_phase_difference,

        "category":
            "connectivity",

        "requires":
            [
                "time",
                "phase_difference"
            ]

    },

    "spike_raster": {

        "function":
            plot_spike_raster,

        "category":
            "spiking",

        "requires":
            [
                "spike_times"
            ]

    },

    "firing_rate": {

        "function":
            plot_firing_rate,

        "category":
            "spiking",

        "requires":
            [
                "time",
                "firing_rate"
            ]

    },

    "evoked_response": {

        "function":
            plot_evoked_response,

        "category":
            "event_related",

        "requires":
            [
                "time",
                "response"
            ]

    },

    "distribution": {

        "function":
            plot_distribution,

        "category":
            "statistics",

        "requires":
            [
                "values"
            ]

    },

    "boxplot": {

        "function":
            plot_boxplot,

        "category":
            "statistics",

        "requires":
            [
                "datasets"
            ]

    },

    "scatter": {

        "function":
            plot_scatter,

        "category":
            "statistics",

        "requires":
            [
                "x",
                "y"
            ]

    },

    "decoding_accuracy": {

        "function":
            plot_decoding_accuracy,

        "category":
            "decoding",

        "requires":
            [
                "x_values",
                "accuracy"
            ]

    },

    "confusion_matrix": {

        "function":
            plot_confusion_matrix,

        "category":
            "decoding",

        "requires":
            [
                "confusion_matrix"
            ]

    },

    "generic_line": {

        "function":
            plot_line,

        "category":
            "generic",

        "requires":
            [
                "x",
                "y"
            ]

    },

    "generic_bar": {

        "function":
            plot_bar,

        "category":
            "generic",

        "requires":
            [
                "labels",
                "values"
            ]

    }

}


# ==================================================================
# 30. DATA-TYPE COMPATIBILITY
# ==================================================================

VISUALIZATION_DATA_COMPATIBILITY = {

    "EEG": [

        "time_series",
        "multichannel_time_series",
        "stacked_channels",
        "power_spectral_density",
        "multichannel_psd",
        "spectrogram",
        "frequency_band",
        "band_power",
        "connectivity_matrix",
        "coherence",
        "cross_correlation",
        "phase_difference",
        "evoked_response",
        "distribution",
        "boxplot",
        "scatter"

    ],

    "ECoG": [

        "time_series",
        "multichannel_time_series",
        "stacked_channels",
        "power_spectral_density",
        "multichannel_psd",
        "spectrogram",
        "frequency_band",
        "band_power",
        "connectivity_matrix",
        "coherence",
        "cross_correlation",
        "phase_difference",
        "evoked_response",
        "distribution",
        "boxplot",
        "scatter"

    ],

    "LFP": [

        "time_series",
        "multichannel_time_series",
        "stacked_channels",
        "power_spectral_density",
        "multichannel_psd",
        "spectrogram",
        "frequency_band",
        "band_power",
        "connectivity_matrix",
        "coherence",
        "cross_correlation",
        "phase_difference",
        "spike_raster",
        "firing_rate",
        "distribution",
        "boxplot",
        "scatter"

    ],

    "intracortical": [

        "time_series",
        "multichannel_time_series",
        "stacked_channels",
        "power_spectral_density",
        "multichannel_psd",
        "spectrogram",
        "frequency_band",
        "band_power",
        "connectivity_matrix",
        "coherence",
        "cross_correlation",
        "phase_difference",
        "spike_raster",
        "firing_rate",
        "distribution",
        "boxplot",
        "scatter"

    ],

    "MEG": [

        "time_series",
        "multichannel_time_series",
        "stacked_channels",
        "power_spectral_density",
        "multichannel_psd",
        "spectrogram",
        "frequency_band",
        "band_power",
        "connectivity_matrix",
        "coherence",
        "cross_correlation",
        "phase_difference",
        "evoked_response",
        "distribution",
        "boxplot",
        "scatter"

    ],

    "fNIRS": [

        "time_series",
        "multichannel_time_series",
        "stacked_channels",
        "frequency_band",
        "connectivity_matrix",
        "cross_correlation",
        "evoked_response",
        "distribution",
        "boxplot",
        "scatter"

    ],

    "EMG": [

        "time_series",
        "multichannel_time_series",
        "stacked_channels",
        "power_spectral_density",
        "multichannel_psd",
        "spectrogram",
        "frequency_band",
        "band_power",
        "connectivity_matrix",
        "coherence",
        "cross_correlation",
        "distribution",
        "boxplot",
        "scatter"

    ],

    "EOG": [

        "time_series",
        "multichannel_time_series",
        "power_spectral_density",
        "spectrogram",
        "frequency_band",
        "coherence",
        "cross_correlation",
        "evoked_response",
        "distribution",
        "boxplot",
        "scatter"

    ]

}


# ==================================================================
# 31. PIPELINE COMPATIBILITY
# ==================================================================

VISUALIZATION_PIPELINE_COMPATIBILITY = {

    "EEG_analysis": [

        "EEG"

    ],

    "IONM": [

        "EEG",
        "ECoG",
        "EMG",
        "EOG"

    ],

    "intracortical_analysis": [

        "intracortical",
        "LFP"

    ],

    "connectivity_analysis": [

        "EEG",
        "ECoG",
        "MEG",
        "LFP",
        "fNIRS",
        "EMG",
        "EOG",
        "intracortical"

    ],

    "neural_decoding": [

        "EEG",
        "ECoG",
        "LFP",
        "intracortical",
        "MEG"

    ]

}


# ==================================================================
# 32. VISUALIZATION ASSEMBLY RULES
# ==================================================================

VISUALIZATION_ASSEMBLY_RULES = {

    "visualization_is_optional":
        True,

    "statistics_are_terminal_output":
        True,

    "visualization_does_not_generate_popup":
        True,

    "visualization_does_not_generate_report_window":
        True,

    "single_signal_requires_one_dimensional_data":
        True,

    "multichannel_visualization_requires_two_dimensional_data":
        True,

    "spectrogram_requires_sampling_rate":
        True,

    "psd_requires_sampling_rate":
        True,

    "coherence_visualization_requires_frequency_data":
        True,

    "connectivity_matrix_visualization_requires_matrix":
        True,

    "spike_raster_requires_detected_spikes":
        True,

    "firing_rate_requires_rate_data":
        True,

    "decoding_visualization_requires_predictions_or_scores":
        True,

    "visualization_can_be_saved":
        True,

    "visualization_can_be_displayed":
        True,

    "visualization_should_not_modify_statistics":
        True

}


# ==================================================================
# 33. RESOURCE LOOKUP
# ==================================================================

def get_visualization_resource(
    resource_name
):
    """
    Retrieve one visualization resource.
    """

    if resource_name not in (
        VISUALIZATION_RESOURCES
    ):

        raise ValueError(
            f"Unknown visualization resource: "
            f"{resource_name}"
        )

    return VISUALIZATION_RESOURCES[
        resource_name
    ]


# ==================================================================
# 34. LIST VISUALIZATION RESOURCES
# ==================================================================

def list_visualization_resources(
    category=None
):
    """
    List visualization resources.

    If category is supplied, return only resources belonging
    to that category.
    """

    if category is None:

        return list(
            VISUALIZATION_RESOURCES.keys()
        )

    return [

        name

        for name, resource
        in VISUALIZATION_RESOURCES.items()

        if resource[
            "category"
        ] == category

    ]


# ==================================================================
# 35. CHECK DATA COMPATIBILITY
# ==================================================================

def is_visualization_compatible(
    neural_data,
    visualization_name
):
    """
    Determine whether a visualization is compatible with a
    neural-data type.
    """

    if neural_data not in (
        VISUALIZATION_DATA_COMPATIBILITY
    ):

        return False

    return (
        visualization_name
        in
        VISUALIZATION_DATA_COMPATIBILITY[
            neural_data
        ]
    )


# ==================================================================
# 36. GET COMPATIBLE VISUALIZATIONS
# ==================================================================

def get_compatible_visualizations(
    neural_data
):
    """
    Return all visualization resources explicitly compatible
    with a neural-data type.
    """

    return VISUALIZATION_DATA_COMPATIBILITY.get(
        neural_data,
        []
    )


# ==================================================================
# 37. CHECK PIPELINE COMPATIBILITY
# ==================================================================

def is_pipeline_visualization_compatible(
    pipeline_type,
    neural_data
):
    """
    Determine whether a pipeline can use this visualization layer
    for a given neural-data type.
    """

    compatible_data = (
        VISUALIZATION_PIPELINE_COMPATIBILITY.get(
            pipeline_type,
            []
        )
    )

    return (
        neural_data
        in
        compatible_data
    )


# ==================================================================
# 38. BUILD VISUALIZATION PLAN
# ==================================================================

def build_visualization_plan(
    neural_data,
    pipeline_type,
    requested_visualizations
):
    """
    Build a validated visualization plan.

    Every requested visualization must be compatible with the
    selected neural-data type and pipeline type.
    """

    if not is_pipeline_visualization_compatible(
        pipeline_type,
        neural_data
    ):

        raise ValueError(
            f"Pipeline '{pipeline_type}' is not compatible "
            f"with visualization for '{neural_data}'."
        )

    plan = []

    for visualization_name in (
        requested_visualizations
    ):

        if not is_visualization_compatible(
            neural_data,
            visualization_name
        ):

            raise ValueError(
                f"Visualization '{visualization_name}' "
                f"is not compatible with "
                f"neural data '{neural_data}'."
            )

        resource = get_visualization_resource(
            visualization_name
        )

        plan.append({

            "name":
                visualization_name,

            "function":
                resource[
                    "function"
                ],

            "category":
                resource[
                    "category"
                ],

            "requires":
                resource[
                    "requires"
                ]

        })

    return plan


# ==================================================================
# 39. MASTER DOCUMENT SUMMARY
# ==================================================================

MASTER_DOCUMENT_SUMMARY = {

    "document":
        "Master-DOC-visualization",

    "purpose":
        "Reusable neural-data visualization raw materials",

    "resource_count":
        len(
            VISUALIZATION_RESOURCES
        ),

    "resource_categories":
        sorted(
            set(
                resource[
                    "category"
                ]

                for resource
                in VISUALIZATION_RESOURCES.values()
            )
        ),

    "supported_data_types":
        list(
            VISUALIZATION_DATA_COMPATIBILITY.keys()
        ),

    "supported_pipeline_types":
        list(
            VISUALIZATION_PIPELINE_COMPATIBILITY.keys()
        ),

    "standard_frequency_bands":
        STANDARD_FREQUENCY_BANDS,

    "assembly_rules":
        VISUALIZATION_ASSEMBLY_RULES

}


# ==================================================================
# 40. DIRECT TEST
# ==================================================================

if __name__ == "__main__":

    print("=" * 70)

    print(
        "MASTER-DOC-VISUALIZATION"
    )

    print("=" * 70)

    print()

    print(
        "Registered visualization resources:"
    )

    for resource_name in (
        VISUALIZATION_RESOURCES
    ):

        print(
            f"  {resource_name}"
        )

    print()

    print(
        "Total resources:",
        len(
            VISUALIZATION_RESOURCES
        )
    )

    print()

    print(
        "Supported neural-data types:"
    )

    for data_type in (
        VISUALIZATION_DATA_COMPATIBILITY
    ):

        print(
            f"  {data_type}"
        )

    print()

    print(
        "Supported pipeline types:"
    )

    for pipeline_type in (
        VISUALIZATION_PIPELINE_COMPATIBILITY
    ):

        print(
            f"  {pipeline_type}"
        )

    print()

    print(
        "Statistical results:"
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
        "Master-DOC-visualization loaded successfully."
    )

    print("=" * 70)