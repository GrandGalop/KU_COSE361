# search.py
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from ast import AsyncFunctionDef
from operator import index
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    agloc = util.Stack() # DFS는 최근 탐색한 node의 successor들을 탐색하므로 Stack 자료형을 채용하겠다. (agentlocation)
    agloc.push(problem.getStartState()) # StartState를 push
    path = util.Stack() # agloc Stack의 i번째 요소의 pathway를 저장하기 위한 path Stack을 제작. 해당 리스트의 각 요소는 list 자료형이다.
    locpath = util.Stack() # 후술할 for문에서 path.pop()을 통해 꺼낸 마지막 요소(리스트)를 저장하는 변수 (location's pathway)
    
    '''
    시작 노드에서 빼내어 successor들을 저장하는 부분.
    어째서 while문에 산합하지 아니하였나면 이 시점에서 path.list는 null이기 때문에
    path.pop을 수행할 수 없어 별도로 배치하였다.
    '''
    already = [problem.getStartState()]  # 방문한 node를 successor로 지정되는 것을 막기 위해 already list를 만들어 방문 할 때마다 저장할 것  
    location = agloc.pop() # agent의 현재 위치를 받는 변수 location
    if problem.isGoalState(location):
        return [] #만약 location이 Goal이면 Null list를 받게 된다.
    else:
        for successor, action, stepcost in problem.getSuccessors(location): # getSuccessor function은 successor, action, stepcost로 구성된 tupule을 반환.
            if not successor in already:
                agloc.push(successor) # successor location을 받아 agloc에 push
                path.push([action]) # 해당 successor의 action을 받아 path에 push (StartState의 successor의 action들을 각각 배열로 만들어서 push)
                already.append(location) # 작업이 모두 끝나면 location을 already목록에 추가한다.
    
    """
    시작 node의 successor들을 탐색해 나가는 부분
    이 때에는 locpath를 path로부터 push받아 여기에 action이 추가되어 다시 path에 저장된다.
    """
    while problem.isGoalState(agloc.list[-1]) != True: # 가장 최근에 push된 agloc의 요소가 Goal State일 때까지 while문을 돌림.
        location = agloc.pop()
        locpath = path.pop()
        for successor, action, stepcost in problem.getSuccessors(location):
            if not successor in already:
                agloc.push(successor)
                path.push(locpath+[action]) # path의 각 요소는 element이어야 하므로 locpath(각 요소: actions)에 action을 추가하여 이를 element로써 push한다.
                already.append(location)
    return path.list[-1] # while문이 탈출할 때, 즉 agloc의 마지막 요소가 Goal일 때 이에 대응되는 path의 마지막 요소를 return한다.


    
    

    
    

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    agloc = util.Queue() # BFS는 각각 탐색한 노드의 successor들을 먼저 탐색하므로 Queue 자료형을 채용
    agloc.push(problem.getStartState())
    path = util.Queue() 
    locpath = util.Stack() # locpath는 BFS의 특징과 상관없이 pathway를 저장하므로 stack 자료형을 채용
    
    already = [problem.getStartState()]
    location = agloc.pop()
    if problem.isGoalState(location)==True:
        return []
    else:
        for successor, action, stepcost in problem.getSuccessors(location):
            if not successor in already:
                agloc.push(successor)
                path.push([action])
                already.append(successor) # DFS와 달리 successor을 저장하는 이유는 만약 location을 저장할 경우 successor의 successor이 중복 조사 될 수 있다.

    while problem.isGoalState(agloc.list[-1]) != True:
        location = agloc.pop()
        locpath = path.pop() 
        for successor, action, stepcost in problem.getSuccessors(location):
            if not successor in already:
                agloc.push(successor)
                path.push(locpath+[action])
                already.append(successor) 
    return path.list[-1]

    

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    agloc=util.PriorityQueue() # 가장 priority가 낮은 location부터 pop해야 하므로 PriorityQueue를 채용
    agloc.push((problem.getStartState(), []), 0) # priorityQueue는 pop하는 리스트의 번호가 일관적이지 않으므로 한 번에 튜플로 묶어 관리하였다.
    already = []
    if problem.isGoalState(problem.getStartState()):
        return []
    else:
        location, path = agloc.pop()
        already += [location]
        for successor, action, stepcost in problem.getSuccessors(location):
            if not successor in already:
                agloc.push((successor, [action]), problem.getCostOfActions([action])) # priority cost는 해당 successor까지 도달하는 action list에 getCostOfActions 함수를 적용시켜 구할 수 있다.
                if problem.isGoalState(successor)!=True:
                    already += [successor] # 처음에 successor가 goal일 때에는 넣지 않는 이유는, 산입했을 경우 더 cost가 낮은 pathway가 존재해도 goal state가 already에 있어 조사하지 않는 경우가 생길 수 있기 때문이다.


    while len(agloc.heap) != 0: # PriorityQueue는 탐색할 node의 list 번호를 알 수 없으므로, heap이 모두 비워지기 전까지 while문을 수행시켰다.
        location, path = agloc.pop()
        if problem.isGoalState(location):
            return path # pop한 location이 종점인지를 DFS, BFS와 달리 해당 부분에서 수행한다. 
        else:
            for successor, action, stepcost in problem.getSuccessors(location):
                if not successor in already:
                    agloc.push((successor, path + [action]), problem.getCostOfActions(path + [action])+stepcost) # 각각 successor의 priority는 path+action의 getCostOfActions이다.
                    already += [successor] 




def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    agloc = util.PriorityQueue()
    agloc.push((problem.getStartState(), [], 0), heuristic(problem.getStartState(), problem)) # location과 pathway, cost를 tuple로 묶어 저장함.
    already = []
    pathdic={} # 어떤 node의 path를 저장하는 dictionary
    costdic={} # 어떤 node의 cost를 저장하는 dictionary
    while len(agloc.heap) != 0:
        location, path, cost = agloc.pop()
        pathdic[location]=path
        costdic[location]=cost
        # node를 pop할 때 마다 해당 노드의 path와 cost를 각각의 dictionary에 저장하여준다.
        if problem.isGoalState(location):
            return path 

        if location in already:
            continue # 탐색하는 후보가 이미 방문했으면 skip하고 진행함. 이 부분 덕분에 agloc에 중복된 location이 쌓여도 모두 kill 될 수 있다.

        already += [location] # 탐색하는 node를 already에 추가시켜 주어 재탐색되는 것을 방지함

        for successor, action, stepcost in problem.getSuccessors(location):
            """
            만약 successor가 agloc에 있지만 새롭게 발견된 path가 더욱 efficient하다면 갱신해줄 필요가 있다. 
            더 나중에 push되어도 priorityQueue이므로 갱신된 node가 먼저 pop될 것이고,
            더 priority 순위가 낮은 node는 221번째 줄에 의해 kill될 것이다.
            """
            if successor in pathdic and costdic[successor]>cost+stepcost: 
                costdic[successor]=cost+stepcost
                path[successor]=path+[action]
                agloc.push((successor, path+[action], cost+stepcost), cost+stepcost+heuristic(successor, problem))
            elif not successor in already:
                agloc.push((successor, path+[action], cost+stepcost), cost+stepcost+heuristic(successor, problem))


        

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
