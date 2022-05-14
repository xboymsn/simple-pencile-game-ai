import random
from copy import deepcopy


class Node:


    def __init__(self, childs = [], game = None, depth = 0):
        self.childs = childs
        self.game = game
        self.depth = depth


    def AddChilds(self,child,i):#child : /Node(game)  game : nodeparent.game.child
        self.childs.append(child)
        child.game = self.game.childs[i]
        child.depth = self.depth+1
        self.Set_Color()


    def SetChilds(self):
        n = len(self.game.points)
        child_number = int(((n * (n - 1)) / 2) - self.depth)
        for i in range(child_number):
            self.AddChilds(Node([]),i)

    def Set_Color(self):
        if not IsMAxNode(self): color = "red"
        else: color = "blue"
        for point in self.game.points:
            for neighbor in point.neighbors:
                neighbor.color = color



class Point :


    def __init__(self,name):
        # self.coordinate = None
        self.neighbors = []
        self.name = name#not nessecery
        self.value = 0
        # self.coordinate = None
        #وقتی همسایه ای وجود دارد یعنی بین دو نقطه خط کشیده شده است


    # def AddNeighbors(self,point):
    #     self.neighbors.append(point)
    #     point.neighbors.append(self)
    #     self.value = len(self.neighbors)
    #     point.value = len(point.neighbors)

    def AddNeighbors(self,point):
        # if IsMAxNode(): color = "red"
        # else: color = "blue"
        self.neighbors.append(Neighbors(self,point,""))

    # def AddNeighbors_Red(self,point):
    #     n = Neighbors(self,point,"red")
    #
    #
    # def AddNeighbors_Blue(self,point):
    #     self.neighbors.append(point)
    #     point.neighbors.append(self)
    #     self.value = len(self.neighbors)
    #     point.value = len(point.neighbors)
    #     color = "blue"




    def Show(self):
        #Display
        pass


    def ConnectNeighbors(self,point):
        # Line(board,self,point)
        pass


class Neighbors:

    def __init__(self,point_a, point_b,color):
        self.p1 = point_a
        self.p2 = point_b
        self.color = color
        self.AddNeighbors(point_a,point_b)
        self.name = f"{point_a.name}{point_b.name}"


    def AddNeighbors(self,p1,p2):
        # p1.neighbors.append(p2)
        # p2.neighbors.append(p1)
        p1.neighbors.append(self)
        p2.neighbors.append(self)
        p1.value = len(p1.neighbors)
        p2.value = len(p2.neighbors)

    # def show_name(self):
    #     print(f"{self.p1.name}{self.p2.name}")


class Game:


    def __init__(self, points = []):
        lines = ("color","dot 1","dot2")
        self.points = points
        self.childs = []
        self.value = 0
        self.name = ""
        # self.lines = []
        # value $$$$$$$$$$$$$$$$$$$
        # self.lines = lines
        #list of dots
        #color that came from alphaBeta function

    # def SetChilds(self):
    #     n = len(self.points)
    #     child_number = int((n * (n - 1)) / 2)
    #     for i in range(child_number):
    #         self.childs.append(self.childs2())
    #
    #
    # def Childs1(self):
    #     p = self.points.copy()
    #     n = len(p)
    #     game = Game()
    #     for i in range(n):
    #         for j in range(i + 1, n):# لیست این تو باید ریست بشه هر بار
    #             points = p.copy()
    #             if not (self.Connected(points[i], points[j])):
    #                 points[i].AddNeighbors(points[j])
    #                 # print(f"i:{points[i].name}  j:{points[j].name}")
    #                 game.points = points
    #                 return game  # فقط یک گیم تولید کرده و برمیگردونه
    #
    #
    # def Childs2(self):
    #     p = deepcopy(self.points)
    #     n = len(p)
    #     for i in range(n):
    #         for j in range(i+1,n):#self.Connected?!
    #             if not (Connected(p[i],p[j])):
    #                 p[i].AddNeighbors(p[j])
    #                 game = Game()
    #                 game.points = p
    #                 return game

    def Set_Name(self):
        for point in self.points:
            self.name.join(point.name)

    def Childs(self):
        game_list = []
        p = deepcopy(self.points)
        h = deepcopy(p)
        n = len(p)#مشکل ازینه
        for i in range(n):
            for j in range(i + 1, n):  # self.Connected?!
                if not (Connected(h[i], h[j])):
                    p[i].AddNeighbors(p[j])
                    h[i].AddNeighbors(h[j])
                    game = Game()
                    game.points = p
                    game.Value()
                    game_list.append(game)
                    p = deepcopy(self.points)
        self.childs = game_list# فرزندان حالت فعلی را ست میکند
        pass



    def Connected(self,a,b):
        #چک میکنیم که آیا بین a b خطی وجود دارد یا نه
        n = Neighbors(a,b,"")#رنگش باید درست بشه
        return a.neighbors.__contains__(n)
        # print(a.neighbors.__contains__(Neighbors(a, b, "blue")))
        # return a.neighbors.__contains__(b)


    def Lose(self,a,b,c):
        if self.Connected(a,b) and self.Connected(b,c) and self.Connected(a,c):
            return True#fail = -10

    def Value(self):
        for point in self.points:
            self.value += point.value


    # def Lose2(self,point):
    #     neighbors = point.neighbors
    #     for i in range(len(neighbors)):
    #         if i>len(neighbors):break
    #         if self.Connected(neighbors[i],neighbors[i+1]):
    #             print("sombody losed")


    def AddPoint(self,point):
        self.points.append(point)

    def Display(self,board):
        list = self.MatchCase(len(self.points))
        i=0
        for point in self.points:
            board[list[i][0]][list[i][1]] = f"{point.name}"
            i+=1
        Display(board)


    def MatchCase(self,n):
        match n:
            case 4: return [(0,0),(0,9),(9,0),(9,9)]
            case 5: return [(0,4),(4,0),(4,8),(8,0),(8,8)]
            case 6: return [(0,4),(3,1),(3,7),(5,1),(5,7),(8,4)]

    #state


def Connected(a,b):
    #چک میکنیم که آیا بین a b خطی وجود دارد یا نه
    # return a.neighbors.__contains__(b)
    n = Neighbors(a, b, "")  # رنگش باید درست بشه
    return a.neighbors.__contains__(n)


def AlphaBeta(node, depth, IsMaxNode, alpha, beta):
    if (depth == 0):# or final:
        return None #huristic value of the node
    for child in node:
        if IsMaxNode:
            alpha = max(alpha, AlphaBeta(child, depth-1, not (IsMaxNode), alpha, beta))
        else:
            beta = min(alpha, AlphaBeta(child, depth - 1, not (IsMaxNode), alpha, beta))
        if beta <= alpha : break
        if IsMaxNode : return alpha
        else :  return beta

def IsMAxNode(node):
    if node.depth%2 == 0: return True
    else: return False

def Board(n):
    board = [["." for i in range(n)] for i in range(n)]
    return board


def Display(board):
    for item in board:
        print(*item)


# def Calculate(min_x,max_x,min_y,max_y):
#     i_list = []
#     j_list = []
#     for i in range(min_y, max_y + 1):
#         i_list.append(i)
#     for j in range((-1 * (max_x)), (-1 * (min_x)) + 1):
#         j_list.append(abs(j))
#     for m in range(len(i_list)):
#         board[j_list[m]][i_list[m]] = "O"


def play():
    game = Game()
    #while True:
        #if game.lose:
            #break
        #cp.select/alphaBeta
        #player.select
    pass


# def Line(board, dot1, dot2):
#     max_x = max(dot1[0],dot2[0])
#     min_x = min(dot1[0],dot2[0])
#     max_y = max(dot1[1],dot2[1])
#     min_y = min(dot1[1],dot2[1])
#     n = len(board)
#     if dot1[0]==dot2[0]:
#         for i in range(min_y,max_y+1):
#             board[dot1[0]][i] = "O"# دلار بزار برای کابر و هشتگ برای کامپیوتر
#     elif dot1[1]==dot2[1]:
#         for i in range(min_x,max_x+1):
#             board[i][dot1[1]] = "O"
#     else:
#         Calculate(min_x, max_x, min_y, max_y)
#         pass

def child_in_childs(game,node,depth):
    if depth == 0 : return
    game.Childs()
    node.SetChilds()
    depth-=1
    for i in range(len(game.childs)):
        print(f"node.depth:{node.depth}")
        print(len(game.childs))
        child_in_childs(game.childs[i],node.childs[i],depth)


if __name__ == '__main__':
    game = Game()
    name_list = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "u","v","t", "w", "x", "y", "z"]
    for i in range(4):
        game.AddPoint(Point(name_list[i]))
    node = Node()
    game.Childs()
    node.game = game
    child_in_childs(game,node,2)

    # a = Point("a")
    # b = Point("b")
    # c = Point("c")
    # n =Neighbors(a,b,0)
    # m =Neighbors(a,c,1)
    # print(a.neighbors[0].name)
    # print(a.neighbors.__contains__(m))


    input()
