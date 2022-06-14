# Client-Server-Hangman

Program is in Python3. To play, run the server first and then the client.
Typing “\q” on the client will only close the client, to close both, type “/q” in the server.
The game is two-person, so both the server and the client participate by guessing letters. However, the hangman game is instantiated in the server and only runs there.
The client and server states are kept insync by a JSON object sent back and forth between them. This JSON object contains important information about already guessed letters, the current state of the guessed word, the number of strikes
remaining, the letter guessed by the other player, etc...
The game is case-sensitive and both uppercase and lowercase letters can be used. 
