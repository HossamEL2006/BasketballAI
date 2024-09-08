def simple_ai(data):
    if data[1] > 550:     # If the player's Y coord is more than 550
        return '400 0'    # Jump towards the point (400, 0): To the top
    else:                 # Otherwise
        return "NO JUMP"  # Don't Jump


# This AI will simply make sure that the basketball doesn't fall into the void by
# constantly jumping up
