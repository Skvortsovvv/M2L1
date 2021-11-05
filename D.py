import sys

class Node:

    def __init__(self, value=''):
        self.value = value  # буква
        self.sons = {}  # словарь из Node`ов (дети данной вершины)
        self.word = ''


class Tree:

    def __init__(self):
        self.root = Node()  # Корень дерева

    def add(self, word):
        """
        Сложность по времени:
        Сложность O(n) n - длина добавляемого слова, т.к. нужно проверить каждый символ
        вставляемого слова на предмет того, есть ли данная буква в дереве и, если нет, создаем
        для нее отдельный узел в дереве

        Сложность по памяти:
        Сложность по памяти O(n), где n - длина добавляемого слова, т.к. в худшем случае
        нужно создать n узлов в дереве
        """
        temp_node = self.root
        for symb in word:
            if symb not in temp_node.sons:
                temp_node.sons[symb] = Node(symb)
            temp_node = temp_node.sons[symb]

        temp_node.word = word

    def search(self, word, maxcost=1):
        """
        Сложность по времени:
        Сложность O(m*n) m - максимальная длина слова из словаря, включая проверяемое слово,
        n - число узлов в дереве. При проверке слова, для каждой буквы из дерева создается
        по крайней мере одна строка в матрице. В каждой строке находится m+1 символ, т.к.
        в алгоритме нумерация с единицы.

        Здесь мы берем длину максимального слова потому, что, если проверяемое слово окажется
        короче слова из словаря, то число побуквенных проверок не будет соответсовать тому числу, если бы
        мы взяли и перемножили <длина проверяемого слова> * <число узлов в дереве>.
        Как показано в примере ниже, при проверке слова cat, происходит 18 проверок (со словом cult буква 'c'
        не проверяется, так как она была проверена на прошлом слове). И тогда получается, если применять ранее
        упомянутую формулу (длина <word> * число узлов), то получим 3 * 5 = 15, но это не так. Поэтому верхняя
        оценка будет строиться из произведения слова максимальной длины среди всех словаря, включая проверяеммое слово,
        и числа узлов в дереве. В данном случае она равна: len(cult) * 5 = 4 * 5 = 20, что удовлетворяет услвоию.

        #|c|a|t|                              #|c|a|t|
        c|0|1|2|  c->c    c->ca   c->cat      c|0|1|2|
        u|1|1|2|  cu->c   cu->ca  cu->cat     u|1|1|2|    cu->c   cu->ca   cu->cat
        t|2|2|1|  cut->c  cut->ca cut->cat    l|2|2|2|    cul->c   cul->ca    cul->cat
                                              t|3|3|2|    cult->c   cat->ca    cut->cat

        Сложность по памяти:
        Рекурсивно вызывается searchRecursive, следовательно, заполняется стек вызовов - O(n), где n - число узлов
        (в худшем случае мы будем проходить все узлы). Для проверки каждого узла требуется 3 строки матрицы
        (предпредыдущая, предыдущая и текущая) в процессе выполнения функции создается и заполняется
        очередная строка. Ее  длина m+1 (т.к в алгоритме нумерация с единицы), m - длина проверяемого слова.
        Это O(m) по памяти для каждого вызова функции.
        Таким образом, сложность по памяти O(n*m)
        """

        currentrow = range(len(word) + 1)
        results = []
        for symb in self.root.sons:
            self.searchRecursive(self.root.sons[symb], word.lower(), currentrow, results, maxcost)
        return results

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
            for symb in node.sons:
                self.searchRecursive(node.sons[symb], word, currentrow, results, maxcost, node.value, previousrow)


def print_results(results, word):
    word_old = word
    word = word.lower()
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
            if i != length - 1:
                sys.stdout.write(', ')
            else:
                sys.stdout.write('\n')


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
                print_results(pref_tree.search(input_word), input_word)
        except EOFError:
            break
    pass
