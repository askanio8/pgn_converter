from start_position import start_position
from game import Game
import time

f = open('lichess_db_standard_rated_2013-02.pgn', 'r')
s = f.readlines()
f.close()

games = list(filter(lambda c: c[:2] == '1.' and len(c) > 100, s))

ex = 0
stat = time.time()
for game in games[:1000]:
    try:
        Game(game, start_position)
    except:
        ex = ex + 1
print('%', ex/len(games))
print('time', time.time() - stat)
