from app.club_path import fill_gaps


def test_short_gap_is_filled():
    positions = [(0, 0), None, None, (30, 60)]

    filled = fill_gaps(positions)

    assert filled == [(0, 0), (10, 20), (20, 40), (30, 60)]


def test_long_gap_is_left_empty():
    positions = [(0, 0), None, None, None, (40, 40)]

    filled = fill_gaps(positions, max_gap=2)

    assert filled == [(0, 0), None, None, None, (40, 40)]


def test_gap_at_the_start_is_left_empty():
    positions = [None, None, (10, 10), (20, 20)]

    filled = fill_gaps(positions)

    assert filled == [None, None, (10, 10), (20, 20)]


def test_original_list_is_not_changed():
    positions = [(0, 0), None, (20, 20)]

    fill_gaps(positions)

    assert positions == [(0, 0), None, (20, 20)]