
def wait_for_sync(robot):
    """Wait for other robot to finish"""
    while robot.read_robot_connection_bit() == 0:
        print("Waiting for other robot to finish")
        continue
