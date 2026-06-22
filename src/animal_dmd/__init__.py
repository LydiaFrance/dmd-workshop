"""Comparative DMD analysis across animal species."""

from .custom import (
    CustomSkeleton,
    PreparedCustomMotion,
    default_custom_skeleton_path,
    expand_analysis_motion,
    load_custom_skeleton,
    prepare_analysis_motion,
    prepare_custom_motion,
)
from .data import load_hawk_motion
try:
    from .dmd import reconstruct_known_pairs
except ModuleNotFoundError as exc:
    if exc.name != "birddmd":
        raise

    def reconstruct_known_pairs(dmd_result, known_frequencies_hz: dict[str, float]) -> tuple:  # noqa: ARG001 - signature mirrors real impl; stub only raises
        raise ModuleNotFoundError(
            "reconstruct_known_pairs requires BirdDMD. Install the workshop dependencies first."
        ) from exc

from .plots import (
    animate_hawk_svd_mode,
    draw_toy_shape,
    hold_last_frame,
    phase_frames,
    plot_combined_toy_motion,
    plot_dmd_pair_traces,
    plot_hawk_svd_component_shapes,
    plot_hawk_wingtip_trace_comparison,
    plot_marker_traces,
    plot_power_spectrum,
    plot_reconstructed_pair_motions,
    plot_reconstruction_marker_traces,
    plot_short_clip_fft_limit,
    plot_svd_summary,
    plot_toy_components,
    plot_trace_fft_comparison,
    plot_toy_svd_component_shapes,
    plot_unit_circle_eigenvalues,
    plot_upsampling_comparison,
    print_dmd_summary,
)
from .setup import setup_workshop
from .toy import TOY_MARKER_NAMES, make_toy_motion

__all__ = [
    "PreparedCustomMotion",
    "CustomSkeleton",
    "TOY_MARKER_NAMES",
    "animate_hawk_svd_mode",
    "draw_toy_shape",
    "default_custom_skeleton_path",
    "expand_analysis_motion",
    "hold_last_frame",
    "load_hawk_motion",
    "load_custom_skeleton",
    "make_toy_motion",
    "phase_frames",
    "plot_combined_toy_motion",
    "plot_dmd_pair_traces",
    "plot_hawk_svd_component_shapes",
    "plot_hawk_wingtip_trace_comparison",
    "plot_marker_traces",
    "plot_power_spectrum",
    "plot_reconstructed_pair_motions",
    "plot_reconstruction_marker_traces",
    "plot_short_clip_fft_limit",
    "plot_svd_summary",
    "plot_toy_components",
    "plot_trace_fft_comparison",
    "plot_toy_svd_component_shapes",
    "plot_unit_circle_eigenvalues",
    "plot_upsampling_comparison",
    "print_dmd_summary",
    "prepare_analysis_motion",
    "prepare_custom_motion",
    "reconstruct_known_pairs",
    "setup_workshop",
]
