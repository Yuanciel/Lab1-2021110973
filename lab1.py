import random
import re
import networkx as nx
import matplotlib.pyplot as plt
import heapq
from graphviz import Digraph
import pydot
directed_graph = nx.MultiDiGraph()
lastone = None
random = random.Random()

import re
import networkx as nx

directed_graph = nx.DiGraph()
last_one = None  # Change variable name to follow PEP8 naming conventions

def showDirectedGraph(filename):
    global last_one
    try:
        with open(filename, 'r') as file:
            for line in file:
                words = re.findall(r'\b[A-Za-z]\w*\b', line)
                # 将所有单词转换为小写
                words = [word.lower() for word in words]
                for word in words:
                    add_node_if_not_exists(word)
                    if last_one:        
                        add_edge_with_weight(last_one, word)
                    last_one = word
    except FileNotFoundError:
        print("File not found!")

def add_node_if_not_exists(node_id):
    if not directed_graph.has_node(node_id):
        directed_graph.add_node(node_id)

def add_edge_with_weight(from_node, to_node):
    if directed_graph.has_node(from_node) and directed_graph.has_node(to_node):
        if directed_graph.has_edge(from_node, to_node):
            # Increment edge weight by 1 if the edge already exists
            directed_graph[from_node][to_node]['weight'] += 1
            #print(directed_graph[from_node][to_node]['weight'])  #打印边权值的 测试用的

        else:
            # Add edge with weight 1 if it doesn't exist
            directed_graph.add_edge(from_node, to_node, weight=1)


def randomWalk():
    if not directed_graph:
        return "Graph is empty."

    visited_nodes = []  #存已经访问的节点和边
    visited_edges = []
    current_node = random.choice(list(directed_graph.nodes))

    while True:
        visited_nodes.append(current_node)
        neighbors = list(directed_graph.neighbors(current_node))
        if not neighbors:
            break

        next_node = random.choice(neighbors)
        visited_edges.append((current_node, next_node))

        if next_node in visited_nodes:
            break

        current_node = next_node

    result = "Visited Nodes:\n"
    for node in visited_nodes:
        result += f"- {node}\n"

    with open("random_walk_output.txt", "w") as file:
        file.write(result)

    return result

def queryBridgeWords(word1, word2, flag=True): # False表示只返回桥接词不输出提示语句
    word3 = []
    # 判断word1和word2是否在图中
    if flag:
        if not directed_graph.has_node(word1) and not directed_graph.has_node(word2):
            print(f"No \"{word1}\" and \"{word2}\" in the graph!")
        elif not directed_graph.has_node(word1):
            print(f"No \"{word1}\" in the graph!")
        elif not directed_graph.has_node(word2):
            print(f"No \"{word2}\" in the graph!")
    if not directed_graph.has_node(word1) or not directed_graph.has_node(word2):
        return word3
    # 用word3记录word1和word2的桥接词
    # 遍历word1的邻居，再遍历word1的邻居的邻居，判断是否有word2的邻居
    for neighbor in directed_graph.neighbors(word1):
        for neighbor2 in directed_graph.neighbors(neighbor):
            if neighbor2 == word2:
                word3.append(neighbor)
    if flag:
        if not word3:
            print(f"No bridge words from \"{word1}\" to \"{word2}\"!")
        else:
            print(f"The bridge words from \"{word1}\" to \"{word2}\" are: {', '.join(word3)}")
    return word3

def generateNewText(input_text):
    new_text = []
    words = input_text.lower().split()
    # print(words)
    for i in range(len(words) - 1):
        word1 = words[i]
        word2 = words[i + 1]
        new_text.append(word1)
        if directed_graph.has_node(word1) and directed_graph.has_node(word2):
            bridge_word = queryBridgeWords(word1, word2, False) #查询是否有桥接词
            if bridge_word: 
                random_num = random.randint(0, len(bridge_word)-1)
                new_text.append(bridge_word[random_num])
    new_text.append(words[-1])
    return ' '.join(new_text)

def calcShortestPath(word1, word2):
    if not directed_graph.has_node(word1) or not directed_graph.has_node(word2):
        return "Word1 or Word2 not in the graph!"

    distances = {node: float('inf') for node in directed_graph}
    distances[word1] = 0
    previous_nodes = {}
    min_heap = [(0, word1)]

    while min_heap:
        current_distance, current_node = heapq.heappop(min_heap)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in directed_graph[current_node].items():
            distance = current_distance + weight['weight']

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(min_heap, (distance, neighbor))

    path = []
    current = word2
    while current in previous_nodes:
        path.insert(0, current)
        current = previous_nodes[current]
    path.insert(0, word1)

    return f"Shortest path: {' -> '.join(path)}, Length: {distances[word2]}"


def visualize_graph():
    PG = nx.nx_pydot.to_pydot(directed_graph)
    # 将原图中的边权值加入PG中，PG是Graphviz的图对象
    for edge in PG.get_edges():
        edge_label = str(directed_graph[edge.get_source()][edge.get_destination()]['weight'])
        edge.set_label(edge_label)
    PG.write_png('graph.png')


if __name__ == "__main__":
    filename = input("Enter the input file name: ")
    showDirectedGraph(filename)

    while True:
        print("\nChoose an option:")
        print("1. Show Directed Graph")
        print("2. Query Bridge Words")
        print("3. Generate New Text")
        print("4. Calculate Shortest Path")
        print("5. Random Walk")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            visualize_graph()
            #for edge in directed_graph.edges(data=True):
                #print(edge)

        elif choice == "2":
            word1 = input("Enter word1: ")
            word2 = input("Enter word2: ")
            queryBridgeWords(word1, word2)
        elif choice == "3":
            input_text = input("Enter new text: ")
            new_text = generateNewText(input_text)
            print("New Text:", new_text)
        elif choice == "4":
            word1 = input("Enter word1: ")
            word2 = input("Enter word2: ")
            result = calcShortestPath(word1, word2)
            print(result)
        elif choice == "5":
            randomWalk()
            print("Random walk completed! Check 'random_walk_output.txt' for the result.")
        elif choice == "6":
            print("Exiting program.")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 6.")
