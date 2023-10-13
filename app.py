# Imports
from robot_controller import robot
from netcode import get_remote_position, send_position
from wait_for_sync import wait_for_sync
from translate import translate
from random_position import create_random_position

block_home = [526, -589, 260, -93, 62, 177]  # fix these numbers
safe_above_block = [526, -589, 260, -93, 62, 177]  # fix these numbers
robert = "ip"  # fix this ip

# TODO Use offset to move quickly to a position near his robot and then slowly to the final position



def part1(robot, ip):
    """Part 1 of the lab"""
    # get the other robot's position and move to it
    wait_for_sync(robot)
    robot.write_robot_connection_bit(1)
    position = get_remote_position(ip)
    robot.shunk_gripper("open")
    converted_position = translate(position)
    robot.write_cartesian_position(converted_position)
    robot.start_robot()

    # handoff
    robot.shunk_gripper("close")
    robot.write_robot_connection_bit(0)
    wait_for_sync(robot)

    robot.write_robot_connection_bit(1)
    # move to home position
    robot.set_joints_to_home_position()
    robot.start_robot()

    # move to a random position and then talk to the other robot's controller
    random_position = create_random_position()
    robot.write_cartesian_position(random_position)
    robot.start_robot()
    robot.write_robot_connection_bit(0)
    send_position(random_position)

    # Handoff
    wait_for_sync(robot)
    robot.write_robot_connection_bit(1)
    robot.shunk_gripper("open")
    robot.set_joints_to_home_position()
    robot.start_robot()
    robot.write_robot_connection_bit(0)


def intermission(robot, ip):
    # find the other robot's position, move to it and grab the die
    wait_for_sync(robot)
    position = get_remote_position(ip)
    converted_position = translate(position)
    wait_for_sync(robot)
    robot.write_robot_connection_bit(1)
    robot.write_cartesian_position(converted_position)
    robot.start_robot()
    robot.shunk_gripper("close")
    robot.write_robot_connection_bit(0)

    # move the die to the home position, drop it
    wait_for_sync(robot)
    robot.write_robot_connection_bit(1)
    robot.write_cartesian_position(safe_above_block)
    robot.start_robot()
    robot.write_cartesian_position(block_home)
    robot.start_robot()
    robot.shunk_gripper("open")


def part2(robot, ip):
    """Part 2 of the lab"""

    # pick up the die
    robot.write_cartesian_position(safe_above_block)
    robot.start_robot()
    robot.write_cartesian_position(block_home)
    robot.start_robot()
    robot.shunk_gripper("close")

    # move the die to a random position and then talk to the other robot's controller
    random_position = create_random_position()
    robot.write_cartesian_position(random_position)
    robot.start_robot()
    robot.write_robot_connection_bit(0)
    send_position(random_position)
    wait_for_sync(robot)
    robot.write_robot_connection_bit(1)
    # let go of the die and move back to the home position
    robot.shunk_gripper("open")
    robot.set_joints_to_home_position()
    robot.start_robot()
    robot.write_robot_connection_bit(0)

    # when we can move, move to the other robot's position and grab the die
    wait_for_sync(robot)
    position = get_remote_position(ip)
    converted_position = translate(position)
    robot.write_robot_connection_bit(1)
    robot.write_cartesian_position(converted_position)
    robot.start_robot()
    robot.shunk_gripper("close")
    # communicate the handoff
    robot.write_robot_connection_bit(0)
    wait_for_sync(robot)
    robot.write_robot_connection_bit(1)
    # move the die to the home position and drop it
    robot.write_cartesian_position(safe_above_block)
    robot.start_robot()
    robot.write_cartesian_position(block_home)
    robot.start_robot()
    robot.shunk_gripper("open")


def main():
    robert = "172.29.208.119"
    bunsen = "172.29.208.123"
    # Create robot object
    crx10 = robot(bunsen)
    crx10.set_speed(100)

    for i in range(2):
        part1(crx10, robert)

    intermission(crx10, robert)

    for i in range(2):
        part2(crx10, robert)


if __name__ == "__main__":
    main()
