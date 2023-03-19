#%% Question 1
import math

class Graph1:
    class Vertex:
        def __init__(self, id):
            """
            Initialise a vertex in a graph
            :best time complexity: O(1)
            :worst time complexity: O(1)
            :aux space complexity: O(1)
            """
            self.edges = []
            self.cap = 0
            self.value = -math.inf

    class Edge:
        def __init__(self, v, r):
            """
            Initialise an edge in graph
            :best time complexity: O(1)
            :worst time complexity: O(1)
            :aux space complexity: O(1)
            """
            self.dest = v
            self.ratio = r 

    def __init__(self, n):
        """
        Initialise a graph by creating the adj list with vertices
        :param n: number of vertices
        :best time complexity: O(n)
        :worst time complexity: O(n)
        :aux space complexity: O(n)
        """
        self.adj_list = [Graph1.Vertex(i) for i in range(n)]

    def add_edge(self, e):
        """
        Add a directed edge between two vertices in graph
        :param e: 3 elements tuple, e[0] is the source, 
                  e[1] is the destination, e[2] is the 'weight'
        :best time complexity: O(1)
        :worst time complexity: O(1)
        :aux space complexity: O(1)
        """
        u, v, r = e[0], e[1], e[2]
        edge = Graph1.Edge(v, r)
        self.adj_list[u].edges.append(edge)

def best_trades(prices, starting_liquid, max_trades, townspeople):
    """
    Gets the maximum value obtained through trading valueable liquids with people,
    constrained by no of max trades and one unlimited container without mixing liquids
    :param prices: array of length n, where prices[i] is the value of 1L of the liquid with ID i
    :param starting_liquid: ID of the starter liquid, always 1L
    :param max_trades: maximum number of trades allowed
    :param townspeople: a list of non-empty lists, each interior list corresponds to the trades offered by a particular person
                        the interior lists contain 3 element tuples, (give, receive, ratio)
                            - each tuple indicates that this person is willing to be given liquid with ID (give) in 
                              exchange for liquid with ID (receive) at the given (ratio) 
    :return max_value: maximum value obtained after performing at most max_trades trades
    :best time complexity: O(N) where n is length of prices array if max_trades is 0 
    :worst time complexity: O(TM) where T is total no of trades available, M is max_trades
    :aux space complexity: O(N+T)
    """
    # create graph
    graph = Graph1(len(prices))
    for person in townspeople:
        for trade in person:
            graph.add_edge(trade)
    # set starting liquid value and capacity
    graph.adj_list[starting_liquid].cap = 1
    graph.adj_list[starting_liquid].value = prices[starting_liquid]

    for _ in range(max_trades):
        pr, cp = [], []
        # price and capacity before iteration
        for i in range(len(prices)):
            pr.append(graph.adj_list[i].value)
            cp.append(graph.adj_list[i].cap)

        for v in graph.adj_list:
            if v.value != -math.inf:
                for e in v.edges:
                    traded = v.cap * e.ratio * prices[e.dest]
                    # if trade results in higher value
                    if traded > pr[e.dest]:
                        pr[e.dest] = traded
                        cp[e.dest] = v.cap * e.ratio
                    # if trade results in same value but higher capacity
                    elif traded == pr[e.dest] and v.cap * e.ratio > cp[e.dest]:
                        cp[e.dest] = v.cap * e.ratio
        # change price and capacity after iteration
        for j in range(len(prices)):
            graph.adj_list[j].value = pr[j]
            graph.adj_list[j].cap = cp[j]
    # find maximum value
    max_value = graph.adj_list[0].value
    for k in range(1, len(prices)):
        v = graph.adj_list[k]
        if v.value != -math.inf and v.value > max_value:
            max_value = v.value
    return max_value

#%% Question 2
class Graph2:
    class Vertex:
        def __init__(self, id):
            """
            Initialise a vertex in a graph
            :best time complexity: O(1)
            :worst time complexity: O(1)
            :aux space complexity: O(1)
            """
            self.id = id
            self.edges = []
            self.distance = -math.inf
            self.previous = None
            self.discovered = False
            self.visited = False

    class Edge:
        def __init__(self, v, w):
            """
            Initialise an edge in graph
            :best time complexity: O(1)
            :worst time complexity: O(1)
            :aux space complexity: O(1)
            """
            self.v = v
            self.w = w    

    def __init__(self, n):
        """
        Initialise a graph by creating the adj list with vertices
        :param n: number of vertices
        :best time complexity: O(n)
        :worst time complexity: O(n)
        :aux space complexity: O(n)
        """
        self.adj_list = [Graph2.Vertex(i) for i in range(n)]

    def add_edge(self, e):
        """
        Add an undirected edge between two vertices in graph
        :param e: 3 elements tuple, e[0] iand e[1] are the
                  two connected vertices, e[2] is the weight
        :best time complexity: O(1)
        :worst time complexity: O(1)
        :aux space complexity: O(1)
        """
        u, v, w = e[0], e[1], e[2]
        self.adj_list[u].edges.append(Graph2.Edge(v, w))
        self.adj_list[v].edges.append(Graph2.Edge(u, w))

class MinHeap:
    def __init__(self, source, n):
        """
        Initialise a min heap and corresponding index array for Dijkstra algorithm,
        with item = [i, dist] where i is ID of a vertex, dist is the distance of vertex from source
        :param source: root of the heap
        :param n: size of heap
        :best time complexity: O(n)
        :worst time complexity: O(n)
        :aux space complexity: O(n)
        """
        self.size = n
        self.heap = [None, [source, 0]]
        for i in range(self.size):
            if i != source:
                self.heap.append([i, math.inf])
        self.index = [None] * (self.size)
        # keeps track of position of vertex in heap
        for j in range(1, self.size+1):
            self.index[self.heap[j][0]] = j   

    def serve(self):
        """
        Serve an item from the heap by swapping root with last item and performing downheap
        :return: the item that is served
        :best time complexity: O(1)
        :worst time complexity: O(1)
        :aux space complexity: O(1)
        """
        self.swap(1, self.size)
        self.size -= 1
        self.sink(1)
        return self.heap[self.size+1]

    def swap(self, x, y):
        """
        Swap two items in the heap and the corresponding index array
        :param x: first item to be swapped
        :param y: second item to be swapped
        :best time complexity: O(1)
        :worst time complexity: O(1)
        :aux space complexity: O(1)
        """
        self.heap[x], self.heap[y] = self.heap[y], self.heap[x]
        # update index
        self.index[self.heap[x][0]], self.index[self.heap[y][0]] = self.index[self.heap[y][0]], self.index[self.heap[x][0]]

    def rise(self, k):
        """
        Perform upheap for a certain item in min heap
        :param k: the index of item in heap to rise
        :best time complexity: O(1) if item at k is smallest  
        :worst time complexity: O(logN) where N is the size of heap
        :aux space complexity: O(1)
        """
        if k <= self.size:
            while k > 1 and self.heap[k][1] < self.heap[k//2][1]:
                self.swap(k, k//2)
                k = k//2   

    def sink(self, k):
        """
        Perform downheap for a certain item in min heap
        :param k: the index of item in heap to sink
        :best time complexity: O(1) if item at k is larger than parent
        :worst time complexity: O(logN) where N is the size of heap
        :aux space complexity: O(1)
        """
        while 2*k <= self.size:
            child = self.smallest_child(k)
            if self.heap[k][1] <= self.heap[child][1]:
                break
            self.swap(k, child)
            k = child  

    def smallest_child(self, k):
        """
        Finds the smallest child of an item in min heap if exists
        :param k: the index of parent in heap
        :return: the index of smallest child in heap
        :best time complexity: O(1)
        :worst time complexity: O(1)
        :aux space complexity: O(1)
        """
        if 2*k == self.size or self.heap[2*k][1] < self.heap[2*k+1][1]:
            return 2*k
        else:
            return 2*k+1
    
def opt_delivery(n, roads, start, end, delivery):
    """
    Determines minimum cost of travelling from start city to end city, with or
    without delivering an item from one particular city to another 
    particular city to make money on the way 
    :param n: the number of cities
    :param roads: a list of tuples, each tuple = (u,v,w)
                    - each tuple represents an road between cities u and v and 
                      w is the cost of traveling along that road, which is always non-negative
                    - roads represent a simple connected graph
    :param start: start city
    :param end: end city
    :param delivery: 3 elements tuple
                        - first value is the city where item can be picked up
                        - second value is the city to deliver the item
                        - third value is the amount of money made if manage to deliver
    :return: tuple with 2 elements (cost, path)
                - cost is the cost travelling from start city to end city, includes profit
                  made from delivery if choose to make delivery
                - path is a list of integers representing cities travelled from start to end
    :best time complexity: O(Rlog(N)) where R is the total number of roads, N is the total number of cities
    :worst time complexity: O(Rlog(N))
    :aux space complexity: O(N+R)
    """
    # create graph
    graph = Graph2(n)
    for edge in roads:
        graph.add_edge(edge)

    def backtrack(start, end):
        """
        Backtracks from end city to start city to find the path taken
        :param start: start city
        :param end: end city
        :return path: path taken from start to end excluding start city
        :best time complexity: O(1) if start city is the same as end city
        :worst time complexity: O(N) where N is the number of cities travelled in path
        :aux space complexity: O(N)
        """
        path = []
        curr = graph.adj_list[end]
        # backtrack until right before start
        while curr.id != start:
            path.append(curr.id)
            curr = graph.adj_list[curr.previous]
        # reverse to get actual path
        path.reverse()
        return path

    def reset():
        """
        Resets each vertex and some of its payload to initial values
        :best time complexity: O(N) where N is the number of vertices in graph
        :worst time complexity: O(N)
        :aux space complexity: O(1)
        """
        for v in graph.adj_list:
            v.distance = -math.inf
            v.discovered = False
            v.visited = False

    def dijkstra(start, end):
        """
        Dijkstra algorithm to find minimum cost of travelling from start city to end city
        :param start: start city
        :param end: end city
        :return (cost, path): cost is the cost of travelling from start to end,
                              path is the cities travelled excluding start
        :best time complexity: O(1) if start city and end city are the same
        :worst time complexity: O(Rlog(N)), R is the total number of edges in graph
                                           N is the total number of vertices in graph
        :aux space complexity: O(N+M) where M is the number of cities in path
        """
        # initialise heap
        heap = MinHeap(start, n)
        graph.adj_list[start].distance = 0
        graph.adj_list[start].discovered = True

        while heap.size > 1:
            serve = heap.serve()
            u = graph.adj_list[serve[0]]
            u.visited = True
            # if end vertex is finalised, end
            if u == end:
                break
            for edge in u.edges:
                v = graph.adj_list[edge.v]
                index = heap.index[edge.v]
                # add adjacent into heap
                if v.discovered == False:
                    v.discovered = True
                    v.previous = u.id
                    v.distance = serve[1] + edge.w
                    heap.heap[index][1] = serve[1] + edge.w
                # edge relaxation
                elif v.visited == False:
                    if serve[1] + edge.w < heap.heap[index][1]:
                        v.previous = u.id
                        v.distance = serve[1] + edge.w
                        heap.heap[index][1] = serve[1] + edge.w
                # update heap
                heap.rise(index)

        cost = graph.adj_list[end].distance
        path = backtrack(start, end)
        reset()
        return (cost, path)

    # dijkstra from start to end without delivery
    no_deliver = dijkstra(start, end)
    # dijkstra from start to pickup city, from pickup city to delivery city, from delivery city to end
    deliver = [dijkstra(start, delivery[0]), dijkstra(delivery[0], delivery[1]), dijkstra(delivery[1], end)]
    # cost of travelling with delivery
    cost_deliver = deliver[0][0] + deliver[1][0] + deliver[2][0] - delivery[2]
    
    path = [start]
    # if cost of travelling without delivery is smaller or equal than delivery
    if no_deliver[0] <= cost_deliver:
        path.extend(no_deliver[1])
        return (no_deliver[0], path)
    else:
        for i in range(len(deliver)):
            path.extend(deliver[i][1])
        return (cost_deliver, path)