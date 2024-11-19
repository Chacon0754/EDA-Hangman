# Hangman Game
# Autores:
# Martin Eduardo Chacon Orduño - 351840
# Oscar Joaquin Marquez Ortega - 367726
#
# 30/09/2024


import pygame
import math
from wordBank import HashTable


class HangmanGame:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 500
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Hangman Game")
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.running = True

        # Game variables
        self.hangman_status = 0
        self.guessed = []
        self.letters = []
        self.word = ""
        self.hint_used = False

        # Load assets
        self.load_fonts()
        self.load_images()
        self.create_buttons()

        # Initialize HashTable
        self.hash_table = HashTable()
        self.hash_table.add_words_from_file("pistas_ahorcado.csv")
        self.load_new_word() 

    def load_new_word(self):
        result = self.hash_table.get_word()

        if isinstance(result, tuple):
            self.word, _  = result
            self.word = self.word.upper()

            # Calculate new width
            char_width = self.WORD_FONT.size("A")[0]
            padding = 100
            min_width = 800
            word_width =  len(self.word) * char_width + padding
            image_width = self.images[0].get_width() + padding
            total_width = word_width + image_width + padding
            new_width = max(min_width, total_width)

            if new_width != self.WIDTH:
                self.WIDTH = new_width
                self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
                print(f"Screen width updated to {self.WIDTH, self.HEIGHT}")

            print(f"New word: {self.word}")
        else:
            print("No more words available. Ending game")
            self.running = False

    def load_fonts(self):
        self.LETTER_FONT = pygame.font.SysFont("comicsans", 40)
        self.WORD_FONT = pygame.font.SysFont("comicsans", 45)
        self.TITLE_FONT = pygame.font.SysFont("comicsans", 70)
        self.BUTTON_FONT = pygame.font.SysFont("comicsans", 30)
        self.HINT_FONT = pygame.font.SysFont("comicsans", 12)

    def load_images(self):
        self.images = []
        for i in range(8):
            img_url = f"img/hangman{i}.png"
            image = pygame.image.load(img_url)
            scaled_image = pygame.transform.scale(
                image, (400, int(image.get_height() * (200 / image.get_width())))
            )
            self.images.append(scaled_image)
        self.background_color = self.images[0].get_at((10, 10))

    def create_buttons(self):
        radius = 20
        gap = 15
        start_x = round((self.WIDTH - (radius * 2 + gap) * 13) / 2)
        start_y = 400
        A = 65

        for i in range(26):
            x = start_x + gap * 2 + ((radius * 2 + gap) * (i % 13))
            y = start_y + ((i // 13) * (gap + radius * 2))
            self.letters.append([x, y, chr(A + i), True])
        
        # Add "Get Hint" button
        button_text = "Hint"
        text_width, text_height = self.BUTTON_FONT.size(button_text)  # Calculate text size
        button_width = text_width + 10  # Add smaller padding for the width
        button_height = text_height + 5  # Add smaller padding for the height

        margin_top = 10  # Top margin below the title
        margin_right = 10  # Right margin
        title_height = self.TITLE_FONT.size("HANGMAN")[1]  # Height of the title text
        image_top = (self.HEIGHT - self.images[0].get_height()) // 2

        # Ensure the button does not overlap with the image
        safe_y_position = min(title_height + margin_top, image_top - button_height - margin_top)

        self.hint_button = pygame.Rect(
            self.WIDTH - button_width - margin_right,  # Align to the right
            safe_y_position,  # Ensure button is below title and above image
            button_width,
            button_height
        )
    
    def draw(self):
        self.window.fill(self.background_color)

        # Draw title
        title_text = "HANGMAN"
        text = self.TITLE_FONT.render(title_text, 1, (0, 0, 0))
        title_x = (self.WIDTH / 2) - (text.get_width() / 2)
        title_y = 20
        self.window.blit(text, (title_x, title_y))

        # Draw "Get Hint" button
        pygame.draw.rect(self.window, (0, 0, 0), self.hint_button, 2)  # Border only (line width = 2)
        button_text = "Hint"
        text = self.BUTTON_FONT.render(button_text, 1, (0, 0, 0))
        self.window.blit(
            text,
            (self.hint_button.x + (self.hint_button.width - text.get_width()) // 2,
            self.hint_button.y + (self.hint_button.height - text.get_height()) // 2)
        )


        # Position calculations
        image_width = self.images[self.hangman_status].get_width()
        image_height = self.images[self.hangman_status].get_height()
        word_width = self.WORD_FONT.size(self.word)[0]

        # Margins and spacing
        word_x = 50  # Left margin for the word
        word_y = (self.HEIGHT - image_height) // 2  # Align the word vertically with the image
        image_x = self.WIDTH - image_width - 50  # Right margin for the image
        image_y = (self.HEIGHT - image_height) // 2  # Center the image vertically

        # Adjust vertical centering to account for buttons
        button_area_height = 100  # Approximate height for the buttons area
        if image_y + image_height + button_area_height > self.HEIGHT:
            image_y = self.HEIGHT - image_height - button_area_height - 20  # Add padding below the image


        # Draw hangman image
        self.window.blit(self.images[self.hangman_status], (image_x, image_y))

        # Draw word
        display_word = "".join([letter + " " if letter in self.guessed else "_ " for letter in self.word])
        text = self.WORD_FONT.render(display_word, 1, (0, 0, 0))
        self.window.blit(text, (word_x, word_y))

        # Draw buttons
        for letter in self.letters:
            x, y, ltr, visible = letter
            if visible:
                pygame.draw.circle(self.window, (0, 0, 0), (x, y), 20, 3)
                text = self.LETTER_FONT.render(ltr, 1, (0, 0, 0))
                self.window.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))


        pygame.display.update()

    def display_message(self, message):
        pygame.time.delay(1000)
        self.window.fill(self.background_color)
        text = self.WORD_FONT.render(message, 1, (0, 0, 0))
        self.window.blit(text, (self.WIDTH / 2 - text.get_width(), self.HEIGHT / 2 - text.get_height() / 2))
        pygame.display.update()
        pygame.time.delay(3000)

    def show_hint(self):
        hint_node = self.hash_table.search_word(self.word)
        

        if isinstance(hint_node, str):
            self.hint = "No hint available for this word."
        else:
            self.hint = hint_node.hint

        # Calculate window size based on the hint length
        char_width = self.HINT_FONT.size("A")[0]  # Approximate width of one character
        hint_width = len(self.hint) * char_width + 40  # Add padding
        hint_height = 100  # Fixed height
        hint_width = max(hint_width, 300)  # Ensure a minimum width

        # Create a new window
        hint_window = pygame.display.set_mode((hint_width, hint_height))
        pygame.display.set_caption("Hint")
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            hint_window.fill((255, 255, 255))  # White background
            text = self.HINT_FONT.render(self.hint, 1, (0, 0, 0))  # Render the hint
            hint_window.blit(text, (hint_width // 2 - text.get_width() // 2, hint_height // 2 - text.get_height() // 2))
            pygame.display.update()

        # Return to the main game window
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Hangman Game")


    def reset_game(self):
        self.hangman_status = 0
        self.guessed = []
        self.hint_used = False

        for letter in self.letters:
            letter[3] = True

        self.load_new_word()

    def handle_mouse_click(self, pos):
        mX, mY = pos

        if self.hint_button.collidepoint(mX, mY) and not self.hint_used:
            self.hint_used = True
            self.hangman_status +=1
            self.show_hint()
            return
        
        for letter in self.letters:
            x, y, ltr, visible = letter
            if visible:
                dis = math.sqrt((x - mX) ** 2 + (y - mY) ** 2)
                if dis < 20:
                    letter[3] = False
                    self.guessed.append(ltr)
                    if ltr not in self.word:
                        self.hangman_status += 1

    def handle_key_press(self, key_pressed):
        if pygame.K_a <= key_pressed <= pygame.K_z:
            ltr = chr(key_pressed).upper()
            if ltr not in self.guessed:  # Only process unguessed letters
                self.guessed.append(ltr)
                for letter in self.letters:
                    if letter[2] == ltr and letter[3]:  
                        letter[3] = False  
                        if ltr not in self.word:  
                            self.hangman_status += 1 

    def run(self):
        while self.running:
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(pygame.mouse.get_pos())
                elif event.type == pygame.KEYDOWN:
                    self.handle_key_press(event.key)

            self.draw()

            # Check if the game is won or lost
            if all(letter in self.guessed for letter in self.word):
                self.hash_table.delete_word(self.word)
                self.display_message("You Won")
                self.reset_game()
            if self.hangman_status == 7:
                self.display_message("You LOST!!")
                break

        pygame.quit()


if __name__ == "__main__":
    game = HangmanGame()
    game.run()
