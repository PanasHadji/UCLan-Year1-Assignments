# Wordle.py
# Author: Panagiotis Hadjidemetriou (G20965620)
# Email: PHadjidemetriou1@uclan.ac.uk
# Description: The Wordle.py program firstly presents every requirement of the assignment
# and then demonstrates the Wordle game in 2 modes: autoplay and interactive-play mode.
# In the autoplay mode the computer tries to guess a randomly generated word.
# In the interactive-play mode the user also tries to guess a randomly generated word
# but is guided by an array with colors depending on the letters he used.
# Gray: the letter doesn't appear in the word. Yellow: the letter is in the word but not
# in the correct position. Green: is the correct letter in the correct position.
# **In the autoplay mode there is a small chance dew to many words having the same constrictions
# where the computer has 100+ tries to find a word**

import random  # Importing the random library

# ============================================================================================#
# Creating arrays and dictionaries that we will use in the functions bellow
wordles = []
aplh_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
letter_frequency = [0] * 26

auto_grays = []
auto_yellows = {}
auto_greens = {}

# Reading the file wordles.txt from outside this file and creating an array (wordles) with every word od the file
file = open('wordles.txt', 'r')  # open for read-only
all_lines = file.readlines()
for line in all_lines:
    wordles.append(line.strip())  # strip clears non-visible characters, like 'next line'


# ============================================================================================#


# A function that reads every word in the array (wordles) and prints the frequencies of every letter in descending order
# (Code inspired by the solutions of the Exercise (part-B) provided under Week09, xtras)
def print_frequencies(words: [str]):
    """
    Prints the frequencies for each letter 'a' to 'z', as found in the given list of words.
    :param words: a list of string containing the words to count the letters for
    """
    global letter_frequency, aplh_letters  # Using global to access data from outside the function

    for word1 in words:  # Reads one word at a time from (wordles) and if a letter appears
        for i in range(len(word1)):  # its frequency increases by one in another array
            for j in range(len(aplh_letters)):
                if word1[i] == aplh_letters[j]:
                    letter_frequency[j] += 1
                    break

    # The following line sorts the two arrays in descending order
    # Code reused from https://stackoverflow.com/questions/30212452/sort-two-lists-in-python
    letter_frequency, letters = zip(*sorted(zip(letter_frequency, aplh_letters), reverse=True))

    # Prints everything in descending order
    for d in range(26):
        print(letters[d], '->', letter_frequency[d])


# ============================================================================================#


# A function that reads every word in the array (wordles) and a list of 5 letter from the
# user and returns the words containing them.
# (Code inspired by the solutions of the Exercise 5 provided under Week10, step1002)
def find_words_with_letters(words: [str], letters: [str]) -> [str]:
    """
    Find all words in the given list, which match all the given letters.
    For example for letters ['a', 'd', 'n'] and words list ['and', 'din', 'aid', 'dan'], return ['and', 'dan'].
    :param words: the list of words to be checked
    :param letters: the list of letters to be matched
    :return: a sublist of words which match the given characters
    """
    for word2 in words:  # Reads every word in the words list
        word_set = set(word2.strip())  # Creates a set with each words' letters and if that set is equal
        if word_set == set(letters):  # to the set created from the users list then the word is appended
            input_letters.append(word2)  # to a list that gets printed in the end

    # If no word is found, None is returned. Else the list of word found is returned
    if len(input_letters) == 0:
        return None
    return input_letters


# ============================================================================================#


# A function that takes two words (a secret word and a checking word) and returns a list
# that tells the user which letters are in the word and the correct position
# (Code inspired by the Exercises provided under Week10, step1002)
def check(secret: str, check_word: str) -> [str]:
    """
    Given a secret word and a check_word, which must be of equal length, return a list of words which
    are either 'gray', 'yellow' or 'green'. The semantics match the rules of Wordle:
    - 'gray' if the checked character does not appear in the secret word
    - 'yellow' if the checked character does appear in the secret word, but not in the same position
    - 'green' if the checked character matches the character at the same position in the secret word.
    For example for the secret word 'store' and check_word 'raise', it should return the list
    ['yellow', 'gray', 'gray', 'yellow', 'green']
    :param secret: a word to be checked against
    :param check_word: another word of equal length to be checked based on Wordle's rules
    :return: a list containing the values 'gray', 'yellow', 'green'
    """
    # Creating list that will help us in the process below
    check_secret = [''] * 5
    secret_array = list(secret.strip())
    check_word_array = list(check_word.strip())

    positions = [0, 1, 2, 3, 4]

    # The following a For loops containing If statements are checking each letter of the
    # checking word with the letters of the secret word. If the letter is the same and in the correct position
    # as the secret words' letter the is appends 'green'. If it's in the wrong position, but it appears in the secret
    # word then it appends 'yellow'. Else it appends 'gray'.
    for d in range(5):
        for j in range(5):
            if secret_array[d] == check_word_array[j]:
                check_secret[d] = 'green'
            else:
                for i in range(len(check_word_array)):
                    if check_word_array[d] == secret_array[i]:
                        check_secret[d] = 'yellow'
                        break
                    else:
                        check_secret[d] = 'gray'

    # The code bellow creates an auto_grays list auto_yellows and auto_greens dictionaries that will help in the auto_mode of the game
    for j in range(5):
        if check_secret[j] == 'gray':  # Checks if a position of the list is 'gray' and
            # the letter isn't already in the list,
            if check_word_array[j] not in auto_grays:
                auto_grays.append(check_word_array[j])  # It appends teh letter in the list

        if check_secret[j] == 'yellow':  # Checks if a position of the list is 'yellow' and
            # the letter isn't already in the list or a key in it,

            if check_word_array[j] in auto_yellows:
                if positions[j] not in auto_yellows[check_word_array[j]]:
                    auto_yellows[check_word_array[j]].add(positions[j])  # It appends the position in the keys list
            else:
                auto_yellows[check_word_array[j]] = set()  # It creates a key with its position
                auto_yellows[check_word_array[j]].add(positions[j])

        if check_secret[j] == 'green':  # Checks if a position of the list is 'green' and
            # the letter isn't already in the list or a key in it,
            if check_word_array[j] in auto_greens:
                if positions[j] not in auto_greens[check_word_array[j]]:
                    auto_greens[check_word_array[j]].add(positions[j])  # It appends the position in the keys list
            else:
                auto_greens[check_word_array[j]] = set()  # It creates a key with its position
                auto_greens[check_word_array[j]].add(positions[j])

    # It returns the list created, containing the colors
    return check_secret


# ============================================================================================#


# A function that takes two list and two dictionaries containing all the words and constrains
# for the word it has to find and when it finds it is prints it
# (Code inspired by the Exercises provided under Week10, step1002)
def find_word(words: [str], grays: [str], yellows: {}, greens: {}):
    """
    Given a list of words and constraints, it returns a suitable word, if it exists, otherwise the constant 'None'.
    The constraints are:
    - grays: A list of characters which are known to not exist in the target word
    - yellows: A dictionary of characters to sets of indices. The keys are characters, and the corresponding values
        are sets of integers, indicating the indices where it is known that the corresponding character is NOT at.
    - greens: A dictionary of characters to sets of indices. The keys are characters, and the corresponding values
        are sets of integers, indicating the indices where it is known that the corresponding character is found at.
    For example, the call:
        find_word(['batch', 'ozone'], 'abcd', {'n': {2}, 'z': {2, 3}}, {'o': {0, 2}, 'e': {4}})
    It looks for a word in the given list so that it does not contain any of the characters 'a', 'b', 'c', 'd'.
    Also it contains 'n' but not at index 2, and 'z' but not at indices 2, or 3.
    Finally, it contains 'o' at indices 0, 2, and it also contains 'e' at index 4.
    This for example excludes 'batch' but could return 'ozone'.
    remember that the indices are 0-base which means the first position is index 0, and the last one (5th) is index 4.
    :param words: the list of words to be checked against the constraints
    :param grays: a list of characters in the form of a string (gray constraint)
    :param yellows: a dictionary of characters to set of indices (yellow constraint)
    :param greens: a dictionary of characters to set of indices (green constraint)
    :return: a word from the given list which satisfies the constraints, or None if none is found
    """
    word_count = 0  # Declaring and assigning a variable

    for word3 in words:  # Reads every word in (wordles)

        # Creating variables and lists/dictionaries for every word that will help us in the process bellow
        yes = False
        word_count += 1
        yellow_equality = 0
        green_equality = 0

        word_dict = {}

        word_array = word3.strip()
        word_array_positions = [0, 1, 2, 3, 4]

        for letter in word3:  # Creating a dictionary with the letters of the word as a key
            word_dict[letter] = set()

        for i in range(len(word_array)):

            # Checks if the keys from above are equal to a letter in the word, and if they are
            # their position number is added to the list of that key
            for key in word_dict:
                if word_array[i] == key:
                    word_dict[key].add(word_array_positions[i])

            for gray in grays:  # If a letter of the grays list is equal to a letter of the word (yes) becomes true
                if gray == word_array[i]:
                    yes = True

        if not yes:  # If (yes) is not true then,

            for word_key in word_dict:  # Checks if the keys from above are in (yellows) and are equal to a key in the (word_dict),
                for yel_key in yellows:  # and if their lists aren't equal (yellow_equality) increases by 1
                    if word_key == yel_key:
                        if word_dict[word_key] != yellows[yel_key]:
                            yellow_equality += 1

                for gr_key in greens:  # and if their lists are equal (green_equality) increases by 1
                    if word_key == gr_key:
                        if word_dict[word_key] == greens[gr_key]:
                            green_equality += 1

            # If yes is False, (yellow_equality) is equal to the length of (yellows) and(green_equality) is equal to the length of (greens) then,
            if not yes and yellow_equality == len(yellows) and green_equality == len(greens):  # It returns the word
                return word3
        if word_count == len(
                words):  # If no word was found then (word_count) is equal to the number of the words and returns None
            return None


# ============================================================================================#
# The following lines demonstrate the assignments requirements in order until we reach the actual game


print(" Reading wordle words from file ...")
print('(40%)', '\n', 'Printing letter frequencies', '\n')
print_frequencies(wordles)

print('\n', '(50%)', '\n', 'Finding words with letters', '\n')
input_list = []
go = False

# Taking input from the user, turning it into a list and before executing the code we check, If the list has more than
# five elements, If the elements are actual letters and If the elements are single letters and not words.
# If everything is okay we proceed with the execution, else we clear the list and ask for input again
while not go and len(input_list) <= 5:
    clear = False
    go = False
    print('Type up to 5 different letters with a "," inbetween')
    input_list = list(input().lower().split(','))

    for inp in input_list:
        if inp not in aplh_letters:
            print('One of the characters is not a letter, try again!')
            clear = True
            break
        if not inp.isalpha():
            print('One of the characters is not a letter, try again!')
            clear = True
            break

    if len(input_list) > 5:
        print('Input larger than 5, try again!')
        clear = True

    if clear:
        input_list.clear()
    else:
        go = True

input_letters = []
print(find_words_with_letters(wordles, input_list))

print('\n', '(60%)', '\n', 'Checking secret word', '\n', 'Secret: crane  Check word: raise')
print(check('crane', 'raise'))

# After this step is clears the auto lists so that we don't affect the auto_play mode latter
auto_grays.clear()
auto_yellows.clear()
auto_greens.clear()

print('\n', '(70%)', '\n', 'Finding a word with constrains', '\n',
      'Constrains: grays:[''i, o, u, l, d, w, t]'' yellows:{''s'': {1, 2}, ''p'': {3}}'' greens:{''s'': {0}, ''a'': {2}})',
      '\n')
print('Word found: ',
      find_word(wordles, ['i', 'o', 'u', 'l', 'd', 'w', 't'], {'s': {1, 2}, 'p': {3}}, {'s': {0}, 'a': {2}}))

print('\n', 'Welcome to the text-based Wordle game.', '\n', 'I have guessed a secret word. Can you find it?', '\n',
      '(Type "1" for auto game, "2" for interactive game, or "quit" to exit)')

# ============================================================================================#
# GAME #

# Creating variables and lists that will help in the actual game
game_input = ''
enter_word = ''
enter_word_list = []

tries = 0

secret_1 = random.choice(wordles)  # Generates a secret word for each mode
secret_2 = random.choice(wordles)

auto_word = 'arose'  # Generates a random starting word for the auto_play mode

while game_input != 'quit':  # While the users input isn't 'quit' then,
    print('Enter your choice:')
    game_input = input().lower()  # Declaring and assigning a variable to the users input

    if game_input == 'quit':  # If the users input is 'quit' then the program end with a message
        print('Bye!')

    if game_input == '1':  # If the users input is '1' then,

        # Declaring and assigning a variable
        tries = 0
        counter = 0

        while auto_word != secret_1:  # While the (auto_word) isn't equal to (secret_1) then,

            tries += 1  # with each loop (tries) and (counter) are increased by 1
            counter += 1

            print('Trying -> ', auto_word)  # prints first message and word

            # If (auto_word) is None or (counter) is larger or equal to 10
            if auto_word is None or counter >= 10:
                auto_word = random.choice(wordles)  # (auto_word) gets randomized and the auto arrays get cleared
                auto_grays.clear()
                auto_yellows.clear()
                auto_greens.clear()
                counter = 0

            print(tries, '->', check(secret_1, auto_word), '\n')  # prints second message and array with colors

            auto_word = find_word(wordles, auto_grays, auto_yellows,
                                  auto_greens)  # tries to find word and assigns it to (auto_word)

            # If (auto_word) is equal to (secret_1) it prints the final message and the program ends
            if auto_word == secret_1:
                tries += 1
                print('Trying -> ', auto_word, '\n', tries, '->', ['green', 'green', 'green', 'green', 'green'], '\n')
                print('Congratulations! You found the wordle in', tries, 'tries', '\n', 'Bye!')
                game_input = 'quit'

    elif game_input == '2':  # If the users input is '1' then,
        tries = 0

        while enter_word != secret_2:  # While the (enter_word) isn't equal to (secret_2) then,
            print('Enter a 5 letter word, or "q" to quit')

            # Declaring and assigning variables and a list with the users input
            is_a_word = 0
            clear = False
            enter_word = input().lower()
            enter_word_list = list(enter_word.lower().strip())  # strips the word of the users input into letters

            if enter_word == 'q':  # If the users input is 'q' then the program ends
                print('Bye!')
                quit()

            for word in wordles:  # For every word it checks if the input is a word of the file
                if enter_word == word:
                    is_a_word += 1

            for inp in enter_word_list:  # For every letter of the input array it checks if it's a letter, if not it prints an error message
                if not inp.isalpha():
                    print(enter_word, ' is not a word.')
                    clear = True
                    break
                if len(enter_word_list) != 5:  # it checks if the length of the list is not 5, if not it prints an error message
                    print(enter_word, ' is not 5 letters long.')
                    clear = True
                    break

            if is_a_word == 0 and not clear:  # If the word is not in the file it prints an error message
                print(enter_word, ' is not in the list of accepted words.')
                clear = True

            if clear:  # if (clear) is true it prints an error message
                print('Please try again', '\n')

            else:  # If nothing from the above is true it proceeds with the game where thw user puts a word and gets a similarity array
                tries += 1
                print(tries, '->', check(secret_2, enter_word), '\n')
                if enter_word == secret_2:  # If (enter_word) is equal to (secret_2) it prints the final message and the program ends
                    print('Congratulations! You found the wordle in', tries, 'tries', '\n', 'Bye!')
                    game_input = 'quit'

    else:  # if the choice is wrong it prints an error message
        print('Invalid choice!')
