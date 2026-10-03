
# ============================================================
# NEURAL ANALYSIS SYSTEM
# ============================================================
#
# This file is the analysis / pipeline-compilation layer of
# the Neural Analysis Pipeline Generator.
#
# Ingestion.py sends the user's parameter object here.
#
# analysis.py does NOT invent scientific algorithms.
#
# It uses the executable resources contained inside the
# Master-DOC's library to select, validate, and eventually
# compile the requested pipeline.
# ============================================================


# ============================================================
# IMPORTS
# ============================================================

from pathlib import Path
import importlib.util
from importlib.machinery import SourceFileLoader


# ============================================================
# MASTER-DOC DIRECTORY
# ============================================================
#
# Locate the Master-DOC library relative to analysis.py.
#
# analysis.py
#     │
#     └── Master-DOC's/
#
# Every file inside this directory is considered part of the
# Master-DOC resource library.
# ============================================================

MASTER_DOC_DIRECTORY = (
    Path(__file__).resolve().parent /
    "Master-DOC's"
)


# ============================================================
# MASTER-DOC LOADER
# ============================================================
#
# Every Master-DOC is treated as executable Python source.
#
# The files do not need a .py extension.
#
# SourceFileLoader explicitly tells Python that the file is
# Python source code.
# ============================================================

def load_master_docs():

    """
    Discover and execute every Master-DOC in the
    Master-DOC's directory.

    Returns
    -------
    dict
        Dictionary containing every successfully loaded
        Master-DOC module.

    Notes
    -----
    The physical filenames are preserved as the dictionary
    keys.

    Example:

        {
            "Master-DOC-Ingestion": <module>,
            "Master-DOC-Validation": <module>,
            ...
        }
    """

    # --------------------------------------------------------
    # VERIFY MASTER-DOC DIRECTORY
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # MASTER-DOC REGISTRY
    # --------------------------------------------------------
    #
    # This dictionary becomes the central library available
    # to the pipeline compiler.
    # --------------------------------------------------------

    master_docs = {}


    # --------------------------------------------------------
    # LOAD ERRORS
    # --------------------------------------------------------
    #
    # Errors are recorded separately so that one problematic
    # Master-DOC can be identified precisely.
    #
    # We do NOT silently ignore failures.
    # --------------------------------------------------------

    load_errors = {}


    # --------------------------------------------------------
    # DISCOVER EVERY FILE
    # --------------------------------------------------------

    document_paths = sorted(
        (
            path
            for path in MASTER_DOC_DIRECTORY.iterdir()
            if path.is_file()
        ),
        key=lambda path: path.name
    )


    # --------------------------------------------------------
    # EXECUTE EVERY MASTER-DOC
    # --------------------------------------------------------

    for document_path in document_paths:

        try:

            # ------------------------------------------------
            # CREATE SAFE INTERNAL MODULE NAME
            # ------------------------------------------------
            #
            # The physical filename remains unchanged.
            #
            # Only Python's internal module name is normalized.
            # ------------------------------------------------

            module_name = (
                document_path.name
                .replace("-", "_")
                .replace(" ", "_")
            )


            # ------------------------------------------------
            # CREATE SOURCE LOADER
            # ------------------------------------------------

            loader = SourceFileLoader(
                module_name,
                str(document_path)
            )


            # ------------------------------------------------
            # CREATE MODULE SPECIFICATION
            # ------------------------------------------------

            spec = importlib.util.spec_from_loader(
                module_name,
                loader
            )


            if spec is None:

                raise ImportError(
                    "Unable to create module specification."
                )


            # ------------------------------------------------
            # CREATE MODULE OBJECT
            # ------------------------------------------------

            module = importlib.util.module_from_spec(
                spec
            )


            # ------------------------------------------------
            # EXECUTE MASTER-DOC
            # ------------------------------------------------
            #
            # The actual Python source contained inside the
            # Master-DOC is executed here.
            #
            # Functions, dictionaries, registries, constants,
            # classes, and other Python objects become available
            # through the resulting module.
            # ------------------------------------------------

            loader.exec_module(module)


            # ------------------------------------------------
            # STORE EXECUTABLE MASTER-DOC
            # ------------------------------------------------

            master_docs[
                document_path.name
            ] = module


        except Exception as error:

            # -----------------------------------------------
            # RECORD FAILURE
            # -----------------------------------------------
            #
            # Do not silently discard the Master-DOC.
            # The compiler needs to know that loading failed.
            # -----------------------------------------------

            load_errors[
                document_path.name
            ] = error


    # ========================================================
    # RETURN MASTER-DOC LIBRARY
    # ========================================================
    #
    # Both successful modules and loading errors are returned.
    #
    # This lets the caller determine whether the complete
    # Master-DOC library is available.
    # ========================================================

    return {
        "loaded": master_docs,
        "errors": load_errors
    }


# ============================================================
# ANALYSIS ENTRY POINT
# ============================================================
#
# Ingestion.py sends the completed parameter object here.
#
# The current stage establishes the compiler state:
#
#     1. Parameters
#     2. Complete Master-DOC library
#     3. Master-DOC loading errors
#
# Pipeline compilation comes after this foundation is verified.
# ============================================================

def analyze(parameters):

    """
    Receive the parameter object from Ingestion.py and load
    the complete Master-DOC resource library.

    Parameters
    ----------
    parameters : object
        Parameter object produced by Ingestion.py.

    Returns
    -------
    dict
        Compiler state containing parameters, loaded
        Master-DOCs, and loading errors.
    """

    # --------------------------------------------------------
    # LOAD MASTER-DOC LIBRARY
    # --------------------------------------------------------

    master_doc_state = load_master_docs()


    # --------------------------------------------------------
    # TEMPORARY COMPILER STATE
    # --------------------------------------------------------
    #
    # The parameter object remains untouched.
    #
    # The Master-DOC library is added alongside it.
    # --------------------------------------------------------

    compiler_state = {

        "parameters": parameters,

        "master_docs": master_doc_state["loaded"],

        "master_doc_errors": master_doc_state["errors"]

    }


    return compiler_state


# ============================================================
# DIRECT TEST
# ============================================================
#
# Running:
#
#     python analysis.py
#
# tests the Master-DOC library independently of Ingestion.py.
#
# It reports:
#
#     DISCOVERED
#     LOADED
#     FAILED
#
# This is intentionally NOT generating a pipeline yet.
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # LOAD MASTER-DOC LIBRARY
    # --------------------------------------------------------

    master_doc_state = load_master_docs()


    loaded_docs = master_doc_state["loaded"]

    load_errors = master_doc_state["errors"]


    # ========================================================
    # MASTER-DOC LIBRARY REPORT
    # ========================================================

    print()

    print("=" * 70)

    print(
        "MASTER-DOC LIBRARY"
    )

    print("=" * 70)

    print()


    print(
        "Master-DOC directory:"
    )

    print(
        MASTER_DOC_DIRECTORY
    )

    print()


    # ========================================================
    # SUCCESSFULLY LOADED
    # ========================================================

    print(
        "EXECUTED MASTER-DOCs:"
    )

    print()


    for document_name in loaded_docs:

        print(
            f"  [LOADED] {document_name}"
        )


    print()


    # ========================================================
    # FAILED MASTER-DOCs
    # ========================================================

    if load_errors:

        print(
            "MASTER-DOCs THAT FAILED TO EXECUTE:"
        )

        print()


        for document_name, error in load_errors.items():

            print(
                f"  [FAILED] {document_name}"
            )

            print(
                f"           {type(error).__name__}: {error}"
            )

            print()


    else:

        print(
            "MASTER-DOCs THAT FAILED TO EXECUTE:"
        )

        print(
            "  NONE"
        )

        print()


    # ========================================================
    # SUMMARY
    # ========================================================

    print("=" * 70)

    print(
        f"LOADED: {len(loaded_docs)}"
    )

    print(
        f"FAILED: {len(load_errors)}"
    )

    print("=" * 70)

    print()


    # ========================================================
    # FINAL STATUS
    # ========================================================

    if load_errors:

        print(
            "MASTER-DOC LIBRARY STATUS: INCOMPLETE"
        )

        print(
            "Resolve the failed Master-DOCs before "
            "pipeline compilation."
        )

    else:

        print(
            "MASTER-DOC LIBRARY STATUS: READY"
        )

        print(
            "All discovered Master-DOCs executed successfully."
        )

    print()
