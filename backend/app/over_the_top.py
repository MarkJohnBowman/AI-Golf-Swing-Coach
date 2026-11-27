def find_top(path: list[dict]) -> int:
    """Find the top of the backswing: the point where the club head is highest."""
    # y counts down from the top of the video, so the highest point has the smallest y
    top = 0
    for i in range(len(path)):
        if path[i]["y"] < path[top]["y"]:
            top = i
    return top


def downswing_gap(path: list[dict]) -> float | None:
    """How far the downswing is above (+) or below (-) the backswing, as a % of the swing height."""
    if len(path) < 3:
        return None

    top_index = find_top(path)
    address = path[0]
    top = path[top_index]
    backswing = path[: top_index + 1]
    downswing = path[top_index:]

    swing_height = address["y"] - top["y"]
    if swing_height <= 0:
        return None

    # The ball side of the swing counts as "above" the backswing.
    # This works for right and left-handed golfers.
    if address["x"] > top["x"]:
        outside = 1
    else:
        outside = -1

    # Only look at the first half of the downswing, where coming over the top shows
    halfway = top["y"] + swing_height / 2

    gaps = []
    for point in downswing:
        if point["y"] > halfway:
            break
        # The backswing point at the same height as this downswing point
        match = min(backswing, key=lambda p: abs(p["y"] - point["y"]))
        gaps.append((point["x"] - match["x"]) * outside)

    if len(gaps) == 0:
        return None

    average_gap = sum(gaps) / len(gaps)
    return round(average_gap / swing_height * 100, 1)

# Starting cut-off points from the research (8.3)
SHALLOW_BELOW = -5
OVER_THE_TOP_ABOVE = 5


def swing_result(gap: float | None) -> str:
    """Sort a swing into shallow, neutral or over the top."""
    if gap is None:
        return "Not enough of the swing to measure"
    if gap > OVER_THE_TOP_ABOVE:
        return "Over the top"
    if gap < SHALLOW_BELOW:
        return "Shallow"
    return "Neutral"