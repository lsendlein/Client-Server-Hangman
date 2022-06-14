from http import server
from socket import *
from hangman import Hangman
import json

eot = '~'
serverDisconnect = False

# model for socket server was adapted from "Computer Networking: A Top-Down Approach, 7th Edition" section 2.7.2 
serverPort = 5466
serverHost = 'localhost'
serverSocket = socket(AF_INET, SOCK_STREAM)

# bind the server to chosen port and listen for maximum of 5 queued connections
serverSocket.bind((serverHost, serverPort))
serverSocket.listen(5)

print(f'The server is listening on: {serverHost} on port: {serverPort}')

while not serverDisconnect:
    # accept connection and create new socket for this connection 
    connectionSocket, addr = serverSocket.accept()
    # instantiate new hangman game
    hangman_game = Hangman("helicopter")
    print(f"Connected by {addr}")
    print("Sending game request...")
    connectionSocket.send((f"Connected to {serverHost} on port: {serverPort}.\nLet's play some Hangman!").encode())
    # receive client game acceptance
    data = connectionSocket.recv(1024).decode()
    print(f'>Player 2 has accepted the game.')
    # print initial setup of hangman game
    hangman_game.print_current()

    while data != "\q":
        data = input("Guess a letter: ")
        if data != '\q':
            # requests longer than 1 char or that == @ will break the game
            # also cannot use end of transmission
            while len(data) > 1 or data == '@' or data == eot:
                data = input("Invalid entry, please pick a valid letter: ")
        
        # if the server wants to dc, let the client know first
        if data == '\q':
            data += eot
            connectionSocket.send(data.encode())
            print("Server disconnected.")
            serverDisconnect = True
            break
        
        # make a move in the hangman game with server data
        hangman_game.make_guess(data)
        # convert the game data to json
        hangman_string = hangman_game.conv_to_json()
        hangman_json = json.loads(hangman_string)

        print(f'>You chose the letter: {data}\n')
        print(f'>Your guess was: {hangman_json["guess was"]}\n')
        print(f'>Already chosen letters: {hangman_json["chosen letters"]}\n')
        print(f'>Strikes remaining: {hangman_json["strikes"]}\n')
        print(f'>Currently guessed word: {hangman_json["currently filled word"]}\n')

        # update the state of the client
        data += hangman_string
        data += eot
        connectionSocket.send(data.encode())

        # if we have won or lost, break the loop
        if (hangman_json["game win"] is True) or (hangman_json["game win"] is False):
            break
        
        # receive reply containing client guess
        data = connectionSocket.recv(1024).decode()
        if data == "\q":
            break
        
        # make a guess with client data
        hangman_game.make_guess(data)
        hangman_string = hangman_game.conv_to_json()
        hangman_json = json.loads(hangman_string)

        print(f'>Player 2 chose the letter: {data}\n')
        print(f'>Player 2\'s guess was: {hangman_json["guess was"]}\n')
        print(f'>Already chosen letters: {hangman_json["chosen letters"]}\n')
        print(f'>Strikes remaining: {hangman_json["strikes"]}\n')
        print(f'>Currently guessed word: {hangman_json["currently filled word"]}\n')

        # if we have won or lost the game, update client state and break
        if (hangman_json["game win"] is True) or (hangman_json["game win"] is False):
            data += hangman_string
            data += eot
            connectionSocket.send(data.encode())
            break
        
        # otherwise set the server data to a bogus value
        # when the client receives the bogus value, it knows it has received an
        # updated state message and will not prompt the player to make a move
        data = '@'
        data += hangman_string
        data += eot
        connectionSocket.send(data.encode())
        # client will send a reply acknowleging updated state
        data = connectionSocket.recv(1024).decode()


    print("Client connection closed.")
    # close the socket
    connectionSocket.close()
