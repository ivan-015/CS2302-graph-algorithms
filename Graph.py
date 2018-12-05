from DSF import DisjointSetForest

class KruskalError(Exception):
    pass

class TopologicalSortError(Exception):
    pass

class GraphError(Exception):
    pass

class GraphALNode:
    def __init__(self, item, weight, next):
        self.item = item
        self.weight = weight
        self.next = next


class GraphAL:
    def __init__(self, init_num_vertices, is_directed):
        if init_num_vertices<0:
            raise GraphError("Invalid initial number of vertices")
        self.adj_list = [None] * init_num_vertices
        self.is_directed = is_directed

    def is_valid_vertex(self, u):
        return 0 <= u < len(self.adj_list)

    def add_vertex(self):
        self.adj_list.append(None)
        return len(self.adj_list) - 1

    def add_edge(self, src, dest, weight=1.0):
        # Check both source and destination are valid vertices
        if not self.is_valid_vertex(src) or not self.is_valid_vertex(dest):
            return

        # Check if source already points to destination
        curr = self.adj_list[src]
        while curr is not None:
            if curr.item == dest:
                return
            curr = curr.next
        # Add destination to adjacency list of source
        self.adj_list[src] = GraphALNode(dest, weight, self.adj_list[src])

        # If the graph is undirected, add an edge from
        # destination to source
        if not self.is_directed:
            self.adj_list[dest] = GraphALNode(src, weight, self.adj_list[dest])

    def remove_edge(self, src, dest):
        self.__remove_directed_edge(src, dest)

        if not self.is_directed:
            self.__remove_directed_edge(dest, src)

    def __remove_directed_edge(self, src, dest):
        # Check that the vertices are valid
        if not self.is_valid_vertex(src) or not self.is_valid_vertex(dest):
            return
        # If the current src is not adjacent to any
        # vertices, return
        if self.adj_list[src] is None:
            return
        # If the first vertex in the adjacency list matches the
        # destination, remove its edge
        if self.adj_list[src].item == dest:
            self.adj_list[src] = self.adj_list[src].next
        # Iterate through the edges of the src vertex
        # and search for the edge to remove
        else:
            prev = self.adj_list[src]
            curr = self.adj_list[src].next

            while curr is not None:
                # If the the destinations match, remove the edge
                if curr.item == dest:
                    prev.next = curr.next
                    return
                prev = prev.next
                curr = curr.next

        return len(self.adj_list)

    def get_num_vertices(self):
        return len(self.adj_list)

    # Function that returns a set of every vertex
    # that src points to
    def get_vertices_reachable_from(self, src):
        reachable_vertices = set()

        temp = self.adj_list[src]

        while temp is not None:
            reachable_vertices.add(temp.item)
            temp = temp.next

        return reachable_vertices

    # Function that returns a set of every vertex
    # that points to dest
    def get_vertices_that_point_to(self, dest):
        vertices = set()

        # Go through the adjacency list to look
        # for vertices that point to dest
        for i in range(len(self.adj_list)):
            temp = self.adj_list[i]

            while temp is not None:
                # If a vertex is adjacent to dest,
                # add it to the set
                if temp.item == dest:
                    vertices.add(i)
                    break
                temp = temp.next

        return vertices

    def get_edges(self):
        edge_list = []
        # Traverse adjacency list and add all edges
        for i in range(len(self.adj_list)):
            curr = self.adj_list[i]
            while curr is not None:
                edge_list.append([i, curr.item, curr.weight])
                curr = curr.next
        return edge_list

    # This function returns a representation of the minimal
    # spanning tree of a graph using kruskal's algorithm
    def kruskal_mst(self):
        if self.is_directed:
            raise KruskalError("Kruskal: Graph must be undirected.")
        mst = []
        dsf = DisjointSetForest(self.get_num_vertices())

        # Get list of edges and sort
        edges = self.get_edges()
        self.__merge_sort(edges)

        for i in edges:
            # If current edge creates cycle, skip it
            if dsf.find(i[0]) == dsf.find(i[1]):
                continue
            # Otherwise, unite vertices in dsf
            # and add edge to mst list
            dsf.union(i[0], i[1])
            mst.append(i)

        return mst

    def __merge_sort(self, lst):
        if lst is None or len(lst) <= 1:
            return lst

        # Split the list in two
        mid = len(lst) // 2

        first_half = lst[:mid]
        second_half = lst[mid:]

        # Recursively merge sort both halves
        self.__merge_sort(first_half)
        self.__merge_sort(second_half)

        # Merge two sorted lists
        f = 0  # indicates index of first half
        s = 0  # Indicates index of second half
        i = 0  # Indicates index of lst

        while f < len(first_half) and s < len(second_half):
            # If the weight of the edge in the first half is less,
            # add it to lst and increment the index for first_half
            if first_half[f][2] < second_half[s][2]:
                lst[i] = first_half[f]
                f += 1
            # Otherwise, add edge of second half and increment
            # the index for the second half
            else:
                lst[i] = second_half[s]
                s += 1
            # Increment the index of lst after adding an element
            i += 1

        # Add left-over items from one of the lists
        while f < len(first_half):
            lst[i] = first_half[f]
            f += 1
            i += 1
        while s < len(second_half):
            lst[i] = second_half[s]
            s += 1
            i += 1

    # Function that computes and returns the topological sort of a graph
    def topological_sort(self):
        # If graph has a cycle or is undirected, return
        if not self.is_directed:
            raise TopologicalSortError("Topological sort: Graph must be directed")

        # Compute indegrees of each vertex in graph
        indeg = []
        no_indegree = []  # List to store vertices with no indegree
        for i in range(len(self.adj_list)):
            d = len(self.get_vertices_that_point_to(i))
            indeg.append(d)
            # If the indegree is 0, append it to no_indegree
            if d == 0:
                no_indegree.append(i)

        if len(no_indegree) == 0:
            TopologicalSortError("Topological sort: No vertices with indegree 0 found")

        sorted_vertices = []  # List to store sorted vertices
        while len(no_indegree) > 0:
            # Add the current vertex with indegree of 0 to sorted vertices
            curr_vert = no_indegree.pop(0)
            sorted_vertices.append(curr_vert)

            # Get adjacent vertices and reduce their indegrees
            adj_vert = self.get_vertices_reachable_from(curr_vert)
            for vertex in adj_vert:
                indeg[vertex] -= 1
                # If the new indegree of a vertex is 0, add it to no_indegree
                if indeg[vertex] == 0:
                    no_indegree.append(vertex)
        # If the number of sorted vertices does not match the total number
        # of vertices, it means there is a cycle
        if len(sorted_vertices) != self.get_num_vertices():
            raise TopologicalSortError("Cycle found. No topological sort exists.")

        return sorted_vertices
