from app.over_the_top import downswing_gap, find_top, swing_result


def test_find_top_is_highest_point():
    path = [{"x": 0, "y": 100}, {"x": 0, "y": 20}, {"x": 0, "y": 60}]

    assert find_top(path) == 1


def test_downswing_above_backswing_is_positive():
    # Ball is on the right, so the downswing coming down further right is over the top
    path = [
        {"x": 100, "y": 100},
        {"x": 50, "y": 50},
        {"x": 0, "y": 0},
        {"x": 60, "y": 50},
        {"x": 100, "y": 100},
    ]

    assert downswing_gap(path) > 0


def test_downswing_below_backswing_is_negative():
    path = [
        {"x": 100, "y": 100},
        {"x": 50, "y": 50},
        {"x": 0, "y": 0},
        {"x": 40, "y": 50},
        {"x": 100, "y": 100},
    ]

    assert downswing_gap(path) < 0


def test_left_handed_swing_is_mirrored():
    # Same over the top swing, but mirrored, with the ball on the left
    path = [
        {"x": -100, "y": 100},
        {"x": -50, "y": 50},
        {"x": 0, "y": 0},
        {"x": -60, "y": 50},
        {"x": -100, "y": 100},
    ]

    assert downswing_gap(path) > 0


def test_too_short_path_gives_none():
    assert downswing_gap([{"x": 0, "y": 0}]) is None
    

def test_swing_result_categories():
    assert swing_result(12) == "Over the top"
    assert swing_result(0) == "Neutral"
    assert swing_result(-8) == "Shallow"
    assert swing_result(None) == "Not enough of the swing to measure"