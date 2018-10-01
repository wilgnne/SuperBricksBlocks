from bricks import *

import copy, time
class Snake():
    """docstring for snake"""
    def __init__(self):
        self.corpo = []
        self.dir = Vector2(1, 0)
        self.create()

    def create(self):
        x = 4
        self.corpo = []
        self.dir = Vector2(1, 0)
        for i in range(0,1):
            bk = GameObject(Vector2(x - i, 3))
            bk.setMesh([['2']])
            self.corpo.append(bk)

    def getBody(self):
        return self.corpo

    def add(self, point, total):
        npos = self.corpo[-1].position
        self.move(point, total)
        bk = GameObject(npos)
        bk.setMesh([['2']])
        self.corpo.append(bk)

    def move(self, point, total):
        pos1 = copy.copy(self.corpo[0].position)
        pos1.translate(self.dir)
        npos = []
        npos.append(pos1)
        for id, elem in enumerate(self.corpo):
            if id > 0:
                npos.append(self.corpo[id - 1].position)

        for x, y in enumerate(npos):
            self.corpo[x].position = y

        if self.corpo[0].position.x == point.position.x and self.corpo[0].position.y == point.position.y:
            point.position = randomVector2(self.corpo)
            self.add(point, total)
            total = total + 1
        return total

class game():
    """docstring for SnakeGame"""
    def __init__(self, enginne):
        self.enginne = enginne

    def gameplay(self):
        colors = {'1': (255,0,0),
                 '2': (155,184,165),
                 '3': (154,205,50),
                 '4': (255,165,0),
                 '5': (147,112,219)}
        snake = Snake()
        lifes = 4
        up = Vector2(0, -1)
        down = Vector2(0, 1)
        leaft = Vector2(1, 0)
        rigt = Vector2(-1, 0)
        velSnake = 0

        point = GameObject(randomVector2())
        point.setMesh([['1']])
        pointFrame = 0
        contFrame = 0
        framerate = 1.0/60
        now = time.time()
        nextFramerate = now + framerate
        t= 0
        f = 0
        deltatime = framerate
        total = 0
        exit = False
        while exit == False and lifes > 0:
            t = time.time()

            for event in self.enginne.getEvents():
                if event.type == self.enginne.pg.KEYDOWN:
                    if event.key == self.enginne.pg.K_ESCAPE:
                        exit = True

                    elif event.key == self.enginne.pg.K_d and (snake.dir.y == -1 or snake.dir.y == 1):
                        snake.dir = leaft
                    elif event.key == self.enginne.pg.K_a and (snake.dir.y == -1 or snake.dir.y == 1):
                        snake.dir = rigt
                    elif event.key == self.enginne.pg.K_w and (snake.dir.x == -1 or snake.dir.x == 1):
                        snake.dir = up
                    elif event.key == self.enginne.pg.K_s and (snake.dir.x == -1 or snake.dir.x == 1):
                        snake.dir = down

            if velSnake >= 0.2:
                total = snake.move(point, total)
                velSnake = 0
            else:
                velSnake += deltatime

            if contFrame >= 0.1:
                if pointFrame < 1:
                    pointFrame += 1
                else:
                    pointFrame = 0
                contFrame = 0
            else:
                contFrame += deltatime
            point.setMesh(self.plot(pointFrame))

            for elem in snake.corpo:
                if elem != snake.corpo[0]:
                    if snake.corpo[0].position.x == elem.position.x and snake.corpo[0].position.y == elem.position.y:
                        lifes = self.die(lifes, snake.corpo[0])
                        snake.create()
            if snake.corpo[0].position.x > 9 or snake.corpo[0].position.x < 0 or snake.corpo[0].position.y > 19 or snake.corpo[0].position.y < 0:
                lifes = self.die(lifes, snake.corpo[0])
                snake.create()

            self.enginne.display.overlap(snake.getBody() + [point], colors)
            self.enginne.display.pointWall(self.enginne.lifeBricks(lifes))
            self.enginne.display.attScore(int(total))

            while now < nextFramerate:
                time.sleep(nextFramerate - now)
                now = time.time()
            nextFramerate += framerate
            f = time.time()
            deltatime = f - t

        return int(total)

    def die(self, life, p):
        life = life - 1
        pos = p.position
        if p.position.x >= 9 :
            pos.x = pos.x - 4
        elif p.position.x <= 1:
            pos.x = pos.x + 1
        if p.position.y >= 18:
            pos.y = pos.y - 4
        elif p.position.y <= 1:
            pos.y = pos.y + 1
        for cont in range(0, 2):
            anim = GameObject(pos)
            anim.setMesh(self.enginne.dieBricks(cont))
            self.enginne.display.overlap([anim])
            time.sleep(0.2)
        return life
    def plot(self, frame):
        if frame == 1:
            return [['1']]
        if frame == 0:
            return [['0']]
        return [['1']]

def init(enginne):
    G = game(enginne)
    return G.gameplay()