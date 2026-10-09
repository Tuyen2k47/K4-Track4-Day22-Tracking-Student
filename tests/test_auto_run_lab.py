"""Unit tests for pure functions in auto_run_lab.py."""

from auto_run_lab import get_recommended_configs


def test_recommended_configs_contains_all_videos() -> None:
    configs = get_recommended_configs()
    expected_videos = ["video_1", "video_2", "video_3", "video_4", "video_5"]
    assert list(configs.keys()) == expected_videos


def test_recommended_configs_valid_structure() -> None:
    configs = get_recommended_configs()
    valid_trackers = {"bytetrack", "ocsort", "botsort", "strongsort", "deepocsort"}
    for name, cfg in configs.items():
        assert "tracker" in cfg
        assert cfg["tracker"] in valid_trackers
        assert 0.0 < cfg["conf"] < 1.0
        assert 0.0 < cfg["iou"] < 1.0
        assert isinstance(cfg["reason"], str)
        assert len(cfg["reason"]) > 0
