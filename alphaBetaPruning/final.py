import random
from copy import deepcopy


class Node:#برای ساخت درخت


    def __init__(self, childs = [], game = None, depth = 0):
        self.childs = childs
        self.game = game
        self.depth = depth
        self.parent = None
        # self.select = False
        # self.neighbors = []



    def AddChilds(self,child,i):#اضافه کردن فرزند به گره
        child.parent = self
        self.childs.append(child)
        child.game = self.game.childs[i]
        # child.neighbors = self.game.childs[i].neighbors
        child.depth = self.depth+1


    def SetChilds(self):#تولید تمام فرزندان مجاور
        n = len(self.game.points)
        child_number = int(((n * (n - 1)) / 2) - self.depth)
        for i in range(child_number):
            self.AddChilds(Node([]),i)


    def Set_Color(self):
        if  IsMAxNode(self): color = "red"
        else: color = "blue"
        print(f"IsMaxNode:{IsMAxNode(self)} , Depth:{self.depth}")
        for point in self.game.points:
            for neighbor in point.neighbors:
                if neighbor.color == None:
                    neighbor.color = color


    def Display(self):
        for point in self.game.points:
            for neighbor in point.neighbors:
                print(f"{neighbor.name} , {neighbor.color}")



class Point :


    def __init__(self,name):
        self.neighbors = []
        self.name = name#not nessecery
        self.value = 0
        #وقتی همسایه ای وجود دارد یعنی بین دو نقطه خط کشیده شده است


    def AddNeighbors(self,point):#اضافه شدن همسایه بین دو نقطه به معنی کشیده شدن خط بین آن دو می باشد
        self.neighbors.append(Neighbors(self,point))



class Neighbors:#همسایه ها یا همان خط های کشیده شده ی میان نقاط

    def __init__(self,point_a, point_b):
        self.p1 = point_a
        self.p2 = point_b
        self.color = None
        self.name = f"{point_a.name}{point_b.name}"
        self.AddNeighbors(point_a,point_b)


    def AddNeighbors(self,p1,p2):#ساخت رابظه و کشیدن خط میان دو نقطه
        p1.neighbors.append(self)
        p2.neighbors.append(self)
        p1.value = len(p1.neighbors)
        p2.value = len(p2.neighbors)


class Game:


    def __init__(self, points = []):
        self.points = points
        self.childs = []
        self.value = 0
        self.name = ""
        # self.neighbors = []


    def Value(self):# تابع محاسبه ی هزینه بر اساس تعداد خطوط کشیده شده از هر رنگ بر روی هر نقطه ی بازی
        value = 0
        for point in self.points:
            count_red = 0
            count_blue = 0
            for neighbor in point.neighbors:
                if neighbor.color=='red':
                    count_red+=1
                else:
                    count_blue+=1
            if count_red==1:
                value+=1
            elif count_red>1:
                value+=6
            if count_blue == 1:
                value -= 1
            elif count_blue > 1:
                value -= 4
        self.value = value
        # self.value = 0


    # def Set_Name(self):
    #     for point in self.points:
    #         self.name.join(point.name)

    def Childs(self):#حالت های فرزند و مجاور حالت جاری گیم را تولید می کند
        game_list = []
        p = deepcopy(self.points)
        h = deepcopy(p)
        n = len(p)
        for i in range(n):
            for j in range(i + 1, n):
                if not (Connected(h[i], h[j])):
                    p[i].AddNeighbors(p[j])
                    Delet_Duplicate(p[i])
                    # h[i].AddNeighbors(h[j])
                    game = Game()
                    game.points = p
                    for point in game.points:
                        for neighbor in point.neighbors:
                            if  not(game.name.__contains__(neighbor.name)):
                                game.name += neighbor.name
                    game.Set_Color()
                    game.Value()
                    # for neighbor in p[i].neighbors:
                    #     if not (game.neighbors.__contains__(neighbor)):
                    #         game.neighbors.append(neighbor)
                    game_list.append(game)
                    p = deepcopy(self.points)
        self.childs = game_list# فرزندان حالت فعلی را ست میکند


    def Set_Color(self):#بر اساس عمق مشخص میکند رنگ خطی که در این لحظه تولید میکند آبی ای قرمز است
        n_points = len(self.points)
        n_childs = 0
        for point in self.points:
            n_childs+=len(point.neighbors)
        depth = int(((n_points*(n_points-1))/2)-(n_childs)/2)
        if  IsMAxNode(depth): color = "red"
        else: color = "blue"
        for point in self.points:
            for neighbor in point.neighbors:
                if neighbor.color == None:
                    neighbor.color = color


    def Lose(self,a,b,c):#مثلث ها را پیدا میکند
        ab = Connected_for_Lose(a,b)
        bc = Connected_for_Lose(b,c)
        ac = Connected_for_Lose(a,c)
        l = []
        if ab!=None and bc!=None and ac!=None:
            color = ab.color
            if bc.color == color and ac.color == color:
                l.append(ab)
                l.append(bc)
                l.append(ac)
                return l


    def Check_Failure(self):#تابع آزمون حالت پایانی
        n=len(self.points)
        for i in range(n):
            for j in range(i + 1, n):
                for z in range(j + 1, n):
                    l = self.Lose(self.points[i], self.points[j], self.points[z])
                    if l!=None:
                        if l[0].color == 'red':
                            self.value = -100000
                        elif l[0].color == 'blue':
                            self.value = 100000



    def AddPoint(self,point):#اضافه کردن نقاط به حالات بازی
        self.points.append(point)



def Delet_Duplicate(point):#زمانی که خطوط را به نقاط اضافه میکنیم به دلیل اینکه به هر دو نقطه اضافه میشوند دو جفت از هر خط به وجود می آید که در این تابع یک جفت از آن ها حذف می شود
    i=0
    while i<len(point.neighbors):
        if point.neighbors.count(point.neighbors[i])>1:point.neighbors.pop(i)
        i+=1


def Connected(a,b):#چک کردن اتصال میان نقاط
    #چک میکنیم که آیا بین a b خطی وجود دارد یا نه
    for neighbor in a.neighbors:
        if (neighbor.p1==a and neighbor.p2==b) or (neighbor.p1==b and neighbor.p2==a): return True
    return False

def Connected_for_Lose(a,b):#چک کردن اتصال میان نقاط و بر گرداندن خط مورد نظر در صورت وجود
    #چک میکنیم که آیا بین a b خطی وجود دارد یا نه
    for neighbor in a.neighbors:
        if (neighbor.p1==a and neighbor.p2==b) or (neighbor.p1==b and neighbor.p2==a): return neighbor


def Select(n,depth):#انتخاب پرنت نود داده شده در عمق ورودی
    i = depth
    x = i-2
    while(i>x):
        n = n.parent
        i-=1
    return n






def AlphaBeta(node, depth, alpha, beta, IsMaxNode):#به وجود اوردن درخت مین مکس و هرس الفا بتا در درخت مورد نظر
    if (depth == 4) or abs(node.game.value)==100000:
        global n
        n=node
        # node.select==True
        return node.game.value
    if IsMaxNode:
        bestVal= -99999999
        for child in node.childs:
            value = AlphaBeta(child, depth + 1, alpha, beta, False)
            bestVal = max(bestVal, value)
            alpha = max(alpha, bestVal)
            if beta <= alpha:
                break
        return bestVal

    else:
        bestVal = +99999999
        for child in node.childs:
            value = AlphaBeta(child, depth + 1, alpha, beta,True)
            bestVal = min(bestVal, value)
            beta = min(beta, bestVal)
            if beta <= alpha:
                break
        return bestVal


# def IsMAxNode(node):
#     if node.depth%2 == 0: return True
#     else: return False


def IsMAxNode(depth):#چک کردن اینکه گره مکس است یا مین
    if depth%2 == 0: return True
    else: return False


def child_in_childs(game,node,depth):#برای تولید زنجیره ای فرزندان نوشته شده است
    if depth == 0 : return
    game.Childs()
    node.SetChilds()
    depth-=1
    for i in range(len(game.childs)):
        child_in_childs(game.childs[i],node.childs[i],depth)


def Play(node):# تابع شروع و ادامه ی بازی (دیباگ نشده)
    AlphaBeta(node, 1, -99999999, +99999999, True)
    node = Select(n,2)
    node.game.Check_Failure()
    print(node.game.name)
    i=int(input())
    j=int(input())
    node.game.points[i].AddNeighbors(node.game.points[j])
    node.game.Check_Failure()
    if not (node.game.value==100000):
        Play(node)
    else: return "finish"


if __name__ == '__main__':
    game = Game()
    name_list = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "u","v","t", "w", "x", "y", "z"]
    for i in range(6):
        game.AddPoint(Point(name_list[i]))
    node = Node()
    node.game = game
    child_in_childs(game,node,4)
    AlphaBeta(node, 1, -99999999, +99999999, True)
    x=(Select(n,2))
    print(f"alpha_beta Chosen Node:{n.game.name}")#گره ای که الفا بتا انتخاب میکند
    print(f"parent of chosen node selected by Select():{x.game.name}")#پدر n ام گره بالا که قرار است کامپیوتر انتخاب و بازی کند
    # Play(node)






    input()
    '''
    هوش مصنوعی این پروژه به شکل کامل طراحی شده اما رابط کاربری مناسب آن هنوز کامل نشده
    '''
