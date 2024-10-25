# Hangman Game
# Autores:
# Martin Eduardo Chacon Orduño - 351840
#
# 30/09/2024

import pygame


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
for i in range(26):
    x = startX + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = startY + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y])


# images
images = []
for i in range(6):
    imgUrl = "img\hangman" + str(i) + ".png"
    images.append(pygame.image.load(imgUrl))



# game variables
hangmanStatus = 0

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# game loop
FPS = 60
clock = pygame.time.Clock()
run  = True

def draw():
    window.fill(WHITE)

    for letter in letters:
        x, y = letter
        pygame.draw.circle(window, BLACK, (x, y), RADIUS, 3)

    window.blit(images[hangmanStatus], (150, 100))
    pygame.display.update()

while run:
    clock.tick(FPS)
    draw()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            print(pos)

pygame.quit()