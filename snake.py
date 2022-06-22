import random

import pygame
pygame.font.init()
class Apple:
    GREEN = (10,240,10)
    size = 25
    x = random.randint(100, 1100)
    y = random.randint(120, 600)

    def __init__(self):
        self.apple = pygame.Rect(self.x, self.y, self.size, self.size)
        self.applePic = pygame.transform.scale(pygame.image.load('apple.png'), (25, 25))

    def drawApple(self, screen):
        screen.blit(self.applePic, (self.apple.x, self.apple.y))

    def changePos(self):
        x = random.randint(100, 1100)
        y = random.randint(100, 600)
        self.apple.x = x
        self.apple.y = y

    def returnRect(self):
        return self.apple


class Snake:
    GREEN = (10,240,10)
    size = 30
    SPEED = 20
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.head = pygame.Rect(self.x, self.y, self.size, self.size)
        self.cells = [pygame.Rect(self.x - 4 * self.size, self.y,self.size, self.size),
                      pygame.Rect(self.x - 3 * self.size, self.y, self.size, self.size),
                      pygame.Rect(self.x - 2 * self.size, self.y,self.size, self.size),
                      pygame.Rect(self.x - self.size, self.y,self.size, self.size)]
        self.direction = 'Right'


    def displaySnake(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.head, border_radius=7)
        for i in range(len(self.cells)):
            pygame.draw.rect(screen,self.GREEN, self.cells[i], border_radius=7)


    def addCell(self):
        newRect = pygame.Rect(self.cells[0].x, self.cells[0].y, self.size, self.size)
        self.cells.insert(0, newRect)

    def changeDirection(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if self.direction != 'Left':
                self.direction = 'Right'

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if self.direction != 'Right':
                self.direction = 'Left'

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if self.direction != 'Down':
                self.direction = 'Up'

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if self.direction != 'Up':
                self.direction = 'Down'



    def moveSnake(self):

        self.changeDirection()

        for i in range(len(self.cells)):
            if i == len(self.cells) - 1:
                self.cells[i].x = self.head.x
                self.cells[i].y = self.head.y
            else:
                self.cells[i].x = self.cells[i + 1].x
                self.cells[i].y = self.cells[i + 1].y

        if self.direction == 'Right':
            self.head.x += self.SPEED

        if self.direction == 'Left':
            self.head.x -= self.SPEED

        if self.direction == 'Up':
            self.head.y -= self.SPEED

        if self.direction == 'Down':
            self.head.y += self.SPEED

    def eatApple(self, apple):
        if self.head.colliderect(apple.returnRect()):
            return True

    def outOfBounds(self):
        if self.head.x < 20 or self.head.x > 1175 or self.head.y < 100 or self.head.y > 680:
            return True
        for i in range(len(self.cells) - 1):
            if self.head == self.cells[i]:
                return True


class App:
    score = 0
    SCORE_FONT = pygame.font.SysFont('MalvaVariable-Italic', 70)
    ENDING_FONT = pygame.font.SysFont('MalvaVariable-Italic', 140)
    x = 340
    y = 300
    snakeMoving = True
    highScores = []
    def __init__(self):
        self.running = False
        self.clock = None
        self.screen = None
        self.snake = Snake(self.x, self.y)
        self.apple = Apple()

    def run(self):
        self.init()
        while self.running:
            self.clock.tick(24)
            self.render()
            self.update()
            pygame.display.update()


        self.cleanUp()

    def init(self):
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        self.running = True

    def update(self):
        self.events()
        if self.snake.outOfBounds():
            self.snakeMoving = False
            self.drawEnding()
            keys = pygame.key.get_pressed()
            self.highScores.append(self.score)
            if keys[pygame.K_r]:
                self.score = 0
                self.snakeMoving = True
                app = App()
                app.run()
            elif keys[pygame.K_q]:
                self.running = False

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def render(self):
        self.cleanUp()
        self.drawExtentions()
        self.snake.displaySnake(self.screen)
        if self.snakeMoving:
            self.snake.moveSnake()
        self.apple.drawApple(self.screen)
        if self.snake.eatApple(self.apple):
            self.apple.changePos()
            self.snake.addCell()
            self.score += 1


    def drawExtentions(self):
        str1 = 'Score: ' + str(self.score)
        str2 = 'High Score: '
        if len(self.highScores) == 0:
            str2 += str(0)
        else:
            str2 += str(max(self.highScores))

        score1 = self.SCORE_FONT.render(str1, False, (255, 255, 255))
        self.screen.blit(score1, (60, 10))

        score2 = self.SCORE_FONT.render(str2, False, (255, 255, 255))
        self.screen.blit(score2, (1130 - score2.get_width(), 10))

        upperBorder = pygame.Rect(0, 70, 1200, 10)
        pygame.draw.rect(self.screen, (255,255,255), upperBorder)

        lowerBorder = pygame.Rect(0, 690, 1200, 10)
        pygame.draw.rect(self.screen, (255, 255, 255), lowerBorder)

        leftBorder = pygame.Rect(0, 70, 10, 700)
        pygame.draw.rect(self.screen, (255, 255, 255), leftBorder)

        leftBorder = pygame.Rect(1190, 70, 10, 700)
        pygame.draw.rect(self.screen, (255, 255, 255), leftBorder)

    def drawEnding(self):
        str1 = "Game Over!"
        str2 = "Score: " + str(self.score)
        str3 = "Play Again - SPACE"
        str4 = "Quit - Q"


        ending1 = self.ENDING_FONT.render(str1, False, (255, 255, 255))
        self.screen.blit(ending1, (600 - ending1.get_width()/2, 210 - ending1.get_height()/2))

        ending2 = self.SCORE_FONT.render(str2, False, (255, 255, 255))
        self.screen.blit(ending2, (600 - ending2.get_width() / 2, 300 - ending2.get_height() / 2))

        ending3 = self.SCORE_FONT.render(str3, False, (255, 255, 255))
        self.screen.blit(ending3, (600 - ending3.get_width() / 2, 370 - ending3.get_height() / 2))

        ending4 = self.SCORE_FONT.render(str4, False, (255, 255, 255))
        self.screen.blit(ending4, (600 - ending4.get_width() / 2, 440 - ending4.get_height() / 2))

        keyboard = pygame.Rect(455, 505, 30, 13)
        pygame.draw.rect(self.screen, (0, 0, 0), keyboard)
        QKey = pygame.transform.scale(pygame.image.load('KEYBOARD.png'), (300, 133))
        self.screen.blit(QKey, (450, 500))

    def cleanUp(self):
        self.screen.fill(0)



if __name__ == "__main__":
    app = App()
    app.run()