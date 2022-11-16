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
from avalam import *

class State:
    def __init__(self, percepts, player, depth, time_left):
        self.percepts = percepts
        self.player = player
        self.depth = depth
        self.time_left = time_left
        #self.action = action

class Action:
    def __init__(self, score, action):
        self.score = score
        self.action = action

def 𝗆𝗂𝗇𝗂𝗆𝖺𝗑𝖲𝖾𝖺𝗋𝖼𝗁(s0):    
    visitedStates = {}
    bestAction = 𝗆𝖺𝗑𝖵𝖺𝗅𝗎𝖾(visitedStates,s0,-24,24)
    print("NUMBER of visitedStates: ",len(visitedStates))
    return bestAction

def 𝗆𝖺𝗑𝖵𝖺𝗅𝗎𝖾(visitedStates,s,alpha,beta):
    print("DEPTH: ",s.depth)
    board = dict_to_board(s.percepts)
    if board.is_finished():
        return Action(board.get_score(),None)
    if s.depth >= 13 and is_Quiescent(s):
        return Action(h(s),None)
    action = Action(-24,None)            
    visitedActions = []
    for a in board.get_actions():
        print("max Action: ",a)
        if a not in visitedActions:
            sucsessorborad = board.play_action(a)
            visitedActions.append(a)                
            player = -s.player
            percepts = {'m': sucsessorborad.get_percepts(True), 'rows': 9, 'columns': 9, 'max_height': 5}
            if (hash(str(percepts)),player) in visitedStates:
                minAction = visitedStates[(hash(str(percepts)),player)]
            else:
                depth = s.depth + 1
                time = s.time_left
                sucsessorState = State(percepts,player,depth,time)
                minAction = minValue(visitedStates,sucsessorState,alpha,beta)
                visitedStates.setdefault((hash(str(percepts)),player),minAction)  
            if minAction.score > action.score:
                action.score = minAction.score
                action.action = a
                alpha = max(alpha,action.score)
            if action.score >= beta:
                return action
    print()
    return action

def minValue(visitedStates,s,alpha,beta):
    board = dict_to_board(s.percepts)
    if board.is_finished():
        return Action(board.get_score(),None)
    if s.depth >= 13 and is_Quiescent(s):
        return Action(h(s),None)
    action = Action(24,None)
    visitedActions = []
    for a in board.get_actions():
        print("min Action: ",a)
        if a not in visitedActions:
            sucsessorborad = board.play_action(a)
            visitedActions.append(a)
            player = -s.player
            percepts = {'m': sucsessorborad.get_percepts(True), 'rows': 9, 'columns': 9, 'max_height': 5}
            if (hash(str(percepts)),player) in visitedStates: 
                maxAction = visitedStates[(hash(str(percepts)),player)]
            else:
                depth = s.depth + 1
                time = s.time_left
                sucsessorState = State(percepts,player,depth,time)
                maxAction = minValue(visitedStates,sucsessorState,alpha,beta)
                visitedStates.setdefault((hash(str(percepts)),player),maxAction)
            if maxAction.score < action.score:
                action.score = maxAction.score
                action.action = a
                beta = min(beta,action.score)
            if action.score <= alpha:
                return action
    print()
    return action

def h(s):
    board = dict_to_board(s.percepts)
    score = 0
    for i in range(board.rows):
        for j in range(board.columns):
            if board.m[i][j] < 0:
                if not board.is_tower_movable(i,j):
                    score -= 3
                elif is_Tower_Safe(board,i,j):
                    score -= 2
                elif not is_Tower_Safe(board,i,j):
                    score -= 1
            
            if board.m[i][j] > 0:
                if not board.is_tower_movable(i,j):
                    score += 3
                elif is_Tower_Safe(board,i,j):
                    score += 2
                elif not is_Tower_Safe(board,i,j):
                    score += 1
    if score == 0:
        for i in range(board.rows):
            for j in range(board.columns):
                if board.m[i][j] == -board.max_height:
                    score -= 1
                elif board.m[i][j] == board.max_height:
                    score += 1
    return score

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
    board = dict_to_board(s.percepts)
    for i in range(board.rows):
            for j in range(board.columns):
                if board.m[i][j] == 4 and not is_Tower_Safe(board,i,j):
                    return False
                if board.m[i][j] == 3 and not is_Tower_Safe(board,i,j):
                    return False
    return True 

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
        initialSearchState = State(percepts,player,0,time_left)
        bestAction = 𝗆𝗂𝗇𝗂𝗆𝖺𝗑𝖲𝖾𝖺𝗋𝖼𝗁(initialSearchState)
        print("bestAction: ", bestAction.action)
        return bestAction.action

   

if __name__ == "__main__":
    agent_main(MyAgent())

