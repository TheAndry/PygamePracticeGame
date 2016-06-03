# -*- coding: utf-8 -*-
import sys, random, time
import pygame


__author__ = ('Andry Kõre')

pygame.init()
WIDTH = 890
HEIGHT = 660
gameScreen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('MemoryGame')

# TODO: Try to make image thing better
'''Pictures from https://pixabay.com/'''  # TODO: Need 12 cards
card_back = pygame.image.load('./resources/cardBack.png').convert_alpha()
card_fox = pygame.image.load('./resources/cardFox.png').convert_alpha()
card_dachshund = pygame.image.load('./resources/cardDachshund.png').convert_alpha()
card_moose = pygame.image.load('./resources/cardMoose.png').convert_alpha()
card_bear = pygame.image.load('./resources/cardBear.png').convert_alpha()
menu_image = pygame.image.load('./resources/gameMenu.png').convert()
memory_text = pygame.image.load('./resources/memoryGameText.png').convert_alpha()

cardSize = card_back.get_rect().size

allCardsList = [card_fox ] # card_dachshund, card_bear, card_moose


def Text(screen, text, size, color, coords):
    lfont = pygame.font.SysFont('Arial Bold', size)
    labl = lfont.render(text, 1, color)
    screen.blit(labl, coords)


class Card:
    def __init__(self, x, y, picture):
        global clickable, pause
        self.x = x
        self.y = y
        self.pic = picture
        self.card = card_back
        self.commenceaction = False
        clickable = True
        pause = False

    def mouse(self, pos, click):  # TODO: Think how to make hover
        global last
        if not pause:
            if clickable:
                if self.x + cardSize[0] > pos[0] > self.x and self.y + cardSize[1] > pos[1] > self.y:
                    if click[0]:
                        last = pygame.time.get_ticks()
                        self.card = self.pic
                        if self in mouseClicks:
                            pass
                        elif self in openedCards:
                            pass
                        else:
                            mouseClicks.append(self)

    def flipBack(self):
        self.card = card_back
        
    def drawCard(self, scren):
        scren.blit(self.card, [self.x, self.y])


class Button:
    def __init__(self, xpos, ypos, height, width, buttontext, regularcolor, hovercolor, clickcolor, function, size=30, textfont='Arial Bold'):
        global clickableButton
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
        self.font = pygame.font.SysFont(textfont, size)
        self.textcontent = self.font.render(self.buttontext, 1, (10, 10, 10))
        self.textposition = pygame.Rect((self.xpos, self.ypos), (self.width, self.height))
        self.textposition[0] = self.xpos + ((self.width - self.textcontent.get_width()) / 2)
        self.textposition[1] = self.ypos + ((self.width - self.textcontent.get_height()) / 6)
        clickableButton = True

    def mousemovement(self, position, key):
        if clickableButton:
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

    def clearList(self):
        del self.cards[:]


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
    fade = 3
    end = 4


class Game:
    def __init__(self, screen):  # TODO: Make this area better
        global mouseClicks, openedCards
        self.currentStatus = Status.menu
        self.currentScreen = screen
        self.screenRect = self.currentScreen.get_rect()
        self.cards = Cards()
        self.correct = None
        self.clickNow = 0
        self.t1 = 0
        self.playtime = 0
        self.clickedTime = 0
        self.addTime = False
        self.timerPause = False
        self.clock = pygame.time.Clock()
        self.clock2 = pygame.time.Clock()
        self.clock3 = pygame.time.Clock()
        self.surface = pygame.Surface((WIDTH, HEIGHT))
        self.surface.fill((0, 255, 0))
        self.surfaceAlpha = 0
        self.ajutised_ajad = []
        openedCards = []
        mouseClicks = []

    def makeGrid(self):
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

    def turnCards(self):
        global clickable, last
        if len(mouseClicks) == 2:
            pygame.display.flip()
            if mouseClicks[0].pic is mouseClicks[1].pic:
                self.correct = True
                openedCards.append(mouseClicks[0]); openedCards.append(mouseClicks[1])
                del mouseClicks[:]
            else:
                clickable = False
                self.correct = False
                self.clickNow = pygame.time.get_ticks()
                if self.clickNow - last >= 1200:
                    self.correct = None
                    last = self.clickNow
                    clickable = True
                    mouseClicks[0].flipBack(); mouseClicks[1].flipBack()
                    del mouseClicks[:]

    def correctWrong(self):
        if self.correct:
            self.clickNow = pygame.time.get_ticks()
            Text(self.currentScreen, 'CORRECT', 50, (0, 220, 0), (self.screenRect.centerx-40, 26))
            if self.clickNow - last >= 1200:
                self.correct = None
        elif self.correct == False:
            Text(self.currentScreen, 'WRONG', 50, (255, 0, 0), (self.screenRect.centerx-40, 26))

    def ifOpened(self):
        if len(openedCards) == len(allCardsList)*2:
            if not self.addTime:
                self.ajutised_ajad.append(self.playtime)
                self.addTime = True
            self.currentStatus = Status.fade

    def timer(self):
        if not self.timerPause:
            if pause:
                self.t1 = self.clock2.tick()
            else:
                milliseconds = (self.now - self.t1)
                seconds = milliseconds / 1000
                self.playtime += seconds
                self.t1 = 0

    def showMenu(self):
        global buttons
        self.currentStatus = Status.menu
        self.cards.clearList()
        self.playtime = 0
        self.correct = None
        self.addTime = False
        self.timerPause = False
        self.surfaceAlpha = 0
        del openedCards[:]
        del mouseClicks[:]
        buttons = Allbuttons([
            Button(self.screenRect.centerx-(100/2), self.screenRect.centery-80, 40, 100, 'PLAY', (0,210,00), (10,240,110), (160,245,225), self.startGame),
            Button(self.screenRect.centerx-(100/2), self.screenRect.centery-30, 40, 100, 'INFO', (0,210,00), (10,240,110), (160,245,225), self.showMenu),  # TODO: Make info tab
            Button(self.screenRect.centerx-(100/2), self.screenRect.centery+20, 40, 100, 'EXIT', (0,210,00), (10,240,110), (160,245,225), self.quitGame)
            ])
        #pygame.mixer.music.stop()
        #pygame.mixer.music.load(BACKGROUND MUSIC)
        #pygame.mixer.music.play(-1)

    def startGame(self):
        global buttons
        self.currentStatus = Status.game
        self.cards.board(self.makeGrid())
        buttons = Allbuttons([
            Button(810, 25, 30, 70, 'EXIT', (0,210,00), (10,240,110), (160,245,225), self.quitGame, 26),
            Button(725, 25, 30, 70, 'PAUSE', (0,210,00), (10,240,110), (160,245,225), self.goPause, 26),
            Button(640, 25, 30, 70, 'BACK', (0,210,00), (10,240,110), (160,245,225), self.showMenu, 26)
            ])
        #pygame.mixer.music.stop()
        #pygame.mixer.music.load(BACKGROUND MUSIC WHILE PLAYING)
        #pygame.mixer.music.play(-1)

    def goPause(self):
        global pause
        if pause:
            pause = False
        else:
            pause = True
        #pygame.mixer.music.pause()

    def goFade(self):
        global clickableButton
        self.surfaceAlpha = min(255, self.surfaceAlpha + (self.now/1000) * 210)
        self.surface.set_alpha(self.surfaceAlpha)
        self.currentScreen.blit(self.surface, (0, 0))
        self.timerPause = True
        clickableButton = False
        if self.surfaceAlpha == 255:
            self.gameEnd()

    def gameEnd(self):
        global buttons, clickableButton
        self.currentStatus = Status.end
        clickableButton = True
        print(self.ajutised_ajad)
        buttons = Allbuttons([
            Button(100, 100, 30, 70, 'To menu', (0,210,00), (10,240,110), (160,245,225), game.showMenu, 26)
        ])
        #sound = pygame.mixer.Sound(GAME END SOUND)
        #sound.play()
        #pygame.mixer.music.stop()

    def quitGame(self):
        pygame.quit()
        sys.exit()

    def updateScreen(self):
        global buttons, last
        self.now = self.clock.tick()

        if self.currentStatus == Status.menu:
            self.currentScreen.blit(menu_image, (0, 0))
            buttons.drawbutton(self.currentScreen)
            pygame.display.flip()

        elif self.currentStatus == Status.game or self.currentStatus == Status.fade:  # Make time tick
            buttons.drawbutton(self.currentScreen)
            self.currentScreen.blit(memory_text, (10, 20))
            pygame.draw.line(self.currentScreen, [0, 0, 0], [0, 70], [WIDTH, 70])
            self.cards.drawBoard(self.currentScreen)
            self.timer()
            Text(self.currentScreen, str(round(self.playtime, 1)), 40, (225, 0, 0), (self.screenRect.centerx-140, 32))
            if pause:
                Text(self.currentScreen, 'GAME PAUSED', 70, (225, 0, 0), (self.screenRect.centerx-180, self.screenRect.centery))
            self.correctWrong()
            self.turnCards()
            self.ifOpened()
            if self.currentStatus == Status.fade:
                self.goFade()
            pygame.display.flip()
            self.currentScreen.fill([255, 220, 153])

        elif self.currentStatus == Status.end:
            self.currentScreen.fill([0, 255, 0])
            buttons.drawbutton(self.currentScreen)
            Text(self.currentScreen, 'Game completed!', 70, (0, 0, 0), (0, 0))
            pygame.display.flip()


game = Game(gameScreen)
game.showMenu()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            buttons.mousemovement(pygame.mouse.get_pos(), pygame.mouse.get_pressed())
 
        if event.type == pygame.MOUSEBUTTONDOWN:
            game.cards.mouse(pygame.mouse.get_pos(), pygame.mouse.get_pressed())

    game.updateScreen()



