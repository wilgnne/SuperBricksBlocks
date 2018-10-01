import os

def checkDir():
    diretories = os.listdir()
    if 'games' not in diretories:
        os.mkdir('games')
    diretories = os.listdir('games/')
    if diretories == []:
        return False
    else:
        return True

biblioteca = []
transition = []

def loadLibrary():
    global biblioteca
    global transition

    biblioteca = os.listdir('games/')
    print('Loading library')
    for index, game in enumerate(biblioteca):
        arq = open('games/'+game+'/splash.txt', 'r')
        splash = arq.read()
        arq.close()
        splash = splash.split('#')
        splash = [[e.split(' ') for e in a.split('\n') if e != ''] for a in splash]

        arq = open('games/'+game+'/score.txt', 'r')
        score = arq.read()
        arq.close()

        biblioteca[index] = [game, splash, int(score)]
        print('{} loaded'.format(game))
    arq = open('modules/transition.txt', 'r')
    splash = arq.read()
    arq.close()
    splash = splash.split('#')
    transition = [[e.split(' ') for e in a.split('\n') if e != ''] for a in splash]