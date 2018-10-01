try:
    print('Importing pygame')
    import pygame as pg
    import random
except:
    print('Error on import pygame')

def getEvents():
    return pg.event.get()

def close():
    pg.quit()

class BricksWall():
    def __init__(self, tam = 20, itam = 5, esp = 2, colors = {}):
        self.i = 20
        self.j = 10
        self.tam = tam
        self.itam = itam
        self.esp = esp
        self.colors = colors
        width = self.j * (self.tam + self.esp) + 105
        self.width = width
        height = self.i * (self.tam + self.esp) + 6
        WINSIZE = [width, height]
        pg.init()
        self.screen = pg.display.set_mode(WINSIZE)
        pg.display.set_caption('SuperBricksBlocks')
        self.screen.fill((217, 217, 243))

        self.font = pg.font.Font("modules/Display.ttf", 20)
        self.score = self.font.render("Score", True, (0, 0, 0))
        self.screen.blit(self.score, (width - self.score.get_width() - 5, 10))
        self.Hscore = self.font.render("Hight Score", True, (0, 0, 0))
        self.screen.blit(self.Hscore, (width - self.Hscore.get_width() - 5, 80))

        self.construction()
        self.attScore(0)
        self.attHScore(0)
        self.draw()
        self.auxDraw()
        self.clock = pg.time.Clock()


    def attScore(self, point):
        pg.draw.rect(self.screen, (217, 217, 243), self.recScore, 0)
        score = self.font.render(str(point), True, (255, 0, 0))
        self.screen.blit(score, (self.width - score.get_width() - 5, 35 ))

    def attHScore(self, point):
        pg.draw.rect(self.screen, (217, 217, 243), self.recHScore, 0)
        Hscore = self.font.render(str(point), True, (255, 0, 0))
        self.screen.blit(Hscore, (self.width - Hscore.get_width() - 5, 105 ))

    def construction(self):
        self.wall = []
        for i in range(self.i):
            line = []
            for j in range(self.j):
                rec = pg.Rect(0, 0, 20, 20)
                irec = pg.Rect(5, 5, 10, 10)

                dx = (j * 20) + (j * 2) + 2
                dy = (i * 20) + (i * 2) + 2

                rec = rec.move(dx, dy)
                irec = irec.move(dx, dy)

                line.append([rec, irec])
            self.wall.append(line)

        initX = int(dx) + 30
        initY = int(dy)

        print(initX)
        self.recScore = pg.Rect(0, 0, self.score.get_width() + 30, self.score.get_height())
        self.recScore.move_ip(self.width - (self.score.get_width() + 30) - 5, self.score.get_height() + 10)

        self.recHScore = pg.Rect(0, 0, self.score.get_width() + 30, self.score.get_height())
        self.recHScore.move_ip(self.width - (self.score.get_width() + 30) - 5, self.Hscore.get_height() + 80)

        self.auxWall = []
        for i in range(4):
            line = []
            for j in range(4):
                rec = pg.Rect(0, 0, 20, 20)
                irec = pg.Rect(5, 5, 10, 10)

                dx = (j * 20) + (j * 2) + 2 + initX
                dy = (i * 20) + (i * 2) + 2 + (initY / 2)

                rec = rec.move(dx, dy)
                irec = irec.move(dx, dy)

                line.append([rec, irec])
            self.auxWall.append(line)


    def draw(self):
        for i in range(self.i):
            for j in range(self.j):
                rec, irec = self.wall[i][j]
                pg.draw.rect(self.screen, (255, 255, 255), rec, 1)
                pg.draw.rect(self.screen, (0, 255, 255), irec, 0)
        pg.display.flip()

    def auxDraw(self):
        for i in range(4):
            for j in range(4):
                rec, irec = self.auxWall[i][j]
                pg.draw.rect(self.screen, (255, 255, 255), rec, 1)
                pg.draw.rect(self.screen, (255, 255, 255), irec, 0)
        pg.display.flip()

    def overlap(self, objects, colors = {'1': (255, 0, 0), '2': (0, 0, 255)}):
        matriz = []
        for a in range(20):
            l = []
            for b in range(10):
                l.append('0')
            matriz.append(l)

        for gameObject in objects:
            for i in range(len(gameObject.mesh)):
                for j in range(len(gameObject.mesh[0])):
                    x = gameObject.position.x + j
                    y = gameObject.position.y + i
                    if gameObject.mesh[i][j] != '0' and x < self.j and y < self.i and x >= 0 and y >= 0:
                        matriz[y][x] = gameObject.mesh[i][j]

        #for a in matriz:
        #    s = ' '.join(a)
        #    print(s)
        #print("#")

        self.drawMatriz(matriz, colors)

        pg.display.flip()

    def drawMatriz(self, matriz, colors = {'1': (255, 0, 0), '2': (0, 0, 255)}):
        for i in range(len(matriz)):
            for j in range(len(matriz[0])):
                if matriz[i][j] == '0':
                    rec, irec = self.wall[i][j]
                    pg.draw.rect(self.screen, (255, 255, 255), rec, 1)
                    pg.draw.rect(self.screen, (255, 255, 255), irec, 0)
                else:
                    rec, irec = self.wall[i][j]
                    color = colors[matriz[i][j]]
                    pg.draw.rect(self.screen, color, rec, 1)
                    pg.draw.rect(self.screen, color, irec, 0)
        pg.display.flip()

    def drawMatrizTransparente(self, matriz, colors = {'1': (255, 0, 0), '2': (0, 0, 255)}):
        for i in range(len(matriz)):
            for j in range(len(matriz[0])):
                if matriz[i][j] != '0':
                    rec, irec = self.wall[i][j]
                    color = colors[matriz[i][j]]
                    pg.draw.rect(self.screen, color, rec, 1)
                    pg.draw.rect(self.screen, color, irec, 0)
        pg.display.flip()

    def pointWall(self, matriz, colors = {'1': (0, 255, 0), '2': (0, 0, 255)}):
        for i in range(4):
            for j in range(4):
                if i < len(matriz) and j < len(matriz[0]):
                    if matriz[i][j] == '0':
                        rec, irec = self.auxWall[i][j]
                        pg.draw.rect(self.screen, (255, 255, 255), rec, 1)
                        pg.draw.rect(self.screen, (255, 255, 255), irec, 0)
                    else:
                        rec, irec = self.auxWall[i][j]
                        color = colors[matriz[i][j]]
                        pg.draw.rect(self.screen, color, rec, 1)
                        pg.draw.rect(self.screen, color, irec, 0)
                else:
                    rec, irec = self.auxWall[i][j]
                    pg.draw.rect(self.screen, (255, 255, 255), rec, 1)
                    pg.draw.rect(self.screen, (255, 255, 255), irec, 0)
        pg.display.flip()


display = BricksWall()

def lifeBricks(life):
    if life == 4:
        return [['1', '0', '0', '0'],
                ['1', '0', '0', '0'],
                ['1', '0', '0', '0'],
                ['1', '0', '0', '0']]
    elif life == 3:
        return [['0', '0', '0', '0'],
                ['1', '0', '0', '0'],
                ['1', '0', '0', '0'],
                ['1', '0', '0', '0']]
    elif life == 2:
        return [['0', '0', '0', '0'],
                ['0', '0', '0', '0'],
                ['1', '0', '0', '0'],
                ['1', '0', '0', '0']]
    elif life == 1:
        return [['0', '0', '0', '0'],
                ['0', '0', '0', '0'],
                ['0', '0', '0', '0'],
                ['1', '0', '0', '0']]
    elif life < 1 or life > 4:
        return [['0', '0', '0', '0'],
                ['0', '0', '0', '0'],
                ['0', '0', '0', '0'],
                ['0', '0', '0', '0']]

def dieBricks(frame):
    if frame == 0:
        return [['1', '0', '0', '1'],
                ['0', '1', '1', '0'],
                ['0', '1', '1', '0'],
                ['1', '0', '0', '1']]
    elif frame == 1:
        return [['0', '1', '1', '0'],
                ['1', '0', '0', '1'],
                ['1', '0', '0', '1'],
                ['0', '1', '1', '0']]
    elif frame == 2:
        return [['1', '0', '0', '1'],
                ['0', '1', '1', '0'],
                ['0', '1', '1', '0'],
                ['1', '0', '0', '1']]

def error():
    return[['0','1','1','1','0','0','1','1','1','0'],
           ['0','1','0','0','0','0','1','0','1','0'],
           ['0','1','1','1','0','0','1','1','1','0'],
           ['0','1','0','0','0','0','1','1','0','0'],
           ['0','1','1','1','0','0','1','0','1','0'],
           ['0','0','0','0','0','0','0','0','0','0'],
           ['0','1','1','1','0','0','1','1','1','0'],
           ['0','1','0','1','0','0','1','0','1','0'],
           ['0','1','1','1','0','0','1','0','1','0'],
           ['0','1','1','0','0','0','1','0','1','0'],
           ['0','1','0','1','0','0','1','1','1','0'],
           ['0','0','0','0','0','0','0','0','0','0'],
           ['0','0','1','1','0','0','1','1','0','0'],
           ['0','0','1','1','0','0','1','1','0','0'],
           ['0','0','1','1','0','0','1','1','0','0'],
           ['0','0','1','1','0','0','1','1','0','0'],
           ['0','0','1','1','0','0','1','1','0','0'],
           ['0','0','0','0','0','0','0','0','0','0'],
           ['0','0','1','1','0','0','1','1','0','0'],
           ['0','0','1','1','0','0','1','1','0','0']]

def errorShow():
    while 1:
        for event in getEvents():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        close()
        display.drawMatriz(error())
