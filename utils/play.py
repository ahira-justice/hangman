def verify_guess(guess, already_guessed):
    message = {}

    if len(guess) != 1:
        message = {'guess': 'Please enter a single letter'}
    elif guess in already_guessed:
        message = {'message': 'You have already guessed that letter'}
    elif guess not in 'abcdefghijklmnopqrstuvwxyz':
        message = {'message': 'Please enter a LETTER'}

    return message


def check_if_won(correct_letters, secret_word):
    found_all_letters = True

    for i in range(len(secret_word)):
        if secret_word[i] not in correct_letters:
            found_all_letters = False

    return found_all_letters


def check_if_lost(missed_letters, max_guesses):
    return len(missed_letters) == max_guesses
