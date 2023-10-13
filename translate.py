offset = [-33, 1431, 0, 186, -121, 0]


def translate(position):
    """This function will translate the position of the robot to the other robot's coordinate system."""
    for i in range(len(position)):
        position[i] = position[i] + offset[i]
    return position
