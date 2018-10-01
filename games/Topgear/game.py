from bricks import *
import time, random
class game():
    """docstring for Topgear"""
    def __init__(self, enginne):
        self.enginne = enginne
        self.colors = {'1': (0,191,255),
                 '2': (155,184,165),
                 '3': (154,205,50),
                 '4': (255,165,0),
                 '5': (147,112,219)}

    def meshCar(self, c):
        return [['0', c, '0'], [c, c, c], ['0', c, '0'], [c, '0', c]]

    def randomMesh(self, colors):
        c = random.randint(1, len(colors))
        return self.meshCar(str(c))

    def gameplay(self):

        carList = []
        player = GameObject(Vector2(2, 16))
        player.setMesh(self.randomMesh(self.colors))

        road = [['4', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
                ['4', '0', '0', '0', '0', '0', '0', '0', '0', '4'],
                ['0', '0', '0', '0', '0', '0', '0', '0', '0', '4']]
        roadList = []
        cont = 0
        lifes = 4

        for x in range(0,8):
            r = GameObject(Vector2(0, (x*3) - 3))
            r.setMesh(road)
            roadList.append(r)
        speed = 0
        vel = 0.05
        framerate = 1.0/120
        now = time.time()
        nextFramerate = now + framerate
        t= 0
        f = 0
        deltatime = framerate
        total = 0
        exit = False
        while exit == False and lifes > 0:
        #for x in range(0, 100):
            t = time.time()
            if speed > vel:
                if cont == 8:
                    rand = random.randint(0, 3)
                    if rand == 1:
                        car = GameObject(Vector2(2, -4))
                        car.setMesh(self.randomMesh(self.colors))
                        carList.append(car)
                    if rand == 2:
                        car = GameObject(Vector2(5, -4))
                        car.setMesh(self.randomMesh(self.colors))
                        carList.append(car)
                    cont = 0
                else:
                    cont += 1

                for elem in roadList:
                    elem.position.translate(Vector2(0, 1))
                    if elem.position.y > 19:
                        elem.position.y = -4

                for elem in carList:
                    elem.position.translate(Vector2(0, 1))
                    if player.position.y - elem.position.y == 3 and player.position.x == elem.position.x:
                        lifes = self.die(lifes, player, roadList, carList)
                        carList.remove(elem)
                    if elem.position.y > 19:
                        carList.remove(elem)
                total += deltatime
                speed = 0
            else:
                speed += deltatime;

            vel = 0.05
            for event in self.enginne.getEvents():
                if event.type == self.enginne.pg.KEYDOWN:
                    if event.key == self.enginne.pg.K_ESCAPE:
                        exit = True
                    elif event.key == self.enginne.pg.K_d and player.position.x < 6:
                        player.position = Vector2(5, 16)
                    elif event.key == self.enginne.pg.K_a and player.position.x > 1:
                        player.position = Vector2(2, 16)


            key = self.enginne.pg.key.get_pressed()  #checking pressed keys
            if key[self.enginne.pg.K_SPACE]: vel = 0

            self.enginne.display.overlap(roadList + carList + [player], self.colors)
            self.enginne.display.pointWall(self.enginne.lifeBricks(lifes))
            self.enginne.display.attScore(int(total/1))

            while now < nextFramerate:
                time.sleep(nextFramerate - now)
                now = time.time()
            nextFramerate += framerate
            f = time.time()
            deltatime = f - t
        return int(total/1)

    def die(self, life, p, road, cars):
        life = life - 1
        for cont in range(0, 2):
            anim = GameObject(p.position)
            anim.setMesh(self.enginne.dieBricks(cont))
            self.enginne.display.overlap(road + cars + [anim], self.colors)
            time.sleep(0.5)
        return life


def init(enginne):
    G = game(enginne)
    return G.gameplay()