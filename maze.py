with open('maze_map.txt', 'w') as outfile:
  outfile.write('2\n')
  outfile.write('3 6 -3\n')
  outfile.write('5 14 -1\n')
  outfile.write('xxxxxxxxxxxxxxxxxxxxxx\n')
  outfile.write('x   x   xx xx        x\n')
  outfile.write('x     x     xxxxxxxxxx\n')
  outfile.write('x x   +xx  xxxx xxx xx\n')
  outfile.write('  x   x x xx   xxxx  x\n')
  outfile.write('x          xx +xx  x x\n')
  outfile.write('xxxxxxx x      xx  x x\n')
  outfile.write('xxxxxxxxx  x x  xx   x\n')
  outfile.write('x          x x Sx x  x\n')
  outfile.write('xxxxx x  x x x     x x\n')
  outfile.write('xxxxxxxxxxxxxxxxxxxxxx')

import os
from queue import PriorityQueue
from collections import deque
import matplotlib.pyplot as plt

def visualize_maze(matrix, bonus, start, end, route=None, path=None):
    """
    Args:
      1. matrix: The matrix read from the input file,
      2. bonus: The array of bonus points,
      3. start, end: The starting and ending points,
      4. route: The route from the starting point to the ending one, defined by an array of (x, y), e.g. route = [(1, 2), (1, 3), (1, 4)]
    """
    #1. Define walls and array of direction based on the route
    walls=[(i,j) for i in range(len(matrix)) for j in range(len(matrix[0])) if matrix[i][j]=='x']

    if route:
        direction=[]
        for i in range(1,len(route)):
            if route[i][0]-route[i-1][0]>0:
                direction.append('v') #^
            elif route[i][0]-route[i-1][0]<0:
                direction.append('^') #v        
            elif route[i][1]-route[i-1][1]>0:
                direction.append('>')
            else:
                direction.append('<')

        direction.pop(0)

    #2. Drawing the map
    ax=plt.figure(dpi=100).add_subplot(111)

    for i in ['top','bottom','right','left']:
        ax.spines[i].set_visible(False)

    plt.scatter([i[1] for i in walls],[-i[0] for i in walls],
                marker='X',s=100,color='black')
    
    plt.scatter([i[1] for i in bonus],[-i[0] for i in bonus],
                marker='P',s=100,color='green')

    plt.scatter(start[1],-start[0],marker='*',
                s=100,color='gold')
    if path:
        plt.scatter([i[1] for i in path],[-i[0] for i in path],
                s=3,color='blue')
    if route:
        for i in range(len(route)-2):
            plt.scatter(route[i+1][1],-route[i+1][0],
                        marker=direction[i],color='silver')

    plt.text(end[1],-end[0],'EXIT',color='red',
         horizontalalignment='center',
         verticalalignment='center')
    plt.xticks([])
    plt.yticks([])
    plt.show()

    print(f'Starting point (x, y) = {start[0], start[1]}')
    print(f'Ending point (x, y) = {end[0], end[1]}')
    
    for _, point in enumerate(bonus):
      print(f'Bonus point at position (x, y) = {point[0], point[1]} with point {point[2]}')

def read_file(file_name: str = 'maze_map.txt'):
    f=open(file_name,'r')
    n_bonus_points = int(next(f)[:-1])
    bonus_points = []
    for i in range(n_bonus_points):
        x, y, reward = map(int, next(f)[:-1].split(' '))
        bonus_points.append((x, y, reward))

    text=f.read()
    matrix=[list(i) for i in text.splitlines()]
    f.close()

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j]=='S':
                start=(i,j)
            elif matrix[i][j]==' ':
                if (i==0) or (i==len(matrix)-1) or (j==0) or (j==len(matrix[0])-1):
                    end=(i,j)
            else:
                pass

    return bonus_points, matrix, start, end
<<<<<<< HEAD

# BFS without bonus point:
def BFS(matrix,start,end):

    queue = deque()

    R, C = len(matrix), len(matrix[0])
    queue.appendleft((start[0], start[1], 0, [start[0] * C + start[1]]))
    #directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    directions = [[-1, 0], [1, 0], [0, 1], [0, -1]]
    visited = [[False] * C for _ in range(R)]

    while len(queue) != 0:
        coord = queue.pop()
        visited[coord[0]][coord[1]] = True

        if (coord[0],coord[1]) == end:
            return coord[2], [(i//C, i%C) for i in coord[3]] # Return path length, boxes on path

        for dir in directions:
            nr, nc = coord[0] + dir[0], coord[1] + dir[1]
            if (nr < 0 or nr >= R or nc < 0 or nc >= C or matrix[nr][nc] == "x" or visited[nr][nc]): 
                continue
            queue.appendleft((nr, nc, coord[2] + 1, coord[3] + [nr * C + nc]))

# BFS with bonus:
def BFS_bonus(matrix,start,end,bonus=None):
    
    queue = deque()

    R, C = len(matrix), len(matrix[0])
    queue.appendleft((start[0], start[1], 0, [start[0] * C + start[1]]))
    directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    visited = [[False] * C for _ in range(R)]
    path = []
    while len(queue) != 0:
        coord = queue.pop()
        visited[coord[0]][coord[1]] = True

        if (coord[0],coord[1]) == end:
            return coord[2], [(i//C, i%C) for i in coord[3]], path # Return path length, boxes on path

        for dir in directions:
            nr, nc = coord[0] + dir[0], coord[1] + dir[1]
            if (nr < 0 or nr >= R or nc < 0 or nc >= C or matrix[nr][nc] == "x" or visited[nr][nc]): 
                continue
            queue.appendleft((nr, nc, coord[2] + 1, coord[3] + [nr * C + nc]))
            path.append((nr,nc))

def DFS_a(matrix,start,end):
=======
  
  
def DFS(matrix,start,end,bonus=None):
  stack = [start]
  e = []
  while len(stack)!=0:
      s = stack.pop()
      e.append(s)
      neighbor=[]
      for i in [-1,1]: 
          if matrix[s[0]][s[1]+i] != 'x':
              neighbor.append((s[0],s[1]+i))
      for i in [-1,1]:
          if matrix[s[0]+i][s[1]] != 'x':
              neighbor.append((s[0]+i,s[1]))
      if(end in neighbor):
          e.append(end)
          return e
      for k in neighbor:
          if k not in stack and k not in e:
              stack.append(k)
  #e.remove(start)
  return e       
#DFS without bonus point
def DFS_a(matrix,start,end): #simular with BFS, change queue to stack
>>>>>>> dc8ec516fe58e9d9a568e83ab4eda44ee79ecc87
    stack = [start]
    R, C = len(matrix), len(matrix[0])
    stack.append((start[0], start[1], 0, [start[0] * C + start[1]]))
    directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    visited = [[False] * C for _ in range(R)]

    while len(stack) != 0:
        coord = stack.pop()
        visited[coord[0]][coord[1]] = True

        if (coord[0],coord[1]) == end:
            return coord[2], [(i//C, i%C) for i in coord[3]] # Return path length, boxes on path

        for dir in directions:
            nr, nc = coord[0] + dir[0], coord[1] + dir[1]
            if (nr < 0 or nr >= R or nc < 0 or nc >= C or matrix[nr][nc] == "x" or visited[nr][nc]): continue
            stack.append((nr, nc, coord[2] + 1, coord[3] + [nr * C + nc]))
<<<<<<< HEAD

=======
            
>>>>>>> dc8ec516fe58e9d9a568e83ab4eda44ee79ecc87
def DFS_b(matrix,start,end):
    directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    R, C = len(matrix), len(matrix[0])
    visited = [[False] * C for _ in range(R)]
    #stack
    explored=[start]
    frontier=[start]
    dfsPath={}
    while len(frontier)>0:
        coord=frontier.pop()
        visited[coord[0]][coord[1]] = True
        if coord==end:
            break
        for dir in directions:
            nr, nc = coord[0] + dir[0], coord[1] + dir[1]
            if (nr < 0 or nr >= R or nc < 0 or nc >= C or matrix[nr][nc] == "x" or visited[nr][nc]): continue
            child = nr,nc
            explored.append(child)
            frontier.append(child)
            dfsPath[child]=coord
        
    fwdPath = {}
    route = []
    cell = end
    lenOfRoute = 0
<<<<<<< HEAD
    while cell!=start: #reverse path to find route
=======
    while cell!=start: #find route from end to start
>>>>>>> dc8ec516fe58e9d9a568e83ab4eda44ee79ecc87
        fwdPath[dfsPath[cell]]=cell
        cell=dfsPath[cell]
        route.append(cell)
        lenOfRoute = lenOfRoute+1
    route.reverse()
    return lenOfRoute, route  

<<<<<<< HEAD
=======
# BFS without bonus point:
def BFS(matrix,start,end):
    from collections import deque
    queue = deque()

    R, C = len(matrix), len(matrix[0])
    queue.appendleft((start[0], start[1], 0, [start[0] * C + start[1]]))
    directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    visited = [[False] * C for _ in range(R)]

    while len(queue) != 0:
        coord = queue.pop()
        visited[coord[0]][coord[1]] = True

        if (coord[0],coord[1]) == end:
            return coord[2], [(i//C, i%C) for i in coord[3]] # Return path length, boxes on path

        for dir in directions:
            nr, nc = coord[0] + dir[0], coord[1] + dir[1]
            if (nr < 0 or nr >= R or nc < 0 or nc >= C or matrix[nr][nc] == "x" or visited[nr][nc]): continue
            queue.appendleft((nr, nc, coord[2] + 1, coord[3] + [nr * C + nc]))

>>>>>>> dc8ec516fe58e9d9a568e83ab4eda44ee79ecc87
#A-star
def heuristic(cell1,cell2):
    '''Heuristic function'''
    x1,y1=cell1
    x2,y2=cell2

    return abs(x1-x2) + abs(y1-y2)

def A_star(matrix,start,end):
<<<<<<< HEAD
=======
    from queue import PriorityQueue
>>>>>>> dc8ec516fe58e9d9a568e83ab4eda44ee79ecc87
    queue = PriorityQueue()

    R, C = len(matrix), len(matrix[0])
    h0 = heuristic(start,end)
    queue.put((h0+0,h0,start[0], start[1], 0, [start[0] * C + start[1]]))
    directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    visited = [[False] * C for _ in range(R)]

    while not queue.empty():
        coord = queue.get()
        '''
        coord[0]: f() = h() + g()
        coord[1]: h()
        coord[2][3]: cell point
        coord[4]: g() (length)
        coord[5]: route
        '''
        visited[coord[2]][coord[3]] = True

        if (coord[2],coord[3]) == end:
            return coord[4], [(i//C, i%C) for i in coord[5]] # Return path length, boxes on path

        for dir in directions:
            nr, nc = coord[2] + dir[0], coord[3] + dir[1]
            g = coord[2] + 1
            if (nr < 0 or nr >= R or nc < 0 or nc >= C or matrix[nr][nc] == "x" or visited[nr][nc]): continue
            g = coord[4] + 1
            h = heuristic((nr,nc),end)
            queue.put((h+g, h, nr, nc, g, coord[5] + [nr * C + nc]))

<<<<<<< HEAD
=======
if __name__=="__main__":
    b,m,s,e =read_file()
    route = DFS(m,s,e,b)
    print(route)
    visualize_maze(m,b,s,e,route)
>>>>>>> dc8ec516fe58e9d9a568e83ab4eda44ee79ecc87



def heuristic_bonus(start, end, bonus):
    heuristic(start,bonus) + heuristic(bonus, end) + bonus[2]

def Greedy_BFS(matrix, start, end, bonus = None):
    route_full = []
    open = PriorityQueue()
    open.put(heuristic(start,end),start)
    end_point = (end, 0)
    points = bonus+end
    while not open.empty():
        currCell = open.get()
        for b in bonus:
            leng, route = A_star(matrix, currCell, b)
            cost = leng + b[2]
            route_full += route
            heuristic_bonus()
            open.put(cost, b, route)



if __name__=="__main__":
    b,m,s,e =read_file()
    lenOfRoute, route, path = BFS_bonus(m,s,e)
    
    visualize_maze(m,b,s,e,route,path)
    