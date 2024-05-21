import random
import re
import networkx as nx
import matplotlib.pyplot as plt
import heapq
directed_graph = nx.DiGraph()
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
                for word in words:
                    add_node_if_not_exists(word)
                    if last_one and last_one != word:
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
            print(directed_graph[from_node][to_node]['weight'])  #打印边权值的 测试用的、

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

def visualize_graph():
    pos = nx.kamada_kawai_layout(directed_graph)
    nx.draw(directed_graph, pos, with_labels=True, node_size=800, node_color="skyblue", font_size=10, font_weight="bold",
            arrows=True, arrowsize=10, edge_color="gray", width=1.5, connectionstyle='arc3, rad=0.2')
    plt.show()


'''def queryBridgeWords(word1, word2):
    if not directed_graph.has_node(word1) or not directed_graph.has_node(word2):
        return "No word1 or word2 in the graph!"
    visited = set()
    bridges = []

    def dfs(node, target, path):
        if node == target:
            bridges.extend(path[:-1])  # 添加完整路径
            return True

        visited.add(node)
        for neighbor in directed_graph.neighbors(node):
            if neighbor not in visited and neighbor != word1:
                if dfs(neighbor, target, path + [neighbor]): #这里因为要判断是不是找到了word2所以把word2也加进去了，所以path不该输出最后一个元素
                    return True

    dfs(word1, word2, [])
    visited.clear()  # 清空访问记录，以便下一次查询

    if not bridges:
        return f"No bridge words from {word1} to {word2}!"
    else:
        return f"The bridge words from {word1} to {word2} are: {', '.join(bridges)}"
'''
def queryBridgeWords(word1, word2):
    if not directed_graph.has_node(word1) or not directed_graph.has_node(word2):
        return "No word1 or word2 in the graph!"

    visited = set()
    bridges = []

    def dfs(node, target, path):
        if node == target:
            bridges.extend(path[:-1])  # 不包含最后一个节点
            return True

        visited.add(node)
        for neighbor in directed_graph.neighbors(node):
            if neighbor not in visited and neighbor != word1:
                if dfs(neighbor, target, path + [neighbor]):
                    return True

    dfs(word1, word2, [])
    visited.clear()

    if not bridges:
        return f"No bridge words from {word1} to {word2}!"
    else:
        return f"The bridge words from {word1} to {word2} are: {', '.join(bridges)}"

def generateNewText(input_text):
    new_text = []
    words = input_text.lower().split()
    for i in range(len(words) - 1):
        word1 = words[i]
        word2 = words[i + 1]
        new_text.append(word1)

        if directed_graph.has_node(word1) and directed_graph.has_node(word2):
            bridge_word = queryBridgeWords(word1, word2) #查询是否有桥接词
            if bridge_word:
                new_text.append(bridge_word)

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
    pos = nx.spring_layout(directed_graph, seed=42)
    edge_labels = {(u, v): directed_graph.get_edge_data(u, v)['weight'] for u, v in directed_graph.edges()}
    nx.draw(directed_graph, pos, with_labels=True, node_size=800, node_color="skyblue", font_size=10,
            font_weight="bold", arrows=True, arrowsize=10, edge_color="gray", width=1.5,
            connectionstyle='arc3, rad=0.2')

    # Adjusting edge label positions
    pos_higher = {}
    for k, v in pos.items():
        pos_higher[k] = (v[0], v[1] + 0.08)  # Increase the y-coordinate slightly for better label visibility

    nx.draw_networkx_edge_labels(directed_graph, pos_higher, edge_labels=edge_labels, font_color='red', font_size=8)
    plt.show()





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
#            for edge in directed_graph.edges(data=True):
#                print(edge)

        elif choice == "2":
            word1 = input("Enter word1: ")
            word2 = input("Enter word2: ")
            result = queryBridgeWords(word1, word2)
            print(result)
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
