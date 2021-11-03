import re


class Node:

    def __init__(self, value=''):
        self.value = value  # пометка
        self.sons = []  # массив из Node`ов (дети данной вершины)


class Tree:

    def __init__(self):
        self.root = Node()  # Корень дерева

    def add(self, word):
        temp_node = self.root
        for symb in word:
            node = Node(symb)
            index = self.find(symb, temp_node)
            if index is not None:
                temp_node = temp_node.sons[index]
            else:
                temp_node.sons.append(node)
                temp_node = temp_node.sons[len(temp_node.sons)-1]

    def find(self, symb, node: Node):
        for i in range(0, len(node.sons)):
            if node.sons[i].value == symb:
                return i
        return None

    def wordsearch(self, word):
        node = self.root
        mistake_counter = 0
        for symb in word:
            index = self.find(symb, node)
            if index is not None:
                node = node.sons[index]
            else:
                mistake_counter += 1
                sons = node.sons


if __name__ == "__main__":

    pref_tree = Tree()
    Number = int(input())
    counter = 0
    while True:
        input_word = input()
        if input_word != '':
            input_word = input_word.lower()
            pref_tree.add(input_word)
            counter += 1
            print(counter)
            if counter == Number:
                break
    pref_tree.wordsearch('kek')
    pass

    # while True:
    #     try:
    #         input_word = input()
    #         pass
    #     except EOFError:
    #         break
    #
    # pass
