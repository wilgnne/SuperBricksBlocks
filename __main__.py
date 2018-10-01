import sys
sys.path.append(sys.path[0]+'/modules')

import importlib
import menu, enginne
import time

def loadGame(biblioteca, idgame):
    name = biblioteca[idgame][0]
    print(name)
    arq = open('modules/run.py', 'w')
    arq.write('import games.' + name + '.' + 'game as game')
    arq.close()
    print('Import game library')
    import run as run
    importlib.reload(run)
    score = run.game.init(enginne)
    if score > biblioteca[idgame][2]:
        arq = open('games/'+name+'/score.txt', 'w')
        arq.write(str(int(score)))
        biblioteca[idgame][2] = score
    enginne.display.auxDraw()
    del(run)
    enginne.display.attScore(0)

mod = lambda a, b: a % len(b)

attGame = 0
frameAnim = 0

framerate = 1.0/60
cont = 0
deltatime = framerate * 1

colors = {'1': (0,191,255),
		  '2': (155,184,165),
		  '3': (154,205,50),
		  '4': (255,165,0),
		  '5': (147,112,219)}

try:
    menu.loadLibrary()
    while 1:
        i = time.time()
        for event in enginne.getEvents():
                if event.type == enginne.pg.QUIT:
                    enginne.close()
                elif event.type == enginne.pg.KEYDOWN:
                    if event.key == enginne.pg.K_SPACE:
                        loadGame(menu.biblioteca, attGame)
                        frames = [a for a in range(len(menu.transition))]
                        for frame in frames:
                            enginne.display.drawMatrizTransparente(menu.transition[frame], {'1': (255, 0, 0)})
                            time.sleep(0.001)
                        for frame in frames[::-1]:
                            enginne.display.drawMatriz(menu.transition[frame],{'1': (255, 0, 0)})
                            time.sleep(0.001)
                    elif event.key == enginne.pg.K_d:
                        if attGame == len(menu.biblioteca) -1:
                            attGame = 0
                        else:
                            attGame += 1
                        frameAnim = 0
                        enginne.display.attHScore(menu.biblioteca[attGame][2])
                        enginne.display.drawMatriz(menu.biblioteca[attGame][1][mod(frameAnim, menu.biblioteca[attGame][1])], colors)
                    elif event.key == enginne.pg.K_a:
                        if attGame == 0:
                            attGame = len(menu.biblioteca) -1
                        else:
                            attGame -= 1
                        frameAnim = 0
                        enginne.display.attHScore(menu.biblioteca[attGame][2])
                        enginne.display.drawMatriz(menu.biblioteca[attGame][1][mod(frameAnim, menu.biblioteca[attGame][1])], colors)
        if cont >= framerate:
            enginne.display.drawMatriz(menu.biblioteca[attGame][1][mod(frameAnim, menu.biblioteca[attGame][1])], colors)
            enginne.display.attHScore(menu.biblioteca[attGame][2])
            frameAnim += 1
            cont = 0
        else:
            cont += deltatime
        f = time.time()
        deltatime = f-i

except Exception as e:
    print(e)
    enginne.errorShow()