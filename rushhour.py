import sys
import random
import heapq

class Board:

    def __init__(self):
        self.board = ""

    def stateRepresentation(self, board):
        ''' This function takes in a board as a String and represents it as an array. '''

        array = []
        buffer  = []
        for i in range(0,len(board)):
            if(board[i] == '|'):
                array.append(buffer)
                buffer = []
            else:
                buffer.append(board[i])
            i = i+1

        array.append(buffer)
        return array

    def printBoard(self, board):
        ''' This function displays the board. '''

        buffer = "|"
        space = int(len(self.stateRepresentation(board)))/2 - 1
        print(" ------ ")
        for i in range(0,len(board)):
            if(board[i] == '|'):
                if(space != 0):
                    print(buffer + "|")
                else:
                    print(buffer + " ")
                buffer = ""
                space = space - 1
            buffer = buffer + board[i]
            i = i+1

        print(buffer + "|")
        print(" ------ ")

    def done(self, board):
        ''' This function checks return True if the board is in the done stage and False if not. '''

        flag = False
        space = int(len(self.stateRepresentation(board)))/2 - 1
        for i in range(0,len(board)-1):
            if(board[i] == 'x' and board[i+1] == '|' and space == 0):
                flag = True
                break
            i = i+1
            if(board[i] == '|'):
                space = space - 1

        return flag 

    def generateStringFromArray(self,array):
        ''' This function converts a board from an array to a String. '''

        buffer = ""
        for i in range(0,len(array)):
            for j in range(0, len(array[0])):
                buffer = buffer + array[i][j]
            buffer = buffer + '|'

        return buffer[:-1]

    def makeStringFromRow(self,row):
        ''' This function converts a row board from an array to a String. '''

        s = ""
        for i in range(0,len(row)):
            s = s + row[i]
        
        return s

    def makeRowFromString(self,s):
        ''' This function converts a board row from an String to an array. '''

        row = []
        for i in range(0,len(s)):
            row.append(s[i])
        
        return row

    def makeStringFromColumn(self, array, j):
        ''' This function converts a board column from an array to a String. '''

        s = ""
        for row in array:
            s = s + row[j]
        
        return s

    def makeBoardFromColumn(self, array, s, j):
        ''' This function converts a board column from a String to an array. '''

        i = 0
        for row in array:
            row[j] = s[i]
            i = i+1

        return array

    def getIndex(self, board):
        ''' This function returns the starting positions of all the cars. '''

        unique  = set()
        coordinates = []

        for i in range(0,len(board)):
            for j in range(0, len(board[0])):
                if(board[i][j] != ' ' and board[i][j] not in unique):
                    unique.add(board[i][j])
                    coordinates.append((i,j))
        
        return coordinates

    def getPositions(self, board, car):
        ''' This function returns the starting and the ending positions of a car. '''
        
        positions = []

        for i in range(0,len(board)):
            for j in range(0, len(board[0])):
                if(board[i][j] == car):
                    positions.append((i,j))
        
        return positions

    def clone(self, board):  
        ''' This function creates a copy of a board. '''

        return board.copy()

    def getOrientation(self,cars):
        ''' This function returns the orientation of all the cars on the board. '''

        horizontal = []
        vertical = []

        for car in cars:
            if(car[0][0] == car[-1][0]):
                horizontal.append([car[0],car[-1]])
            else:
                vertical.append([car[0],car[-1]])

        return (horizontal, vertical)

    def getCars(self,array):
        ''' This returns the starting and the ending positions of all the cars. '''

        indices = self.getIndex(array)
        cars = []

        for index in indices:
            cars.append(self.getPositions(array, array[index[0]][index[1]]))
            
        return cars

    def move(self, row, i, j, l, direction):
        ''' This function returns the row after moving in left or right direction. '''

        if(direction == 'left'):
            s = self.makeStringFromRow(row)
            row = self.makeRowFromString(s[:j] + s[j+1: j+l+1] + " " + s[j+l+1:])
        
        elif(direction == 'right'):
            s = self.makeStringFromRow(row)
            row = self.makeRowFromString(s[:j-l] + " " + s[j-l:j] + s[j+1:])
            
        return row

    def next_for_car(self, array, cars):
        ''' This function moves the cars in left or right direction using DFS. '''

        horizontal = self.getOrientation(cars)[0]

        for row in horizontal:
            
            length = row[1][1] - row[0][1] + 1
            left = (row[0][0], row[0][1]-1)
            right = (row[1][0], row[1][1]+1)
            

            if(left[0] >= 0 and left[1] >= 0 and left[0] < len(array) and left[1] < len(array)):
                
                i = left[0]
                j = left[1]
            
                if(array[i][j] == ' '):
                
                    new_row =  self.makeStringFromRow(self.move(self.clone(array[i]), i, j, length, 'left'))
                    if((new_row, i) not in next_boards and (new_row, i) not in current_states):
                        next_boards.add((new_row, i))
                        new_array = self.clone(array)
                        new_array[i] = self.makeRowFromString(new_row)
                        self.next_states(self.generateStringFromArray(new_array))

                        
            if(right[0] >= 0 and right[1] >= 0 and right[0] < len(array) and right[1] < len(array)):
                
                i = right[0]
                j = right[1]

                if(array[i][j] == ' '):
                
                    new_row =  self.makeStringFromRow(self.move(self.clone(array[i]), i, j, length, 'right'))
                    if((new_row, i) not in next_boards and (new_row, i) not in current_states):
                        next_boards.add((new_row, i))
                        new_array = self.clone(array)
                        new_array[i] = self.makeRowFromString(new_row)
                        self.next_states(self.generateStringFromArray(new_array))


    def next_states(self, board):
        ''' This function calculates the next possible moves from a given board state. '''

        array = self.stateRepresentation(board)

        for i, row in enumerate(array):
            current_states.add((self.makeStringFromRow(row), i))

        cars = self.getCars(array)
        self.next_for_car(array, cars)
        
    def next(self, board):
        ''' This function returns the next possible moves from a given board state. '''

        array = self.stateRepresentation(board)
        transpose = self.generateStringFromArray([[array[j][i] for j in range(len(array))] for i in range(len(array[0]))])
        next_strings = []
        self.next_states(board)

        for board in next_boards:
            row_array = self.clone(array)
            row_array[board[1]] = self.makeRowFromString(board[0])
            s = self.generateStringFromArray(row_array)
            next_strings.append(s)

        next_boards.clear()
        current_states.clear()
        self.next_states(transpose)

        for board in next_boards:
            column_array = self.clone(array)
            column = self.makeBoardFromColumn(column_array, board[0], board[1])
            s = self.generateStringFromArray(column)
            next_strings.append(s)
       
        next_boards.clear()
        current_states.clear()

        return next_strings
        
class Path:

    def __init__(self):
        self.boards = []
    
    def clone(self):
        ''' This function clones the current path. '''

        boards = Path(self.boards.copy())
        return boards 
    
    def add(self, board):
        ''' This function adds a board to the path. '''

        self.boards.append(board)
    
    def last(self):
        ''' This function returns the last board in the path. '''

        if len(self.boards) >= 1:
            return self.boards[len(self.boards)-1]
        else:
            return None

    def printPath(self):
        ''' This function prints all the paths. '''

        b = Board()
        for board in self.boards:
            b.printBoard(board)

    def random(self, board):
        ''' This function solves the board using Random Walk algorithm with N=10. '''

        b = Board()
        self.add(board)
        N = 10
        i = 0
    
        while i < N and not b.done(self.last()):
            array = b.next(self.last())
            path = random.choice(array)
            self.add(path)
            i = i + 1

        self.printPath()

    def bfs(self, board):
        ''' This function solves the board using the Breadth First Search algorithm. '''

        b = Board()
        
        queue = []
        visited = []
        root = []

        queue.append(board)
        root.append((board, None))

        i = 0

        while queue: 
            current = queue.pop(0)
            if(current in visited):
                root.pop(i)
                continue
            
            visited.append(current)
            b.printBoard(current)

            if(b.done(current)):
                break
            for string in b.next(current):
                queue.append(string)
                root.append((string, current))
               
            i = i + 1

        print(f"Number of Paths explored: {i}")
        print("Path: ")

        while i >= 0:
           
            if(root[i][0] == current):
                self.add(current)
                current = root[i][1]
            i = i - 1
        
        self.boards.reverse()
        self.printPath()
        
        print(f"Solved in {len(self.boards) - 1} steps.")
    
    def astar(self, board):
        ''' This function solves the board using the A-star algorithm. '''

        b = Board()
        
        queue = []
        visited = []
        root = []

        queue.append(board)
        root.append((board, None))
        i = 0

        while queue: 
            
            current = queue.pop(0)

            if(current in visited): 
                root.pop(i)
                continue
            
            visited.append(current)
            b.printBoard(current)

            if(b.done(current)):
                break
            
            array = self.getHeap(b.next(current), root, i)

            for string in array:
                queue.append(string)
                root.append((string, current))

            i = i + 1

        print(f"Number of Paths explored: {i}")

        while i >= 0:
            
            if(root[i][0] == current):
                self.add(current)
                current = root[i][1]
            i = i - 1
        
        self.boards.reverse()
        self.printPath()
   
        print(f"Solved in {len(self.boards) - 1} steps.")

    def getHeap(self, array, root, i):
        ''' This function adds and return elements in the min heap. '''

        heap = []

        for string in array:
            g = self.getDepth(string, root, i)
            h = self.getHeuristic(string)
            heapq.heappush(heap, (g + h, string))

        return [j[1] for j in heap]

    def getHeuristic(self, board):
        ''' This function calculates the manhattan distance between the current position and the goal position of x car as heuristic. '''

        b = Board()
        array = b.stateRepresentation(board)
        space = (int(len(array))/2 - 1, len(array[0])-1)

        for i in range(0,len(array)):
            for j in range(0,len(array[0])):
                if( array[i][j] == 'x'):
                    car = (i,j)
                    break

        return (abs(car[0] - space[0]) + abs(car[1] - space[1]))

    def getDepth(self, board, root, i):
        ''' This function returns the depth of the board. '''

        depth = 0
        current  = board

        while i >= 0:
           
            if(root[i][0] == current):
                depth = depth + 1
                current = root[i][1]
            i = i - 1
         
        return depth
       

if __name__ == "__main__":

    DEFAULT_BOARD = "  o aa|  o   |xxo   |ppp  q|     q|     q"

    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        board = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_BOARD
        next_boards = set()
        current_states = set()

        b = Board()
        p = Path()

        try:
            if cmd == "print":
                b.printBoard(board)
            elif cmd == "next":
                array = b.next(board)
                for string in array:
                    b.printBoard(string)
            elif cmd == "done":
                x = b.done(board)
                print(x)
            elif cmd == "random":  
                p.random(board)
            elif cmd == "bfs":  
                p.bfs(board)
            elif cmd == "astar":  
                p.astar(board)

        except Exception:
            print("Error Occurred")


'''
Test Commands

print a board:
bash run.sh print "  ooo |ppp q |xx  qa|rrr qa|b c dd|b c ee"

check if a board is in the done state:
bash run.sh done "  oaa |  o   |  o xx|  pppq|     q|     q"

get the next possible board states of a board:
bash run.sh next "  ooo |ppp q |xx  qa|rrr qa|b c dd|b c ee"

solve the board using random walk algorithm with N=10:
bash run.sh random "  oaa |  o   |  o xx|  pppq|     q|     q"

bash run.sh random "  oaa |  o   |  oxx |  pppq|     q|     q"

solve the board using breadth first search algorithm:
bash run.sh bfs "  ooo |ppp q |xx  qa|rrr qa|b c dd|b c ee"

bash run.sh bfs "  oaa |  o   |  o xx|  pppq|     q|     q"

solve the board using A* algorithm:
bash run.sh astar "  ooo |ppp q |xx  qa|rrr qa|b c dd|b c ee"

bash run.sh astar "  oaa |  o   |  o xx|  pppq|     q|     q"

'''
