from typing import Optional


class Node:
    def __init__(self, word, hint):
        self.word = word
        self.hint = hint
        self.next: Optional[Node] = None


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
    return hash_value % MAX_SIZE


def add_word(word):
    global word_count
    global n_collisions
    hint = "testing"

    if word_count >= MAX_WORDS:
        print("Maximum unique words reached.")
        return False

    index = hashing(word)

    if words[index] is None:
        words[index] = Node(word, hint)
        word_count += 1
        print(f"'{word}' added at index {index}.")
        return True
    else:
        # Collision using linked lists
        current = words[index]
        n_collisions += 1
        while current is not None:
            if current.word == word:
                print(f"'{word}' is already in the list at index {index}.")
                return False
            if current.next is None: 
                break
            current = current.next

        current.next = Node(word, hint)
        word_count += 1
        print(f"'{word}' added at index {index} with collision.")
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
    unique_words = []
    for word_node in words:
        current = word_node
        while current is not None:
            unique_words.append(current.word)
            current = current.next
    return unique_words


add_words_from_file("words.txt")
print("Words added:", get_unique_words())
print(f"Number of collisions: '{n_collisions}'")
