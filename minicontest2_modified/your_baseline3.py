# myTeam.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game
from util import nearestPoint

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'DummyAgent', second = 'DummyAgent'):
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class DummyAgent(CaptureAgent):
  def registerInitialState(self, gameState):
    self.start = gameState.getAgentPosition(self.index)
    CaptureAgent.registerInitialState(self, gameState)

  def chooseAction(self, gameState):
    actions = gameState.getLegalActions(self.index)
    enemies = [gameState.getAgentState(i).getPosition() for i in self.getOpponents(gameState)]

    if self.index//2==0:
      values = [self.offensiveevaluate(gameState, a) for a in actions]
      maxValue = max(values)
      bestActions = [a for a, v in zip(actions, values) if v == maxValue]

      foodLeft = len(self.getFood(gameState).asList())

      if gameState.data.agentStates[self.index].numCarrying >= 2 and min([self.getMazeDistance(gameState.getAgentState(self.index).getPosition()  , enemy) for enemy in enemies]) >2:
        # 2개의 food를 먹었을 경우 점수를 get하기 위해 본인 진영으로 이동
        # 상대 agent와의 거리가 2 이하인 경우 greedy한 본인 진영으로의 이동이 아니라 offensiveevaluation에 의해 도망치는 것을 우선순위로 삼음.
        bestDist = 9999
        for action in actions:
          successor = self.getSuccessor(gameState, action)
          pos2 = successor.getAgentPosition(self.index)
          dist = self.getMazeDistance(self.start,pos2)
          if dist < bestDist:
            bestAction = action
            bestDist = dist
        return bestAction

      return random.choice(bestActions)

    else:
      values = [self.defensiveevaluate(gameState, a) for a in actions]
      # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

      maxValue = max(values)
      bestActions = [a for a, v in zip(actions, values) if v == maxValue]

      foodLeft = len(self.getFood(gameState).asList())

      if foodLeft <= 2:
        bestDist = 9999
        for action in actions:
          successor = self.getSuccessor(gameState, action)
          pos2 = successor.getAgentPosition(self.index)
          dist = self.getMazeDistance(self.start,pos2)
          if dist < bestDist:
            bestAction = action
            bestDist = dist
        return bestAction

      return random.choice(bestActions)      

  def getSuccessor(self, gameState, action):
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(self.index, action)
    else:
      return successor

  def offensiveevaluate(self, gameState, action):
    features = self.offensivegetFeatures(gameState, action)
    weights = self.offensivegetWeights(gameState, action)
    return features * weights

  def defensiveevaluate(self, gameState, action):
    features = self.defensivegetFeatures(gameState, action)
    weights = self.defensivegetWeights(gameState, action)
    return features * weights

  def offensivegetFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    foodList = self.getFood(successor).asList()    
    features['successorScore'] = -len(foodList)

    actionlist = successor.getLegalActions(self.index)
    for action in actionlist: # successor에서 할 수 있는 모든 action에 대하여
      virtualsuccessor = self.getSuccessor(successor, action) # virtualsuccessor를 만들고
      virtualPos = virtualsuccessor.getAgentState(self.index).getPosition() # 이 때의 position을 virtualPos
      enemies = [successor.getAgentState(i).getPosition() for i in self.getOpponents(virtualsuccessor)]
      if min([self.getMazeDistance(virtualPos, enemy) for enemy in enemies]) <=2:
        features['distanceToEnemy']=100
      # 즉, enemy와의 거리가 2 이하가 되는 action에 대하여 100점을 할당.
      # 이 100점은 offensivegetWeights에 의해 큰 -가 되어 적으로부터 도망치게 됨.

    if len(foodList) > 0:
      myPos = successor.getAgentState(self.index).getPosition()
      minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
      features['distanceToFood'] = minDistance
    return features

  def offensivegetWeights(self, gameState, action):
    return {'successorScore': 100, 'distanceToFood': -1, 'distanceToEnemy': -10}

  def defensivegetFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)

    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()

    features['onDefense'] = 1
    if myState.isPacman: features['onDefense'] = 0
    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    features['numInvaders'] = len(invaders)
    if len(invaders) > 0:
      dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
      features['invaderDistance'] = min(dists)

    if action == Directions.STOP: features['stop'] = 1
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == rev: features['reverse'] = 1
    return features

  def defensivegetWeights(self, gameState, action):
    return {'numInvaders': -1000, 'onDefense': 100, 'invaderDistance': -10, 'stop': -100, 'reverse': -2}