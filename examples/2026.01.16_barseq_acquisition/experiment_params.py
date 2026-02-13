"""Experiment-specific parameters for BARseq subjects.

These parameters vary by subject and should be updated with actual values
once confirmed with the experimental team.

Structure: Dictionary keyed by subject_id containing all experiment-specific
parameters for that subject.
"""

from datetime import datetime, timezone

# =============================================================================
# EXPERIMENT PARAMETERS BY SUBJECT
# =============================================================================

EXPERIMENT_PARAMS = {
    "780345": {
        "specimen_id": "780345_PLACEHOLDER_SPECIMEN_ID",
        "num_sections": 51,  # Number of 20μm coronal sections through LC
        "ccf_start_plate": 99,  # Starting CCFv3 plate number
        "ccf_end_plate": 112,  # Ending CCFv3 plate number
        "experimenters": ["Imaging core"],
        # Placeholder acquisition times
        # TODO: Replace with actual times extracted from max projection file metadata
        "geneseq_start": datetime(2025, 6, 10, 12, 0, 0, tzinfo=timezone.utc),
        "geneseq_end": datetime(2025, 6, 10, 14, 0, 0, tzinfo=timezone.utc),
        "barcodeseq_start": datetime(2025, 6, 10, 14, 0, 0, tzinfo=timezone.utc),
        "barcodeseq_end": datetime(2025, 6, 10, 18, 0, 0, tzinfo=timezone.utc),
        "hyb_start": datetime(2025, 6, 10, 18, 0, 0, tzinfo=timezone.utc),
        "hyb_end": datetime(2025, 6, 10, 19, 0, 0, tzinfo=timezone.utc),
    },
    "780346": {
        "specimen_id": "780346_PLACEHOLDER_SPECIMEN_ID",
        "num_sections": 51,  # Number of 20μm coronal sections through LC
        "ccf_start_plate": 99,  # Starting CCFv3 plate number
        "ccf_end_plate": 112,  # Ending CCFv3 plate number
        "experimenters": ["Imaging core"],
        # Placeholder acquisition times
        # TODO: Replace with actual times extracted from max projection file metadata
        "geneseq_start": datetime(2025, 6, 11, 12, 0, 0, tzinfo=timezone.utc),
        "geneseq_end": datetime(2025, 6, 11, 14, 0, 0, tzinfo=timezone.utc),
        "barcodeseq_start": datetime(2025, 6, 11, 14, 0, 0, tzinfo=timezone.utc),
        "barcodeseq_end": datetime(2025, 6, 11, 18, 0, 0, tzinfo=timezone.utc),
        "hyb_start": datetime(2025, 6, 11, 18, 0, 0, tzinfo=timezone.utc),
        "hyb_end": datetime(2025, 6, 11, 19, 0, 0, tzinfo=timezone.utc),
    },
}


def get_experiment_params(subject_id: str) -> dict:
    """
    Get experiment parameters for a subject.

    Parameters
    ----------
    subject_id : str
        Subject ID (e.g., "780345", "780346")

    Returns
    -------
    dict
        Dictionary containing experiment parameters for the subject

    Raises
    ------
    ValueError
        If subject_id not found in EXPERIMENT_PARAMS
    """
    if subject_id not in EXPERIMENT_PARAMS:
        available = ", ".join(EXPERIMENT_PARAMS.keys())
        raise ValueError(
            f"No experiment parameters defined for subject {subject_id}. "
            f"Available subjects: {available}. "
            f"Add parameters for this subject in experiment_params.py first."
        )
    return EXPERIMENT_PARAMS[subject_id]
