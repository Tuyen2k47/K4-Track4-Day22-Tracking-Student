"""Unit tests for pure functions in run_tracking.py."""

from run_tracking import color_for_id


def test_color_for_id_returns_valid_rgb() -> None:
    color = color_for_id(1)
    assert isinstance(color, tuple)
    assert len(color) == 3
    for channel in color:
        assert isinstance(channel, int)
        assert 64 <= channel <= 254


def test_color_for_id_deterministic() -> None:
    color_a = color_for_id(42)
    color_b = color_for_id(42)
    assert color_a == color_b


def test_color_for_id_different_ids() -> None:
    color_1 = color_for_id(1)
    color_2 = color_for_id(2)
    assert color_1 != color_2
