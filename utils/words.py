import random

words = {
    'Colors': 'red orange yellow green blue indigo violet white black brown'.split(),
    'Shapes': 'square triangle rectangle circle ellipse rhombus trapezoid chevron pentagon hexagon septagon octagon'.split(),
    'Fruits': 'apple orange lemon lime pear watermelon grape grapefruit cherry banana cantaloupe mango strawberry tomato'.split(),
    'Animals': 'bat bear beaver cat cougar crab leech lion lizard monkey moose mouse rabbit rat shark sheep skunk squid tiger turkey turtle weasel whale wolf'.split()
}


def get_random_word(word_dict):
    # This function returns a random string from the passed dictionary of lists of strings and its key.
    word_key = random.choice(list(word_dict.keys()))
    word_index = random.randint(0, len(word_dict[word_key]) - 1)
    return [word_dict[word_key][word_index], word_key]
