"""Seams use correct north-first edges and preserve unknown cells."""

import numpy as np

from bla_bla_walk.geometry_audit import seam_evidence


def test_seams_compare_touching_native_edges_without_filling_gaps(tmp_path):
    west = np.zeros((4, 4), dtype="float32")
    west[:, -1] = [2, 3, -9999, 5]
    east = np.zeros((4, 4), dtype="float32")
    east[:, 0] = [3, 4, 100, 6]
    np.save(tmp_path / "west.npy", west)
    np.save(tmp_path / "east.npy", east)
    seam = seam_evidence(tmp_path / "west.npy", tmp_path / "east.npy", "east")
    assert seam["paired_samples"] == 3
    assert seam["unknown_samples"] == 1
    assert seam["absolute_jump_p50_p95_max_m"] == [1, 1, 1]
    south = np.full((4, 4), 999, dtype="float32")
    south[0, :] = 20
    north = np.full((4, 4), 999, dtype="float32")
    north[-1, :] = 22
    np.save(tmp_path / "south.npy", south)
    np.save(tmp_path / "north.npy", north)
    seam = seam_evidence(tmp_path / "south.npy", tmp_path / "north.npy", "north")
    assert seam["absolute_jump_p50_p95_max_m"] == [2, 2, 2]
