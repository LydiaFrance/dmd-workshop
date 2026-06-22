import io
import unittest
from contextlib import redirect_stdout

import numpy as np

from animal_dmd.custom import expand_analysis_motion, prepare_analysis_motion, prepare_custom_motion


class DummyAnimal:
    def get_analysis_data(self, motion):
        return motion[:, [0, 2], :]


class PrepareCustomMotionTests(unittest.TestCase):
    def test_prepare_custom_motion_accepts_feature_matrix_and_prints_summary(self):
        motion = np.arange(12).reshape(4, 3)
        times = np.array([0.0, 0.1, 0.2, 0.3])

        output = io.StringIO()
        with redirect_stdout(output):
            prepared = prepare_custom_motion(motion, times)

        self.assertEqual(prepared.motion.shape, (4, 3, 1))
        self.assertEqual(prepared.times.shape, (4,))
        self.assertEqual(prepared.data_matrix.shape, (3, 4))
        self.assertEqual(prepared.marker_names, ["marker_0", "marker_1", "marker_2"])
        self.assertEqual(prepared.dimension_labels, ["x"])
        self.assertAlmostEqual(prepared.dt, 0.1)
        self.assertIn("motion: (4, 3, 1)", output.getvalue())
        self.assertIn("dt: 0.100000 seconds", output.getvalue())

    def test_prepare_custom_motion_reports_marker_name_mismatch(self):
        motion = np.zeros((4, 3, 2))
        times = np.array([0.0, 0.1, 0.2, 0.3])

        with self.assertRaisesRegex(ValueError, "`marker_names` must have one name per marker"):
            prepare_custom_motion(motion, times, marker_names=["only_one"])

    def test_prepare_analysis_motion_uses_animal_analysis_markers(self):
        motion = np.arange(4 * 3 * 2).reshape(4, 3, 2)
        times = np.array([0.0, 0.1, 0.2, 0.3])

        prepared = prepare_analysis_motion(
            motion,
            times,
            ["head", "tag", "tail"],
            animal=DummyAnimal(),
            analysis_marker_names=["head", "tail"],
        )

        self.assertEqual(prepared.motion.shape, (4, 2, 2))
        self.assertEqual(prepared.marker_names, ["head", "tail"])
        np.testing.assert_array_equal(prepared.motion, motion[:, [0, 2], :])

    def test_expand_analysis_motion_inserts_analysis_markers_into_reference(self):
        reference = np.zeros((3, 4, 2))
        analysis_motion = np.ones((3, 2, 2))

        expanded = expand_analysis_motion(
            analysis_motion,
            reference,
            ["head", "tag", "tail", "body"],
            ["head", "tail"],
        )

        np.testing.assert_array_equal(expanded[:, 0, :], 1.0)
        np.testing.assert_array_equal(expanded[:, 2, :], 1.0)
        np.testing.assert_array_equal(expanded[:, 1, :], 0.0)
        np.testing.assert_array_equal(expanded[:, 3, :], 0.0)


if __name__ == "__main__":
    unittest.main()
