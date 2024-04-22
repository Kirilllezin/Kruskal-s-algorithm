from prettytable import PrettyTable
import networkx as nx
import matplotlib.pyplot as plt


class Graph:

    # Создание графа
    def __init__(self, vertices):
        self.V = vertices  # Количество вершин
        self.graph = []  # Список рёбер графа

    # Функция для добавления нового ребра в граф
    def addEdge(self, u, v, w):
        self.graph.append([u, v, w])

    # Функция для поиска множества элемента i
    def find(self, parent, i):
        if parent[i] != i:
            # Присваивание родительского узла узлу i
            # как корневого узла, так как
            # требуется сжатие пути
            parent[i] = self.find(parent, parent[i])
        return parent[i]

    # Функция для объединения двух множеств x и y
    # (применяется объединение по рангу)
    def union(self, parent, rank, x, y):
        # Присоединяем меньшее дерево к корню
        # более высокого дерева (Объединение по рангу)
        if rank[x] < rank[y]:
            parent[x] = y
        elif rank[x] > rank[y]:
            parent[y] = x

        # Если ранги равны, то делаем одно из них корневым
        # и увеличиваем его ранг на один
        else:
            parent[y] = x
            rank[x] += 1

    # Основная функция для построения МОД
    # с использованием алгоритма Краскала
    def KruskalMST(self):

        # Здесь будет храниться результативное МОД
        result = []

        # Индексная переменная для отсортированных рёбер
        i = 0

        # Индексная переменная для result[]
        e = 0

        # Сортируем все рёбра по весу в
        # неубывающем порядке
        self.graph = sorted(self.graph, key=lambda item: item[2])

        parent = []
        rank = []

        # Создаём V подмножеств с одним элементом
        for node in range(self.V):
            parent.append(node)
            rank.append(0)

        # Количество рёбер должно быть на одно меньше чем V
        while e < self.V - 1:

            # Берём самое маленькое ребро и увеличиваем
            # индекс для следующей итерации
            u, v, w = self.graph[i]
            i = i + 1
            x = self.find(parent, u)
            y = self.find(parent, v)

            # Если это ребро не создает цикл, то
            # включаем его в результат и увеличиваем
            # индекс result для следующего ребра
            if x != y:
                e = e + 1
                result.append([u, v, w])
                self.union(parent, rank, x, y)
            # Иначе отбрасываем ребро

        # Сложение веса всех рёбер в новом оставном графе
        minimumCost = 0
        table = PrettyTable()
        table.field_names = ("Вершина 1", "Вершина 2", "Вес ребра")
        for u, v, weight in result:
            minimumCost += weight
            table.add_row([u, v, weight])
        print("Вершины минимального оставного дерева", "\n", table)
        print("Минимальное остовное дерево:", minimumCost)

        # Визуализация исходного графа
        G_original = nx.Graph()
        for u, v, weight in self.graph:
            G_original.add_edge(u, v, weight=weight)

        pos_original = nx.spring_layout(G_original)  # позиции вершин

        # рисуем вершины
        nx.draw_networkx_nodes(G_original, pos_original, node_size=700, node_color='b')

        # рисуем рёбра
        nx.draw_networkx_edges(G_original, pos_original, width=2, edge_color='b')

        # подписываем вершины
        labels_original = nx.get_edge_attributes(G_original, 'weight')
        nx.draw_networkx_labels(G_original, pos_original)
        nx.draw_networkx_edge_labels(G_original, pos_original, edge_labels=labels_original)

        plt.title("Исходный граф")
        plt.axis('off')  # отключаем оси
        plt.show()

        # Визуализация минимального остовного дерева
        G_mst = nx.Graph()
        for u, v, weight in result:
            G_mst.add_edge(u, v, weight=weight)

        pos_mst = nx.spring_layout(G_mst)  # позиции вершин

        # рисуем вершины
        nx.draw_networkx_nodes(G_mst, pos_mst, node_size=700, node_color='g')

        # рисуем рёбра
        nx.draw_networkx_edges(G_mst, pos_mst, width=2, edge_color='g')

        # подписываем вершины
        labels_mst = nx.get_edge_attributes(G_mst, 'weight')
        nx.draw_networkx_labels(G_mst, pos_mst)
        nx.draw_networkx_edge_labels(G_mst, pos_mst, edge_labels=labels_mst)

        plt.title("Минимальное остовное дерево")
        plt.axis('off')  # отключаем оси
        plt.show()


# Задание графа
if __name__ == '__main__':
    g = Graph(7)
    g.addEdge(0, 1, 10)
    g.addEdge(0, 2, 6)
    g.addEdge(0, 3, 5)
    g.addEdge(1, 3, 15)
    g.addEdge(2, 3, 4)
    g.addEdge(5, 6, 19)
    g.addEdge(6, 0, 2)
    g.addEdge(5, 4, 1)

    g.addEdge(1, 2, 4)
    g.addEdge(3, 4, 6)
    g.addEdge(3, 5, 14)
    g.addEdge(3, 6, 27)

    # Вызов функции
    g.KruskalMST()
