# imports
import random
import unittest

# constants
offset = [4, -1444, 0, -186, 121, 0]


def create_random_position():
    """This function will create a random position that's close to the initial position."""
    coords = [526, -589, 260, -93, 62, 177].copy()
    # randomize the first 3 coords within 10 of the initial
    coords[0] = random.randint(coords[0] - 50, coords[0] + 50)
    coords[1] = random.randint(coords[1] - 50, coords[1] + 50)
    coords[2] = random.randint(coords[2] - 100, coords[2] + 100)
    print(f"random position created: {coords}")
    return coords


def move_back(robot):
    """This function will move back along the y axis to a safer position"""
    safe_position = [542.206, -400, 290, -93, 62, 177]
    robot.write_cartesian_position(*safe_position)


def move_away_from_partner(robot, position):
    """We are moving in the positive y direction to get away from the other robot"""
    deep_copy = position.copy()
    deep_copy[1] += 100
    print("backing up...")
    robot.write_cartesian_position(*deep_copy)


def translate(position):
    """This function will translate the position of the robot to the other robot's coordinate system."""
    translated_position = position.copy()
    for i in range(len(translated_position)):
        translated_position[i] = round(translated_position[i] + offset[i], 3)
    print("#debug translated position", translated_position)
    return translated_position


def ease_in(robot, position):
    """This function will reduce the speed of the robot as it approaches the final position.
    create a new position with y and z increased by 20
    this will keep the die higher up and further from its partner
    as it moves to the final position"""
    print("Easing in")
    print("#debug position", position)
    deceleration_point = position.copy()
    # increase y by 20, meaning it will be further from the other robot
    deceleration_point[1] += 40
    # increase z by 20, meaning it will be higher up
    deceleration_point[2] += 40
    print("#debug deceleration point", deceleration_point)
    robot.write_cartesian_position(*deceleration_point)
    robot.start_robot()
    robot.set_speed(50)
    robot.write_cartesian_position(*position)
    robot.start_robot()


def reset_speed(robot, speed):
    """This function will reset the speed of the robot to the top speed"""
    robot.set_speed(speed)


# test cases


class TestMovement(unittest.TestCase):
    def test_create_random_position(self):
        """This function will test the create_random_position function"""
        # test the function 100 times
        for _ in range(100):
            # get a random position
            position = create_random_position()
            # check if the position is within the correct range
            self.assertTrue(476 <= position[0] <= 576)
            self.assertTrue(-639 <= position[1] <= -539)
            self.assertTrue(160 <= position[2] <= 360)
            self.assertTrue(-193 <= position[3] <= -93)
            self.assertTrue(-59 <= position[4] <= 161)
            self.assertTrue(157 <= position[5] <= 357)
            # check if the position is not the same as the initial position
            self.assertNotEqual(position, [526, -589, 260, -93, 62, 177])

    def test_translate(self):
        """This function will test the translate function"""
        start_position = [538.51, 836.662, 256.579, 97.76, -54.847, 178.416]
        end = [505.51, 2267.662, 256.579, 283.76, -175.847, 178.416]
        self.assertEqual(translate(start_position), end)


if __name__ == "__main__":
    unittest.main()
