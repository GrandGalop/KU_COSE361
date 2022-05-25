# multiAgents.py
# --------------
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


from cmath import inf
from lib2to3.pgen2.literals import evalString
from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        currentPos = currentGameState.getPacmanPosition()

        currentFood = currentGameState.getFood()
        currentFoodDistance = float("inf")
        newFood = successorGameState.getFood()
        newFoodDistance = float("inf") 

        newGhostStates = successorGameState.getGhostStates()
        currentGhostStates = currentGameState.getGhostStates()
        newGhostPos = successorGameState.getGhostPositions()
        currentGhostPos = currentGameState.getGhostPositions()
        newGhostDistance = float("inf")
        
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates] # 각 Ghost들의 scared 시간을 가지는 list

        for i in newGhostPos:
            GhostDistanceCandidate = manhattanDistance(newPos, i)
            newGhostDistance = min(newGhostDistance, GhostDistanceCandidate) #action 이행 후 ghost의 position 중 최솟값을 갱신

        for j in range(0, len(newScaredTimes)):
            if newScaredTimes[j]>0 and manhattanDistance(currentGhostPos[j], currentPos) >= manhattanDistance(newGhostPos[j], newPos): 
                return 10000
        # 만약 어떤 Ghost가 scared 상태일 때, 해당 ghost와 거리가 가까워지게 되면 score를 획득       
        if newGhostDistance <2:
            return float("-inf")
        # 그렇지 않는 경우는 거리가 2미만이 되지 않게 조정

        for i in currentFood.asList():
            currentFoodDistanceCandidate = manhattanDistance(currentPos, i)
            currentFoodDistance = min(currentFoodDistance, currentFoodDistanceCandidate)
        # 현재 가장 가까운 Food와의 거리를 currentFoodDistance로 설정

        for i in newFood.asList():
            newFoodDistanceCandidate = manhattanDistance(newPos, i)
            newFoodDistance = min(newFoodDistance, newFoodDistanceCandidate)
        if newFoodDistance < currentFoodDistance:
            return 50000
        # action에 의해 Food로의 거리가 가까워지는 방향으로 action을 취하도록 함

        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def minimax(gameState, depth, agentIndex):
            if depth == self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState) # 만약 depth가 설정해 둔 depth와 같거나 게임이 종결된 상태에선 gameState에 대한 평가 반환
            legalMoves = gameState.getLegalActions(agentIndex)
            if agentIndex == gameState.getNumAgents()-1:
                evals = [minimax(gameState.generateSuccessor(agentIndex, action), depth+1, 0) for action in legalMoves] # 마지막 유령까지 모두 탐색했으면 depth를 하나 키워 agent부터 다시 탐색함.
            else:
                evals = [minimax(gameState.generateSuccessor(agentIndex, action), depth, agentIndex+1) for action in legalMoves] # 그 외의 경우에는 다음 유령을 탐색함.
            if agentIndex >0: #탐색한 agent가 유령이면 eval 중 minimum을 출력하고
                return min(evals)
            else:
                return max(evals) # pacman의 경우엔 maximum을 출력함.
        actions = gameState.getLegalActions(0)
        return max(actions, key=lambda x: minimax(gameState.generateSuccessor(0, x), 0, 1)) # actions에 대해서 depth=0, 첫 번째 ghost부터 재귀 시작


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        "*** YOUR CODE HERE ***"
        def alphabeta(gameState, agentIndex, depth, alpha, beta):
            if depth==0 or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState), Directions.STOP #만약 depth가 모두 소진될 경우 evaluationFunction과 stop을 반환
            
            if agentIndex==0: # pacman의 경우
                next_agent, next_depth = agentIndex + 1, depth # 같은 depth의 유령을 답색할 것임.
                legalActions = gameState.getLegalActions(agentIndex) # 팩맨의 가능한 Action들을 legalActions에 저장
                value, max_action = float('-inf'), Directions.STOP # pacman은 maximum agent -> value를 -inf로 초기화
                for action in legalActions:
                    new_score = alphabeta(gameState.generateSuccessor(agentIndex, action), next_agent, next_depth, alpha, beta)[0] #새롭게 조사된 node의 score에 대하여
                    if new_score > value: 
                        value, max_action = new_score, action #해당 노드가 value보다 클 경우, value를 갱신
                    if new_score > beta: 
                        return new_score, action #new_score가 beta보다 크면 자식들도 검사할 필요가 없으므로 new_score 반환
                    alpha = max(alpha, value)
                return value, max_action #이 value를 가지고 다른 sibling과 경쟁함.
            else:
                legalActions = gameState.getLegalActions(agentIndex) 
                if agentIndex == gameState.getNumAgents() - 1: #만약 마지막 유령이면
                    next_agent, next_depth = 0, depth - 1 # depth를 하나 줄이고 pacman부터 다시 조사할 것임.
                else:
                    next_agent, next_depth = agentIndex + 1, depth
                value, min_action = float('inf'), Directions.STOP #ghost는 minimum agent이므로 value를 inf로 초기화.
                for action in legalActions:
                    new_score = alphabeta(gameState.generateSuccessor(agentIndex, action), next_agent, next_depth, alpha, beta)[0]
                    if new_score < value:
                        value, min_action = new_score, action # 새롭게 조사된 함숫값이 더 작을 경우, value를 갱신함.
                    if new_score < alpha:
                        return new_score, action #새로 acquired된 score가 alpha(이전 agent들의 successor값 중 최소)보다 작은 값이 나왔으면, 자식들도 검사할 필요가 없으므로 new_score 반환
                    beta = min(beta, value)
                return value, min_action

        return alphabeta(gameState, 0, self.depth, float('-inf'), float('inf'))[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
