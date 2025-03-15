from collections import deque

# check ô lân cận đi đc
def get_neighbors(position, maze):
    x, y = position
    neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    valid_neighbors = []

    for nx, ny in neighbors:
        if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] != '#':
            valid_neighbors.append((nx, ny))

    return valid_neighbors

def bfs(start, goal, maze):
    queue = deque([(start, [start])])
    visited = set()
    visited.add(start)

    while queue:
        current, path = queue.popleft()

        if current == goal:
            return path  #  trả về đường tìm đc

        for neighbor in get_neighbors(current, maze):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return []  # 0 thấy đường 


def dfs(start, goal, maze):
    stack = [(start, [start])]
    visited = set()
    visited.add(start)

    while stack:
        current, path = stack.pop()

        if current == goal:
            return path  # trả về đường tìm đc

        for neighbor in get_neighbors(current, maze):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append((neighbor, path + [neighbor]))

    return []  # 0 thấy đường

# define ghost
class Ghost:
    def __init__(self, start_position):
        self.position = start_position

    def move(self, pacman_position, maze):
        pass

# Blue Ghost BFS
class BlueGhost(Ghost):
    def move(self, pacman_position, maze):
        path = bfs(self.position, pacman_position, maze)
        if path and len(path) > 1:
            self.position = path[1]  

# Pink Ghost DFS
class PinkGhost(Ghost):
    def move(self, pacman_position, maze):
        path = dfs(self.position, pacman_position, maze)
        if path and len(path) > 1:
            self.position = path[1]  

# test
if __name__ == "__main__":
    maze = [
        ['.', '.', '.', '#', '.', '.'],
        ['.', '#', '.', '#', '.', '.'],
        ['.', '#', '.', '.', '.', '.'],
        ['.', '.', '#', '#', '#', '.'],
        ['.', '.', '.', '.', '.', '.']
    ]

    pacman_pos = (5, 0)
    blue_ghost = BlueGhost((0, 0))
    pink_ghost = PinkGhost((0, 5))

    print("Pac-Man ở vị trí:", pacman_pos)

    for _ in range(5):
        blue_ghost.move(pacman_pos, maze)
        pink_ghost.move(pacman_pos, maze)

        print(f"Blue Ghost ở vị trí: {blue_ghost.position}")
        print(f"Pink Ghost ở vị trí: {pink_ghost.position}")

        if blue_ghost.position == pacman_pos:
            print("Blue Ghost đã bắt được Pac-Man!")
            break

        if pink_ghost.position == pacman_pos:
            print("Pink Ghost đã bắt được Pac-Man!")
            break
