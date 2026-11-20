from pathlib import Path

# Only fill gaps this many frames long or shorter
MAX_GAP = 5

# The trained club head model, kept in the backend folder
MODEL_PATH = Path(__file__).resolve().parent.parent / "best_v2.pt"


def fill_gaps(positions: list, max_gap: int = MAX_GAP) -> list:
    """Fill short gaps in the club positions with a straight line."""
    positions = list(positions)
    i = 0

    while i < len(positions):
        if positions[i] is None:
            # Find where this gap ends
            end = i
            while end < len(positions) and positions[end] is None:
                end = end + 1

            start = i - 1
            gap = end - i

            # Only fill if there's a point on both sides and the gap is short
            if start >= 0 and end < len(positions) and gap <= max_gap:
                x1, y1 = positions[start]
                x2, y2 = positions[end]
                steps = end - start

                for step in range(1, steps):
                    x = x1 + (x2 - x1) * step / steps
                    y = y1 + (y2 - y1) * step / steps
                    positions[start + step] = (int(x), int(y))

            i = end

        else:
            i = i + 1

    return positions