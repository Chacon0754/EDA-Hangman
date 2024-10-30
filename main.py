# Hangman Game
# Autores:
# Martin Eduardo Chacon Orduño - 351840
#
# 30/09/2024

import pygame
import math
import random


# display
pygame.init()
WIDTH, HEIGHT = 800, 500
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game")

# button variables
RADIUS = 20
GAP = 15
letters = [] 
startX = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
startY = 400
A = 65
B = 66

for i in range(26):
    x = startX + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = startY + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

# fonts
LETTERFONT = pygame.font.SysFont('comicsans', 40)
WORDFONT = pygame.font.SysFont('comicsans', 45)
TITLEFONT = pygame.font.SysFont('comicsans', 70)

# images
images = []
for i in range(8):
    imgUrl = "img\hangman" + str(i) + ".png"
    image = pygame.image.load(imgUrl)

    scaledImage = pygame.transform.scale(image, (400, int(image.get_height() * (200 / image.get_width()))))
    images.append(scaledImage)
backgroundColor = images[0].get_at((10, 10))



# game variables
hangmanStatus = 0
words = ["HELLO ", "PYTHON", "PYGAME", "IDE"]
word = random.choice(words)
guessed = []

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)



def draw():
    window.fill(backgroundColor)

    # draw title
    text = TITLEFONT.render("HANGMAN", 1, BLACK)
    window.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))
    # draw word
    displayWord = ""
    for letter in word:
        if letter in guessed:
            displayWord += letter + " "
        else:
            displayWord +="_ "
    text = WORDFONT.render(displayWord, 1, BLACK)
    window.blit(text, (400, 200))

    # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible: 
            pygame.draw.circle(window, BLACK, (x, y), RADIUS, 3)
            text = LETTERFONT.render(ltr, 1, BLACK)
            window.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    window.blit(images[hangmanStatus], (0, 120))
    pygame.display.update()

def displayMessage(message):
    pygame.time.delay(1000)
    window.fill(backgroundColor)
    text = WORDFONT.render(message, 1, BLACK)
    window.blit(text, (WIDTH / 2 - text.get_width(), HEIGHT  / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    # game loop variables
    FPS = 60
    clock = pygame.time.Clock()
    run  = True

    while run:
        global hangmanStatus
        clock.tick(FPS)

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mX, mY = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - mX)**2 + (y - mY)**2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangmanStatus += 1

            if event.type == pygame.KEYDOWN:
                keyPressed = event.key
                if pygame.K_a <= keyPressed <= pygame.K_z:
                    ltr = chr(keyPressed).upper()
                    for letter in letters:
                        if letter[2] == ltr and letter[3]:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangmanStatus += 1
        
        draw()
        
        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break
        if won:
            displayMessage("You Won!")
            break
        if hangmanStatus == 7:
            displayMessage("You LOST!!")
            break
            

main()
pygame.quit()