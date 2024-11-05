MAX_SIZE = 120000
MAX_WORDS = 90000
words = [None] * MAX_SIZE
word_count = 0
n_collisions = 0


# Hashing function using prime multiplication and modulus operator (to limit the
# value to fit inside the array size)
def hashing(word):
    hash_value = 0
    for char in word:
        hash_value = hash_value * 43 + ord(char)
        # TODO Add linked list
    return hash_value % MAX_SIZE


def add_word(word):
    global word_count
    global n_collisions
    i = 1
    if word_count >= MAX_WORDS:
        print("Maximum unique words reached.")
        return False

    index = hashing(word)
    start_index = index

    # Collision using quadratic probing
    while words[index] is not None:
        if words[index] == word:
            print(f"'{word}' is already in the array at index {index}.")
            return False
        index = (index + i**2) % MAX_SIZE
        i += 1
        n_collisions += 1
        if index == start_index:
            print("Array is full and cannot accommodate more unique words.")
            return False

    words[index] = word
    word_count += 1
    print(f"'{word}' added at index {index}.")
    return True


def add_words_from_file(filename):
    try:
        # Open file as 'read only'
        with open(filename, "r") as file:
            for line in file:
                # Remove whitespace
                word = line.strip()
                if word:
                    add_word(word)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")


def get_unique_words():
    return [word for word in words if word is not None]


add_words_from_file("words.txt")
print("Words added:", get_unique_words())
print(f"Number of collisions: '{n_collisions}'");
