class DisjointSetForest:
    def __init__(self, num_sets):
        self.dsf = [-1] * num_sets

    def is_index_valid(self, i):
        return 0 <= i <= len(self.dsf)

    # Search for a node and return the root
    # of its set if found
    def find(self, node):
        # If node is invalid, return -1
        if not self.is_index_valid(node):
            return -1

        # If node is root, return node
        if self.dsf[node] < 0:
            return node

        # If node is not root, recursively find it while path compressing
        self.dsf[node] = self.find(self.dsf[node])
        return self.dsf[node]

    # Perform union by height of two sets
    def union(self, a, b):
        # Find the set a and b belong to
        ra = self.find(a)
        rb = self.find(b)

        # If they belong to the same set, do nothing
        if ra == rb:
            return

        # If trees have the same height,
        # join b to a
        if self.dsf[ra] == self.dsf[rb]:
            self.dsf[ra] -= 1
            self.dsf[rb] = ra
        # If the height of a is greater,
        # join b to a
        elif self.dsf[ra] < self.dsf[rb]:
            self.dsf[rb] = ra
        # Otherwise, height of b is greater,
        # join set a to b
        else:
            self.dsf[ra] = rb