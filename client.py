import socket
import json

eot = '~'


# receive function modified from myreceive function from https://docs.python.org/3/howto/sockets.html
def receive(r_client):
    chunks = []
    bytes_recd = 0
    while True:
        try:
            chunk = r_client.recv(min(5000 - bytes_recd, 2048)).decode()
        except socket.timeout:
            break
        # receive until we hit end of transmission
        if eot in chunk:
            # remove end of transmission
            chunk = chunk[:-1]
            chunks.append(chunk)
            break
        chunks.append(chunk)
        bytes_recd = bytes_recd + len(chunk)
    return ''.join(chunks)


target_host = "localhost"
target_port = 5466  # create a socket object

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
client.connect((target_host, target_port))
print("Type '\q' to quit.")
# receive welcome message from server
response = client.recv(1024).decode()
print(response)
# since this is the first run through, we need the client to confirm they are playing
start = True

while True:
    if start:
        request = input("Press any letter to continue...")
        # ensure that nothing malicious is sent by only sending first letter entered
        request = request[0]
        start = False
    else:
        request = input("Guess a letter: ")
        if request != "\q":
            # requests longer than 1 char or that == @ will break the game
            # also cannot use end of transmission
            while len(request) > 1 or request == '@' or request == "~":
                request = input("Invalid entry, please pick a valid letter: ")
    
    client.send(request.encode())
    
    if request == '\q':
        break
    
    response = receive(client)
    
    if response == '\q':
        print("Server disconnected.")
        break
    
    # isolate the letter chosen by player_1
    player_1_choice = response[0]
    # the rest of the response is a json file containing game data
    response = response[1:]
    json_file = json.loads(response)

    # if the client receives bogus player_1 data, if knows it is receiving a state update
    # it prints the state update and does not prompt the player
    if player_1_choice == '@':
        print(f'>You chose the letter: {request}\n')
        print(f'>Your guess was: {json_file["guess was"]}\n')
        print(f'>Already chosen letters: {json_file["chosen letters"]}\n')
        print(f'>Strikes remaining: {json_file["strikes"]}\n')
        print(f'>Currently guessed word: {json_file["currently filled word"]}\n')

        # if we have won or lost, break the loop
        if json_file["game win"] is True:
            print(f"Congratulations! You guessed the word -- {json_file['word to guess']}")
            break
        
        if json_file["game win"] is False:
            print(f"You lose! The word was -- {json_file['word to guess']}")
            break

        # let the server know that state has been updated
        request = "Update received"
        client.send(request.encode())
        
        # receive new game data from server
        response = receive(client)
        
        if response == '\q':
            print("Server disconnected.")
            break
        
        # separate player_1 guess from game json
        player_1_choice = response[0]
        response = response[1:]
        json_file = json.loads(response)

    # if the game has been won or lost, break
    if json_file["game win"] is True:
        print(f"Congratulations! You guessed the word -- {json_file['word to guess']}")
        print(f'>You chose the letter: {request}\n')
        print(f'>Your guess was: {json_file["guess was"]}\n')
        print(f'>Already chosen letters: {json_file["chosen letters"]}\n')
        print(f'>Strikes remaining: {json_file["strikes"]}\n')
        print(f'>Currently guessed word: {json_file["currently filled word"]}\n')
        break
    
    if json_file["game win"] is False:
        print(f"You lose! The word was -- {json_file['word to guess']}")
        print(f'>You chose the letter: {request}\n')
        print(f'>Your guess was: {json_file["guess was"]}\n')
        print(f'>Already chosen letters: {json_file["chosen letters"]}\n')
        print(f'>Strikes remaining: {json_file["strikes"]}\n')
        print(f'>Currently guessed word: {json_file["currently filled word"]}\n')
        break

    print(f'>Player 1 chose the letter: {player_1_choice}\n')
    print(f'>Player 1 guess was: {json_file["guess was"]}\n')
    print(f'>Already chosen letters: {json_file["chosen letters"]}\n')
    print(f'>Strikes remaining: {json_file["strikes"]}\n')
    print(f'>Currently guessed word: {json_file["currently filled word"]}\n')

    
    # if the game has been won or lost, break
    if json_file["game win"] is True:
        print(f"Congratulations! You guessed the word -- {json_file['word to guess']}")
        break
    
    if json_file["game win"] is False:
        print(f"You lose! The word was -- {json_file['word to guess']}")
        break

print("Connection closed")
client.close()