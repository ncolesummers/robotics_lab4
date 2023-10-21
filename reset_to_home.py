from robot_controller import robot

bunsen = "172.29.208.123"
top_speed = 75  # mm/s

crx10 = robot(bunsen)
crx10.set_speed(top_speed)
crx10.set_joints_to_home_position()
crx10.shunk_gripper("open")
crx10.start_robot()
