import csv

# Only fill gaps this many frames long or shorter
MAX_GAP = 5

# Read the saved positions, None means the club head wasn't found
positions = []
with open("club_positions.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row["x"] == "":
            positions.append(None)
        else:
            positions.append((int(row["x"]), int(row["y"])))

filled = 0
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
        if start >= 0 and end < len(positions) and gap <= MAX_GAP:
            x1, y1 = positions[start]
            x2, y2 = positions[end]
            steps = end - start

            for step in range(1, steps):
                x = x1 + (x2 - x1) * step / steps
                y = y1 + (y2 - y1) * step / steps
                positions[start + step] = (int(x), int(y))
                filled = filled + 1

        i = end

    else:
        i = i + 1

with open("club_positions_filled.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["frame", "x", "y"])
    for frame_number, position in enumerate(positions):
        if position is None:
            writer.writerow([frame_number, "", ""])
        else:
            writer.writerow([frame_number, position[0], position[1]])

missing = positions.count(None)
print("Frames filled:", filled)
print("Frames still missing:", missing)