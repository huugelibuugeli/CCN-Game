import keyboard
import socket
import time


def client_program():
    print("trying to connect to server")

    #REMEMBER TO CHANGE THIS IP ADDRESS TO YOUR SERVER IP ADDRESS
    host = "10.22.43.145"
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    print("waiting for keyboard input")
    while keyboard.read_key() != 'q':

        if keyboard.is_pressed('a'):
            client_socket.send('a'.encode())  # send message
            time.sleep(0.1)
        if keyboard.is_pressed('d'):
            client_socket.send('d'.encode())  # send message
            time.sleep(0.1)
        if keyboard.is_pressed('s'):
            client_socket.send('s'.encode())  # send message
            time.sleep(0.1)
        if keyboard.is_pressed('w'):
            client_socket.send('w'.encode())  # send message
            time.sleep(0.1)
        if keyboard.is_pressed('r'):
            client_socket.send('r'.encode())  # send message
            time.sleep(0.1)

    client_socket.close()  # close the connection


if __name__ == 'main':
    client_program()