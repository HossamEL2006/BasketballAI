mode = 0


def simple_bot(data):
    global mode
    if mode == 0:
        if data[1] > 450:  # If the player's Y coord is more than 450
            mode = 1
            return "450 0"  # Jump towards the point (400, 0): To the top

    elif mode == 1:
        if data[1] > 550:
            mode = 2
            return "400 0"

    elif mode == 2:
        if abs(data[0] - data[4]) <= 5:
            mode = 3
            return f"{data[0]} 0"

    elif mode == 3:
        if data[1] > 550:
            return f"{data[4]} 150"

    return "NO JUMP"


# This AI will simply make sure that the basketball doesn't fall into the void by
# constantly jumping up
