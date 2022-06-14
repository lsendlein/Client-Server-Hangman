import json

class Hangman:
    def __init__(self, word_to_guess) -> None:
        self.valid_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
        'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A',
        'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
        'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.already_chosen_letters = []
        self.strikes = ["X"] * 5
        self.current_word_list = list(word_to_guess)
        self.current_word_list_empty = [' __ '] * len(self.current_word_list)
        self.word_to_guess = word_to_guess
        self.guessWas = "Correct"
        self.gameWin = None
    
    def print_current(self):
        print(f'Strikes remaining: {self.strikes}')
        print(f'Currently guess word: {self.current_word_list_empty}')
    
    def make_guess(self, player_input):
        # while there are still letters to guess and strikes remaining
        if (' __ ' in self.current_word_list_empty) and (len(self.strikes) != 0):
            guess = player_input
            if guess not in self.valid_letters:
                print("Invalid letter choice -- please choose a valid letter.\n")
                self.guessWas = "An invalid letter choice"
            elif guess in self.already_chosen_letters:
                print("You have already used this letter.\n")
                self.guessWas = "An already used letter choice"
            elif guess in self.current_word_list:
                # if guess in word, replace every instance of letter in empty list
                # remove letter from list containing word chars
                for i in range(len(self.current_word_list)):
                    if self.current_word_list[i] == guess:
                        self.current_word_list_empty[i] = guess
                        self.current_word_list[i] = ' __ '
                        if guess not in self.already_chosen_letters:
                            self.already_chosen_letters.append(guess)
                        self.guessWas = "Correct"
            else:
                print("Incorrect guess\n")
                self.guessWas = "Incorrect"
                self.strikes.remove('X')
                if guess not in self.already_chosen_letters:
                    self.already_chosen_letters.append(guess)

        if len(self.strikes) == 0:
            print(f"You lose! The word was -- {self.word_to_guess}\n")
            self.gameWin = False
        
        if ' __ ' not in self.current_word_list_empty:
            print(f"Congratulations! You guessed the word -- {self.word_to_guess}\n")
            self.gameWin = True

    def conv_to_json(self):
        payload = {
            "word to guess" : self.word_to_guess,
            "chosen letters" : self.already_chosen_letters,
            "strikes" : self.strikes,
            "currently filled word" : self.current_word_list_empty,
            "guess was" : self.guessWas,
            "game win" : self.gameWin
                }
        return json.dumps(payload)


if __name__ == '__main__':
    hangman_game = Hangman("helicopter")
    hangman_game.make_guess("h")
    hangman_game.make_guess("e")
    hangman_game.make_guess("l")
    json_file = hangman_game.conv_to_json()
    result = json.loads(json_file)
    print(result)
    print(result["strikes"])