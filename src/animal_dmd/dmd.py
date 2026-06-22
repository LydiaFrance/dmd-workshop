"""Small DMD helpers for the workshop notebooks."""

from __future__ import annotations

import numpy as np
from birddmd import reconstruct


def reconstruct_known_pairs(dmd_result, known_frequencies_hz: dict[str, float]):
    """Select and reconstruct DMD pairs nearest to known teaching frequencies."""
    pair_frequencies_hz = np.array(
        [dmd_result.pair_frequency(pair_index) for pair_index in range(dmd_result.n_pairs)]
    )
    pair_numbers = {
        label: int(np.argmin(np.abs(pair_frequencies_hz - frequency_hz)))
        for label, frequency_hz in known_frequencies_hz.items()
    }
    selected_frequencies_hz = pair_frequencies_hz[list(pair_numbers.values())]
    pair_motions = {
        label: reconstruct(dmd_result, pairs=[pair_number])
        for label, pair_number in pair_numbers.items()
    }
    return pair_frequencies_hz, pair_numbers, selected_frequencies_hz, pair_motions
