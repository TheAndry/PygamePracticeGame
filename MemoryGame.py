# -*- coding: utf-8 -*-
import sys, random, time
import pygame


__author__ = ("Andry Kõre")

pygame.init()
WIDTH = 890
HEIGHT = 660
gameScreen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('MemoryGame')
time = pygame.time.Clock()

# TODO: Try to make image thing better
'''Pictures from https://pixabay.com/'''  # TODO: Need 12 cards
card_back = pygame.image.load("./resources/cardBack.png").convert_alpha()
card_fox = pygame.image.load("./resources/cardFox.png").convert_alpha()
card_dachshund = pygame.image.load("./resources/cardDachshund.png").convert_alpha()
card_moose = pygame.image.load("./resources/cardMoose.png").convert_alpha()
card_bear = pygame.image.load("./resources/cardBear.png").convert_alpha()
menu_image = pygame.image.load("./resources/gameMenu.png").convert()

cardSize = card_back.get_rect().size

allCardsList = [card_fox, card_dachshund]  # card_bear, card_moose Removed for testing


def Text(screen, text, size, color, coords):
    lfont = pygame.font.SysFont('Arial Bold', size)
    labl = lfont.render(text, 1, color)
    screen.blit(labl, coords)


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
                if self in game.mouseClicks:
                    pass
                elif self in game.openedCards:
                    pass
                else:
                    game.mouseClicks.append(self)
        
    def flipBack(self):
        self.card = card_back
        
    def drawCard(self, scren):
        scren.blit(self.card, [self.x, self.y])


class Button:
    def __init__(self, xpos, ypos, height, width, buttontext, regularcolor, hovercolor, clickcolor, function, textfont):
        self.function = function
        self.buttontext = buttontext
        self.currentcolor = regularcolor
        self.clickcolor = clickcolor
        self.hovercolor = hovercolor
        self.regularcolor = regularcolor
        self.width = width
        self.height = height
        self.ypos = ypos
        self.xpos = xpos
        self.commenceaction = False
        self.font = pygame.font.SysFont(textfont, 30)
        self.textcontent = self.font.render(self.buttontext, 1, (10, 10, 10))
        self.textposition = pygame.Rect((self.xpos, self.ypos), (self.width, self.height))
        self.textposition[0] = self.xpos + ((self.width - self.textcontent.get_width()) / 2)
        self.textposition[1] = self.ypos + ((self.width - self.textcontent.get_height()) / 6)

    def mousemovement(self, position, key):
        if self.xpos < position[0] < self.xpos + self.width and self.ypos < position[1] < self.ypos + self.height:
            if key[0]:
                self.currentcolor = self.clickcolor
                self.commenceaction = True
            else:
                self.currentcolor = self.hovercolor
                if self.commenceaction:
                    self.function()
                    self.commenceaction = False
        else:
            self.currentcolor = self.regularcolor

    def drawbutton(self, scren):
        pygame.draw.rect(scren, self.currentcolor, pygame.Rect((self.xpos, self.ypos), (self.width, self.height)))
        scren.blit(self.textcontent, self.textposition)


class Cards:
    def __init__(self):
        self.cards = []

    def board(self, grid):
        for card in allCardsList:
            for i in range(2):
                position = random.randint(0, len(grid)-1)
                self.cards.append(Card(grid[position][0], grid[position][1], card))
                grid.pop(position)

    def click(self):
        for cardclick in self.cards:
            cardclick.opened()

    def mouse(self, pos, click):
        for cardmouse in self.cards:
            cardmouse.mouse(pos, click)

    def drawBoard(self, display):
        for draw in self.cards:
            draw.drawCard(display)


class Allbuttons:
    def __init__(self, allthebuttons):
        self.buttons = allthebuttons

    def drawbutton(self, scren):
        for button in self.buttons:
            button.drawbutton(scren)

    def mousemovement(self, position, key):
        for button in self.buttons:
            button.mousemovement(position, key)


class Status():
    menu = 1
    game = 2
    end = 3
    pause = 4


class Game:
    def __init__(self, screen):
        self.currentStatus = Status.menu
        self.currentScreen = screen
        self.screenRect = self.currentScreen.get_rect()
        self.cards = Cards()
        self.openedCards = []
        self.mouseClicks = []
        self.gameBackground = None  # TODO: Make game background

    def makeGrid(self):  # Think where to put this
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

    def showMenu(self):
        global buttons
        self.currentStatus = Status.menu
        buttons = Allbuttons([
            Button(self.screenRect.centerx-(100/2), self.screenRect.centery-80, 40, 100, "PLAY", (0,210,00), (10,240,110), (160,245,225), game.startGame, 'Arial Bold'),  # Küsi, kuidas skippida mõndasid osasid funktsioonis
            Button(self.screenRect.centerx-(100/2), self.screenRect.centery-30, 40, 100, "INFO", (0,210,00), (10,240,110), (160,245,225), game.showMenu, 'Arial Bold'),
            Button(self.screenRect.centerx-(100/2), self.screenRect.centery+20, 40, 100, "EXIT", (0,210,00), (10,240,110), (160,245,225), game.quitGame, 'Arial Bold')
            ])
        #pygame.mixer.music.stop()
        #pygame.mixer.music.load(BACKGROUND MUSIC)
        #pygame.mixer.music.play(-1)

    def startGame(self):
        self.currentStatus = Status.game
        self.cards.board(self.makeGrid())
        #pygame.mixer.music.stop()
        #pygame.mixer.music.load(BACKGROUND MUSIC WHILE PLAYING)
        #pygame.mixer.music.play(-1)

    def goPause(self):
        self.currentStatus = Status.pause
        #pygame.mixer.music.pause()

    def backToGame(self):
        self.currentStatus = Status.game
        #pygame.mixer.music.unpause()

    def gameEnd(self):
        self.currentStatus = Status.end
        #sound = pygame.mixer.Sound(GAME END SOUND)
        #sound.play()
        #pygame.mixer.music.stop()

    def quitGame(self):
        pygame.quit()
        sys.exit()

    def turnCards(self):
        if len(self.mouseClicks) == 2:
            pygame.display.flip()
            if self.mouseClicks[0].pic is self.mouseClicks[1].pic:
                self.openedCards.append(self.mouseClicks[0]); self.openedCards.append(self.mouseClicks[1])
                del self.mouseClicks[:]
            else:
                pygame.time.wait(1500)
                self.mouseClicks[0].flipBack(); self.mouseClicks[1].flipBack()

                del self.mouseClicks[:]  # mouseClicks.clear()

    def ifOpened(self):
        if len(self.openedCards) == len(allCardsList)*2:
            self.gameEnd()

    def updateScreen(self):
        global buttons
        if self.currentStatus == Status.menu:
            self.currentScreen.blit(menu_image, (0, 0))
            buttons.drawbutton(self.currentScreen)
            pygame.display.flip()

        elif self.currentStatus == Status.game:  # Make time tick
            self.currentScreen.fill([255, 220, 153])
            pygame.draw.line(self.currentScreen, [0, 0, 0], [0, 70], [WIDTH, 70])
            self.cards.drawBoard(self.currentScreen)
            self.turnCards()
            self.ifOpened()

            pygame.display.flip()

        elif self.currentStatus == Status.end:  # TODO: Make green fade
            pygame.time.wait(600)
            self.currentScreen.fill([0, 207, 0])
            Text(self.currentScreen, 'Game completed!', 70, (0, 0, 0), (0, 0))
            pygame.display.flip()

        elif self.currentStatus == Status.pause:
            pass


game = Game(gameScreen)
game.showMenu()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game.currentStatus == Status.menu:
            if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                buttons.mousemovement(pygame.mouse.get_pos(), pygame.mouse.get_pressed())

        elif game.currentStatus == Status.game:
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.cards.mouse(pygame.mouse.get_pos(), pygame.mouse.get_pressed())

    game.updateScreen()



