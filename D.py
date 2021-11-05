import sys

class Node:

    def __init__(self, value=''):
        self.value = value  # пометка
        self.sons = []  # массив из Node`ов (дети данной вершины)
        self.word = ''


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
        temp_node.word = word

    def find(self, symb, node: Node):
        for i in range(0, len(node.sons)):
            if node.sons[i].value == symb:
                return i
        return None

    def search(self, word, maxcost=1):
        word_old = word
        word = word.lower()
        currentrow = range(len(word) + 1)
        results = []
        for son in self.root.sons:
            self.searchRecursive(son, word, currentrow, results, maxcost)

        length = len(results)

        if length == 0:
            print(word_old, '-?')
        elif length == 1:
            if results[0][1] == 0:
                print(word_old, '- ok')
            else:
                print(word_old, '->', results[0][0])
        else:
            if (word, 0) in results:
                print(word_old, '- ok')
                return
            sys.stdout.write(word_old + ' -> ')
            results.sort()
            for i in range(0, length):
                sys.stdout.write(results[i][0])
                if i != length-1:
                    sys.stdout.write(', ')
                else:
                    sys.stdout.write('\n')

    def searchRecursive(self, node: Node, word, previousrow, results, maxcost, prev_letter=None, prevprev_row=None):

        columns = len(word) + 1
        currentrow = [previousrow[0] + 1]

        for column in range(1, columns):
            insertcost = currentrow[column - 1] + 1
            deletecost = previousrow[column] + 1

            if word[column - 1] != node.value:
                replacecost = previousrow[column - 1] + 1
            else:
                replacecost = previousrow[column - 1]

            if (column > 1) and (prev_letter is not None):
                if (word[column-1] == prev_letter) and (word[column-2] == node.value):
                    swapcost = min(prevprev_row[column - 2] + 1, previousrow[column - 1])
                    currentrow.append(min(insertcost, deletecost, replacecost, swapcost))

                else:
                    currentrow.append(min(insertcost, deletecost, replacecost))
            else:
                currentrow.append(min(insertcost, deletecost, replacecost))

        if currentrow[-1] <= maxcost and node.word != '':
            results.append((node.word, currentrow[-1]))

        if min(currentrow) <= maxcost:
            for son in node.sons:
                self.searchRecursive(son, word, currentrow, results, maxcost, node.value, previousrow)


if __name__ == "__main__":

    pref_tree = Tree()
    Number = int(input())
    counter = 0
    while True:
        if Number == 0:
            break
        input_word = input()
        if input_word != '':
            input_word = input_word.lower()
            pref_tree.add(input_word)
            counter += 1
            if counter == Number:
                break
    while True:
        try:
            input_word = input()
            if input_word != '':
                pref_tree.search(input_word)
        except EOFError:
            break
    pass
