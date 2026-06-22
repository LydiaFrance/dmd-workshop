"""Notebook setup helpers for the Animal DMD workshop."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


REPO_URL = "https://github.com/LydiaFrance/dmd-workshop.git"
DEFAULT_BRANCH = "main"


def _run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def configure_notebook() -> None:
    """Set Colab-friendly plot rendering and tidy NumPy printing.

    Keeps notebook import cells short: this hides the plotly renderer, inline
    figure format, and print-option plumbing behind one call.
    """
    import numpy as np

    np.set_printoptions(precision=3, suppress=True)

    try:
        import plotly.io as pio

        pio.renderers.default = "colab" if "google.colab" in sys.modules else "notebook_connected"
    except Exception:
        pass

    try:
        # Crisp static figures inline: all workshop plots are line/bar (no raster),
        # so svg is sharpest. Animations (jshtml) and Plotly are unaffected.
        from matplotlib_inline.backend_inline import set_matplotlib_formats

        set_matplotlib_formats("svg")
    except Exception:
        pass


def setup_workshop(branch: str | None = None) -> Path:
    """Prepare workshop files and data, returning the notebook directory."""
    branch = branch or os.environ.get("ANIMAL_DMD_BRANCH", DEFAULT_BRANCH)
    root = Path("/content/dmd-workshop") if "google.colab" in sys.modules else Path(__file__).resolve().parents[2]
    notebooks = root / "notebooks"
    data_dir = root / "data" / "hawk"
    spider_dir = root / "data" / "spider"

    if "google.colab" in sys.modules and not root.exists():
        print("Downloading workshop files...")
        _run(["git", "clone", "--depth", "1", "--branch", branch, REPO_URL, str(root)])

    required_files = [
        data_dir / "mean_hawk_shape.csv",
        data_dir / "processed" / "toothless_flapping_9m_avg.npz",
        spider_dir / "mean_spider_shape_carolina.csv",
        spider_dir / "spider_walking.npz",
        notebooks / "00_build_your_own_animal.ipynb",
        notebooks / "01_intro_dmd.ipynb",
        notebooks / "02_bird_flight_dmd.ipynb",
        notebooks / "03_custom_dmd.ipynb",
    ]
    missing = [path for path in required_files if not path.exists()]
    if missing:
        missing_list = "\n".join(f"- {path}" for path in missing)
        raise FileNotFoundError(f"Workshop setup is incomplete:\n{missing_list}")

    os.environ["ANIMAL_DMD_DATA_DIR"] = str(data_dir)
    os.environ["ANIMAL_DMD_SPIDER_DIR"] = str(spider_dir)
    if str(root / "src") not in sys.path:
        sys.path.insert(0, str(root / "src"))

    configure_notebook()

    os.chdir(notebooks)
    print("Ready. Workshop files are loaded.")
    return notebooks
