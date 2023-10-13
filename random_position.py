import random
def create_random_position():
    """This function will create a random position within 10 of the original position."""
    coords = [526, -589, 260, -93, 62, 177]
    # randomize the first 3 coords within 10 of the original
    coords[0] = random.randint(coords[0] - 50, coords[0] + 50)
    coords[1] = random.randint(coords[1] - 50, coords[1] + 50)
    coords[2] = random.randint(coords[2] - 100, coords[2] + 100)
    return coords