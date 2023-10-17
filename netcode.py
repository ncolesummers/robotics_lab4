import socket
import pickle
import time

bind_ip = "0.0.0.0"


def get_remote_position(ip):
    """This function will connect to the other robot's controller and get the current position of the robot.
    In this case, the other controller is my lab partner's laptop."""
    sent = False
    while not sent:
        try:
            # create a socket connection
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # connect to the server on port 12345
            port = 12345

            s.connect((ip, port))
            break
        except ConnectionRefusedError:
            print("Connection Failed, Retrying..")
            time.sleep(1)
            continue
    # print the data received from the server
    data = s.recv(1024)
    # load the data into a list
    data = pickle.loads(data)
    print("Received: ", data)
    # close the socket connection
    s.close()
    return data


def send_position(data):
    """This function will send the current position of the robot to the other robot's controller.
    In this case, the other controller is my lab partner's laptop."""
    # open a file to dump the list into
    with open("position.pickle", "wb") as f:
        pickle.dump(data, f)
    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind the socket to a public host and port
    s.bind((bind_ip, 12345))

    # become a server socket
    s.listen(1)
    sent = False
    while not sent:
        try:
            # accept connections from outside
            (clientsocket, address) = s.accept()
            print("Connection from", address)

            # open the pickled file and send it over the socket
            with open("position.pickle", "rb") as f:
                data = f.read()
                print(data)
                clientsocket.sendall(data)  # send the data
            # close the client socket
            clientsocket.close()
            sent = True
        except socket.error:
            print("Connection attempt Failed")
            time.sleep(0.5)


def pass_baton(ip):
    """This function will send a signal to the other robot that it's their turn to move"""
    sent = False
    while not sent:
        try:
            # create a socket connection
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # connect to the server on port 54321
            port = 54321

            s.connect((connect_ip, port))
            break
        except ConnectionRefusedError:
            print("Connection Failed, Retrying..")
            time.sleep(0.5)
            continue
    print("Connection Established. Sending Baton.")
    baton = 1  # this is the signal to the other robot that it's their turn to move
    s.sendall(baton.to_bytes(1, "big"))

    # close the socket connection
    s.close()


def wait_for_baton():
    """This function will wait for the other robot to signal that it's my turn to move"""
    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind the socket to a public host and port
    s.bind((bind_ip, 54321))
    s.listen(1)
    sent = False
    while not sent:
        try:
            # accept connections from outside
            (clientsocket, address) = s.accept()
            print("Connection from", address)
            # receive the data from the client
            data = clientsocket.recv(1024)
            # print the data received from the client
            print("With data: ", data)
            if data == 1:
                sent = True
                print("Baton Received. Moving...")
                # close the client socket
                clientsocket.close()

        except socket.error:
            print("Connection attempt Failed")
            time.sleep(0.5)


def main():
    raise NotImplementedError(
        "This file is not meant to be run as a standalone script."
    )


if __name__ == "__main__":
    main()
