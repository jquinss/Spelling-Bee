import json
from random import randint

pangrams = {}


def is_pangram(word_in):
    if len(set(word_in)) == 7 and 's' not in word_in:
        return True
    else:
        return False


with open("words_dictionary.json") as json_file:
    words = json.load(json_file)

    for word in words:
        if is_pangram(word):
            pangrams[word] = ""

with open("pangrams.json", "w") as pangram_file:
    json.dump(pangrams, pangram_file)

# Pick a random pangram
rand_num = randint(0, len(pangrams))
random_pangram = list(pangrams.keys())[rand_num]
print(random_pangram)
print(set(random_pangram))