# Imports
import time
from robot_controller import robot
from netcode import get_remote_position, send_position, pass_baton, wait_for_baton
from movement import (
    translate,
    create_random_position,
    ease_in,
    reset_speed,
    move_away_from_partner,
    move_back,
)

# Constants
block_home = [706.529, 262, -197.608, 178.297, 2.664, 28.545]  # mount position
up_from_home = block_home.copy()
up_from_home[2] += 50
top_speed = 250  # mm/s


def part1(robot, ip):
    """Part 1 of the lab"""
    move_back(robot)
    robot.start_robot()
    # get the other robot's position and move to it
    wait_for_baton()
    position = get_remote_position(ip)
    robot.shunk_gripper("open")
    converted_position = translate(position)
    ease_in(robot, converted_position)
    reset_speed(robot, top_speed)

    print("First Handoff")
    # handoff
    robot.shunk_gripper("close")
    pass_baton(ip)
    wait_for_baton()
    # move to home position
    move_away_from_partner(robot, converted_position)
    robot.start_robot()

    # move to a random position and then talk to the other robot's controller
    print("Create Random Position")
    random_position = create_random_position()
    print(f"random position: {random_position}")
    robot.write_cartesian_position(*random_position)
    robot.start_robot()
    pass_baton(ip)
    send_position(random_position)

    print("Second Handoff")
    # Handoff
    wait_for_baton()
    robot.shunk_gripper("open")
    move_away_from_partner(robot, random_position)
    robot.start_robot()
    move_back(robot)
    robot.start_robot()


def intermission(robot, ip):
    """Intermission between part 1 and part 2"""
    # find the other robot's position, move to it and grab the die

    wait_for_baton()
    position = get_remote_position(ip)
    converted_position = translate(position)
    ease_in(robot, converted_position)
    reset_speed(robot, top_speed)
    robot.shunk_gripper("close")
    # hand off
    pass_baton(ip)
    wait_for_baton()
    # move the die to the home position, drop it
    robot.write_cartesian_position(*up_from_home)
    robot.start_robot()
    robot.write_cartesian_position(*block_home)
    robot.start_robot()
    robot.shunk_gripper("open")
    reset_speed(robot, top_speed)
    robot.write_cartesian_position(*up_from_home)
    robot.start_robot()


def part2(robot, ip):
    """Part 2 of the lab"""

    print(" Part 2 grab the die")
    # pick up the die
    robot.write_cartesian_position(*block_home)
    robot.start_robot()
    robot.shunk_gripper("close")

    # move the die to a random position and then talk to the other robot's controller
    random_position = create_random_position()
    robot.write_cartesian_position(*random_position)
    robot.start_robot()
    # hand off
    print("Part 2 first handoff")
    pass_baton(ip)
    send_position(random_position)
    wait_for_baton()
    # let go of the die and move back to the home position
    robot.shunk_gripper("open")
    move_away_from_partner(robot, random_position)
    robot.start_robot()

    # when we can move, move to the other robot's position and grab the die
    position = get_remote_position(ip)
    converted_position = translate(position)
    ease_in(robot, converted_position)
    robot.shunk_gripper("close")
    reset_speed(robot, top_speed)
    # communicate the handoff
    print("Part 2 second handoff")
    pass_baton(ip)
    time.sleep(0.5)
    # move the die to the home position and drop it
    print("part 2 move die to home position and drop it")
    robot.write_cartesian_position(*up_from_home)
    robot.start_robot()
    robot.write_cartesian_position(*block_home)
    robot.start_robot()
    robot.shunk_gripper("open")
    reset_speed(robot, top_speed)
    robot.write_cartesian_position(*up_from_home)
    robot.start_robot()

def cleanup(robot):
    print("Returning robot to safe position")
    move_back(robot)
    robot.start_robot()
    print("Done")

def main():
    """Main function"""
    # IP addresses
    robert = "172.29.208.119"
    bunsen = "172.29.208.123"
    # Create robot object
    crx10 = robot(bunsen)
    crx10.set_speed(top_speed)
    crx10.shunk_gripper("open")

    for i in range(2):
        print(f"Beginning first part iteration {i + 1}")
        part1(crx10, robert)
        print(f"Ending first part iteration {i + 1}")

    intermission(crx10, robert)

    for i in range(2):
        print(f"Beginning second part iteration {i + 1}")
        part2(crx10, robert)
        print(f"Ending second part iteration {i + 1}")

    # Return robot to home position
    cleanup(crx10)


if __name__ == "__main__":
    main()
