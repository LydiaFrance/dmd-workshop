"""Small plotting helpers for the Animal DMD workshop notebooks."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from .toy import TOY_BODY_LINES

MARKER_TRACE_COLOURS = {
    "left": "#7b3294",
    "body": "#c51b7d",
    "right": "#de77ae",
}

SVD_COMPONENT_COLOURS = ["#f2d21b", "#c9de2f", "#9bd743", "#69c94f"]
SVD_OTHER_BAR_COLOUR = "#edf4c7"


def hold_last_frame(motion: np.ndarray, n_total: int) -> np.ndarray:
    """Pad motion by repeating the last frame until ``n_total`` frames."""
    motion = np.asarray(motion)
    n_obs = motion.shape[0]
    if n_total <= n_obs:
        return motion[:n_total]
    pad = np.repeat(motion[-1:], n_total - n_obs, axis=0)
    return np.concatenate([motion, pad], axis=0)


def draw_toy_shape(
    ax,
    points: np.ndarray,
    *,
    colour: str = "0.2",
    label: str | None = None,
    alpha: float = 1.0,
    linewidth: float = 2,
) -> None:
    """Draw the simple 2D stick body used in the intro notebook."""
    for i, j in TOY_BODY_LINES:
        ax.plot(
            [points[i, 0], points[j, 0]],
            [points[i, 1], points[j, 1]],
            color=colour,
            alpha=alpha,
            linewidth=linewidth,
        )
    ax.scatter(points[:, 0], points[:, 1], color=colour, s=28, label=label, alpha=alpha)


def style_toy_axis(ax, title: str) -> None:
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-1.45, 1.45)
    ax.set_ylim(-0.9, 1.05)
    ax.set_title(title)
    ax.set_xlabel("x")
    ax.set_ylabel("y")


def phase_frames(frequency_hz: float, dt: float, phases=(0.0, 0.25, 0.5)) -> list[int]:
    """Frame indices at matched phase fractions of an oscillator cycle."""
    period_frames = 1.0 / (frequency_hz * dt)
    return [int(round(phase * period_frames)) for phase in phases]


def plot_toy_components(
    mean_shape,
    left_arm_only,
    shared_motion_only,
    right_arm_only,
    *,
    dt: float,
    steady_hz: float,
    shared_hz: float,
    decay_hz: float,
):
    """Show the built-in toy motions without exposing shape code."""
    fig, ax = plt.subplots(1, 3, figsize=(15, 4), sharex=True, sharey=True)
    left_frames = phase_frames(steady_hz, dt)
    shared_frames = phase_frames(shared_hz, dt)
    right_frames = phase_frames(decay_hz, dt)

    for frame, alpha in zip(left_frames, [0.95, 0.55, 0.30], strict=True):
        draw_toy_shape(ax[0], left_arm_only[frame], colour="tab:blue", alpha=alpha)
    draw_toy_shape(ax[0], mean_shape, colour="0.75", label="mean shape", alpha=0.8, linewidth=1)
    style_toy_axis(ax[0], f"Left arm: steady {steady_hz:g} Hz wave")

    for frame, alpha in zip(shared_frames, [0.95, 0.55, 0.30], strict=True):
        draw_toy_shape(ax[1], shared_motion_only[frame], colour="tab:green", alpha=alpha)
    draw_toy_shape(ax[1], mean_shape, colour="0.75", label="mean shape", alpha=0.8, linewidth=1)
    style_toy_axis(ax[1], f"Shared: coordinated {shared_hz:g} Hz wave")

    for frame, alpha in zip(right_frames, [0.95, 0.55, 0.30], strict=True):
        draw_toy_shape(ax[2], right_arm_only[frame], colour="tab:orange", alpha=alpha)
    draw_toy_shape(ax[2], mean_shape, colour="0.75", label="mean shape", alpha=0.8, linewidth=1)
    style_toy_axis(ax[2], f"Right arm: decaying {decay_hz:g} Hz wave")

    fig.suptitle("The simple motions we built in")
    plt.tight_layout()
    return fig, ax


def plot_combined_toy_motion(
    mean_shape,
    motion,
    *,
    dt: float,
    snapshot_seconds=(0.0, 0.08, 0.16),
):
    """Show the full toy motion before splitting it into components."""
    fig, ax = plt.subplots(figsize=(5, 4))
    frames = [min(int(round(seconds / dt)), motion.shape[0] - 1) for seconds in snapshot_seconds]
    for frame, alpha in zip(frames, [0.95, 0.55, 0.30], strict=True):
        draw_toy_shape(ax, motion[frame], colour="black", alpha=alpha)
    draw_toy_shape(ax, mean_shape, colour="0.75", label="mean shape", alpha=0.8, linewidth=1)
    style_toy_axis(ax, "Combined toy motion")
    plt.tight_layout()
    return fig, ax


def plot_reconstructed_pair_motions(
    mean_shape,
    reconstructed_pair_motions: dict[str, np.ndarray],
    *,
    times: np.ndarray,
    built_in_waveforms: dict[str, np.ndarray],
    trace_marker_indices: list[int],
    phase_frequencies_hz: list[float],
    dmd_frequencies_hz: list[float],
    dt: float,
    colours: list[str],
):
    """Show reconstructed DMD pairs and their time behaviour."""
    n_pairs = len(reconstructed_pair_motions)
    fig, axes = plt.subplots(
        2,
        n_pairs,
        figsize=(15, 6.0),
        sharex="row",
        gridspec_kw={"height_ratios": [3.0, 1.35]},
    )

    for mode_axis, waveform_axis, (label, pair_motion), built_in_waveform, marker_index, phase_hz, dmd_hz, colour in zip(
        axes[0],
        axes[1],
        reconstructed_pair_motions.items(),
        built_in_waveforms.values(),
        trace_marker_indices,
        phase_frequencies_hz,
        dmd_frequencies_hz,
        colours,
        strict=True,
    ):
        frames = phase_frames(phase_hz, dt)
        for frame, alpha in zip(frames, [0.95, 0.55, 0.30], strict=True):
            draw_toy_shape(mode_axis, pair_motion[frame], colour=colour, alpha=alpha)
        draw_toy_shape(mode_axis, mean_shape, colour="0.75", label="mean shape", alpha=0.8, linewidth=1)
        style_toy_axis(mode_axis, label)

        pair_waveform = pair_motion[:, marker_index, 1]
        waveform_times = times[-pair_waveform.size :]
        built_in_aligned = built_in_waveform[-pair_waveform.size :]
        waveform_axis.plot(waveform_times, built_in_aligned, color="0.65", linestyle="--", linewidth=1.5, label="built-in")
        waveform_axis.plot(waveform_times, pair_waveform, color=colour, linewidth=1.8, label=f"DMD {dmd_hz:.2f} Hz")
        waveform_axis.set_xlim(waveform_times[0], waveform_times[-1])
        waveform_axis.grid(True, alpha=0.2)
        waveform_axis.legend(fontsize="x-small", loc="upper right")

    axes[1, 0].set_ylabel("mode trace")
    axes[1, 1].set_xlabel("Time (s)")

    fig.suptitle("DMD pair reconstructions")
    plt.tight_layout()
    return fig, axes


def plot_marker_traces(times, traces: dict[str, np.ndarray], *, title: str, ylabel: str = "Coordinate value"):
    fig, ax = plt.subplots(figsize=(8, 3))
    colours = list(MARKER_TRACE_COLOURS.values())
    for colour, (label, signal) in zip(colours, traces.items(), strict=True):
        ax.plot(times, signal, color=colour, label=label)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(fontsize="small")
    return fig, ax


def plot_reconstruction_marker_traces(
    times,
    measured_traces: dict[str, np.ndarray],
    reconstructed_traces: dict[str, np.ndarray],
    *,
    title: str,
    ylabel: str = "Coordinate value",
):
    """Overlay measured marker traces and the full DMD reconstruction."""
    fig, ax = plt.subplots(figsize=(8, 3))
    colours = list(MARKER_TRACE_COLOURS.values())

    for colour, (label, measured_signal), reconstructed_signal in zip(
        colours,
        measured_traces.items(),
        reconstructed_traces.values(),
        strict=True,
    ):
        ax.plot(times, measured_signal, color=colour, linewidth=2, label=f"{label}: data")
        ax.plot(times, reconstructed_signal, color=colour, linestyle="--", linewidth=1.5, label=f"{label}: DMD")

    ax.set_xlabel("Time (s)")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(fontsize="x-small", ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.22), frameon=False)
    plt.tight_layout()
    return fig, ax


def plot_dmd_pair_traces(
    times,
    measured_trace: np.ndarray,
    pair_traces: dict[int, np.ndarray],
    *,
    pair_frequencies_hz: np.ndarray,
    trace_label: str,
    ylabel: str = "Coordinate value",
):
    """Compare one measured marker trace with selected DMD pair reconstructions."""
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(times, measured_trace, color="0.75", linewidth=2, label="data")

    for pair_index, pair_trace in pair_traces.items():
        ax.plot(
            times,
            pair_trace,
            linewidth=1.7,
            label=f"pair {pair_index}: {pair_frequencies_hz[pair_index]:.2f} Hz",
        )

    ax.set_xlabel("Time (s)")
    ax.set_ylabel(ylabel)
    ax.set_title(f"Selected DMD pair traces: {trace_label}")
    ax.legend(fontsize="small")
    plt.tight_layout()
    return fig, ax


def plot_power_spectrum(ax, frequencies_hz: np.ndarray, power: np.ndarray, label: str):
    """Plot a precomputed FFT power spectrum."""
    ax.plot(frequencies_hz, power, label=label)


def plot_trace_fft_comparison(
    frequencies_hz: np.ndarray,
    trace_power: dict[str, np.ndarray],
    *,
    true_frequencies: dict[str, tuple[float, str]],
):
    """Show how FFT results change with the chosen marker trace."""
    fig, axes = plt.subplots(len(trace_power), 1, figsize=(8, 2 * len(trace_power)), sharex=True, sharey=True)
    axes = np.atleast_1d(axes)

    for axis, (trace_label, power) in zip(axes, trace_power.items(), strict=True):
        normalised_power = power / power.max()
        axis.plot(frequencies_hz, normalised_power, color="0.2")
        for frequency, colour in true_frequencies.values():
            axis.axvline(frequency, color=colour, linestyle="--", alpha=0.75)
        axis.set_ylabel(trace_label)
        axis.set_xlim(0, 10)
        axis.set_ylim(-0.05, 1.1)

    for frequency_label, (_, colour) in true_frequencies.items():
        axes[0].plot([], [], color=colour, linestyle="--", label=frequency_label)
    axes[0].set_title("FFT depends on which trace we choose")
    axes[0].legend(loc="upper right", ncol=len(true_frequencies))
    axes[-1].set_xlabel("Frequency (Hz)")
    fig.supylabel("Normalised power")
    plt.tight_layout()
    return fig, axes


def plot_short_clip_fft_limit(
    full_clip_fft: tuple[np.ndarray, np.ndarray],
    short_clip_fft: tuple[np.ndarray, np.ndarray],
    *,
    full_duration_seconds: float,
    short_duration_seconds: float,
    marked_frequencies: dict[str, tuple[float, str]],
):
    """Compare FFT resolution for a full clip and a short clip."""
    clips = {
        f"full {full_duration_seconds:g} s clip: bin spacing {1 / full_duration_seconds:.2f} Hz": (
            full_clip_fft[0],
            full_clip_fft[1],
        ),
        f"short {short_duration_seconds:g} s clip: bin spacing {1 / short_duration_seconds:.2f} Hz": (
            short_clip_fft[0],
            short_clip_fft[1],
        ),
    }

    fig, axes = plt.subplots(2, 1, figsize=(8, 4.8), sharex=True, sharey=True)
    for axis, (title, (frequencies_hz, power)) in zip(axes, clips.items(), strict=True):
        normalised_power = power / power.max()
        axis.plot(frequencies_hz, normalised_power, color="0.2", marker="o", markersize=3)
        for frequency, colour in marked_frequencies.values():
            axis.axvline(frequency, color=colour, linestyle="--", alpha=0.75)
        axis.set_title(title)
        axis.set_ylabel("Normalised power")
        axis.set_xlim(0, 8)
        axis.set_ylim(-0.05, 1.1)

    for frequency_label, (_, colour) in marked_frequencies.items():
        axes[0].plot([], [], color=colour, linestyle="--", label=frequency_label)
    axes[0].legend(loc="upper right")
    axes[-1].set_xlabel("Frequency (Hz)")
    plt.tight_layout()
    return fig, axes


def plot_svd_summary(times, explained, scores, *, n_bars: int = 8, n_scores: int = 4, title: str):
    fig, ax = plt.subplots(1, 2, figsize=(10, 3))
    n_coloured = min(n_scores, len(SVD_COMPONENT_COLOURS), n_bars)
    bar_colours = [
        SVD_COMPONENT_COLOURS[component] if component < n_coloured else SVD_OTHER_BAR_COLOUR
        for component in range(n_bars)
    ]
    ax[0].bar(
        np.arange(1, n_bars + 1),
        explained[:n_bars] * 100,
        color=bar_colours,
        edgecolor="white",
        linewidth=0.8,
    )
    ax[0].set_xlabel("SVD component")
    ax[0].set_ylabel("Variance explained (%)")
    ax[0].set_title(title)

    for component in range(min(n_scores, len(SVD_COMPONENT_COLOURS))):
        ax[1].plot(
            times,
            scores[component],
            label=f"component {component + 1}",
            color=SVD_COMPONENT_COLOURS[component],
            linewidth=1.8,
        )
    ax[1].set_xlabel("Time (s)")
    ax[1].set_title("PCA/SVD time scores")
    ax[1].legend(ncol=2)
    plt.tight_layout()
    return fig, ax


def _svd_component_shapes(
    mean_shape,
    spatial_patterns,
    singular_values,
    temporal_scores,
    *,
    n_components: int,
    score_scale: float = 2.0,
):
    """Return mean +/- each SVD component in marker-space coordinates."""
    base_shape = np.asarray(mean_shape)
    if base_shape.ndim == 3:
        base_shape = base_shape[0]

    component_scores = singular_values[:, None] * temporal_scores
    n_components = min(n_components, spatial_patterns.shape[1])
    shapes = []
    for component in range(n_components):
        direction = spatial_patterns[:, component].reshape(base_shape.shape)
        amount = score_scale * np.std(component_scores[component])
        shapes.append(
            (
                base_shape - amount * direction,
                base_shape,
                base_shape + amount * direction,
            )
        )
    return shapes


def plot_toy_svd_component_shapes(
    mean_shape,
    spatial_patterns,
    singular_values,
    temporal_scores,
    *,
    n_components: int = 3,
):
    """Show what the leading SVD spatial components do to the toy shape."""
    component_shapes = _svd_component_shapes(
        mean_shape,
        spatial_patterns,
        singular_values,
        temporal_scores,
        n_components=n_components,
    )
    fig, axes = plt.subplots(1, len(component_shapes), figsize=(4.5 * len(component_shapes), 4), sharex=True, sharey=True)
    axes = np.atleast_1d(axes)

    for component, (axis, (negative, mean, positive)) in enumerate(zip(axes, component_shapes, strict=True)):
        colour = SVD_COMPONENT_COLOURS[component % len(SVD_COMPONENT_COLOURS)]
        draw_toy_shape(axis, negative, colour=colour, alpha=0.35, linewidth=1.5)
        draw_toy_shape(axis, mean, colour="0.75", alpha=0.75, linewidth=1)
        draw_toy_shape(axis, positive, colour=colour, alpha=0.95, linewidth=2.2)
        style_toy_axis(axis, f"SVD component {component + 1}")

    fig.suptitle("Spatial directions found by SVD")
    plt.tight_layout()
    return fig, axes


def _plot_hawk_shape_xz(axis, points, marker_names, *, colour, alpha, linestyle="-", linewidth=2.0):
    """Draw a simple x-z projection of the hawk analysis markers."""
    marker_index = {name: i for i, name in enumerate(marker_names)}
    wing_chains = [
        ["left_wingtip", "left_primary", "left_secondary"],
        ["right_wingtip", "right_primary", "right_secondary"],
    ]
    for chain in wing_chains:
        if all(name in marker_index for name in chain):
            indices = [marker_index[name] for name in chain]
            axis.plot(
                points[indices, 0],
                points[indices, 2],
                color=colour,
                alpha=alpha,
                linestyle=linestyle,
                linewidth=linewidth,
            )
    if {"left_tailtip", "right_tailtip"}.issubset(marker_index):
        indices = [marker_index["left_tailtip"], marker_index["right_tailtip"]]
        axis.plot(
            points[indices, 0],
            points[indices, 2],
            color=colour,
            alpha=alpha,
            linestyle=linestyle,
            linewidth=linewidth,
        )
    axis.scatter(points[:, 0], points[:, 2], color=colour, alpha=alpha, s=28)


def plot_hawk_svd_component_shapes(
    marker_names,
    mean_pose,
    spatial_patterns,
    singular_values,
    temporal_scores,
    *,
    n_components: int = 3,
):
    """Show the leading SVD spatial components as hawk x-z shape changes."""
    component_shapes = _svd_component_shapes(
        mean_pose,
        spatial_patterns,
        singular_values,
        temporal_scores,
        n_components=n_components,
    )
    fig, axes = plt.subplots(1, len(component_shapes), figsize=(4.5 * len(component_shapes), 4), sharex=True, sharey=True)
    axes = np.atleast_1d(axes)

    for component, (axis, (negative, mean, positive)) in enumerate(zip(axes, component_shapes, strict=True)):
        colour = SVD_COMPONENT_COLOURS[component % len(SVD_COMPONENT_COLOURS)]
        _plot_hawk_shape_xz(axis, negative, marker_names, colour=colour, alpha=0.35, linestyle="--", linewidth=1.5)
        _plot_hawk_shape_xz(axis, mean, marker_names, colour="0.75", alpha=0.75, linewidth=1.0)
        _plot_hawk_shape_xz(axis, positive, marker_names, colour=colour, alpha=0.95, linewidth=2.2)
        axis.set_aspect("equal", adjustable="box")
        axis.set_title(f"SVD component {component + 1}")
        axis.set_xlabel("x")
        axis.grid(True, alpha=0.2)

    axes[0].set_ylabel("z")
    fig.suptitle("Spatial directions found by SVD")
    plt.tight_layout()
    return fig, axes


def animate_hawk_svd_mode(
    hawk,
    mean_pose,
    spatial_patterns,
    singular_values,
    temporal_scores,
    *,
    component: int = 1,
    n_frames: int = 25,
    score_scale: float = 2.0,
):
    """Animate one hawk SVD component as a +/- score sweep."""
    import morphing_birds as mb

    if n_frames < 3:
        raise ValueError("n_frames must be at least 3 for an out-and-back animation.")

    component_index = component - 1
    if component_index < 0 or component_index >= spatial_patterns.shape[1]:
        raise ValueError("component must be between 1 and the number of SVD components.")

    base_shape = np.asarray(mean_pose)
    if base_shape.ndim == 3:
        base_shape = base_shape[0]

    component_scores = singular_values[:, None] * temporal_scores
    score_amount = score_scale * np.std(component_scores[component_index])
    rising = np.linspace(-score_amount, score_amount, n_frames // 2 + 1)
    falling = np.linspace(score_amount, -score_amount, n_frames - rising.size + 1)[1:]
    score_sweep = np.concatenate([rising, falling])

    direction = spatial_patterns[:, component_index].reshape(base_shape.shape)
    mode_frames = base_shape[None, :, :] + score_sweep[:, None, None] * direction[None, :, :]

    fig = mb.animate_plotly(
        hawk,
        keypoints_frames=mode_frames,
        colour=SVD_COMPONENT_COLOURS[component_index % len(SVD_COMPONENT_COLOURS)],
        score_vals=score_sweep,
        axes_visible=True,
    )
    fig.update_layout(title=f"SVD component {component}: +/- {score_scale:g} SD score sweep")
    return fig


def plot_unit_circle_eigenvalues(per_step_eigenvalues: np.ndarray):
    """Plot DMD eigenvalues on the discrete-time unit circle."""
    values = np.asarray(per_step_eigenvalues)
    fig, ax = plt.subplots(1, 2, figsize=(9, 4.2))
    theta = np.linspace(0, 2 * np.pi, 400)
    radii = np.abs(values)

    ax[0].plot(np.cos(theta), np.sin(theta), color="0.75", linewidth=1, label="unit circle")
    ax[0].scatter(values.real, values.imag, s=85, marker="x", linewidths=2.5)
    ax[0].set_aspect("equal", adjustable="box")
    ax[0].set_xlabel("real")
    ax[0].set_ylabel("imaginary")
    ax[0].set_title("Full unit circle")

    ax[1].axvline(1.0, color="0.75", linewidth=1.5, label="unit radius")
    ax[1].scatter(radii, values.imag, s=85, marker="x", linewidths=2.5)
    ax[1].set_xlabel("radius from origin")
    ax[1].set_ylabel("imaginary")
    ax[1].set_title("Zoomed radius")
    ax[1].grid(True, alpha=0.25)

    for i, value in enumerate(values):
        ax[0].text(value.real + 0.015, value.imag + 0.015, str(i))
        ax[1].text(radii[i] + 0.0005, value.imag + 0.01, str(i), fontsize=9)

    radius_margin = max(0.002, 0.25 * np.ptp(radii))
    ax[1].set_xlim(radii.min() - radius_margin, max(1.0, radii.max()) + radius_margin)
    ax[1].set_ylim(values.imag.min() - 0.08, values.imag.max() + 0.08)
    ax[0].set_xlim(-1.1, 1.1)
    ax[0].set_ylim(-1.1, 1.1)
    ax[0].legend(loc="upper left")
    ax[1].legend(loc="upper right")
    fig.suptitle("DMD eigenvalues per time step")
    plt.tight_layout()
    return fig, ax


def plot_hawk_wingtip_trace_comparison(
    trace_data: dict[str, tuple[np.ndarray, np.ndarray]],
    *,
    title: str,
    ylabel: str = "Wingtip z (m)",
    end_time: float | None = None,
    styles: dict[str, dict] | None = None,
):
    """Compare one hawk wingtip coordinate across fitted or generated motions."""
    fig, ax = plt.subplots(figsize=(10, 3))
    colours = ["black", "crimson", "royalblue", "darkorange", "seagreen"]
    styles = styles or {}

    for i, (label, (trace_times, trace_values)) in enumerate(trace_data.items()):
        plot_kwargs = {
            "color": colours[i % len(colours)],
            "linewidth": 1.5,
            "label": label,
        }
        plot_kwargs.update(styles.get(label, {}))
        ax.plot(trace_times, trace_values, **plot_kwargs)

    if end_time is not None:
        ax.axvline(end_time, color="grey", linestyle=":", label="End of training data")

    ax.set_xlabel("Time (s)")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()
    plt.tight_layout()
    return fig, ax


def print_dmd_summary(
    growth_per_s: np.ndarray,
    frequency_hz: np.ndarray,
    reconstruction_rmse: float,
    *,
    label: str = "reconstruction",
) -> None:
    for i, (growth, frequency) in enumerate(zip(growth_per_s, frequency_hz, strict=True)):
        print(
            f"mode {i}: growth={growth:7.3f} per s, "
            f"frequency={frequency:7.2f} Hz"
        )
    print(f"{label} RMSE: {reconstruction_rmse:.6f}")
