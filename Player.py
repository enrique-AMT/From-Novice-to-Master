import chess
import sunfish
from sunfish import Position
#ABSTRACT CLASS
class Player(object):
    def move(self, gn_current):
        raise NotImplementedError()
        


class Computer(Player):
    def __init__(self, func, maxd=5):
        self._func = func
        self._pos = sunfish.Position(sunfish.initial, 0,(True,True), (True,True), 0, 0)
        self._maxd = maxd

    def move(self, gn_current):
        assert(gn_current.board().turn == True)

        if gn_current.move is not None:
            # Apply last_move
            crdn = str(gn_current.move)
            move = (119 - sunfish.parse(crdn[0:2]),\
                    119 - sunfish.parse(crdn[2:4]))
            self._pos = self._pos.move(move)

        # for depth in xrange(1, self._maxd+1):
        alpha = float('-inf')
        beta = float('inf')

        depth = self._maxd
        t0 = time.time()
        best_value, best_move = negamax(self._pos, depth, alpha,beta, 1, self._func)
        crdn = sunfish.render(best_move[0]) + sunfish.render(best_move[1])
        print(depth, best_value, crdn, time.time() - t0)

        self._pos = self._pos.move(best_move)
        crdn = sunfish.render(best_move[0]) + sunfish.render(best_move[1])
        move = create_move(gn_current.board(), crdn)
        
        gn_new = chess.pgn.GameNode()
        gn_new.parent = gn_current
        gn_new.move = move


        return gn_new


class Human(Player):
    def move(self, gn_current):
        bb = gn_current.board()

        print(bb)

        def get_move(move_str):
            try:
                move = chess.Move.from_uci(move_str)
            except:
                print('cant parse')
                return False
            if move not in bb.legal_moves:
                print('not a legal move')
                return False
            else:
                return move

        while True:
            print('your turn:')
            move = get_move(raw_input())
            if move:
                break

        gn_new = chess.pgn.GameNode()
        gn_new.parent = gn_current
        gn_new.move = move
        
        return gn_new


class Sunfish_AI(Player):
    def __init__(self, secs=1):
        self._searcher = sunfish.Searcher()
        self._pos = sunfish.Position(sunfish.initial, 0,(True,True), (True,True), 0, 0)
        self._secs = secs

    def move(self, gn_current):
        import sunfish

        assert(gn_current.board().turn == False)

        # Apply last_move
        crdn = str(gn_current.move)
        move = (sunfish.parse(crdn[0:2]), sunfish.parse(crdn[2:4]))
        self._pos = self._pos.move(move)

        t0 = time.time()
        move, score = self._searcher.search(self._pos, self._secs)
        print(time.time() - t0, move, score)
        self._pos = self._pos.move(move)

        crdn = sunfish.render(119-move[0]) + sunfish.render(119 - move[1])
        move = create_move(gn_current.board(), crdn)
        
        gn_new = chess.pgn.GameNode()
        gn_new.parent = gn_current
        gn_new.move = move

        return gn_new
