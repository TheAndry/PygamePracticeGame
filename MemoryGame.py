import pygame, sys

pygame.init()

width = 870 #TODO Find the best size
height = 600
screen = pygame.display.set_mode([width, height])

pygame.display.set_caption('MemoryGame')

card_back = pygame.image.load("./resources/cardBack.png").convert_alpha()
card_fox = pygame.image.load("./resources/cardFox.png").convert_alpha()
card_dachshund = pygame.image.load("./resources/cardDachshund.png").convert_alpha() #TODO Fix the picture

allcards = [card_fox, card_dachshund]

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

class Cards:
    def __init__(self):
        self.cards1 = []
        self.cards2 = []

    def cardBoard(self): #TODO Finish the function and make it work correctly
        x = 10
        y = 10
        for card in allcards:
            self.cards1.append(Card(x, y, card))
            x += 140
            print(self.cards1) #For testing list

    def mouse(self, pos, click):
        for cardmouse in self.cards1:
            cardmouse.mouse(pos, click)

    def drawBoard(self, display):
        for draw in self.cards1:
            draw.drawCard(display)

def playGame():
    pass

kaartid = Cards() #For testing
kaartid.cardBoard()

while True:
    screen.fill([255, 255, 255])

    kaartid.drawBoard(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            kaartid.mouse(pygame.mouse.get_pos(), pygame.mouse.get_pressed())

    pygame.display.flip()
