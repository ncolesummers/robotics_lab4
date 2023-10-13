# imports
import random

# constants
offset = [-33, 1431, 0, 186, -121, 0]


def create_random_position():
    """This function will create a random position that's close to the initial position."""
    coords = [526, -589, 260, -93, 62, 177]
    # randomize the first 3 coords within 10 of the initial
    coords[0] = random.randint(coords[0] - 50, coords[0] + 50)
    coords[1] = random.randint(coords[1] - 50, coords[1] + 50)
    coords[2] = random.randint(coords[2] - 100, coords[2] + 100)
    return coords


def translate(position):
    """This function will translate the position of the robot to the other robot's coordinate system."""
    for i in range(len(position)):
        position[i] = position[i] + offset[i]
    return position


def ease_in(robot, position):
    """This function will reduce the speed of the robot as it approaches the final position.
    create a new position with y and z increased by 20
    this will keep the higher up and further from its partner
    as it moves to the final position"""
    deceleration_point = position.copy()
    deceleration_point[1] += 20
    deceleration_point[2] += 20
    robot.write_cartesian_position(deceleration_point)
    robot.start_robot()
    robot.set_speed(50)
    robot.write_cartesian_position(position)
    robot.start_robot()


def reset_speed(robot, speed):
    """This function will reset the speed of the robot to 100"""
    robot.set_speed(speed)
