import pygame, sys, random

pygame.init()

width = 890
height = 660
screen = pygame.display.set_mode([width, height])

pygame.display.set_caption('MemoryGame')

'''Pictures from https://pixabay.com/'''  # TODO: Need 12 cards
card_back = pygame.image.load("./resources/cardBack.png").convert_alpha()
card_fox = pygame.image.load("./resources/cardFox.png").convert_alpha()
card_dachshund = pygame.image.load("./resources/cardDachshund.png").convert_alpha()
card_moose = pygame.image.load("./resources/cardMoose.png").convert_alpha()
card_bear = pygame.image.load("./resources/cardBear.png").convert_alpha()

cardSize = card_back.get_rect().size

allCardsList = [card_fox, card_dachshund, card_moose, card_bear]

class Card:
    def __init__(self, x, y, picture):
        self.x = x
        self.y = y
        self.pic = picture
        self.card = card_back

    def mouse(self, pos, click):  # TODO: Think how to make hover

        if self.x + cardSize[0] > pos[0] > self.x and self.y + cardSize[1] > pos[1] > self.y:
            if click[0] == 1:
                self.card = self.pic

    def ifClicked(self):  # Not sure if it is important
        if self.card == self.pic:
            return True
        else:
            return False

    def drawCard(self, scren):
        scren.blit(self.card, [self.x, self.y])

class Cards:
    def __init__(self):
        self.cards1 = []
        self.cards2 = []

    def board(self):  # TODO: Find if there is any bugs and check if it works correctly
        coordinates = makeGrid()
        for card in allCardsList:
            position = random.randint(0, len(coordinates)-1)
            self.cards1.append(Card(coordinates[position][0], coordinates[position][1], card))
            coordinates.pop(position)
            position = random.randint(0, len(coordinates)-1)
            self.cards2.append(Card(coordinates[position][0], coordinates[position][1], card))
            coordinates.pop(position)

    def mouse(self, pos, click):
        for cardmouse in self.cards1:
            cardmouse.mouse(pos, click)
        for cardmouse2 in self.cards2:
            cardmouse2.mouse(pos, click)

    def drawBoard(self, display):
        for draw in self.cards1:
            draw.drawCard(display)
        for draw2 in self.cards2:
            draw2.drawCard(display)

def makeGrid():
    gridList = []

    for i in range(4):  # cards in vertical |
        y = 80 + (i*10)
        y += i*cardSize[1]
        for j in range(6):  # cards in horizontal --
            x = 30 + (j*10)
            x += j*cardSize[0]
            f = x, y
            gridList.append(f)

    random.shuffle(gridList)
    return gridList

def playGame():
    pass

kaartid = Cards()  # For testing
kaartid.board()

while True:
    screen.fill([255, 255, 255])
    pygame.draw.line(screen, [0,0,0], [0, 70], [width, 70])  # Remove this

    kaartid.drawBoard(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            kaartid.mouse(pygame.mouse.get_pos(), pygame.mouse.get_pressed())

    pygame.display.flip()
