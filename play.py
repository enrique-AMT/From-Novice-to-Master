import load
import pickle
import theano
import theano.tensor as T
import math
import chess, chess.pgn
import heapq
import time
import re
import string
import numpy
import sunfish
import Player
import pickle
import random
import traceback
from sunfish import Position
from memoize import Memoize as memo

#File is never closed here, may cause memory leak
def get_model_from_pickle(fn):
    f = open(fn, 'rb')
    Ws, bs = pickle.load(f)
    
    Ws_s, bs_s = load.get_parameters(Ws=Ws, bs=bs)
    x, p = load.get_model(Ws_s, bs_s)
    
    predict = theano.function(
        inputs=[x],
        outputs=p)

    return predict

strip_whitespace = re.compile(r"\s+")
translate_pieces = str.maketrans(".pnbrqkPNBRQK", "\x00" + "\x01\x02\x03\x04\x05\x06" + "\x08\x09\x0a\x0b\x0c\x0d")

def sf2array(pos, flip):
    # Create a numpy array from a sunfish representation
    pos = strip_whitespace.sub('', pos.board) # should be 64 characters now
    pos = pos.translate(translate_pieces)
    m = numpy.fromstring(pos, dtype=numpy.int8)
    if flip:
        m = numpy.fliplr(m.reshape(8, 8)).reshape(64)
    return m

CHECKMATE_SCORE = 1e6
@memo
def negamax(pos, depth, alpha, beta, color, func):
    moves = []
    X = []
    pos_children = []
    for move in pos.gen_moves():
        pos_child = pos.move(move)
        moves.append(move)
        X.append(sf2array(pos_child, flip=(color==1)))
        pos_children.append(pos_child)

    if len(X) == 0:
        return Exception('eh?')

    # Use model to predict scores
    scores = func(X)

    for i, pos_child in enumerate(pos_children):
        if pos_child.board.find('K') == -1:
            scores[i] = CHECKMATE_SCORE

    child_nodes = sorted(zip(scores, moves), reverse=True)

    best_value = float('-inf')
    best_move = None
    
    for score, move in child_nodes:
        if depth == 1 or score == CHECKMATE_SCORE:
            value = score
        else:
            # print 'ok will recurse', sunfish.render(move[0]) + sunfish.render(move[1])
            pos_child = pos.move(move)
            neg_value, _ = negamax(pos_child, depth-1, -beta, -alpha, -color, func)
            value = -neg_value

        # value += random.gauss(0, 0.001)

        # crdn = sunfish.render(move[0]) + sunfish.render(move[1])
        # print '\t' * (3 - depth), crdn, score, value

        if value > best_value:
            best_value = value
            best_move = move

        if value > alpha:
            alpha = value

        if alpha > beta:
            break

    return best_value, best_move


def create_move(board, crdn):
    # workaround for pawn promotions
    move = chess.Move.from_uci(crdn)
    if board.piece_at(move.from_square).piece_type == chess.PAWN:
        if int(move.to_square/8) in range(7):
            move.promotion = chess.QUEEN # always promote to queen
    return move

def game(func):
    gn_current = chess.pgn.Game()

    maxd = random.randint(1, 2) # max depth for deep pink
    #secs = random.random() # max seconds for sunfish
    secs = 5
    print ('maxd %f secs %f' % (maxd, secs))

    player_a = Computer(func, maxd=maxd)
    player_b = Sunfish_AI(secs=secs)

    times = {'A': 0.0, 'B': 0.0}
    
    while True:
        for side, player in [('A', player_a), ('B', player_b)]:
            t0 = time.time()
            try:
                gn_current = player.move(gn_current)
            except KeyboardInterrupt:
                return
            except:
                traceback.print_exc()
                return side + '-exception', times

            times[side] += time.time() - t0
            print('=========== Player %s: %s' % (side, gn_current.move))
            print(str(gn_current.board()))
            
            if gn_current.board().is_checkmate():
                return side, times
            elif gn_current.board().is_stalemate():
                return '-', times
            elif gn_current.board().can_claim_fifty_moves():
                return '-', times
            elif s.find('K') == -1 or s.find('k') == -1:
                # Both AI's suck at checkmating, so also detect capturing the king
                return side, times
            
def play():
    func = get_model_from_pickle('model.pickle')
    while True:
        side, times = game(func)
        with open('stats.txt', 'a') as f:
            f.write('%s %f %f\n' % (side, times['A'], times['B']))
        

        
if __name__ == '__main__':
    play()
