
from math import log, sqrt

class Node:
    def __init__(self, board, parent, color, action):
        self.parent = parent # 父节点
        self.children = [] # 子节点列表
        self.visit_times = 0 # 访问次数
        self.board = board # 游戏选择这个Node的时的棋盘
        self.color = color # 当前玩家
        self.prevAction = action # 到达这个节点的action
        self.actions = list(board.get_legal_actions(self.color)) # 所有的legal actions
        self.unvisitActions = list(board.get_legal_actions(self.color)) # 未访问过的actions

        def gameover():
            l1 = list(board.get_legal_actions('X'))
            l2 = list(board.get_legal_actions('O'))
            return len(l1)==0 and len(l2)==0
        self.isover = gameover # 是否结束了

        self.reward = {'X': 0, 'O': 0}
        self.bestVal = {'X': 0, 'O': 0}
    
    def get_board(self):
        return self.board

    def get_parent(self):
        return self.parent

    def add_child(self, sub_node):
        sub_node.set_parent(self)
        self.children.append(sub_node)

    def get_children(self):
        return self.children

    def set_visit_times(self, times):
        self.visit_times = times

    def get_visit_times(self):
        return self.visit_times

    def visit_times_add_one(self):
        self.visit_times += 1

    def calcBestVal(self, balance, color):
        self.bestVal[color] = self.reward[color] / self.visit_times + \
            balance * sqrt(2 * log(self.parent.visit_times) / self.visit_times)