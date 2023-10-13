import socket
import pickle
import time


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
            continue
        sent = True
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
    s.bind(("172.29.208.47", 12345))

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

def main():
    robert = "172.29.208.119"
    print()
    position = get_remote_position(robert)
    print(position)

if __name__ == "__main__":
    main()