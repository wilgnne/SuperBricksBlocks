from bricks import *
import time, math, random
class game():
    """docstring for Topgear"""
    def __init__(self, enginne):
        self.enginne = enginne

    def pista(self, x):
        if x == 2:
            return [['0', '0', '0', '0', '0', '4', '4', '4', '4', '4']]
        elif x == 1:
            return [['4', '0', '0', '0', '0', '0', '4', '4', '4', '4']]
        elif x == 0:
            return [['4', '4', '0', '0', '0', '0', '0', '4', '4', '4']]
        elif x == -1:
            return [['4', '4', '4', '0', '0', '0', '0', '0', '4', '4']]
        elif x == -2:
            return [['4', '4', '4', '4', '0', '0', '0', '0', '0', '4']]
        elif x == -3:
            return [['4', '4', '4', '4', '4', '0', '0', '0', '0', '0']]

        return [['2', '2', '0', '0', '0', '0', '0', '2', '2', '2']]


    def gerador(self, point, T = 2, A = 2.5, D = -0.5):
        rad = math.radians(point)
        c = math.cos((2*math.pi) * (rad/T))
        c = (c * A) + D
        return c

    def periodo(self, point):
        rad = math.radians(point)
        c = math.cos((2*math.pi) * (rad/10))
        c = (c * 0.5) + 3
        return c

    def amplitude(self, point):
        rad = math.radians(point)
        c = math.sin((2*math.pi) * (rad))
        c = (c * 1) + 1.1
        return c

    def checkCurveL(self, player, road):
        road1 = road[player.position.y]
        road = road[player.position.y + len(player.mesh) - 1]
        ident = 0
        ident1 = 0
        for a in road.mesh[0]:
            if a != '0':
                ident += 1
            else:
                break
        for a in road1.mesh[0]:
            if a != '0':
                ident1 += 1
            else:
                break
        if player.position.x > ident and player.position.x > ident1:
            return True
        return False

    def checkCurveR(self, player, road):
        road1 = road[player.position.y]
        road = road[player.position.y + len(player.mesh) - 1]
        ident = 0
        ident1 = 0
        for a in road.mesh[0]:
            if a != '0':
                ident += 1
            else:
                break
        for a in road1.mesh[0]:
            if a != '0':
                ident1 += 1
            else:
                break
        ident = 5 - ident
        ident1 = 5 - ident1
        if player.position.x + len(player.mesh[0]) < 10 - ident and player.position.x + len(player.mesh[0]) < 10 - ident1:
            return True
        return False

    def checkCol(self, player, road):
        road = road[player.position.y]
        if road.mesh[0][player.position.x] != '0':
            return (True, 0)
        elif road.mesh[0][player.position.x + len(player.mesh[0]) - 1] != '0':
            return (True, 1)
        return (False, 0)


    def gameplay(self):

        colors = {'1': (0,191,255),
		  '2': (155,184,165),
		  '3': (154,205,50),
		  '4': (255,165,0),
		  '5': (147,112,219)}

        meshCar = [['0', '2', '0'], ['2', '2', '2'], ['0', '2', '0'], ['2', '0', '2']]
        player = GameObject(Vector2(2, 14))
        player.setMesh(meshCar)

        roadList = []
        cont = 0
        lifes = 4

        frameAtt = 20

        for x in range(0,20):
            r = GameObject(Vector2(0, x))
            p = self.periodo(frameAtt)
            a = self.amplitude(frameAtt)
            g = self.gerador(frameAtt, p, a)
            r.setMesh(self.pista(int(g)))
            roadList.append(r)
            frameAtt -= 1

        frameAtt = frameAtt+20

        speed = 0
        framerate = 1.0/60
        now = time.time()
        nextFramerate = now + framerate
        t= 0
        f = 0
        deltatime = framerate
        self.bech = []
        total = 0
        exit = False
        while exit == False and lifes > 0:
        #for x in range(0, 100):
            t = time.time()

            if speed > 0.01:
                for a in roadList:
                    a.position.translate(Vector2(0, 1))
                del(roadList[-1])
                r = GameObject(Vector2(0, 0))
                a = self.amplitude(frameAtt)
                p = self.periodo(frameAtt)
                g = self.gerador(frameAtt, p, a)
                r.setMesh(self.pista(int(g)))
                frameAtt += 1
                roadList.insert(0, r)

                speed = 0
            else:
                speed += deltatime


            for event in self.enginne.getEvents():
                if event.type == self.enginne.pg.KEYDOWN:
                    if event.key == self.enginne.pg.K_ESCAPE:
                        exit = True
                    elif event.key == self.enginne.pg.K_d and player.position.x < 6 and self.checkCurveR(player, roadList):
                        player.position.translate(Vector2(1, 0))
                    elif event.key == self.enginne.pg.K_a and player.position.x > 1 and self.checkCurveL(player, roadList):
                        player.position.translate(Vector2(-1, 0))

            check = self.checkCol(player, roadList)
            if check[0] == True:
                lifes = self.die(lifes, player, roadList, colors)
                if check[1] == 0:
                    player.position.translate(Vector2(1, 0))
                if check[1] == 1:
                    player.position.translate(Vector2(-1, 0))


            self.enginne.display.overlap(roadList +[player], colors)
            self.enginne.display.pointWall(self.enginne.lifeBricks(lifes))
            self.enginne.display.attScore(int(total/1))

            while now < nextFramerate:
                time.sleep(nextFramerate - now)
                now = time.time()
            nextFramerate += framerate
            f = time.time()
            deltatime = f - t
            total += deltatime
            self.bech.append(1.0/deltatime)
        return int(total/1)

    def die(self, life, p, road, colors):
        life = life - 1
        for cont in range(0, 2):
            anim = GameObject(p.position)
            anim.setMesh(self.enginne.dieBricks(cont))
            self.enginne.display.overlap(road + [anim], colors)
            time.sleep(0.5)
        return life


def init(enginne):
    G = game(enginne)
    return G.gameplay()