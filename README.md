# **Readme - Korea University COSES361 인공지능 (prof. HyunWoo Kim)**
Pacman project

Assignment 1: Single-agent searching with implemented Depth First Search / Breadth First Search / Uniform Cost Search / A* search algorithms

Assignment 2: Multi-agent searching with implemented Minimax and Alpha-Beta pruning algorithms

Minicontest 1: Playing Pacman with implemented custom agent

Minicontest 2: Competitive gaming with implemented custom agent

## **Assignment 1: Search Algorithms for Pacman**
This assignment involves implementing various **search algorithms** to control Pacman in a **grid-based environment**. The algorithms will be used to navigate Pacman efficiently towards a goal while avoiding obstacles.

### **1. Depth-First Search (DFS)**
- Explores the **deepest nodes first** using a **stack (LIFO)** structure.
- Not guaranteed to find the shortest path.
- May get stuck in loops unless properly implemented with a **visited state list**.

  **Implementation Details:**
  - Uses a `Stack` to store nodes.
  - Expands a node by **pushing successors** onto the stack.
  - Returns the **first found goal state path**.

### **2. Breadth-First Search (BFS)**
- Explores the **shallowest nodes first** using a **queue (FIFO)** structure.
- Guarantees the **shortest path** in an **unweighted grid**.
- Uses a `Queue` to expand nodes in order of discovery.

  **Implementation Details:**
  - Uses a `Queue` to store frontier nodes.
  - Expands a node by **enqueuing its successors**.
  - Ensures **goal state is reached with minimal steps**.

### **3. Uniform Cost Search (UCS)**
- A **cost-based search** that expands the **lowest-cost node first**.
- Uses a **Priority Queue**, ordering nodes by **total cost from the start state**.
- Guarantees the **optimal path** if all costs are positive.

  **Implementation Details:**
  - Uses a **PriorityQueue** to store nodes based on cost.
  - Expands the node with the **lowest total cost** first.
  - Updates cost dynamically as new paths are explored.

### **4. A* Search (A-Star)**
- A heuristic-based search that combines **UCS with a heuristic function**.
- Expands nodes based on:
  
  $$f(s) = g(s) + h(s)$$

  where:
  - \( g(s) \) = cost to reach node \( s \)
  - \( h(s) \) = heuristic estimate to goal
- Guarantees **optimal path** if the heuristic function is **admissible and consistent**.

  **Implementation Details:**
  - Uses a **PriorityQueue**, prioritizing based on **cost + heuristic**.
  - Maintains a dictionary to track **best-cost paths**.
  - If a **better path** to a node is found, it updates the cost.

### **Pacman Integration**
- The implemented algorithms are used to **control Pacman** in a **grid-world environment**.
- The **search algorithms are called by the Pacman agent**, which runs the simulation.
- Pacman **navigates the maze efficiently** based on the search method selected.

## **Assignment 2: Adversarial Search in Pacman**
This assignment involves implementing **Minimax** and **Alpha-Beta Pruning** search algorithms to control Pacman in an **adversarial environment**. The goal is to help Pacman make optimal decisions against one or more ghosts, treating them as opponents.

### **1. Minimax Algorithm**
- A **game tree search** algorithm used for decision-making in adversarial environments.
- Assumes **Pacman (agent 0) maximizes score** and **ghosts minimize Pacman’s score**.
- Constructs a **game tree** up to a certain depth and evaluates possible moves.

  **Implementation Details:**
  - Pacman chooses actions using the **maximization strategy**.
  - Ghosts choose actions using the **minimization strategy**.
  - The game state is evaluated using a **heuristic function**.
  - The recursive Minimax function alternates between **Pacman (max) and ghosts (min)**.

  **Mathematical Representation:**
  $$v(s) =\begin{cases} \max_{a} v(s') & \text{if agent is Pacman} \\\min_{a} v(s') & \text{if agent is a Ghost}\end{cases}$$
  where:
  - \( s' \) is the successor state after action \( a \).
  - The search tree expands up to a **fixed depth**.

### **2. Alpha-Beta Pruning**
- An **optimized version of Minimax** that eliminates unnecessary branches.
- Uses **two bounds, α (alpha) and β (beta)**, to skip evaluating nodes that cannot influence the final decision.
- Ensures the **same optimal decision** as Minimax but improves efficiency.

  **Implementation Details:**
  - **α (alpha)**: The best **max** value found so far (Pacman).
  - **β (beta)**: The best **min** value found so far (Ghosts).
  - **Pruning occurs** when:
    $$\alpha \geq \beta$$
    - If a node’s value **exceeds β**, the branch is **pruned**.
    - If a node’s value **is less than α**, the branch is **pruned**.

  **Performance Improvement:**
  - Reduces the number of nodes evaluated compared to Minimax.
  - Faster decision-making for Pacman.

### **Pacman Integration**
- The implemented algorithms are used to **control Pacman** in an **adversarial setting**.
- The **game tree is dynamically built** based on **Pacman’s and ghosts’ actions**.
- The **search depth** controls the complexity of decision-making.
