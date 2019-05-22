import game


class Guess:
    """
    Represents the game.
    """

    def __init__(self):
        """
        Constructs a new object and initializes the attributes of the class Guess.
        """
        self.game = game.Game()
        self.gameList = []
        self.gameRoundsCounter = 0

    def main(self):
        """
        The entry point function into the game.
        :return: None
        :rtype: None
        """
        self.gameList.append(game.Game(self.gameRoundsCounter))
        shouldContinue = True

        print("** The great guessing game **")

        while shouldContinue:
            print("\nCurrent Guess: %s" % self.gameList[self.gameRoundsCounter].currentGuess)
            action = input("\ng = guess, t = tell me, l for a letter, and q to quit").lower()

            if action not in "gtlq" or len(action) != 1:
                print("\n@")
                print("@ FEEDBACK: I don't know how to do that!")
                print("@")
                continue

            if action == 'g':
                self.try_guess()
            elif action == 't':
                self.tell_me()
            elif action == 'l':
                self.try_letter()
            elif action == 'q':
                print("\n@")
                wantToQuit = input("Are you sure you want to quit?(y/n)").lower()
                print("@")
                if wantToQuit == "y":
                    shouldContinue = False
                    self.print_report()
                    print("\n@")
                    print("@ FEEDBACK: Bye-bye! Thank you for playing the game!")
                    print("@")

    def try_guess(self):
        """
        Asks to enter a guess word and verifies if it is a correct guess or not.
        :return: None
        :rtype: None
        """
        guessInput = input("\nPlease enter guess:").lower()

        currentWordString = str(self.gameList[self.gameRoundsCounter].currentWord)

        if guessInput == currentWordString:
            self.gameList[self.gameRoundsCounter].isSuccess = True
            self.gameList[self.gameRoundsCounter].didFinish = True
            print("\n@")
            print("@ FEEDBACK: Woo hoo! It was a correct guess..!")
            print("@")
            self.update_score()
            self.start_new_game()
        else:
            self.gameList[self.gameRoundsCounter].incorrectGuesses += 1
            print("\n@")
            print("@ FEEDBACK: Try again, Loser! It wasn't a correct guess..!")
            print("@")

    def try_letter(self):
        """
        Asks a letter and verifies if the current word contains the letter or not.
        :return: None
        :rtype: None
        """
        letter = input("\nEnter a letter:").lower()

        if len(letter) != 1:
            print("\n@")
            print("@ FEEDBACK: Not a valid single letter! Please, Try again.")
            print("@")
            return

        self.gameList[self.gameRoundsCounter].turnOverLetters += 1

        currentGuessString = str(self.gameList[self.gameRoundsCounter].currentGuess)
        currentWordString = str(self.gameList[self.gameRoundsCounter].currentWord)

        numberOfOccurrences = currentWordString.count(letter)
        charOccurrenceList = self.find_occurrences(currentWordString, letter)

        if len(charOccurrenceList) > 0:
            print("\n@")
            print("@ FEEDBACK: You found %d letters" % numberOfOccurrences)
            print("@")
            for index in charOccurrenceList:
                if currentGuessString[index] == "-":
                    currentGuessString = currentGuessString[:index] + letter + currentGuessString[index + 1:]
                else:
                    print("\n@")
                    print("@ FEEDBACK: But you already previously revealed the letter: '%s'" % letter)
                    print("@")
                    break

            self.gameList[self.gameRoundsCounter].currentGuess = currentGuessString

            if currentGuessString == currentWordString:
                self.gameList[self.gameRoundsCounter].isSuccess = True
                self.gameList[self.gameRoundsCounter].didFinish = True
                print("\n@")
                print("@ FEEDBACK: Woo hoo! You ended up revealing all the missing character.")
                print("@")
                self.update_score()
                self.start_new_game()

        else:
            self.gameList[self.gameRoundsCounter].missedLetters += 1
            print("\n@")
            print("@ FEEDBACK: Oops! It wasn't a match. Try again.")
            print("@")

    def tell_me(self):
        """
        User gave up, and show the current word.
        :return: None
        :rtype: None
        """
        self.gameList[self.gameRoundsCounter].didGaveUp = True
        self.gameList[self.gameRoundsCounter].didFinish = True
        print("\n@")
        print("@ FEEDBACK: You gave up! The correct guess was: %s" % self.gameList[self.gameRoundsCounter].currentWord)
        print("@")
        self.update_score()
        self.start_new_game()

    def update_score(self):
        """
        Updates score and tracks the score.
        :return: None
        :rtype: None
        """
        currentScore = float(self.gameList[self.gameRoundsCounter].score)
        incorrectGuesses = int(self.gameList[self.gameRoundsCounter].incorrectGuesses)
        turnOverLetters = int(self.gameList[self.gameRoundsCounter].turnOverLetters)
        currentGuessString = str(self.gameList[self.gameRoundsCounter].currentGuess)
        currentWordString = str(self.gameList[self.gameRoundsCounter].currentWord)
        didGaveUp = bool(self.gameList[self.gameRoundsCounter].didGaveUp)
        isSuccess = bool(self.gameList[self.gameRoundsCounter].isSuccess)

        if isSuccess:
            charIndex = 0
            pointValuesForLettersDictionary = game.Game.pointValuesForLettersDictionary
            for char in currentGuessString:
                if char == "-":
                    charFromWord = currentWordString[charIndex]
                    pointValueForChar = pointValuesForLettersDictionary.get(charFromWord)
                    currentScore += pointValueForChar
                charIndex += 1

            if turnOverLetters > 0:
                currentScore = currentScore / turnOverLetters

            if incorrectGuesses > 0:
                while incorrectGuesses > 0:
                    currentScore = currentScore - (currentScore * 0.10)
                    incorrectGuesses -= 1

        if didGaveUp:
            charIndex = 0
            pointValuesForLettersDictionary = game.Game.pointValuesForLettersDictionary
            for char in currentGuessString:
                if char == "-":
                    charFromWord = currentWordString[charIndex]
                    pointValueForChar = pointValuesForLettersDictionary.get(charFromWord)
                    currentScore -= pointValueForChar
                charIndex += 1

        self.gameList[self.gameRoundsCounter].score = currentScore

    def start_new_game(self):
        """
        Starts a new game.
        :return: None
        :rtype: None
        """
        self.gameRoundsCounter += 1
        self.gameList.append(game.Game(self.gameRoundsCounter))
        print("\n")
        print(" Game ended, You are playing a new game. ".center(70, "*"))

    def find_occurrences(self, s, ch):
        """
        Find occurrences of the character in a given string.
        :param s: String in which you want to find occurrences of the letter.
        :type s: str
        :param ch: The letter you want to find occurrences in a string.
        :type ch: str
        :return: List of the occurrences index.
        :rtype: List
        """
        return [i for i, letter in enumerate(s) if letter == ch]

    def print_report(self):
        """
        Prints score report.
        :return: None
        :rtype: None
        """
        finalScore = 0.0
        gameIndex = 0
        didFinish = bool(self.gameList[gameIndex].didFinish)

        if not didFinish:
            return

        print("\n@")
        print("@ Game Report:")
        print("@")
        print("\n")
        print("Game".ljust(8, " ") + "Word".ljust(8, " ") + "Status".ljust(11, " ") + "Bad Guesses".ljust(15, " ") + "Missed Letters".ljust(18, " ") + "Score".ljust(8, " "))
        print("----".ljust(8, " ") + "----".ljust(8, " ") + "------".ljust(11, " ") + "-----------".ljust(15, " ") + "---------------".ljust(18, " ") + "-----".ljust(8, " "))

        while gameIndex <= self.gameRoundsCounter:
            gameNumber = str(gameIndex + 1)
            word = str(self.gameList[gameIndex].currentWord)
            if bool(self.gameList[gameIndex].isSuccess):
                status = "Success"
            elif bool(self.gameList[gameIndex].didGaveUp):
                status = "Gave up"
            else:
                status = "NIL"
            badGuesses = str(self.gameList[gameIndex].incorrectGuesses)
            missedLetters = str(self.gameList[gameIndex].missedLetters)
            scoreFloat = float(self.gameList[gameIndex].score)
            score = "{0:.2f}".format(scoreFloat)
            didFinish = bool(self.gameList[gameIndex].didFinish)
            if didFinish:
                print(gameNumber.ljust(8, " ") + word.ljust(8, " ") + status.ljust(11, " ") + badGuesses.ljust(15, " ") + missedLetters.ljust(18, " ") + score.ljust(8, " "))
                finalScore = finalScore + float(self.gameList[gameIndex].score)
            gameIndex += 1
            status = "NIL"
        print("\nFinal Score: %.2f" % finalScore)


if __name__ == '__main__':
    guess = Guess()
    guess.main()