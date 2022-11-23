#!/usr/bin/env python3
"""
Avalam agent.
Copyright (C) 2022, <<<<<<<<<<< YOUR NAMES HERE >>>>>>>>>>>
Polytechnique Montréal

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/>.

"""
import math
from avalam import *

MIN = 0
MAX = 1

def 𝗆𝗂𝗇𝗂𝗆𝖺𝗑𝖲𝖾𝖺𝗋𝖼𝗁(s0,player,depth,maxDepth):    
    visitedStates = {}
    bestAction = 𝗆𝖺𝗑𝖵𝖺𝗅𝗎𝖾(visitedStates,s0,player,depth,-math.inf,math.inf,maxDepth)
    return bestAction

def 𝗆𝖺𝗑𝖵𝖺𝗅𝗎𝖾(visitedStates,s,player,depth,alpha,beta,maxDepth):
    if s.is_finished():
        return player*s.get_score(),None
    if depth >= maxDepth:
        return h(s,player),None
    bestScore,bestAction = -math.inf,None
    for action in s.get_actions():  
        nextState = s.play_action(action).clone()
        if (hash(str(nextState)),MIN) in visitedStates:
            minScore = visitedStates[(hash(str(nextState)),MIN)]
        else:
            minScore,_ = minValue(visitedStates,nextState,player,depth+1,alpha,beta,maxDepth)
            visitedStates.setdefault((hash(str(nextState)),MIN),minScore)
        if  minScore > bestScore:
            bestScore,bestAction =  minScore,action
            alpha = max(alpha,bestScore)
        if bestScore >= beta:
            return bestScore,bestAction   
    return bestScore,bestAction


def minValue(visitedStates,s,player,depth,alpha,beta,maxDepth):
    if s.is_finished():            
        return player*s.get_score(),None
    if depth >= maxDepth:
        return h(s,player),None
    bestScore,bestAction = math.inf,None
    for action in s.get_actions():
        nextState = s.play_action(action).clone()
        if (hash(str(nextState)),MAX) in visitedStates:
            maxScore = visitedStates[(hash(str(nextState)),MAX)]
        else:
            maxScore,_ = maxValue(visitedStates,nextState,player,depth+1,alpha,beta,maxDepth)
            visitedStates.setdefault((hash(str(nextState)),MAX),maxScore)
        if maxScore < bestScore:
            bestScore,bestAction = maxScore,action
            beta = min(beta,bestScore)
        if bestScore <= alpha: 
            return bestScore,bestAction
    return bestScore,bestAction

def h(s,player):
    score = player*s.get_score()    
    return score
   

    """
    score = 0
    for i in range(board.rows):
        for j in range(board.columns):
            if board.m[i][j] < 0:
                #if not board.is_tower_movable(i,j):
                    #score -= 3
                if is_Tower_Safe(board,i,j):
                    score -= 1
                elif not is_Tower_Safe(board,i,j):
                    score += 1

            if board.m[i][j] > 0:
                #if not board.is_tower_movable(i,j):
                    #score += 3
                if is_Tower_Safe(board,i,j):
                    score += 1
                elif not is_Tower_Safe(board,i,j):
                    score -= 1
    if score == 0:
        for i in range(board.rows):
            for j in range(board.columns):
                if board.m[i][j] == -board.max_height:
                    score -= 1
                elif board.m[i][j] == board.max_height:
                    score += 1
    """


def is_Tower_Safe(board,i,j):
    h = abs(board.m[i][j])
    if h > 0 and h < board.max_height:
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                action = (i, j, i+di, j+dj)
                if board.is_action_valid(action) and is_Opposite_Sign(board.m[i][j],board.m[i+di][j+dj]):
                   return False
    return True

def is_Opposite_Sign(a,b):
    if a < 0 and b >= 0: return True
    elif a >= 0 and b < 0: return True
    return False

def is_Quiescent(s):
    #board = dict_to_board(s.percepts)
    #for i in range(board.rows):
    #       for j in range(board.columns):
    #            if board.m[i][j] == 4 and not is_Tower_Safe(board,i,j):
    #               return False
    #            if board.m[i][j] == -4 and not is_Tower_Safe(board,i,j):
    #                return False
    return True 

def set_maxDepth(step):
        return 10

class MyAgent(Agent):

    """My Avalam agent."""
    
    def play(self, percepts, player, step, time_left):
        """
        This function is used to play a move according
        to the percepts, player and time left provided as input.
        It must return an action representing the move the player
        will perform.
        :param percepts: dictionary representing the current board
            in a form that can be fed to `dict_to_board()` in avalam.py.
        :param player: the player to control in this step (-1 or 1)
        :param step: the current step number, starting from 1
        :param time_left: a float giving the number of seconds left from the time
            credit. If the game is not time-limited, time_left is None.
        :return: an action
            eg; (1, 4, 1 , 3) to move tower on cell (1,4) to cell (1,3)
        """
        #print("percept:", percepts)
        print("player:", player)
        print("step:", step)
        print("time left:", time_left if time_left else '+inf')
        # TODO: implement your agent and return an action for the current step.
        board = dict_to_board(percepts)        
        score,action = 𝗆𝗂𝗇𝗂𝗆𝖺𝗑𝖲𝖾𝖺𝗋𝖼𝗁(board,player,0,set_maxDepth(step))
        return action

   

if __name__ == "__main__":
    agent_main(MyAgent())

