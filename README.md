# 软工lab1代码更迭内容

# 需求分析

开发一个程序，实现从文本文件中读取数据并根据要求生成图结构，输出该图结构，并在其上进行一系列计算操作，实时展示各操作的结果。

开发的程序可以是命令行方式运行，也可以用图形化用户界面GUI的方式运行。无论何种方式，均应覆盖后续所有功能需求。

![Untitled](https://github.com/Yuanciel/Lab1-2021110973/assets/151415789/5f322b49-4d00-4143-9de3-1b57405170d6)


## 功能需求

### 1-读入文本并生成有向图

▪ **程序首先让用户选择或输入文本文件的位置和文件名。也可以参数的形式，在启动程序时提供文件路径和文件名。**

▪ **程序读入文本数据，进行分析，将其转化为有向图：**

– 有向图的节点为文本中包含的某个单词（不区分大小写）

– 两个节点A,B之间存在一条边A→B，意味着在文本中至少有一处位置A和B相邻出现（即A和B之间有且仅有1或多个空格）。

– A→B的权重w=文本中A和B相邻出现的次数，w>=1。

### 2-展示有向图（void showDirectedGraph(type G, …)）

▪ **展示生成的有向图。**

▪ **可选功能：将生成的有向图以图形文件形式保存到磁盘，可以调用外部绘图库或绘图工具API自动生成有向图，但不能采用手工方式绘图。**

### 3-查找桥接词（String queryBridgeWords(String word1, String word2)）

▪ **在生成有向图之后，用户输入任意两个英文单词word1、word2，程序从图中查询它们的“桥接词”。**

▪ **word1、word2的桥接词word3：图中存在两条边word1→word3,word3→word2。**

▪ **输入的word1或word2如果不在图中出现，则输出“No word1 or word2 in the graph!”**

▪ **如果不存在桥接词，则输出“No bridge words from word1 to word2!”**

▪ **如果存在一个或多个桥接词，则输出“The bridge words from word1 to word2 are: xxx, xxx, and xxx.”**

### 4-根据桥接词生成新文本（generateNewText(String inputText)）

▪ **用户输入一行新文本，程序根据之前输入文件生成的图，计算该新文本中两两相邻的单词的bridge word，将bridge word插入新文本的两个单词之间，输出到屏幕上展示。**

– 如果两个单词无bridge word，则保持不变，不插入任何单词；

– 如果两个单词之间存在多个bridge words，则随机从中选择一个插入进去形成新文本。

▪ **例如用户输入：Seek to explore new and exciting synergies**

▪ **则输出结果为：Seek to explore strange new life and exciting synergies**

### 5-计算两个单词之间的最短路径（calcShortestPath(String word1, String word2)）

▪ **用户输入两个单词，程序计算它们之间在图中的最短路径（路径上所有边权值之和最小），以某**

**种突出的方式将路径标注在原图并展示在屏幕上，同时展示路径的长度（所有边权值之和）。**

– 例如：输入to和and，则其最短路径为to→explore→strange→new→life→and

▪ **如果有多条最短路径，只需要展示一条即可。**

– 可选：计算出所有的最短路径，并以不同的突出显示方式展示出来。

– 例如to和and之间还有另一条路径：to→seek→out→new→life→and。

▪ **如果输入的两个单词“不可达”，则提示。**

▪ **可选功能：如果用户只输入一个单词，则程序计算出该单词到图中其他任一单词的最短路径，并**

**逐项展示出来。**

### 6-随机游走（randomWalk()）

▪ **进入该功能时，程序随机的从图中选择一个节点，以此为起点沿出边进行随机遍历，记录经过的所有节点和边，直到出现第一条重复的边为止，或者进入的某个节点不存在出边为止。**

**在遍历过程中，用户也可随时停止遍历。**

▪ **将遍历的节点输出为文本，并以文件形式写入磁盘。**

▪ **例如：**

– to seek out new life and new worlds to explore strange new civilizations

– to explore strange new worlds to explore

# 添加将读入的词变成小写的情况（2024-5-15）

## 修改前

![Untitled 1](https://github.com/Yuanciel/Lab1-2021110973/assets/151415789/38839348-4ecc-403f-8b43-ea8237a3972e)


![Untitled 2](https://github.com/Yuanciel/Lab1-2021110973/assets/151415789/9523a6e8-67ff-46b2-a2b2-4ff98d04adac)


## 修改后

在处理每行数据的时候加入一步全部转换为小写

```python
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
```

![Untitled 3](https://github.com/Yuanciel/Lab1-2021110973/assets/151415789/6f525200-a660-4616-a52a-0c784327ac84)


# 双向边出错情况

## 修改前

`input.txt` 内容如下：

> To explore strange new worlds,
To seek out new life and new civilizations and life and
> 

图像如下：

![Untitled 4](https://github.com/Yuanciel/Lab1-2021110973/assets/151415789/d6b1b2c5-6b48-4ec3-bd98-175be88dfede)


查找边权值没有问题：

![Untitled 5](https://github.com/Yuanciel/Lab1-2021110973/assets/151415789/3c88640c-388e-45d6-b392-921d15fde77e)


可能是如同内环一样，**标签被覆盖了**

首先对图的类别进行了修改：

[多重图---有自循环和平行边的无向图 — NetworkX 2.8 文档](https://www.osgeo.cn/networkx/reference/classes/multigraph.html)

```python
directed_graph = nx.MultiDiGraph()
```

但是作图仍然有问题，看官网给的提示是用其他的库对图像进行绘制：

[绘图 — NetworkX 2.8 文档](https://www.osgeo.cn/networkx/reference/drawing.html)

![Untitled 6](https://github.com/Yuanciel/Lab1-2021110973/assets/151415789/ed8786b3-841e-4f6b-96d4-62b6e53cb2e6)


可喜的是使用Graphviz后我们得到了初步想要的结果：

![Untitled 7](https://github.com/Yuanciel/Lab1-2021110973/assets/151415789/50f75830-45eb-494c-9597-27e31fb41959)


接下来填上边权值就行

<aside>
✨ 关于报warning问题看下面的链接，这个函数确实有潜在的问题（转换的时候边权值转不过去）

</aside>

## 修改后

![Untitled 8](https://github.com/Yuanciel/Lab1-2021110973/assets/151415789/0625ef41-3e6a-4b43-8957-662f7c779e16)


---

```python
def visualize_graph():
    PG = nx.nx_pydot.to_pydot(directed_graph)
    # 将原图中的边权值加入PG中，PG是Graphviz的图对象
    for edge in PG.get_edges():
        edge_label = str(directed_graph[edge.get_source()][edge.get_destination()]['weight'])
        edge.set_label(edge_label)
        
    PG.write_png('graph.png')
```

正常结果如上，一些带自环和平行边情况如下：

![Untitled 9](https://github.com/Yuanciel/Lab1-2021110973/assets/151415789/eabfdea6-3dee-4bac-b521-81e6d35122d3)


# 桥接词寻找（2024-5-16）

## 修改前

采用dfs算法进行搜树

## 修改后

```python
def queryBridgeWords(word1, word2):
    # 判断word1和word2是否在图中
    if not directed_graph.has_node(word1) and not directed_graph.has_node(word2):
        return f"No \"{word1}\" and \"{word2}\" in the graph!"
    elif not directed_graph.has_node(word1):
        return f"No \"{word1}\" in the graph!"
    elif not directed_graph.has_node(word2):
        return f"No \"{word2}\" in the graph!"
    # 用word3记录word1和word2的桥接词
    word3 = set()
    # 遍历word1的邻居，再遍历word1的邻居的邻居，判断是否有word2的邻居
    for neighbor in directed_graph.neighbors(word1):
        for neighbor2 in directed_graph.neighbors(neighbor):
            if neighbor2 == word2:
                word3.add(neighbor)
    if not word3:
        return f"No bridge words from \"{word1}\" to \"{word2}\"!"
    else:
        return f"The bridge words from \"{word1}\" to \"{word2}\" are: {', '.join(word3)}"
```

在实验指导书上的案例完全符合（指导书甚至打错系动词形式了），对于自环和平行边情况也可处理。

# 插入文本问题

## 修改前

```python
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
```

## 修改后

```python
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
```

主要添加了随机选取操作

同时对桥接词部分进行修改：

```python
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
```

主函数中不再输出result，2时不需要输入第三个参数，3时第三个参数设为False

# 最短路径寻找（2024-5-17）

## 修改前

```python
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
```

使用了比较高级的堆算法+Dijkstra算法，没看懂…..选择改成普通的Dijkstra算法

## 修改后

```python
def calcShortestPath(word1, word2): # 计算word1到word2的最短路径
    if not directed_graph.has_node(word1) or not directed_graph.has_node(word2):
        return "Word1 or Word2 not in the graph!"

    # Dijkstra算法寻找从word1到word2的最短路径
    distances = {node: float('inf') for node in directed_graph}
    distances[word1] = 0
    previous_nodes = {node: word1 for node in directed_graph}
    flag = {node: False for node in directed_graph}  # 标记是否已经加入顶点集
    # 初始化distance矩阵
    for neighbor, weight in directed_graph[word1].items():
        distances[neighbor] = weight['weight']
        previous_nodes[neighbor] = word1
    distances[word1] = 0
    flag[word1] = True
    # 寻找distance矩阵中最小值
    for j in range(len(directed_graph)-1): 
        min = float('inf')
        current_node = None
        for i in distances:
            if flag[i]:
                continue
            else:
                if distances[i] < min:
                    min = distances[i]
                    current_node = i
        flag[current_node] = True
        # 更新distance矩阵和previous_nodes矩阵
        for i in distances:
            if flag[i]:
                continue
            else:
                if directed_graph.has_edge(current_node, i):
                    distance = min + directed_graph[current_node][i]['weight']
                    if distance < distances[i]:
                        distances[i] = distance
                        previous_nodes[i] = current_node
                else:
                    continue
    # print(distances)
    # print(previous_nodes)
    # 回溯路径
    path = []
    current = word2
    # while current in previous_nodes:
    while current != word1:
        path.insert(0, current)
        current = previous_nodes[current]
    path.insert(0, word1)
    return f"Shortest path: {' -> '.join(path)}, Length: {distances[word2]}"
```

## 关于可选功能

### 可选功能1-所有可能的最短路径（已完成）（2024-5-20）

可选功能要求输出所有可能的最短路径，最短路径不同源自于在某次寻找`distance`最小值的时候可能出现多个相同的最小值，默认选取的是标号从小到大的第一个，导致后续结果不同。

<aside>
👉 [1]王志坚,韩伟一,李一军.具有多条最短路径的最短路问题[J].哈尔滨工业大学学报,2010,42(09):1428-1431.
</aside>

根据论文中的伪代码实现最短路径图，在图上通过深度优先搜索遍历从`word1` 到`word2` 的路径输出，对于每个路径都输出不同的图`minPath_word1_word2_n.png` 

结果如下：

![Untitled 10](https://github.com/Yuanciel/Lab1-2021110973/assets/151415789/9e91471a-a637-4118-ba4b-43f2cc6c3fd0)


![Untitled 11](https://github.com/Yuanciel/Lab1-2021110973/assets/151415789/0db3a109-42ef-4ed8-a540-17f023d7a245)


There are 2 shortest paths from "to" to "and". Their lengths are: 5.

Choose an option:

1. Show Directed Graph
2. Query Bridge Words
3. Generate New Text
4. Calculate Shortest Path
5. Random Walk
6. Exit
Exiting program.

### 可选功能2-在图上进行标注（已完成）（2024-5-17）

采用重新产生图像`minPath_word1_word2.png` 的方式，在UI中可以展示这一画面

![Untitled 12](https://github.com/Yuanciel/Lab1-2021110973/assets/151415789/425a8e57-0103-41ba-935b-9bfca2e483d3)


# (to be continued)可进一步内容

## 套壳UI

可以用`PyQt5`进行套壳，但是我个人感觉没必要，之后可能转战java，在Python上花太多功夫没有什么用

## 改java

to be continued

# randomwalk和如何允许用户打断遍历（2024-5-18）

## 修改前

没有允许打断操作，且没有给用户打断的时间整个遍历就会结束

```python
def randomWalk(directed_graph):
if not directed_graph or len(directed_graph.nodes) == 0:
return "Graph is empty."
visited_nodes = []  # 存储已经访问的节点
visited_edges = set()  # 使用集合来存储已经访问的边，确保边不重复
current_node = random.choice(list(directed_graph.nodes))

while True:
    visited_nodes.append(current_node)
    neighbors = list(directed_graph.neighbors(current_node))

    # 过滤掉已经访问过的边
    unvisited_neighbors = [n for n in neighbors if (current_node, n) not in visited_edges]
    if not unvisited_neighbors:
        break

    next_node = random.choice(unvisited_neighbors)
    visited_edges.add((current_node, next_node))

    current_node = next_node

result = "Visited Nodes:\\n"
for node in visited_nodes:
    result += f"- {node}\\n"

with open("random_walk_output.txt", "w") as file:
    file.write(result)

return result

```

## 修改后

加入线程，检测用户是否输入enter

并引入time.sleep()函数，将delay设置为1，也就是一秒钟往下游走一个节点，让用户有足够的时间随时打断。并且引入标志位来确保如果没有被打断不会一直等待用户输入，而是正常结束

线程部分：一旦用户按下 Enter 键，**`stop_event.set()`** 被调用。**`set()`** 方法将 **`stop_event`** 标记为已设置，这将在主线程中被检测到，并触发停止随机游走并输出结果的操作。

```python
def check_user_input(stop_event):
    input("Press Enter to stop the random walk...")
    stop_event.set()

def randomWalk(delay=1):
    if not directed_graph or len(directed_graph.nodes) == 0:
        return "Graph is empty."

    visited_nodes = []  # 存储已经访问的节点
    visited_edges = set()  # 使用集合来存储已经访问的边，确保边不重复
    current_node = random.choice(list(directed_graph.nodes))
    interrupted_by_user = False  # 标志位，表示是否被用户打断

    # 事件用于标记是否用户请求停止
    stop_event = threading.Event()
    input_thread = threading.Thread(target=check_user_input, args=(stop_event,))
    input_thread.start()

    try:
        while True:
            visited_nodes.append(current_node)
            neighbors = list(directed_graph.neighbors(current_node))

            # 过滤掉已经访问过的边
            unvisited_neighbors = [n for n in neighbors if (current_node, n) not in visited_edges]
            if not unvisited_neighbors:
                break

            next_node = random.choice(unvisited_neighbors)
            visited_edges.add((current_node, next_node))

            current_node = next_node

            # 加入延迟
            time.sleep(delay)

            # 检查用户是否打断游走
            if threading.main_thread().is_alive() and not interrupted_by_user:
                continue  # 继续下一次迭代
            else:
                break  # 用户打断或者遍历完所有节点，退出循环
    except KeyboardInterrupt:
        interrupted_by_user = True
    finally:
        if interrupted_by_user:
            visited_nodes.append("(Interrupted by user)")
        else:
            visited_nodes.append("(Finished without interruption)")

        result = "Visited Nodes:\n"
        for node in visited_nodes:
            result += f"- {node}\n"

        with open("random_walk_output.txt", "w") as file:
            file.write(result)

    return result
```

## 修改后2.0

发现有的时候按enter打断不了，所以感觉是判断是否break的条件有问题改成了如下判断：

```jsx
if stop_event.is_set():
    interrupted_by_user = True
    break  # 用户打断，退出循环

```

原来的那个感觉会因为没有实时监控是否被打断而出不去循环，只能等他遍历完而不能打断，但是不知道为什么第一天写的时候这里诡异的测过去了、

# 修正Dijkstra算法

## 修改前

仅输出其中一条最短路径

## 修改后

输出图上所有最短路径，如果`word1`到`word2`不可达，也输出相应信息。

[可选功能1-所有可能的最短路径（已完成）（2024-5-20）](https://www.notion.so/1-2024-5-20-aa295954fda34d68a0c379c4cb4b85e6?pvs=21) 

# 简单修改使生成的中间图像输出出来

## 修改前

图在磁盘中存储，并不展示出来

## 修改后

通过`matplotlib` 将磁盘中的图显示展示出来
