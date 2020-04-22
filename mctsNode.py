
from math import log, sqrt

class Node:
    def __init__(self, board, parent, color, action):
        self.parent = parent # 父节点
        self.children = [] # 子节点列表
        self.visit_times = 0 # 访问次数
        self.board = board # 游戏选择这个Node的时的棋盘
        self.color = color # 当前玩家
        self.prevAction = action # 到达这个节点的action
        self.unvisitActions = list(board.get_legal_actions(color)) # 未访问过的actions
        self.isover = self.gameover(board) # 是否结束了
        if (self.isover == False) and (len(self.unvisitActions) == 0): # 没得走了但游戏还没结束
            self.unvisitActions.append("noway")

        self.reward = {'X': 0, 'O': 0}
        self.bestVal = {'X': 0, 'O': 0}

    def gameover(self, board):
        l1 = list(board.get_legal_actions('X'))
        l2 = list(board.get_legal_actions('O'))
        return len(l1)==0 and len(l2)==0

    def calcBestVal(self, balance, color):
        if self.visit_times==0:
            print("-------------------------")
            print("oops!visit_times==0!")
            self.board.display()
            print("-------------------------")
        self.bestVal[color] = self.reward[color] / self.visit_times + balance * sqrt(2 * log(self.parent.visit_times) / self.visit_times)