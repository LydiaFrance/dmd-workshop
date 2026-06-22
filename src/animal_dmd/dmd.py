"""Small DMD helpers for the workshop notebooks."""

from __future__ import annotations

import numpy as np
from birddmd import reconstruct


def reconstruct_known_pairs(dmd_result, known_frequencies_hz: dict[str, float]):
    """Select and reconstruct DMD pairs nearest to known teaching frequencies.

    For each target frequency we keep the DMD pair whose frequency is closest,
    i.e. argmin_k |f_k - f_target|, then rebuild that pair's contribution.

    Maths
    -----
    DMD fits the linear map x_{t+1} = A x_t. Its eigen-decomposition gives the
    modal expansion

        x(t) ~= sum_k  phi_k * exp(omega_k * t) * b_k,

    with discrete eigenvalues lambda_k and continuous rates omega_k =
    log(lambda_k) / dt. Real oscillations show up as complex-conjugate
    eigenvalue *pairs*; a pair's frequency is

        f_k = Im(omega_k) / (2*pi) = |angle(lambda_k)| / (2*pi*dt).

    Reconstructing one pair keeps only its two conjugate modes in the sum.
    """
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
