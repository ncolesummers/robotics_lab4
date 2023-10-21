# Lab 4

Nathan Summers and Robert Carne

CS 453

## Introduction

This project serves as one-half of the solution to Lab 4 of CS453. It contains all of the logic to control Bunsen. The robots must pass a die back and forth between each other. The location will be random within a box above the conveyor belts.

We will not be using vision to detect the die but instead will be communicating the location of the die between the robots.

## Approach

Each robot will have a controller. The controllers use the provided robot controller module to operate the robots. The controllers communicate by binding to sockets with the socket library in Python. Serialization and deserialization use the `pickle` library.

`app.py` contains the higher-level functionality. This module will be responsible for initializing an instance of the robot controller as implemented in `robot_controller.py`. `netcode.py` handles the communication between controllers. Here, we define how we send the random positions to each other and communicate which robot should be moving. `movement.py` handles the creation of the random positions. This module also contains the logic to translate the position received from the other robot into a movement command.


### [Communication](netcode.py):

The communication between the robots uses sockets. The robots will bind to a port and wait for a connection from the other robot. Once the connection is established, the robots will send their random positions to each other. Once the robot receives the message, it will move to the position sent to it. We are tearing down the connection after each message is sent to ensure the robots are not waiting for a message that will never come. During development, occasionally, we ran into a situation where the robots could not connect to each other due to the port being in use. By setting the socket to reuse the address, we avoided this issue. 

During the lab, we were unable to get the synchronization bit working. Eventually, we realized there was an issue with the robot controller. It was trying to write to a register that was already in use. We worked around this issue by having the controllers send a message to each other when they were ready to move. 

This would be an excellent place for some unit tests. We could mock the robot controller and test the communication logic without having to run the robots.

### [Movement](movement.py):

The functions in `movement.py` translate the random positions into movement commands. The random positions are generated using the `random` library. The positions are generated within a box above the conveyor belts. The positions are then translated into a movement command. This module is also responsible for translating the position received from the other robot into a movement command. I also define some safer movement commands here,  such as the ability to decelerate before reaching the position. It also helps to ensure we don't trigger the force sensor while handing off the die. Test coverage for this module is low. I want to add some unit tests to ensure that the movement commands are being generated correctly.


### [Main](app.py):

The main function is here to map the lab's requirements to the functions in the other modules. It is responsible for initializing the robot controller and starting the communication between the robots. It also handles the logic for determining which robot should be moving. Most of the constants are defined here. I want to move these into a separate file in the future.

## Conclusion

If I were programming these robots for a real-world application, I would use a more robust communication protocol, such as MQTT with a message broker. Decoupling the robots from each other would allow for more flexibility in the future. For example, if we wanted to add a third robot, we would only need to add a new controller and update the message broker. In addition, I would move the communication logic onto a separate thread, allowing the robots to continue moving while waiting for the other robot's message.


# Quick Start

1. Connect to vandalrobot wifi
2. Install dependencies
3. Run the main function in `app.py`

## Running the code
```bash
# install dependencies
pip install -r requirements.txt
# run the code
python app.py
```