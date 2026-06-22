import unittest

import numpy as np

from animal_dmd.plots import plot_dmd_pair_traces


class PlotDmdPairTracesTests(unittest.TestCase):
    def test_plot_dmd_pair_traces_labels_data_and_selected_pairs(self):
        times = np.array([0.1, 0.2, 0.3])
        measured_trace = np.array([1.0, 0.0, -1.0])
        pair_traces = {
            0: np.array([0.8, 0.0, -0.8]),
            2: np.array([0.2, 0.1, 0.0]),
        }
        pair_frequencies_hz = np.array([1.5, 2.5, 3.5])

        fig, ax = plot_dmd_pair_traces(
            times,
            measured_trace,
            pair_traces,
            pair_frequencies_hz=pair_frequencies_hz,
            trace_label="tail z",
        )

        labels = [line.get_label() for line in ax.lines]
        self.assertEqual(labels, ["data", "pair 0: 1.50 Hz", "pair 2: 3.50 Hz"])
        self.assertEqual(ax.get_title(), "Selected DMD pair traces: tail z")
        fig.clear()


if __name__ == "__main__":
    unittest.main()
