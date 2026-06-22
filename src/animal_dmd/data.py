"""Data-loading helpers for the workshop notebooks."""

from __future__ import annotations

from pathlib import Path
import os

import morphing_birds as mb
import numpy as np


def load_hawk_motion(dataset: str = "toothless_flapping_9m_avg.npz"):
    """Load one packaged hawk motion dataset in notebook-friendly form."""
    data_dir = Path(
        os.environ.get(
            "ANIMAL_DMD_DATA_DIR",
            Path(__file__).resolve().parents[2] / "data" / "hawk",
        )
    )
    hawk = mb.Animal3D("hawk", data=str(data_dir / "mean_hawk_shape.csv"))
    data = np.load(data_dir / "processed" / dataset, allow_pickle=True)

    markers = data["markers"].astype(float)
    times = data["times"].astype(float)
    marker_names = [str(name) for name in data["marker_names"]]

    # Keep the data array in the same marker order as the plotting skeleton.
    hawk.exclude_markers([name for name in hawk.analysis_marker_names if name not in marker_names])
    order = [marker_names.index(name) for name in hawk.analysis_marker_names]
    markers = markers[:, order, :]
    marker_names = list(hawk.analysis_marker_names)

    dt = float(np.median(np.diff(times)))
    return hawk, markers, times, marker_names, dt


def load_spider_motion(dataset: str = "spider_walking.npz"):
    """Load the packaged spider walking dataset in notebook-friendly form."""
    data_dir = Path(
        os.environ.get(
            "ANIMAL_DMD_SPIDER_DIR",
            Path(__file__).resolve().parents[2] / "data" / "spider",
        )
    )
    spider = mb.Animal3D("spider", data=str(data_dir / "mean_spider_shape_carolina.csv"))
    data = np.load(data_dir / dataset, allow_pickle=True)

    markers = data["motion"].astype(float)
    times = data["times"].astype(float)
    marker_names = [str(name) for name in data["marker_names"]]

    # Keep the data array in the same marker order as the plotting skeleton.
    order = [marker_names.index(name) for name in spider.analysis_marker_names]
    markers = markers[:, order, :]
    marker_names = list(spider.analysis_marker_names)

    dt = float(np.median(np.diff(times)))
    return spider, markers, times, marker_names, dt
