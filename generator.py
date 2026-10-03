# ============================================================
# PIPELINE GENERATOR
# ============================================================
#
# generator.py is the construction layer of the
# Neural Analysis Pipeline Generator.
#
# analysis.py produces a compiled generation specification.
#
# generator.py receives that specification.
#
# At this stage, generator.py does NOT yet retrieve or
# assemble Master-DOC code.
# ============================================================


# ============================================================
# GENERATOR ENTRY POINT
# ============================================================

def generate(generation_specification):
    """
    Receive the compiled generation specification produced
    by analysis.py.

    Parameters
    ----------
    generation_specification : object
        The validated pipeline specification produced by
        the analysis layer.

    Returns
    -------
    object
        The received generation specification.

    """

    if generation_specification is None:

        raise ValueError(
            "Generator received no generation specification."
        )

    return generation_specification


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("PIPELINE GENERATOR")
    print("=" * 60)

    print(
        "Generator is ready to receive a generation specification."
    )

    print("=" * 60)