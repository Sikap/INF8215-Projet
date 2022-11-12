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
    def __init__(self, percepts, player, depth, time_left,action):
        self.percepts = percepts
        self.player = player
        self.depth = depth
        self.time_left = time_left
        self.action = action

class Action:
    def __init__(self, score, action):
        self.score = score
        self.action = action

def 𝗆𝗂𝗇𝗂𝗆𝖺𝗑𝖲𝖾𝖺𝗋𝖼𝗁(s0):    
    visitedStates = []
    bestAction = 𝗆𝖺𝗑𝖵𝖺𝗅𝗎𝖾(visitedStates,s0,-24,24)
    return bestAction

def 𝗆𝖺𝗑𝖵𝖺𝗅𝗎𝖾(visitedStates,s,alpha,beta):
    board = dict_to_board(s.percepts)
    if board.is_finished():
        return Action(board.get_score(),s.action)
    if s.depth >= 4:
        return Action(h(s),s.action)
    action = Action(-24,None)            
    visitedActions = []
    for a in board.get_actions():
        if a not in visitedActions:
            sucsessorborad = board.play_action(a)
            visitedActions.append(a)
            if sucsessorborad.get_percepts() not in visitedStates: 
                depth= s.depth + 1
                s.percept = {'m': sucsessorborad.get_percepts(True), 'rows': 9, 'columns': 9, 'max_height': 5}
                sucsessorState = State(s.percept,-s.player,depth,s.time_left,a)
                minAction = minValue(visitedStates,sucsessorState,alpha,beta)
                if minAction.score > action.score:
                    action.score = minAction.score
                    action.action = minAction.action
                    alpha = max(alpha,action.score)
                if action.score >= beta:
                    return action
                visitedStates.append(s.percept)
    return action

def minValue(visitedStates,s,alpha,beta):
    board = dict_to_board(s.percepts)
    if board.is_finished():
        return Action(board.get_score(),s.action)
    if s.depth >= 4:
        return Action(h(s),s.action)
    action = Action(24,None)
    visitedActions = []
    for a in board.get_actions():
        if a not in visitedActions:
            sucsessorborad = board.play_action(a)
            visitedActions.append(a)
            if sucsessorborad.get_percepts() not in visitedStates:
                depth = s.depth + 1
                s.percept = {'m': sucsessorborad.get_percepts(True) , 'rows': 9, 'columns': 9, 'max_height': 5}
                sucsessorState = State(s.percept,-s.player,depth,s.time_left,a)
                maxAction = maxValue(visitedStates,sucsessorState,alpha,beta)
                if maxAction.score < action.score:
                    action.score = maxAction.score
                    action.action = maxAction.action
                    beta = min(beta,action.score)
                if action.score <= alpha:
                    return action
                visitedStates.append(s.percept)
    return action

def h(s):
    board = dict_to_board(s.percepts)
    return board.get_score()

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
        initialSearchState = State(percepts,player,0,time_left,None)
        bestAction = 𝗆𝗂𝗇𝗂𝗆𝖺𝗑𝖲𝖾𝖺𝗋𝖼𝗁(initialSearchState)
        print("bestAction: ", bestAction.action)
        return bestAction.action

   

if __name__ == "__main__":
    agent_main(MyAgent())

