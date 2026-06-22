"""Helpers for the custom-data workshop notebook."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass(frozen=True)
class PreparedCustomMotion:
    """Validated motion data and derived arrays used by the custom notebook."""

    motion: np.ndarray
    times: np.ndarray
    marker_names: list[str]
    dimension_labels: list[str]
    mean_pose: np.ndarray
    centred_motion: np.ndarray
    data_matrix: np.ndarray
    dt: float

    @property
    def n_frames(self) -> int:
        return self.motion.shape[0]

    @property
    def n_markers(self) -> int:
        return self.motion.shape[1]

    @property
    def n_dimensions(self) -> int:
        return self.motion.shape[2]


@dataclass(frozen=True)
class CustomSkeleton:
    """Optional custom skeleton plus the marker names used for DMD analysis."""

    animal: object | None
    skeleton: object | None
    marker_names: list[str]
    analysis_marker_names: list[str]


def prepare_custom_motion(
    motion,
    times,
    *,
    marker_names: list[str] | None = None,
    print_summary: bool = True,
) -> PreparedCustomMotion:
    """Validate custom motion inputs and prepare the arrays used for DMD.

    Maths
    -----
    Markers are centred by subtracting the mean pose, then flattened into the
    snapshot/data matrix X of shape (features, frames), features = markers *
    dims. Column t of X is the pose at frame t -- the standard input that both
    SVD (X = U S V^T) and DMD (x_{t+1} = A x_t) operate on.
    """
    motion = np.asarray(motion, dtype=float)
    times = np.asarray(times, dtype=float)

    if motion.ndim == 2:
        motion = motion[:, :, None]
    elif motion.ndim != 3:
        raise ValueError("`motion` must have shape (frames, markers, dimensions) or (frames, features).")

    if times.ndim != 1:
        raise ValueError("`times` must be a 1D array.")
    if len(times) != motion.shape[0]:
        raise ValueError("`times` must have one value per frame in `motion`.")
    if motion.shape[0] < 3:
        raise ValueError("DMD needs at least three frames.")
    if not np.all(np.isfinite(motion)):
        raise ValueError("DMD needs finite values. Interpolate or remove missing values before this notebook.")
    if not np.all(np.diff(times) > 0):
        raise ValueError("`times` must increase strictly.")

    n_frames, n_markers, n_dimensions = motion.shape
    dt = float(np.median(np.diff(times)))

    if marker_names is None:
        marker_names = [f"marker_{i}" for i in range(n_markers)]
    else:
        marker_names = list(marker_names)

    if len(marker_names) != n_markers:
        raise ValueError("`marker_names` must have one name per marker.")

    dimension_labels = ["x", "y", "z"][:n_dimensions]
    if len(dimension_labels) < n_dimensions:
        dimension_labels.extend([f"dim_{i}" for i in range(len(dimension_labels), n_dimensions)])

    mean_pose = motion.mean(axis=0, keepdims=True)
    centred_motion = motion - mean_pose
    data_matrix = centred_motion.reshape(n_frames, -1).T

    if print_summary:
        print("motion:", motion.shape)
        print("times:", times.shape)
        print("data_matrix:", data_matrix.shape)
        print(f"dt: {dt:.6f} seconds")

    return PreparedCustomMotion(
        motion=motion,
        times=times,
        marker_names=marker_names,
        dimension_labels=dimension_labels,
        mean_pose=mean_pose,
        centred_motion=centred_motion,
        data_matrix=data_matrix,
        dt=dt,
    )


def default_custom_skeleton_path() -> Path:
    """Return where notebook 00 saves the custom skeleton by default."""
    return Path("/content/custom_skeleton.json") if "google.colab" in sys.modules else Path("custom_skeleton.json")


def load_custom_skeleton(
    skeleton_path,
    motion: np.ndarray,
    marker_names: list[str],
    mean_pose: np.ndarray,
    *,
    files=None,
) -> CustomSkeleton:
    """Load an optional notebook-00 skeleton for animation and analysis markers."""
    if files is None:
        try:
            from google.colab import files as colab_files
        except ImportError:
            colab_files = None
        files = colab_files

    marker_names = list(marker_names)
    if skeleton_path is None:
        print("No skeleton path provided, continuing without animation.")
        return CustomSkeleton(None, None, marker_names, marker_names)

    skeleton_path = Path(skeleton_path)
    if not skeleton_path.exists() and files is not None:
        print(f"Could not find {skeleton_path}. Upload custom_skeleton.json from notebook 00.")
        uploaded_files = files.upload()
        if uploaded_files:
            uploaded_name, uploaded_content = next(iter(uploaded_files.items()))
            skeleton_path = Path("/content") / uploaded_name if "google.colab" in sys.modules else Path(uploaded_name)
            skeleton_path.write_bytes(uploaded_content)

    if not skeleton_path.exists():
        print(f"No skeleton file found at {skeleton_path}, continuing without animation.")
        return CustomSkeleton(None, None, marker_names, marker_names)

    motion = np.asarray(motion)
    if motion.ndim != 3 or motion.shape[2] != 3:
        raise ValueError("Skeleton animation needs 3D motion shaped (frames, markers, 3).")

    skeleton_config = json.loads(skeleton_path.read_text())
    skeleton_marker_names = list(skeleton_config["marker_names"])
    if len(skeleton_marker_names) != motion.shape[1]:
        raise ValueError(
            "The skeleton marker count does not match `motion`. "
            "Check that your motion marker order matches notebook 00."
        )

    from morphing_birds import Animal3D, SkeletonDefinition

    skeleton = SkeletonDefinition.from_markers(
        skeleton_config["name"],
        skeleton_marker_names,
        body_sections=skeleton_config["body_sections"],
        analysis_exclude=skeleton_config["analysis_exclude"],
        marker_pairs=[tuple(pair) for pair in skeleton_config["marker_pairs"]],
        centre_markers=skeleton_config["centre_markers"],
    )
    base_pose = np.asarray(mean_pose)
    if base_pose.ndim == 3:
        base_pose = base_pose[0]
    animal = Animal3D(skeleton, data=base_pose)
    analysis_marker_names = list(getattr(skeleton, "analysis_markers"))

    print(f"Loaded skeleton from {skeleton_path}")
    print(f"Using {len(analysis_marker_names)} moving markers for DMD analysis.")
    return CustomSkeleton(animal, skeleton, skeleton_marker_names, analysis_marker_names)


def prepare_analysis_motion(
    motion: np.ndarray,
    times: np.ndarray,
    marker_names: list[str],
    *,
    animal=None,
    analysis_marker_names: list[str] | None = None,
) -> PreparedCustomMotion:
    """Prepare the DMD input, respecting skeleton analysis exclusions when present."""
    if animal is None:
        return prepare_custom_motion(motion, times, marker_names=marker_names)

    analysis_motion = animal.get_analysis_data(motion)
    if analysis_marker_names is None:
        analysis_marker_names = [f"marker_{i}" for i in range(analysis_motion.shape[1])]
    return prepare_custom_motion(analysis_motion, times, marker_names=analysis_marker_names)


def expand_analysis_motion(
    analysis_motion: np.ndarray,
    reference_motion: np.ndarray,
    marker_names: list[str],
    analysis_marker_names: list[str],
) -> np.ndarray:
    """Insert analysis-marker motion back into a full-marker array for animation."""
    expanded = np.array(reference_motion, copy=True)
    analysis_motion = np.asarray(analysis_motion)
    if expanded.shape[0] != analysis_motion.shape[0]:
        raise ValueError("analysis_motion and reference_motion must have the same number of frames.")
    if expanded.shape[2] != analysis_motion.shape[2]:
        raise ValueError("analysis_motion and reference_motion must have the same coordinate dimension.")

    marker_lookup = {name: index for index, name in enumerate(marker_names)}
    analysis_indices = [marker_lookup[name] for name in analysis_marker_names]
    expanded[:, analysis_indices, :] = analysis_motion
    return expanded
