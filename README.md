# Finding Dynamic Modes in Natural Motion

These are the workshop materials for learning Dynamic Mode Decomposition (DMD)
from animal keypoint data.

We start with a tiny synthetic example, then repeat the same workflow on hawk
flight. The aim is to make the DMD vocabulary concrete before the eigenvalue
plots and complex modes appear in the real animal data.

<p align="center">
  <img src="https://raw.githubusercontent.com/LydiaFrance/BirdDMD/main/notebooks/figures/DMD_figure1.png" width="720" alt="DMD summary figure for hawk flapping modes">
</p>

## Start here

| Path | Notebook | Use it for |
|------|----------|------------|
| Main route | [01 Intro DMD](notebooks/01_intro_dmd.ipynb) | A toy animal with three known motions: steady, shared, and decaying. |
| Main route | [02 Bird Flight DMD](notebooks/02_bird_flight_dmd.ipynb) | The same PCA/SVD -> FFT -> DMD workflow on public hawk keypoints. |
| Optional | [00 Build Your Own Animal](notebooks/00_build_your_own_animal.ipynb) | A separate setup notebook if you brought your own keypoint data. |
| Optional | [03 Custom DMD](notebooks/03_custom_dmd.ipynb) | A higher-confidence template for running DMD on your own non-hawk data. |

[![Open intro DMD in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/LydiaFrance/dmd-workshop/blob/main/notebooks/01_intro_dmd.ipynb)

[![Open bird flight DMD in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/LydiaFrance/dmd-workshop/blob/main/notebooks/02_bird_flight_dmd.ipynb)

[![Open custom animal setup in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/LydiaFrance/dmd-workshop/blob/main/notebooks/00_build_your_own_animal.ipynb)

[![Open custom DMD in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/LydiaFrance/dmd-workshop/blob/main/notebooks/03_custom_dmd.ipynb)

No local installation is needed for the workshop route. Colab installs the small
Python dependencies inside the notebook runtime.

## What we are trying to make less mysterious

By the end of the main route, the DMD output should feel less like a collection
of magic numbers. The key words are:

- **state vector** - one flattened frame of marker coordinates
- **mode** - a coordinated spatial pattern
- **eigenvalue angle** - oscillation frequency
- **eigenvalue radius** - growth or decay
- **conjugate pair** - two complex DMD modes that combine into one real oscillation

We also compare DMD with two familiar tools:

- **PCA/SVD** finds compact spatial directions, but does not label them with
  frequencies.
- **FFT** finds frequencies in a chosen trace, but does not by itself recover a
  full spatial mode.

## Workshop flow

### 1. Intro DMD

The first notebook uses dummy data where we know the answer. The left arm waves
at 2 Hz with constant amplitude, a shared 3 Hz motion coordinates both sides,
and the right arm waves at 5 Hz while decaying. This gives us a readable first
encounter with the unit circle: steady oscillations stay on it, and the decaying
oscillation sits inside it.

### 2. Bird Flight DMD

The second notebook repeats the same analysis on a small Toothless hawk dataset.
We load flapping keypoints, animate the raw motion, compare PCA/SVD and FFT,
fit DMD, animate a mode pair, remove/recombine modes, and extend the motion
forward in time.

<p align="center">
  <img src="https://raw.githubusercontent.com/LydiaFrance/BirdDMD/main/notebooks/figures/01_full_reconstruction_compare.gif" width="360" alt="Original and DMD reconstructed hawk flapping motion">
  <img src="https://raw.githubusercontent.com/LydiaFrance/BirdDMD/main/notebooks/figures/07_synthetic_flight.gif" width="360" alt="Generated hawk flapping motion from DMD">
</p>

### 3. Bring Your Own Animal

The custom-animal notebook is separate on purpose. Most people can ignore it
during the main workshop. Use it if you have your own data shaped like:

```text
(frames, markers, xyz)
```

It helps you define marker names, body sections, left/right pairs, display-only
markers, and a first animation before trying DMD.

## Data

Included teaching files:

- `data/hawk/mean_hawk_shape.csv` - mean hawk shape for `morphing_birds`
- `data/hawk/processed/toothless_flapping_9m_avg.npz` - the clean first tutorial
  dataset
- `data/hawk/processed/toothless_control_9m_avg.npz` and
  `toothless_rightturn_obstacle_avg.npz` - small public comparison datasets

Marker arrays are shaped `(n_frames, n_markers, 3)` and use backpack-relative
coordinates in metres. See [data/hawk/README.md](data/hawk/README.md) for the
data dictionary.

## Related Project

This workshop is adapted from my longer
[BirdDMD](https://github.com/LydiaFrance/BirdDMD) research notebooks and docs.
BirdDMD contains the manuscript analysis, API documentation, and more advanced
notebooks on reconstruction accuracy, doubled-frequency modes, full-flight
transitions, and generative forecasts.

## Data scope

This is a compact teaching package. It contains the notebooks and small hawk
data files needed for the workshop route above.
