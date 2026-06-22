"""Toy motion used in the introductory DMD workshop notebook."""

from __future__ import annotations

import numpy as np

TOY_MARKER_NAMES = [
    "body",
    "left_shoulder",
    "left_hand",
    "right_shoulder",
    "right_hand",
    "head",
    "tail",
]

TOY_BODY_LINES = [(6, 0), (0, 5), (0, 1), (1, 2), (0, 3), (3, 4)]

TOY_MEAN_SHAPE = np.array(
    [
        [0.0, 0.0, 0.0],
        [-0.45, 0.35, 0.0],
        [-1.15, 0.35, 0.0],
        [0.45, 0.35, 0.0],
        [1.15, 0.35, 0.0],
        [0.0, 0.85, 0.0],
        [0.0, -0.70, 0.0],
    ],
    dtype=float,
)


def make_toy_motion(
    steady_wave: np.ndarray,
    steady_sideways: np.ndarray,
    shared_wave: np.ndarray,
    shared_sideways: np.ndarray,
    decaying_wave: np.ndarray,
    decaying_sideways: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Build the intro stick-body motion from visible time functions.

    The notebook owns the temporal functions because those are the lesson.
    This helper only hides the uninteresting marker bookkeeping.

    Maths
    -----
    Each marker coordinate is the mean shape plus a sum of scaled time
    functions,

        p_m(t) = p_mean_m + sum_j  a_{m,j} * w_j(t),

    so the motion is linear in the waveforms w_j(t) (steady, shared, decaying).
    This linear-superposition structure is exactly what SVD and DMD later
    recover.
    """
    waves = [
        np.asarray(steady_wave, dtype=float),
        np.asarray(steady_sideways, dtype=float),
        np.asarray(shared_wave, dtype=float),
        np.asarray(shared_sideways, dtype=float),
        np.asarray(decaying_wave, dtype=float),
        np.asarray(decaying_sideways, dtype=float),
    ]
    if len({wave.shape for wave in waves}) != 1:
        raise ValueError("All toy waves must have the same shape.")

    motion = np.repeat(TOY_MEAN_SHAPE[None, :, :], waves[0].size, axis=0)
    body = TOY_MARKER_NAMES.index("body")
    left_hand = TOY_MARKER_NAMES.index("left_hand")
    right_hand = TOY_MARKER_NAMES.index("right_hand")
    head = TOY_MARKER_NAMES.index("head")
    tail = TOY_MARKER_NAMES.index("tail")

    motion[:, left_hand, 1] += 0.42 * waves[0]
    motion[:, left_hand, 0] += 0.10 * waves[1]
    motion[:, [left_hand, right_hand], 1] += 0.14 * waves[2][:, None]
    motion[:, [left_hand, right_hand], 0] += 0.05 * waves[3][:, None]
    motion[:, body, 1] += 0.06 * waves[2]
    motion[:, head, 1] += 0.08 * waves[2]
    motion[:, tail, 1] -= 0.05 * waves[2]
    motion[:, right_hand, 1] += 0.42 * waves[4]
    motion[:, right_hand, 0] += 0.10 * waves[5]
    return motion, TOY_MEAN_SHAPE.copy(), np.array(TOY_MARKER_NAMES)
