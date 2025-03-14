from collections import deque

def bfs(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]     # Di chuyển lên, xuống, trái, phải
    queue = deque([(start, [])])                        # Vị trí hiện tại
    visited = set()
    visited.add(start)
    
    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == goal:
            return path + [(x, y)]                      # Trả về đường đi hoàn chỉnh
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] != '#' and (nx, ny) not in visited:
                queue.append(((nx, ny), path + [(x, y)]))
                visited.add((nx, ny))
                
    return None                                         # Không tìm thấy đường dẫn

maze = [
    ['#', '#', '#', '#', '#', 'P', '#'],
    ['#', 'G', '#', ' ', '#', ' ', '#'],
    ['#', ' ', ' ', ' ', '#', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', '#', '#', '#', '#', '#', '#']
]

start = (3, 1)  # Vị trí của ma (G)
goal = (3, 5)   # Vị trí của Pac-Man (P)

path = bfs(maze, start, goal)
print("Path:", path)