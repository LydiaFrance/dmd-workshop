# Data dictionary
Three datasets, all from **Toothless** (BirdID 4 in BirdDMD, the bird with the most/best data: 477 sequences, ~60k frames in the full cohort).
## Coordinate space & units
- **Marker coordinates are backpack-relative, in physical units (metres).** Each marker is given relative to the backpack position, so the markers describe the bird's _shape/posture_, while the backpack global trajectory (below) describes _where it was_. The pipeline is BirdDMD `BilateralNoRot`: markers are paired left/right bilaterally, but `NoRot` **means no rotation correction is applied** — the body is _not_ de-rotated into a fixed frame. Values sit at roughly ±0.5 around the centre of the hawk.
  
- As the bird pitches up into the landing flare, the tail and wings swing relative to the backpack. You will see clear motion in marker z — e.g. `tailtip` z falls as `body_pitch` rises (corr ≈ −0.9 in the raw flight), and the wingtips span ~0.8 m in z.
  
- `times` are in **seconds**. Frames are sampled at **200 Hz** (0.005 s steps). Averaged datasets are time-binned at 0.005 s; the raw dataset keeps original frame timing (uneven where gaps occur).
  
- **Axis order** for every `markers` array: `(number of frames, marker number, xyz dims)`.
  
## Common fields in every file
- `marker_names` (8,) marker labels below
  
- `marker_columns` (24,) flat `<marker>_<axis>` names
  
- `axes` (3,) `["x","y","z"]`
  
## Marker layout (8 bilateral markers)
These markers are from different feathers on the wings and tail. The markers on the wing are wingtip, primary (a marker in the middle of the hand-wing) and secondary (on the trailing edge of the wing).

Index order in `marker_names` and axis 1 of `markers`:

```
0 left_wingtip     1 right_wingtip
2 left_primary     3 right_primary
4 left_secondary   5 right_secondary
6 left_tailtip     7 right_tailtip
```

(`marker_columns` also stores the flat 24-name ordering: `<marker>_<x|y|z>`.)
## Flight trajectory -- 2D and 3D both provided
The bird's path through the room is given in **two equivalent forms** so each collaborator can take the one they need. They describe the same flight:

- **3D (world frame):** `backpack_global_x`, `backpack_global_y`, `backpack_global_z` the backpack position in metres. A backpack is an approximation for the centre of mass. `x` is lateral, `y` is along the approach, `z` is vertical. Use this for full 3D trajectory work; the lateral `x` carries the turn signal (it spans +0.17→+0.78 m in the right-turn dataset, ~0 in the straight flights).
  
- **2D:** `HorzDistance` and `VertDistance` a horizontal-plus-height view for 2D trajectory work.
  
  - `HorzDistance` **= √(**`global_x`**² +** `global_y`**²)** horizontal-plane distance to the perch (perch at 0; decreases through the flight). If lateral/turn detail is needed use the 3D form.
    
  - `VertDistance` **≡** `global_z` identical to the global vertical (height). Provided as a separate name only for convenience. (floor at 0)
    
- _Averaging caveat:_ in the averaged files `HorzDistance` is binned directly, so it ≈ √(x̄²+ȳ²) but is not bit-identical (the mean of a magnitude ≠ the magnitude of the means). In the raw flight they match exactly.
  
- _Noise caveat (averaged files):_ the global `x/y/z` trajectory in the two averaged datasets is noisy, because it is averaged across many flights that did not follow identical paths through the room. Treat the averaged global trajectory as indicative, not exact. Use the raw flight if you need a clean single-flight path.
  
- `body_pitch` body pitch angle in **degrees**. `0°` = body level (tail in line with the nose, horizontal); `90°` = nose straight up, tail directly underneath. Rises through the approach as the bird pitches up into the landing flare.
  
## Origins & time reference
- `time = 0` **is the take-off jump.** This is a very clean, sharp signal in the original data (the launch impulse), so it makes a reliable time origin. (`times` can therefore be slightly negative just before the jump — the raw flight starts at −0.045 s.)
  
- `HorzDistance = 0` **is the destination perch**, a physical object in the room whose position was easy to calibrate consistently across flights. Note the asymmetry: **landing is hard to resolve cleanly in _time_, but easy in _position_.** So distance-to-perch is the trustworthy progress coordinate near the end of a flight, not elapsed time.
  
- `VertDistance = 0` **is the floor** (height above ground).
  
## Files
### `toothless_flapping_9m_avg.npz` — averaged flapping-only control window
- `markers` (139, 8, 3), `times` (139,), span 0.003–0.692 s
  
- Averaged 9 m straight Toothless flapping window, built from BirdDMD `Flapping_9mToothless_BilateralNoRot.npz`. This is the recommended first tutorial dataset because it gives a clean repeated wingbeat for PCA/SVD, FFT, DMD mode pairs, recombination, and generative extension.
  
- Clean, smooth, no gaps. The source contains flapping frames only; `behaviour` remains the flight-condition label (`Straight`), not a flapping/gliding phase label.
  
- `frame_info` = per-time-bin **means** of `time, HorzDistance, VertDistance, body_pitch, behaviour`. This source does not carry `backpack_global_{x,y,z}`.
  
### `toothless_control_9m_avg.npz` — averaged control flight
- `markers` (250, 8, 3), `times` (250,), span 0.103–1.347 s
  
- Averaged **whole** 9 m straight flight: flapping → glide → approach (`Obstacle=0`, `behaviour=Straight`, `Year=2020`, 67 flights). Glide phase begins ~0.78 s.
  
- Clean, smooth, no gaps. The baseline / control condition.
  
- `frame_info` = per-time-bin **means** of `time, HorzDistance, VertDistance, body_pitch, behaviour, backpack_global_{x,y,z}`.
  
### `toothless_rightturn_obstacle_avg.npz` — averaged right turn
- `markers` (260, 8, 3), `times` (260,)
  
- Averaged right-turn obstacle-avoidance flights (`Obstacle=1`, `behaviour=Right`).
  
- Clean, smooth, no gaps. Contrast against the control to study turning.
  
- `frame_info` = per-time-bin **means** of `time, HorzDistance, VertDistance, body_pitch, behaviour, backpack_global_{x,y,z}`.
  
### `toothless_single_flight_raw.npz` — single raw flight (control) with data gaps
- `markers` (225, 8, 3), `times` (225,), span −0.045–1.340 s
  
- One real **whole** control flight (flapping → glide → approach), seqID `04_09_042_2`. **Unaveraged.** Contains real mocap dropout gaps but stays clean: max Δt 0.050 s (~10× the 0.005 s frame step).
  
- Extra per-frame info in `frame_info_columns` / `frame_info_values`: `frameID, time, HorzDistance, VertDistance, body_pitch, behaviour, backpack_global_{x,y,z}`.
  
  - `HorzDistance` — metres to the landing perch, **= √(global_x² + global_y²)** (decreases through the flight; perch at 0). See the trajectory section above.
    
  - `VertDistance` — metres, height; **≡** `backpack_global_z`.
    
  - `body_pitch` — degrees (rises into the landing flare).
    
  - `backpack_global_{x,y,z}` — backpack world position (metres); the full 3D flight trajectory. The markers are backpack-relative, so these columns are how you recover where the bird actually was. `x` lateral, `y` along-approach, `z` vertical.
