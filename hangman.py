# hangman.py
import random

HANGMAN_ASCII_ART = """                                     
   | |  | |                                        
   | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
   |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
   | |  | | (_| | | | | (_| | | | | | | (_| | | | |
   |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                       __/ |                       
                       |___/"""

max_tries = 6

HANGMAN_PHOTOS = {
    1: "x-------x",
    2: """
x-------x
|
|
|
|
|
""",
    3: """
x-------x
|       |
|       0
|
|
|
""",
    4: """
x-------x
|       |
|       0
|       |
|
|
""",
    5: r"""
x-------x
|       |
|       0
|      /|\
|
|
""",
    6: r"""
x-------x
|       |
|       0
|      /|\
|      /
|
""",
    7: r"""
x-------x
|       |
|       0
|      /|\
|      / \
|
""",
}

# words + clues live here
word_dict = {}
used_words = set()

def load_words(path="musicians_clues.txt"):
    global word_dict
    try:
        with open(path, "r") as file:
            for line in file:
                if ":" in line:
                    (name, clue) = line.strip().split(":", 1)
                    name = name.replace("_", " ").lower()
                    word_dict[name] = clue
    except FileNotFoundError:
        
        word_dict = {
            "elvis presley": "The King of Rock and Roll",
            "michael jackson": "King of Pop",
            "freddie mercury": "Queen's legendary frontman",
            "john lennon": "Beatles member and peace activist",
            "bob dylan": "Folk rock legend and Nobel Prize winner",
            "david bowie": "Ziggy Stardust creator",
            "jimi hendrix": "Guitar virtuoso of the 60s",
            "kurt cobain": "Nirvana frontman",
            "madonna": "Queen of Pop",
            "prince": "Purple Rain artist"
        }

def random_word():
    global word_dict, used_words
    if not word_dict:
        load_words()
    available_words = [w for w in word_dict.keys() if w not in used_words]
    if not available_words:
        print("All words have been used! Resetting word list.")
        used_words.clear()
        available_words = list(word_dict.keys())
    return random.choice(available_words)

def print_hangman(num_of_tries):
    num_of_tries = min(num_of_tries, max(HANGMAN_PHOTOS.keys()))
    print(HANGMAN_PHOTOS[num_of_tries])

def hint(word, num_of_tries):
    """Return a textual hint once the player has missed enough times."""
    global word_dict
    clue = word_dict.get(word, "")
    if num_of_tries >= 4:
        return clue
    return ""

def is_guess_valid(guess):
    return len(guess) == 1 and guess.isalpha()

def check_already_guessed(guess, old_letters_guessed, wrong_letters):
    return guess in old_letters_guessed or guess in wrong_letters

def show_hidden_word(word, old_letter_guessed):
    
    return "".join(ch if ch == " " or ch in old_letter_guessed else "-" for ch in word)

def play_hangman_game():
  
    global used_words

    print("\n" + "="*50)
    print("hello welcome to the hanging man festival")
    print(HANGMAN_ASCII_ART)
    print(f"if you want to enter you have {max_tries} tries.\ndont leave me hanging!!")
    print("Win and earn 10 points!")

    old_letter_guessed = set()
    wrong_letters = set()
    num_of_tries = 0
    word = random_word()
    print("-" * len(word))

    while True:
        if num_of_tries >= max_tries:
            print("you lost cant get in go home!!")
            print(f"the word was: {word}")
            return False  

        if show_hidden_word(word, old_letter_guessed) == word:
            print(f"\n🎉 ok ok you can enjoy the festival! The word was: {word}")
            used_words.add(word)
            return True  

        hint(word, num_of_tries)
        guess = input("guess a letter: ").lower()

        if not is_guess_valid(guess):
            print("x\nwrong input one letter only")
            continue

        if check_already_guessed(guess, old_letter_guessed, wrong_letters):
            print("already guessed it")
            print("Guessed letters: " + ", ".join(sorted(old_letter_guessed)))
            continue

        if guess in word:
            print("nice one!")
            old_letter_guessed.add(guess)
            print(show_hidden_word(word, old_letter_guessed))
        else:
            num_of_tries += 1
            print_hangman(num_of_tries)
            wrong_letters.add(guess)
            print(f"Wrong letters: {', '.join(sorted(wrong_letters))}")
            print(show_hidden_word(word, old_letter_guessed))
            print(f"you are {max_tries - num_of_tries} tries away from leaving the festival!!")
