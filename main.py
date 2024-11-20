# Hangman Game
# Autores:
# Martin Eduardo Chacon Orduño - 351840
# Oscar Joaquin Marquez Ortega - 367726
# Kevin Alejando Morales Schwartz - 367718
# 30/09/2024

import pygame
import math
import os
import sys
from wordBank import HashTable
from maxHeap import MaxHeap

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

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
        self.accepting_input = True

        # Load assets
        self.load_fonts()
        self.load_images()

        # Initialize HashTable
        self.hash_table = HashTable()
        csv_path = os.path.join(base_path, 'pistas_ahorcado.csv')
        self.hash_table.add_words_from_file(csv_path)
        self.load_new_word() 

        # Create buttons after loading the word and updating the window size
        self.create_buttons()

        # Initialize MaxHeap
        self.max_heap = MaxHeap()
        self.total_scores_heap = MaxHeap()

        # Game counter
        self.game_number = 1

        # Game total score
        self.total_score_game = 0

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
            img_url = os.path.join(base_path, 'img', f'hangman{i}.png')
            image = pygame.image.load(img_url)
            scaled_image = pygame.transform.scale(
                image, (400, int(image.get_height() * (200 / image.get_width())))
            )
            self.images.append(scaled_image)
        self.background_color = self.images[0].get_at((10, 10))

    def assign_scores(self):
        base_score = 50 
        length_bonus = len(self.word) * 20

        penalty_per_mistake = 15
        hint_penalty = 30

        score = base_score + length_bonus - (self.hangman_status * penalty_per_mistake)

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
        text_width, text_height = self.BUTTON_FONT.size(button_text)
        button_width = text_width + 10
        button_height = text_height + 5

        margin_top = 10
        margin_right = 10
        title_height = self.TITLE_FONT.size("HANGMAN")[1]
        image_top = (self.HEIGHT - self.images[0].get_height()) // 2

        # Ensure the button does not overlap with the image
        safe_y_position = min(title_height + margin_top, image_top - button_height - margin_top)

        self.hint_button = pygame.Rect(
            self.WIDTH - button_width - margin_right, 
            safe_y_position,
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
        pygame.draw.rect(self.window, (0, 0, 0), self.hint_button, 2)
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
        word_x = 50
        word_y = (self.HEIGHT - image_height) // 2
        image_x = self.WIDTH - image_width - 50
        image_y = (self.HEIGHT - image_height) // 2

        # Adjust vertical centering to account for buttons
        button_area_height = 100
        if image_y + image_height + button_area_height > self.HEIGHT:
            image_y = self.HEIGHT - image_height - button_area_height - 20


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
        display_duration = 600
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < display_duration:
            self.window.fill(self.background_color)
            text = self.WORD_FONT.render(message, 1, (0, 0, 0))
            self.window.blit(text, (self.WIDTH / 2 - text.get_width(), self.HEIGHT / 2 - text.get_height() / 2))
            pygame.display.update()

            # Process events to handle quit and prevent event queue buildup
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.clock.tick(self.FPS)



    def show_scores(self):
        pygame.display.set_caption("High Scores")

        running = True

        # Extract scores from the heap
        scores = []
        self.total_score_game = 0
        while not self.max_heap.is_empty():
            node = self.max_heap.delete_max()
            scores.append(node)
            self.total_score_game += node.score

        # Timer variables
        start_ticks = pygame.time.get_ticks()
        display_duration = 5000

        # Scroll variables
        scroll_offset = 0
        line_spacing = 40
        total_score_space = 60
        if scores:
            total_height = len(scores) * line_spacing + 100 + total_score_space
        else:
            total_height = 100

        max_scroll = max(0, total_height - self.HEIGHT)
        scrollbar_height = self.HEIGHT * self.HEIGHT / total_height if total_height > 0 else 0
        scrollbar_x = self.WIDTH - 20
        scrollbar_y = 0
        dragging = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.running = False
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
                    scrollbar_y = max(0, min(self.HEIGHT - scrollbar_height, mouse_y))
                    scroll_offset = (scrollbar_y / (self.HEIGHT - scrollbar_height)) * max_scroll
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        self.running = False

            # Check if seconds have passed
            if pygame.time.get_ticks() - start_ticks >= display_duration:
                running = False

            self.window.fill((255, 255, 255))

            # Render title
            title_text = self.SCORE_TITILE_FONT.render("High Scores", True, (0, 0, 0))
            self.window.blit(title_text, (self.WIDTH // 2 - title_text.get_width() // 2, 20))

            start_y = 100 - scroll_offset

            if scores:
                # Render scores with scroll
                for i, node in enumerate(scores):
                    score_text = self.SCORE_WORD_FONT.render(f"{i+1}. {node.word}: {node.score} points", True, (0, 0, 0))
                    self.window.blit(score_text, (50, start_y + i * line_spacing))

                # Render Total score
                total_y = start_y + len(scores) * line_spacing + 20
                total_text = self.SCORE_WORD_FONT.render(f"Total score: {self.total_score_game} points", True, (0, 0, 0))
                pygame.draw.line(self.window, (0, 0, 0), (50, total_y - 10), (self.WIDTH - 50, total_y - 10), 2)
                self.window.blit(total_text, (50, total_y))
            else:
                # Display no guessed words
                message = "0 palabras adivinadas"
                message_text = self.SCORE_WORD_FONT.render(message, True, (0, 0, 0))
                message_x = self.WIDTH // 2 - message_text.get_width() // 2
                message_y = start_y + 50 
                self.window.blit(message_text, (message_x, message_y))

            # Draw scrollbar only if necessary
            if total_height > self.HEIGHT:
                # Draw scrollbar background
                pygame.draw.rect(self.window, (200, 200, 200), (scrollbar_x, 0, 20, self.HEIGHT))
                # Draw scrollbar handle
                pygame.draw.rect(self.window, (100, 100, 100), (scrollbar_x, scrollbar_y, 20, scrollbar_height))

            pygame.display.update()

        pygame.display.set_caption("Hangman Game")

    def show_total_game_scores(self):
        pygame.display.set_caption("Total Game Scores")
        running = True

        # Extract total scores from the heap
        total_scores = []
        while not self.total_scores_heap.is_empty():
            node = self.total_scores_heap.delete_max()
            total_scores.append(node)

        # Timer variables
        start_ticks = pygame.time.get_ticks()
        display_duration = 3000

        # Scroll variables
        scroll_offset = 0
        line_spacing = 40
        if total_scores:
            total_height = len(total_scores) * line_spacing + 100
        else:
            total_height = 100

        max_scroll = max(0, total_height - self.HEIGHT)
        scrollbar_height = self.HEIGHT * self.HEIGHT / total_height if total_height > 0 else 0
        scrollbar_x = self.WIDTH - 20
        scrollbar_y = 0
        dragging = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.running = False
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
                    scrollbar_y = max(0, min(self.HEIGHT - scrollbar_height, mouse_y))
                    scroll_offset = (scrollbar_y / (self.HEIGHT - scrollbar_height)) * max_scroll
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        self.running = False

            # Check if 3 seconds have passed
            if pygame.time.get_ticks() - start_ticks >= display_duration:
                running = False
                self.running = False

            self.window.fill((255, 255, 255))

            # Render title
            title_text = self.SCORE_TITILE_FONT.render("Total Games Score", True, (0, 0, 0))
            self.window.blit(title_text, (self.WIDTH // 2 - title_text.get_width() // 2, 20))

            start_y = 100 - scroll_offset

            if total_scores:
                # Render total game scores with scroll
                for i, node in enumerate(total_scores):
                    score_text = self.SCORE_WORD_FONT.render(f"{i+1}. {node.word}: {node.score} points", True, (0, 0, 0))
                    self.window.blit(score_text, (50, start_y + i * line_spacing))
            else:
                # Display no games played
                message = "No games played"
                message_text = self.SCORE_WORD_FONT.render(message, True, (0, 0, 0))
                message_x = self.WIDTH // 2 - message_text.get_width() // 2
                message_y = start_y + 50
                self.window.blit(message_text, (message_x, message_y))

            # Draw scrollbar only if necessary
            if total_height > self.HEIGHT:
                # Draw scrollbar background
                pygame.draw.rect(self.window, (200, 200, 200), (scrollbar_x, 0, 20, self.HEIGHT))
                # Draw scrollbar handle
                pygame.draw.rect(self.window, (100, 100, 100), (scrollbar_x, scrollbar_y, 20, scrollbar_height))

            pygame.display.update()

        # After displaying, quit the game
        pygame.quit()
        exit()


    def show_play_again_screen(self):
        pygame.display.set_caption("Play Again")

        message_font = pygame.font.SysFont("comicsans", 40)
        button_font = pygame.font.SysFont("comicsans", 30)

        message_text = "Play again?"
        message_render = message_font.render(message_text, True, (0, 0, 0))

        message_x = self.WIDTH // 2 - message_render.get_width() // 2
        message_y = 100

        # Create buttons
        button_width = 100
        button_height = 50
        button_gap = 20

        total_buttons_width = button_width * 2 + button_gap
        start_x = self.WIDTH // 2 - total_buttons_width // 2

        reset_button_rect = pygame.Rect(start_x, 200, button_width, button_height)
        exit_button_rect = pygame.Rect(start_x + button_width + button_gap, 200, button_width, button_height)

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if reset_button_rect.collidepoint(mouse_pos):
                        # Reset the game completely
                        self.reset_full_game()
                        running = False
                    elif exit_button_rect.collidepoint(mouse_pos):
                        # Before exiting, save the current game score
                        self.save_current_game_score()
                        # Show total game scores
                        self.show_total_game_scores()
                        # Exit the game
                        running = False
                        self.running = False 

            # Drawing code
            self.window.fill((255, 255, 255))
            # Draw message
            self.window.blit(message_render, (message_x, message_y))

            # Draw buttons
            pygame.draw.rect(self.window, (0, 0, 0), reset_button_rect, 2)
            reset_text = button_font.render("Reset", True, (0, 0, 0))
            reset_text_x = reset_button_rect.centerx - reset_text.get_width() // 2
            reset_text_y = reset_button_rect.centery - reset_text.get_height() // 2
            self.window.blit(reset_text, (reset_text_x, reset_text_y))

            pygame.draw.rect(self.window, (0, 0, 0), exit_button_rect, 2)
            exit_text = button_font.render("Exit", True, (0, 0, 0))
            exit_text_x = exit_button_rect.centerx - exit_text.get_width() // 2
            exit_text_y = exit_button_rect.centery - exit_text.get_height() // 2
            self.window.blit(exit_text, (exit_text_x, exit_text_y))

            pygame.display.update()

        pygame.display.set_caption("Hangman Game")

    def save_current_game_score(self):
        if self.total_score_game > 0:
            partida_label = f"Partida {self.game_number}"
            self.total_scores_heap.insert(self.total_score_game, partida_label)
            self.game_number += 1
        self.total_score_game = 0 


    def reset_full_game(self): 
        # Save the total score of the current game
        self.save_current_game_score()

        # Reset game variables
        self.hangman_status = 0
        self.guessed = []
        self.hint_used = False
        self.letters = []
        self.total_score_game = 0

        # Reinitialize HashTable
        self.hash_table = HashTable()
        self.hash_table.add_words_from_file("pistas_ahorcado.csv")

        # Reinitialize MaxHeap
        self.max_heap = MaxHeap()

        # Load a new word
        self.load_new_word()
        self.create_buttons()

        # Recreate the game window
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Hangman Game")

        # Accept input
        self.accepting_input = True

        # Set running to True to continue the main game loop
        self.running = True

    def show_hint(self):
        hint_node = self.hash_table.search_word(self.word)

        if isinstance(hint_node, str):
            self.hint = "No hint available for this word."
        else:
            self.hint = hint_node.hint

        # Set maximum width for the hint window
        max_width = 800
        char_width = self.HINT_FONT.size("A")[0]
        hint_width = min(len(self.hint) * char_width + 40, max_width)
        hint_height = 150

        # Create a new window
        hint_window = pygame.display.set_mode((max_width, hint_height))
        pygame.display.set_caption("Hint")

        # Scrolling variables
        scroll_offset = 0
        max_scroll = max(0, len(self.hint) * char_width - max_width + 40)
        scrollbar_width = max_width * max_width / (max_width + max_scroll)
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
            hint_window.fill((255, 255, 255))

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
            if ltr not in self.guessed:
                self.guessed.append(ltr)
                for letter in self.letters:
                    if letter[2] == ltr and letter[3]:  
                        letter[3] = False  
                        if ltr not in self.word:  
                            self.hangman_status += 1 

    def run(self):
        while True:
            self.running = True
            while self.running:
                self.clock.tick(self.FPS)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        pygame.quit()
                        return
                    elif self.accepting_input:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.handle_mouse_click(pygame.mouse.get_pos())
                        elif event.type == pygame.KEYDOWN:
                            self.handle_key_press(event.key)

                self.draw()

                # Check if the game is won or lost
                if all(letter in self.guessed for letter in self.word):
                    self.accepting_input = False
                    self.hash_table.delete_word(self.word)
                    self.display_message("Loading next word...")
                    score = self.assign_scores()
                    self.max_heap.insert(score, self.word)
                    print(f"Inserted into MaxHeap: score= {score}, word = {self.word}")
                    self.reset_game()
                    self.accepting_input = True
                elif self.hangman_status == 7:
                    self.accepting_input = False
                    self.display_message("You LOST!!")
                    self.show_scores()
                    self.running = False

            # After the game is over, show play again screen
            self.show_play_again_screen()

            # If the user chose to exit, break out of the outer loop
            if not self.running:
                break

        pygame.quit()


if __name__ == "__main__":
    game = HangmanGame()
    game.run()
