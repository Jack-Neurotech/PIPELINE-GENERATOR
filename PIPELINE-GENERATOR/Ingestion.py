
import tkinter as tk
from tkinter import messagebox

# ============================================================
# CONNECT TO THE ANALYSIS SYSTEM
# ============================================================
#
# The analysis system is now a separate Python file.
#
# Ingestion.py collects the user's selections.
# analysis_system.py receives those selections.
#
# Both files should be in the same directory.
# ============================================================

from analysis import analyze


# ============================================================
# NEURAL DATA
# ============================================================
#
# These are the neural-data types currently supported by the
# project resources.
#
# File-type options are intentionally limited to formats for
# which we have an actual ingestion path or a concrete,
# project-supported representation.
# ============================================================

NEURAL_DATA = {

    "EEG": [
        "EEGLAB (.set)",
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
# PIPELINE TYPES
# ============================================================

PIPELINES = {

    "Signal Processing Pipeline": [
        "EEG",
        "IONM",
        "Intracortical / Extracellular"
    ],

    "EEG Analysis Pipeline": [
        "EEG"
    ],

    "IONM Pipeline": [
        "IONM",
        "EEG"
    ],

    "Intracortical Analysis Pipeline": [
        "Intracortical / Extracellular"
    ],

    "Spike Analysis Pipeline": [
        "Intracortical / Extracellular"
    ],

    "Time-Series Analysis Pipeline": [
        "EEG",
        "IONM",
        "Intracortical / Extracellular"
    ],

    "Statistical Analysis Pipeline": [
        "EEG",
        "IONM",
        "Intracortical / Extracellular"
    ],

    "Neural Decoding Pipeline": [
        "Intracortical / Extracellular",
        "EEG"
    ],

    "Neural Population Analysis Pipeline": [
        "Intracortical / Extracellular"
    ],

    "Custom Pipeline": [
        "EEG",
        "IONM",
        "Intracortical / Extracellular"
    ]
}

# ============================================================
# PIPELINE TYPES
# ============================================================
#
# Each pipeline specifies which neural-data types it can use.
# ============================================================

PIPELINES = {

    "Signal Processing Pipeline": [
        "EEG",
        "ECoG",
        "MEG",
        "IONM",
        "EMG",
        "EOG",
        "Local Field Potentials (LFP)"
    ],

    "EEG Analysis Pipeline": [
        "EEG"
    ],

    "IONM Pipeline": [
        "IONM",
        "EEG",
        "ECoG",
        "EMG",
        "EOG"
    ],

    "Intracortical Analysis Pipeline": [
        "Intracortical / Extracellular",
        "Single-Unit Recordings",
        "Multi-Unit Recordings",
        "Local Field Potentials (LFP)"
    ],

    "ECoG Analysis Pipeline": [
        "ECoG",
        "EEG",
        "Local Field Potentials (LFP)"
    ],

    "MRI Structural Analysis Pipeline": [
        "Structural MRI"
    ],

    "fMRI Analysis Pipeline": [
        "fMRI"
    ],

    "Diffusion / DTI Pipeline": [
        "DTI / Diffusion MRI"
    ],

    "MEG Analysis Pipeline": [
        "MEG"
    ],

    "fNIRS Analysis Pipeline": [
        "fNIRS"
    ],

    "Spike Analysis Pipeline": [
        "Intracortical / Extracellular",
        "Single-Unit Recordings",
        "Multi-Unit Recordings"
    ],

    "Local Field Potential Pipeline": [
        "Local Field Potentials (LFP)",
        "Intracortical / Extracellular",
        "ECoG",
        "EEG",
        "MEG"
    ],

    "Connectivity Analysis Pipeline": [
        "EEG",
        "ECoG",
        "MEG",
        "fMRI",
        "fNIRS",
        "Local Field Potentials (LFP)"
    ],

    "Time-Series Analysis Pipeline": [
        "EEG",
        "ECoG",
        "MEG",
        "IONM",
        "fNIRS",
        "Local Field Potentials (LFP)",
        "EMG"
    ],

    "Statistical Analysis Pipeline": list(NEURAL_DATA.keys()),

    "Machine Learning Pipeline": [
        "EEG",
        "ECoG",
        "MEG",
        "fMRI",
        "fNIRS",
        "Intracortical / Extracellular",
        "Local Field Potentials (LFP)",
        "Neural + Behavioral Data"
    ],

    "Neural Decoding Pipeline": [
        "Intracortical / Extracellular",
        "EEG",
        "ECoG",
        "Local Field Potentials (LFP)",
        "MEG",
        "Neural + Behavioral Data"
    ],

    "Neural Population Analysis Pipeline": [
        "Intracortical / Extracellular",
        "Single-Unit Recordings",
        "Multi-Unit Recordings",
        "Local Field Potentials (LFP)"
    ],

    "Multimodal Neural Analysis Pipeline": list(NEURAL_DATA.keys()),

    "Custom Pipeline": list(NEURAL_DATA.keys())
}


# ============================================================
# PIPELINE-SPECIFIC STATISTICAL / ANALYTICAL OUTPUTS
# ============================================================
#
# The selected pipeline determines what outputs are available.
# ============================================================

PIPELINE_OUTPUTS = {

    "EEG Analysis Pipeline": [
        "Mean",
        "Median",
        "Variance",
        "Standard Deviation",
        "RMS",
        "Spectral Power",
        "Relative Band Power",
        "Dominant Frequency",
        "Peak Frequency",
        "Peak Alpha Frequency",
        "Spectral Entropy",
        "Spectral Edge Frequency",
        "Signal-to-Noise Ratio",
        "Coherence",
        "Cross-Correlation",
        "P-value",
        "Confidence Interval",
        "Effect Size"
    ],

    "IONM Pipeline": [
        "Baseline Amplitude",
        "Peak Amplitude",
        "Amplitude Change",
        "Percentage Amplitude Change",
        "Baseline Latency",
        "Peak Latency",
        "Latency Change",
        "Baseline Comparison",
        "Threshold Analysis",
        "Mean",
        "Standard Deviation",
        "Variance",
        "P-value",
        "Confidence Interval",
        "Effect Size"
    ],

    "Intracortical Analysis Pipeline": [
        "Spike Count",
        "Firing Rate",
        "Inter-Spike Interval",
        "Burst Rate",
        "Peri-Stimulus Time Histogram (PSTH)",
        "Population Activity",
        "Tuning Curves",
        "Mean Firing Rate",
        "Firing Rate Variance",
        "Correlation",
        "Cross-Correlation",
        "P-value",
        "Confidence Interval",
        "Effect Size"
    ],

    "ECoG Analysis Pipeline": [
        "Mean",
        "Variance",
        "Standard Deviation",
        "RMS",
        "Spectral Power",
        "Relative Band Power",
        "Dominant Frequency",
        "Spectral Entropy",
        "High-Gamma Power",
        "Coherence",
        "Cross-Correlation",
        "P-value",
        "Confidence Interval",
        "Effect Size"
    ],

    "MRI Structural Analysis Pipeline": [
        "Regional Volume",
        "Total Brain Volume",
        "Cortical Thickness",
        "Voxel Statistics",
        "Regional Comparison",
        "Mean",
        "Standard Deviation",
        "Variance",
        "Correlation",
        "P-value",
        "Confidence Interval",
        "Effect Size"
    ],

    "fMRI Analysis Pipeline": [
        "BOLD Signal Change",
        "Regional Activation",
        "Voxel-Wise Statistics",
        "GLM Beta Coefficients",
        "T-Statistics",
        "Z-Statistics",
        "Functional Connectivity",
        "Correlation",
        "P-value",
        "False Discovery Rate",
        "Effect Size"
    ],

    "Diffusion / DTI Pipeline": [
        "Fractional Anisotropy (FA)",
        "Mean Diffusivity (MD)",
        "Axial Diffusivity (AD)",
        "Radial Diffusivity (RD)",
        "Tract Volume",
        "Tract Length",
        "Regional Comparison",
        "Mean",
        "Standard Deviation",
        "Variance",
        "Correlation",
        "P-value",
        "Effect Size"
    ],

    "MEG Analysis Pipeline": [
        "Mean",
        "Standard Deviation",
        "RMS",
        "Spectral Power",
        "Relative Band Power",
        "Dominant Frequency",
        "Spectral Entropy",
        "Source Localization",
        "Coherence",
        "Phase Synchronization",
        "P-value",
        "Confidence Interval",
        "Effect Size"
    ],

    "fNIRS Analysis Pipeline": [
        "Oxyhemoglobin Change",
        "Deoxyhemoglobin Change",
        "Total Hemoglobin Change",
        "Mean",
        "Standard Deviation",
        "Variance",
        "Peak Response",
        "Response Latency",
        "Correlation",
        "P-value",
        "Effect Size"
    ],

    "Spike Analysis Pipeline": [
        "Spike Count",
        "Firing Rate",
        "Inter-Spike Interval",
        "Burst Rate",
        "PSTH",
        "Spike-Train Variability",
        "Auto-Correlation",
        "Cross-Correlation",
        "Population Activity",
        "P-value",
        "Confidence Interval",
        "Effect Size"
    ],

    "Local Field Potential Pipeline": [
        "Mean",
        "Variance",
        "Standard Deviation",
        "RMS",
        "Spectral Power",
        "Relative Band Power",
        "Dominant Frequency",
        "Spectral Entropy",
        "Phase-Amplitude Coupling",
        "Coherence",
        "Cross-Correlation",
        "P-value",
        "Effect Size"
    ],

    "Connectivity Analysis Pipeline": [
        "Pearson Correlation",
        "Spearman Correlation",
        "Coherence",
        "Phase Synchronization",
        "Phase-Locking Value",
        "Functional Connectivity",
        "Connectivity Matrix",
        "Network Degree",
        "Clustering Coefficient",
        "P-value",
        "False Discovery Rate",
        "Effect Size"
    ],

    "Time-Series Analysis Pipeline": [
        "Mean",
        "Variance",
        "Standard Deviation",
        "RMS",
        "Peak Detection",
        "Signal-to-Noise Ratio",
        "Autocorrelation",
        "Cross-Correlation",
        "Spectral Power",
        "Dominant Frequency",
        "P-value",
        "Confidence Interval"
    ],

    "Statistical Analysis Pipeline": [
        "Mean",
        "Median",
        "Mode",
        "Minimum",
        "Maximum",
        "Range",
        "Variance",
        "Standard Deviation",
        "Standard Error",
        "Skewness",
        "Kurtosis",
        "Independent t-test",
        "Paired t-test",
        "One-way ANOVA",
        "Repeated-Measures ANOVA",
        "Mann-Whitney U",
        "Wilcoxon Signed-Rank",
        "Kruskal-Wallis",
        "Pearson Correlation",
        "Spearman Correlation",
        "Linear Regression",
        "Multiple Linear Regression",
        "P-value",
        "Confidence Interval",
        "Effect Size",
        "Bonferroni",
        "False Discovery Rate",
        "Permutation Testing",
        "Bootstrap Confidence Intervals"
    ],

    "Machine Learning Pipeline": [
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score",
        "ROC-AUC",
        "Confusion Matrix",
        "Mean Absolute Error (MAE)",
        "Mean Squared Error (MSE)",
        "Root Mean Squared Error (RMSE)",
        "R²",
        "Cross-Validation",
        "Feature Importance"
    ],

    "Neural Decoding Pipeline": [
        "Classification Accuracy",
        "Precision",
        "Recall",
        "F1 Score",
        "ROC-AUC",
        "Confusion Matrix",
        "Decoding Error",
        "Mean Absolute Error",
        "Cross-Validation",
        "Feature Importance"
    ],

    "Neural Population Analysis Pipeline": [
        "Spike Count",
        "Firing Rate",
        "Population Activity",
        "PSTH",
        "Tuning Curves",
        "Population Correlation",
        "Cross-Correlation",
        "Dimensionality Reduction",
        "P-value",
        "Effect Size"
    ],

    "Multimodal Neural Analysis Pipeline": [
        "Cross-Modal Correlation",
        "Cross-Modal Connectivity",
        "Multimodal Regression",
        "Multimodal Classification",
        "Feature Importance",
        "P-value",
        "Confidence Interval",
        "Effect Size"
    ],

    "Custom Pipeline": [
        "Mean",
        "Standard Deviation",
        "Variance",
        "Correlation",
        "P-value",
        "Confidence Interval",
        "Effect Size"
    ]
}


# ============================================================
# APPLICATION STATE
# ============================================================

selected_neural_data = None
selected_file_type = None
selected_pipeline = None
selected_statistics = []


# ============================================================
# GENERATE PIPELINE
# ============================================================
#
# This is the main handoff.
#
# The GUI collects all selections and packages them into
# ONE parameter object.
#
# That object is then passed to analysis_system.py.
# ============================================================

def generate_pipeline():

    global selected_neural_data
    global selected_file_type
    global selected_pipeline
    global selected_statistics

    # --------------------------------------------------------
    # Collect selections
    # --------------------------------------------------------

    selected_neural_data = neural_data_var.get()
    selected_file_type = file_type_var.get()
    selected_pipeline = pipeline_var.get()

    selected_statistics = [
        statistic
        for statistic, variable in statistic_vars.items()
        if variable.get()
    ]

    # --------------------------------------------------------
    # Validate neural data
    # --------------------------------------------------------

    if not selected_neural_data:

        messagebox.showwarning(
            "Missing Selection",
            "Please select a neural-data type."
        )

        return

    # --------------------------------------------------------
    # Validate file type
    # --------------------------------------------------------

    if not selected_file_type:

        messagebox.showwarning(
            "Missing Selection",
            "Please select a file type."
        )

        return

    # --------------------------------------------------------
    # Validate pipeline
    # --------------------------------------------------------

    if not selected_pipeline:

        messagebox.showwarning(
            "Missing Selection",
            "Please select a pipeline type."
        )

        return

    # --------------------------------------------------------
    # Validate statistical outputs
    # --------------------------------------------------------

    if not selected_statistics:

        messagebox.showwarning(
            "Missing Selection",
            "Please select at least one statistical or "
            "analytical output."
        )

        return

    # --------------------------------------------------------
    # Create complete parameter object
    # --------------------------------------------------------

    parameters = {

        "neural_data": selected_neural_data,

        "file_type": selected_file_type,

        "pipeline_type": selected_pipeline,

        "statistics": selected_statistics
    }

    # --------------------------------------------------------
    # SEND PARAMETERS TO ANALYSIS SYSTEM
    # --------------------------------------------------------
    #
    # This is where Ingestion.py hands control to
    # analysis_system.py.
    # --------------------------------------------------------

    analyze(parameters)


# ============================================================
# UPDATE FILE TYPES
# ============================================================
#
# Selecting neural data automatically changes the available
# file types.
# ============================================================

def update_file_types(*args):

    neural_data = neural_data_var.get()

    file_type_menu["menu"].delete(0, "end")

    if neural_data in NEURAL_DATA:

        for file_type in NEURAL_DATA[neural_data]:

            file_type_menu["menu"].add_command(

                label=file_type,

                command=tk._setit(
                    file_type_var,
                    file_type
                )
            )

    file_type_var.set("")


# ============================================================
# UPDATE PIPELINE TYPES
# ============================================================
#
# Selecting neural data automatically changes the available
# pipeline types.
# ============================================================

def update_pipeline_types(*args):

    neural_data = neural_data_var.get()

    pipeline_menu["menu"].delete(0, "end")

    for pipeline, compatible_data in PIPELINES.items():

        if neural_data in compatible_data:

            pipeline_menu["menu"].add_command(

                label=pipeline,

                command=tk._setit(
                    pipeline_var,
                    pipeline
                )
            )

    pipeline_var.set("")

    clear_statistics()


# ============================================================
# CLEAR STATISTICAL OUTPUTS
# ============================================================

def clear_statistics():

    global statistic_vars

    for widget in statistics_frame.winfo_children():

        widget.destroy()

    statistic_vars = {}


# ============================================================
# UPDATE STATISTICAL OUTPUTS
# ============================================================
#
# Pipeline type determines which statistical and analytical
# outputs become available.
# ============================================================

def update_statistics(*args):

    global statistic_vars

    pipeline = pipeline_var.get()

    clear_statistics()

    if pipeline not in PIPELINE_OUTPUTS:

        return

    outputs = PIPELINE_OUTPUTS[pipeline]

    columns = 3

    for index, output in enumerate(outputs):

        variable = tk.BooleanVar()

        statistic_vars[output] = variable

        row = index // columns
        column = index % columns

        checkbox = tk.Checkbutton(

            statistics_frame,

            text=output,

            variable=variable,

            anchor="w"
        )

        checkbox.grid(

            row=row,

            column=column,

            sticky="w",

            padx=15,

            pady=3
        )


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title(
    "Neural Analysis Pipeline Generator"
)

root.geometry(
    "900x800"
)

root.minsize(
    700,
    600
)


# ============================================================
# HEADER
# ============================================================

header = tk.Frame(root)

header.pack(
    fill="x",
    padx=20,
    pady=15
)


title = tk.Label(

    header,

    text="NEURAL ANALYSIS PIPELINE GENERATOR",

    font=("Helvetica", 22, "bold")
)

title.pack()


# ============================================================
# SCROLLABLE CONTENT CONTAINER
# ============================================================

content_container = tk.Frame(root)

content_container.pack(

    fill="both",

    expand=True,

    padx=20
)


# ============================================================
# CANVAS
# ============================================================

canvas = tk.Canvas(

    content_container
)

canvas.pack(

    side="left",

    fill="both",

    expand=True
)


# ============================================================
# SCROLLBAR
# ============================================================

scrollbar = tk.Scrollbar(

    content_container,

    orient="vertical",

    command=canvas.yview
)

scrollbar.pack(

    side="right",

    fill="y"
)


canvas.configure(

    yscrollcommand=scrollbar.set
)


# ============================================================
# SCROLLABLE FRAME
# ============================================================

scrollable_frame = tk.Frame(

    canvas
)


canvas_window = canvas.create_window(

    (0, 0),

    window=scrollable_frame,

    anchor="nw"
)


def update_scroll_region(event=None):

    canvas.configure(

        scrollregion=canvas.bbox("all")
    )


scrollable_frame.bind(

    "<Configure>",

    update_scroll_region
)


# ============================================================
# STEP 1 — NEURAL DATA
# ============================================================

step1_label = tk.Label(

    scrollable_frame,

    text="STEP 1 — NEURAL DATA",

    font=("Helvetica", 16, "bold")
)

step1_label.pack(

    pady=(10, 5)
)


neural_data_var = tk.StringVar()


neural_data_menu = tk.OptionMenu(

    scrollable_frame,

    neural_data_var,

    *NEURAL_DATA.keys()
)

neural_data_menu.config(

    width=35
)

neural_data_menu.pack()


# ============================================================
# FILE TYPE
# ============================================================

file_type_label = tk.Label(

    scrollable_frame,

    text="FILE TYPE",

    font=("Helvetica", 13, "bold")
)

file_type_label.pack(

    pady=(15, 5)
)


file_type_var = tk.StringVar()


file_type_menu = tk.OptionMenu(

    scrollable_frame,

    file_type_var,

    ""
)

file_type_menu.config(

    width=35
)

file_type_menu.pack()


# ============================================================
# STEP 2 — PIPELINE TYPE
# ============================================================

step2_label = tk.Label(

    scrollable_frame,

    text="STEP 2 — PIPELINE TYPE",

    font=("Helvetica", 16, "bold")
)

step2_label.pack(

    pady=(25, 5)
)


pipeline_var = tk.StringVar()


pipeline_menu = tk.OptionMenu(

    scrollable_frame,

    pipeline_var,

    ""
)

pipeline_menu.config(

    width=35
)

pipeline_menu.pack()


# ============================================================
# STEP 3 — STATISTICAL / ANALYTICAL OUTPUT
# ============================================================

step3_label = tk.Label(

    scrollable_frame,

    text="STEP 3 — STATISTICAL / ANALYTICAL OUTPUT",

    font=("Helvetica", 16, "bold")
)

step3_label.pack(

    pady=(25, 5)
)


# ============================================================
# DYNAMIC STATISTICS FRAME
# ============================================================
#
# This frame is populated based on the selected pipeline.
# ============================================================

statistics_frame = tk.Frame(

    scrollable_frame
)

statistics_frame.pack(

    fill="x",

    padx=20,

    pady=10
)


statistic_vars = {}


# ============================================================
# GENERATE BUTTON
# ============================================================
#
# This is outside the scrollable area.
# Therefore it remains visible.
# ============================================================

button_frame = tk.Frame(root)

button_frame.pack(

    fill="x",

    padx=20,

    pady=15
)


generate_button = tk.Button(

    button_frame,

    text="GENERATE PIPELINE",

    command=generate_pipeline,

    font=("Helvetica", 14, "bold"),

    padx=30,

    pady=12
)

generate_button.pack()


# ============================================================
# EVENT CONNECTIONS
# ============================================================

neural_data_var.trace_add(

    "write",

    update_file_types
)


neural_data_var.trace_add(

    "write",

    update_pipeline_types
)


pipeline_var.trace_add(

    "write",

    update_statistics
)


# ============================================================
# START APPLICATION
# ============================================================

root.mainloop()
