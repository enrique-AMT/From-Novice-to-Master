import load
import math
import pickle
import string


import chess, chess.pgn
import heapq
import time
import re

from memoize import Memoize as memo
import numpy

import pickle
import Player
import random
import sunfish
import theano
import theano.tensor as T
import traceback
import dequeue

#This method should use an auxiliary method
#That is run in parallel by CUDA processors, yielding the int
#Representing the amount of times it appears at pos i in X amount
# of games within our provided model
def best_moves(model, pos=0 , arr=numpy.array()):
    pq  = dequeue()
    with open(model.pickle) as f:
        #read all the moves per game in Pickled Dataset
        #if move m at pos i
        #is the most common winning move then,
        #add to a PQ as move to verify first

    return pq

def get_model_from_pickle(fn):
    f = open(fn)
    Ws, bs = pickle.load(f)
    
    Ws_s, bs_s = load.get_parameters(Ws=Ws, bs=bs)
    x, p = load.get_model(Ws_s, bs_s)
    
    predict = theano.function(
        inputs=[x],
        outputs=p)

    return predict

strip_whitespace = re.compile(r"\s+")
translate_pieces = string.maketrans(".pnbrqkPNBRQK", "\x00" + "\x01\x02\x03\x04\x05\x06" + "\x08\x09\x0a\x0b\x0c\x0d")

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
            neg_value, _ = negamax(pos_child, depth-1,\
                                   -beta, -alpha, -color, func)
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
        if int(move.to_square/8) in [0, 7]:
            move.promotion = chess.QUEEN # always promote to queen
    return move



def game(func):
    gn_current = chess.pgn.Game()

    maxd = random.randint(1, 2) # max depth for deep pink
    #WE want consistency here peeps
    #secs = random.random() # max seconds for sunfish pre-Alejandro Intervene
    secs = 5

    print('maxd {} secs {}'.format(maxd, secs))

    player_a = Computer(func, maxd=maxd)
    player_b = Sunfish(secs=secs)

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
            print('=========== Player {}: {}'.format(side, gn_current.move))
            s = str(gn_current.board())
            print(s)
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
        #f = open('stats.txt', 'a')
        with open('stats.txt','a') as f:
            f.write('{} {} {}\n'.format(side, times['A'], times['B']))
        #f.close()

        
if __name__ == '__main__':
    play()
