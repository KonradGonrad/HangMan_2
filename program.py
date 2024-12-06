from hangman import hangman_stage
from words import choose_word

def check_word(word: str,
               guess: str):
    if guess == word:
        return word
    else:
        if guess in word:
            return word.index(guess)
        return None

def reveal_letter(word,
                  guess: str, 
                  letters: list):
    for i in range(len(word)):
        if word[i] == guess:
            letters[i] = word[i]
    return letters


def hangman(ITER: int = None,
            GUESS: str = None,
            WORD: str = None,
            LETTERS: list = None,
            GUESSED: list = None,
            WIN: bool = False
            ):
    WORD = WORD.lower()
    GUESS = str(GUESS).lower()
    if len(GUESS) > 1:
        if GUESS == WORD:
            LETTERS = [char for char in WORD]
            WIN = True
        else:
            ITER += 1
    else:
        if GUESS in GUESSED:
            pass
        else:
            GUESSED.append(GUESS)
            if GUESS in WORD:
                LETTERS = reveal_letter(WORD, GUESS, LETTERS)
            else:
                ITER += 1
    
    if "".join(LETTERS) == WORD:
        WIN = True
        

    return ITER, LETTERS, GUESSED, WIN
        
if __name__ == "__main__":
    ITER = 0
    WORD = 'tulip'
    WORD_SPLITTED = [char for char in WORD]
    LETTERS = ["_" for i in range(len(WORD))]
    GUESSED = []
    guesses = 'tulip'
    i = 0
    while ITER < 10:
        GUESS = guesses[i]
        ITER, LETTERS, GUESSED = hangman(ITER=ITER, GUESS=GUESS, WORD=WORD, LETTERS=LETTERS, GUESSED=GUESSED)
        if LETTERS == WORD_SPLITTED:
            break
        i += 1