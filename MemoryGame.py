import pygame, sys

pygame.init()

width = 870 #TODO Find the best size
height = 600
screen = pygame.display.set_mode([width, height])

pygame.display.set_caption('MemoryGame')

card_back = pygame.image.load("./resources/cardBack.png").convert_alpha()
card_fox = pygame.image.load("./resources/cardFox.png").convert_alpha()

allcards = [card_back, card_fox]

class Card:
    def __init__(self, x, y, picture):
        self.x = x
        self.y = y
        self.pic = picture
        self.card = card_back

    def mouse(self, pos, click):  #TODO Think how to make hover
        size = self.card.get_rect().size
        if self.x + size[0] > pos[0] > self.x and self.y + size[1] > pos[1] > self.y:
            if click[0] == 1:
                self.card = self.pic

    def drawCard(self, scren):
        scren.blit(self.card, [self.x, self.y])


card = Card(10, 10, card_fox)

while True:
    screen.fill([255, 255, 255])

    card.drawCard(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            card.mouse(pygame.mouse.get_pos(), pygame.mouse.get_pressed())

    pygame.display.flip()
