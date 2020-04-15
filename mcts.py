from mctsNode import Node
from copy import deepcopy
from func_timeout import FunctionTimedOut, func_timeout
import random
import board
import sys
import math

class MonteCarlo:
    # uct方法的实现
    # return: action(string)
    def search(self, board, color): 
        # board: 当前棋局
        # color: 当前玩家

        # 特殊情况：只有一种选择
        actions=list(board.get_legal_actions(color))
        if len(actions) == 1:
            return list(actions)[0]

        # 创建根节点
        newboard = deepcopy(board)
        root = Node(newboard, None, color, None)

        # 考虑时间限制
        def whileFunc(node):
            while True:
                # mcts four steps
                # selection,expantion
                expand_node = self.tree_policy(node, color)
                # simulation
                reward = self.default_policy(expand_node)
                # Backpropagation
                self.backup(expand_node, reward)                
        
        try:
            # 测试程序规定每一步在60s以内
            func_timeout(59, whileFunc, args=[root]) 
        except FunctionTimedOut:
            pass

        return self.best_child(root, math.sqrt(2), color).prevAction

    

    def expand(self, node):
        """ 
        输入一个节点，在该节点上拓展一个新的节点，使用random方法执行Action，返回新增的节点 
        """

        action = random.choice(node.unvisitActions)
        node.unvisitActions.remove(action)

        # 执行action，得到新的board
        newBoard = deepcopy(node.board)
        newBoard._move(action, node.color)

        newColor = 'X' if node.color=='O' else 'O'
        newNode = Node(newBoard,node,newColor,action)
        node.children.append(newNode)

        return newNode
    
    def best_child(self, node, balance, color):
        # 对每个子节点调用一次计算bestValue
        for child in node.children:
            child.calcBestVal(balance, color)

        # 对子节点按照bestValue排序，降序
        sortedChildren = sorted(node.children, key=lambda x: x.bestVal[color], reverse = True)

        # 返回bestValue最大的元素
        return sortedChildren[0]

    def tree_policy(self, node, color):
        """
        传入当前需要开始搜索的节点（例如根节点）
        根据exploration/exploitation算法返回最好的需要expend的节点
        注意如果节点是叶子结点直接返回。

        基本策略是先找当前未选择过的子节点，如果有多个则随机选。
        如果都选择过就找权衡过exploration/exploitation的UCB值最大的，如果UCB值相等则随机选。
        """
        while not node.isover:
            if len(node.unvisitActions)>0:
                # 还有未展开的节点
                sub_node = expand(node)
                return sub_node
            else:
                if len(node.actions)==0:
                    newBoard = deepcopy(node.board)
                    newColor = 'X' if node.color=='O' else 'O'
                    newNode = Node(newBoard,node,newColor,None)
                    node.children.append(newNode)
                    return newNode
                # 选择ucb最大的
                node = self.best_child(node, math.sqrt(2), color)

        return node

    def default_policy(self, node):
        """
        蒙特卡罗树搜索的Simulation阶段
        输入一个需要expand的节点，随机操作后创建新的节点，返回新增节点的reward。
        注意输入的节点应该不是子节点，而且是有未执行的Action可以expend的。

        基本策略是随机选择Action。
        """
        newBoard = deepcopy(node.board)
        newColor = node.color
        while not node.isover:
            actions = list(newBoard.get_legal_actions(newColor))
            if len(actions)>0:
                action = random.choice(actions)
                newBoard._move(action, newColor)
            newColor = 'X' if node.color=='O' else 'O'
        
        # 0黑 1白 2平局
        winner, diff = newBoard.get_winner()
        diff /= 64
        return winner, diff

    def backup(self, node, reward):
        newNode = node
        # 节点不为None时
        while newNode is not None:
            newNode.visit_times += 1

            if reward[0] == 0:
                newNode.reward['X'] += reward[1]
                newNode.reward['O'] -= reward[1]
            elif reward[0] == 1:
                newNode.reward['X'] -= reward[1]
                newNode.reward['O'] += reward[1]
            elif reward[0] == 2:
                pass

            newNode = newNode.parent
        


