from typing import Optional
import csv


class Node:
    def __init__(self, word, hint):
        self.word = word
        self.hint = hint
        self.next: Optional[Node] = None

class HashTable:
    def __init__(self, max_size=120000, max_words=90000):
        self.MAX_SIZE = max_size
        self.MAX_WORDS = max_words
        self.words = [None] * self.MAX_SIZE
        self.word_count = 0
        self.n_collisions = 0

    # Hashing function using prime multiplication and modulus operator (to limit the
    # value to fit inside the array size)
    def hashing(self, word):
        hash_value = 0
        for char in word:
            hash_value = hash_value * 43 + ord(char)
        return hash_value % self.MAX_SIZE

    def add_word(self, word, hint):
        if self.word_count >= self.MAX_WORDS:
            print("Maximum unique words reached.")
            return False

        index = self.hashing(word)

        if self.words[index] is None:
            self.words[index] = Node(word, hint)
            self.word_count += 1
            print(f"'{word}' added at index {index}.")
            return True
        else:
            # Collision using linked lists
            current = self.words[index]
            self.n_collisions += 1
            while current is not None:
                if current.word == word:
                    print(f"'{word}' is already in the list at index {index}.")
                    return False
                if current.next is None:
                    break
                current = current.next

            current.next = Node(word, hint)
            self.word_count += 1
            print(f"'{word}' added at index {index} with collision.")
            return True

    def add_words_from_file(self, filename):
        try:
            # Open file as 'read only'
            with open(filename, mode="r", newline='', encoding="Windows-1252") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) < 2:
                        print(f"Skipping invalid row: {row}")
                        continue

                    key = row[0].strip()
                    hint = row[1].strip()
                    self.add_word(key, hint)
        except FileNotFoundError:
            print(f"File '{filename}' not found.")

    def get_unique_words(self):
        unique_words = []
        for word_node in self.words:
            current = word_node
            while current is not None:
                unique_words.append(current.word)
                current = current.next
        return unique_words

    def search_word(self, word):
        index = self.hashing(word)
        current = self.words[index]

        # Traverse the linked list
        while current is not None:
            if current.word == word:
                return current
            current = current.next
        return f"'{word}' was not found."


