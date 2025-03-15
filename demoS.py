import heapq

def uniform_cost_search(graph, start, goal):
    priority_queue = [(0, start)]  # (cost, node)
    visited = {}
    
    while priority_queue:
        cost, node = heapq.heappop(priority_queue)
        
        if node in visited:
            continue
        
        visited[node] = cost
        
        if node == goal:
            return cost
        
        for neighbor, weight in graph.get(node, []):
            if neighbor not in visited:
                heapq.heappush(priority_queue, (cost + weight, neighbor))
    
    return float("inf")  # Goal not reachable

def a_star_search(graph, start, goal, heuristic):
    priority_queue = [(heuristic[start], 0, start)]  # (estimated cost, cost so far, node)
    visited = {}
    
    while priority_queue:
        _, cost, node = heapq.heappop(priority_queue)
        
        if node in visited:
            continue
        
        visited[node] = cost
        
        if node == goal:
            return cost
        
        for neighbor, weight in graph.get(node, []):
            if neighbor not in visited:
                estimated_cost = cost + weight + heuristic[neighbor]
                heapq.heappush(priority_queue, (estimated_cost, cost + weight, neighbor))
    
    return float("inf")  # Goal not reachable

# Example graph (Adjacency List Representation)
graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('D', 2), ('E', 5)],
    'C': [('E', 1)],
    'D': [('G', 3)],
    'E': [('G', 1)],
    'G': []
}

# Example heuristic values for A*
heuristic = {
    'A': 7, 'B': 6, 'C': 2, 'D': 3, 'E': 1, 'G': 0
}

# Run UCS and A*
start, goal = 'A', 'G'
print("Uniform Cost Search Cost:", uniform_cost_search(graph, start, goal))
print("A* Search Cost:", a_star_search(graph, start, goal, heuristic))
