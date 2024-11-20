# Hangman Game
# Autores:
# Martin Eduardo Chacon Orduño - 351840
# Oscar Joaquin Marquez Ortega - 367726
#
# 30/09/2024

import pygame
import math
from wordBank import HashTable
from maxHeap import MaxHeap

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

        # Initialize HashTable
        self.hash_table = HashTable()
        self.hash_table.add_words_from_file("pistas_ahorcado.csv")
        self.load_new_word() 

        # Create buttons after loading the word and updating the window size
        self.create_buttons()

        # Initialize MaxHeap
        self.max_heap = MaxHeap()

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
        self.HINT_FONT = pygame.font.SysFont("comicsans", 20)
        self.SCORE_TITILE_FONT = pygame.font.SysFont("comicsans", 50)
        self.SCORE_WORD_FONT = pygame.font.SysFont("comicsans", 25)

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

    def assign_scores(self):
        base_score = 100
        lenght_bonus = len(self.word) * 10
        print(f"Len(word) = {len(self.word)}, initial score = {base_score +lenght_bonus}")

        penalty_per_mistake = 10
        
        hint_penalty = 10

        score = base_score + lenght_bonus - (self.hangman_status* penalty_per_mistake)
        print(f"score = {base_score} + {lenght_bonus} - {self.hangman_status} * {penalty_per_mistake}")
        if self.hint_used:
            score -= hint_penalty
        return max(0, score)

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
        pygame.time.delay(400)
        self.window.fill(self.background_color)
        text = self.WORD_FONT.render(message, 1, (0, 0, 0))
        self.window.blit(text, (self.WIDTH / 2 - text.get_width(), self.HEIGHT / 2 - text.get_height() / 2))
        pygame.display.update()
        pygame.time.delay(500)

    def show_scores(self):
        score_screen_width = 600
        score_screen_height = 400
        pygame.display.set_caption("High Scores")

        # Create a new window for scores
        score_window = pygame.display.set_mode((score_screen_width, score_screen_height))
        running = True

        # Extract scores from the heap
        scores = []
        total_score = 0
        while not self.max_heap.is_empty():
            node = self.max_heap.delete_max()
            scores.append(node)
            total_score += node.score

        # Scroll variables
        scroll_offset = 0
        line_spacing = 40
        total_score_space = 60  # Space needed for Total Score and line
        total_height = len(scores) * line_spacing + 100 + total_score_space  # Include Total Score in height
        max_scroll = max(0, total_height - score_screen_height)  # Calculate max scroll amount

        scrollbar_height = score_screen_height * score_screen_height / total_height  # Dynamic size for scrollbar
        scrollbar_x = score_screen_width - 20
        scrollbar_y = 0
        dragging = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if the scrollbar is clicked
                    mouse_x, mouse_y = event.pos
                    if scrollbar_x <= mouse_x <= scrollbar_x + 20 and scrollbar_y <= mouse_y <= scrollbar_y + scrollbar_height:
                        dragging = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    dragging = False
                elif event.type == pygame.MOUSEMOTION and dragging:
                    # Update scrollbar position
                    mouse_x, mouse_y = event.pos
                    scrollbar_y = max(0, min(score_screen_height - scrollbar_height, mouse_y))
                    scroll_offset = (scrollbar_y / (score_screen_height - scrollbar_height)) * max_scroll
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            score_window.fill((255, 255, 255))

            # Render title
            title_text = self.SCORE_TITILE_FONT.render("High Scores", True, (0, 0, 0))
            score_window.blit(title_text, (score_screen_width // 2 - title_text.get_width() // 2, 20))

            # Render scores with scroll
            start_y = 100 - scroll_offset
            for i, node in enumerate(scores):
                score_text = self.SCORE_WORD_FONT.render(f"{i+1}. {node.word}: {node.score} points", True, (0, 0, 0))
                score_window.blit(score_text, (50, start_y + i * line_spacing))

            # Render Total score
            total_y = start_y + len(scores) * line_spacing + 20  # Adjust for Total Score
            if scores:
                total_text = self.SCORE_WORD_FONT.render(f"Total score: {total_score} points", True, (0, 0, 0))
                pygame.draw.line(score_window, (0, 0, 0), (50, total_y - 10), (score_screen_width - 50, total_y - 10), 2)
                score_window.blit(total_text, (50, total_y))

            # Draw scrollbar background
            pygame.draw.rect(score_window, (200, 200, 200), (scrollbar_x, 0, 20, score_screen_height))
            # Draw scrollbar handle
            pygame.draw.rect(score_window, (100, 100, 100), (scrollbar_x, scrollbar_y, 20, scrollbar_height))

            pygame.display.update()

        pygame.quit()

    def show_hint(self):
        hint_node = self.hash_table.search_word(self.word)

        if isinstance(hint_node, str):
            self.hint = "No hint available for this word."
        else:
            self.hint = hint_node.hint

        # Set maximum width for the hint window
        max_width = 800  # Max width for the hint window
        char_width = self.HINT_FONT.size("A")[0]  # Approximate width of one character
        hint_width = min(len(self.hint) * char_width + 40, max_width)  # Cap width at max_width
        hint_height = 150  # Increased height to include scrollbar

        # Create a new window
        hint_window = pygame.display.set_mode((max_width, hint_height))
        pygame.display.set_caption("Hint")

        # Scrolling variables
        scroll_offset = 0
        max_scroll = max(0, len(self.hint) * char_width - max_width + 40)  # Calculate max scroll amount
        scrollbar_width = max_width * max_width / (max_width + max_scroll)  # Dynamic size for the scrollbar
        scrollbar_x = 0
        scrollbar_y = hint_height - 20
        dragging = False

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if the scrollbar is clicked
                    mouse_x, mouse_y = event.pos
                    if scrollbar_y <= mouse_y <= scrollbar_y + 20 and scrollbar_x <= mouse_x <= scrollbar_x + scrollbar_width:
                        dragging = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    dragging = False
                elif event.type == pygame.MOUSEMOTION and dragging:
                    # Update scrollbar position
                    mouse_x, _ = event.pos
                    scrollbar_x = max(0, min(max_width - scrollbar_width, mouse_x))
                    scroll_offset = (scrollbar_x / (max_width - scrollbar_width)) * max_scroll

            # Clear the window
            hint_window.fill((255, 255, 255))  # White background

            # Render and display the hint with scrolling
            hint_surface = self.HINT_FONT.render(self.hint, True, (0, 0, 0))
            hint_window.blit(hint_surface, (-scroll_offset, 50))

            # Draw the scrollbar background
            pygame.draw.rect(hint_window, (200, 200, 200), (0, scrollbar_y, max_width, 20))
            # Draw the scrollbar handle
            pygame.draw.rect(hint_window, (100, 100, 100), (scrollbar_x, scrollbar_y, scrollbar_width, 20))

            pygame.display.update()

        # Return to the main game window
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Hangman Game")



    def reset_game(self):
        self.hangman_status = 0
        self.guessed = []
        self.hint_used = False

        self.load_new_word()
        self.letters = []
        self.create_buttons()
        print("Game reset. Ready for the next word.")

    def handle_mouse_click(self, pos):
        mX, mY = pos

        # Check if hint button is clicked and conditions are met
        if self.hint_button.collidepoint(mX, mY):
            if self.hangman_status == 6:
                print("Hint cannot be used, the game will end if you lose one more attempt!")
                return
            if not self.hint_used:
                self.hint_used = True
                self.hangman_status += 1
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
                self.display_message("Loading next word...")
                self.assign_scores()
                score = self.assign_scores()
                self.max_heap.insert(score, self.word)
                print(f"Inserted into MaxHeap: score= {score}, word = {self.word}")
                self.reset_game()
            if self.hangman_status == 7:
                self.display_message("You LOST!!")
                self.show_scores()
                break

        pygame.quit()


if __name__ == "__main__":
    game = HangmanGame()
    game.run()
