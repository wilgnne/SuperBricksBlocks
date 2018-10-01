from bricks import *
import random, copy, time
class SolidBlock():
    """docstring for SolidBlock"""
    def __init__(self):
        self.init()

    def init(self):
        self.solid = []
        self.gameObject = GameObject()
        self.gameObject.setMesh(self.solid)
        for i in range(0,20):
            linha = []
            for j in range(0,10):
                linha.append('0')
            self.solid.append(linha)

    def checkCol(self, obj):

        if self.solid[0].count('0') != 10:
            self.init()

        base = copy.copy(obj.mesh[-1])
        posY = obj.position.y + len(obj.mesh) - 1

        for linha in range(len(obj.mesh)):
            for elem in range(len(obj.mesh[0])):
                posY = obj.position.y + linha
                posX = obj.position.x + elem

                if posY + 1 < 20:
                    if obj.mesh[linha][elem] != '0' and self.solid[posY+1][posX] != '0':
                        return self.add(obj)
        return False

    def checkArownd(self, obj):
        posY = obj.position.y + len(obj.mesh) - 1

        for linha in range(len(obj.mesh)):
            for elem in range(len(obj.mesh[0])):
                posY = obj.position.y + linha
                posX = obj.position.x + elem

                if posX + 1 < 10:
                    if obj.mesh[linha][elem] != '0' and (self.solid[posY][posX + 1] != '0' or self.solid[posY][posX - 1] != '0'):
                        return False
        return True


    def add(self, obj):
        for linha in range(0, len(obj.mesh)):
            for elem in range(0, len(obj.mesh[0])):
                if obj.mesh[linha][elem] != '0':
                    self.solid[linha + obj.position.y][elem + obj.position.x] = str(obj.mesh[linha][elem])
        self.gameObject.setMesh(self.solid)
        return True

    def checkSolid(self, points):
        new = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        for i in range(len(self.solid)):
            if self.solid[i].count('0') == 0:
                self.solid.remove(self.solid[i])
                self.solid.insert(0, new)
                points += 10
        return points

class game():
    """docstring for game"""
    def __init__(self, enginne):
        self.enginne = enginne

    def gameplay(self):
        colors = {'1': (0,191,255),
                 '2': (155,184,165),
                 '3': (154,205,50),
                 '4': (255,165,0),
                 '5': (147,112,219)}
        player = self.randomBlock()

        nextblock = self.randomBlock()

        solidBlocks = SolidBlock()
        vel = 1
        cont = 0
        framerate = 1.0/120
        now = time.time()
        nextFramerate = now + framerate
        t= 0
        f = 0
        deltatime = framerate
        total = 0
        exit = False
        while exit == False:
            t = time.time()
            if player.position.y + len(player.mesh) == 20 or solidBlocks.checkCol(player):
                solidBlocks.add(player)
                total = solidBlocks.checkSolid(total)
                player = nextblock
                nextblock = self.randomBlock()

            for event in self.enginne.getEvents():
                if event.type == self.enginne.pg.KEYDOWN:
                    if event.key == self.enginne.pg.K_ESCAPE:
                        exit = True
                    elif event.key == self.enginne.pg.K_SPACE:
                        player.fazgirar()
                    elif event.key == self.enginne.pg.K_d and player.position.x < (10 - len(player.mesh[0])) and solidBlocks.checkArownd(player):
                        player.position.translate(Vector2(1, 0))
                    elif event.key == self.enginne.pg.K_a and player.position.x > 0 and solidBlocks.checkArownd(player):
                        player.position.translate(Vector2(-1, 0))
            vel = 1
            key = self.enginne.pg.key.get_pressed()  #checking pressed keys
            if key[self.enginne.pg.K_s] and player.position.x < 15:
                vel = 0.05

            if cont >= vel:
                player.position.translate(Vector2(0, 1))
                cont = 0
            else:
                cont += deltatime

            self.enginne.display.overlap([solidBlocks.gameObject, player], colors)
            self.enginne.display.pointWall(nextblock.mesh, colors)
            self.enginne.display.attScore(int(total))

            while now < nextFramerate:
                time.sleep(nextFramerate - now)
                now = time.time()
            nextFramerate += framerate
            f = time.time()
            deltatime = f - t
        return int(total)

    def block(self, tam):
        if tam == 0:
            return [['1', '1'],
                    ['1', '1']]
        if tam == 1:
            return [['2', '0', '0'],
                   ['2', '2', '2']]
        if tam == 2:
            return [['3', '3', '3', '3']]
        if tam == 3:
            return [['4', '4', '0'],
                   ['0', '4', '4']]
        if tam == 4:
            return [['0', '5', '0'],
                   ['5', '5', '5']]

    def randomBlock(self):
        mesh = self.block(random.randint(0, 4))
        go = GameObject(Vector2(3, 0))
        go.setMesh(mesh)
        for i in range(0, random.randint(0, 4)):
            go.fazgirar()
        return go

def init(enginne):
    G = game(enginne)
    return G.gameplay()