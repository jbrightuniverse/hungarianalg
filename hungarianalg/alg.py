"""

Hungarian Algorithm No. 5 by James Yuming Yu
Vancouver School of Economics, UBC
8 March 2021

Based on http://www.cse.ust.hk/~golin/COMP572/Notes/Matching.pdf and https://montoya.econ.ubc.ca/Econ514/hungarian.pdf

"""
import numpy as np

class Node:
    """A simple node for an alternating tree."""
    
    def __init__(self, val, parent = None):
        self.val = val
        self.parent = parent

def hungarian(matrx):
    """Runs the Hungarian Algorithm on a given matrix and returns the optimal matching with potentials."""
    
    # Step 1: Prep matrix, get size
    matrx = np.array(matrx)
    size = matrx.shape[0]
    
    # Step 2: Generate trivial potentials
    rpotentials = []
    cpotentials = [0 for i in range(size)]
    for i in range(len(matrx)):
        row = matrx[i]
        rpotentials.append(max(row))

    # Step 3: Initialize alternating tree
    matching = []
    S = {0}
    T = set()

    tree_root = Node(0)
    x_nodes = {0: tree_root}
    
    # Create helper functions

    def neighbours(wset):
        """Finds all firms in equality graph with workers in wset."""
    
        result = []
        for x in wset:
            # get row of firms for worker x
            nbs = matrx[x, :]
            for y in range(len(nbs)):
                # check for equality
                if nbs[y] == rpotentials[x] + cpotentials[y]:
                    result.append([x, y])

        return result
    

    def update_potentials():
        """Find the smallest difference between treed workers and untreed firms 
            and use it to update potentials."""
        
        # when using functions in functions, if modifying variables, call nonlocal
        nonlocal rpotentials, cpotentials 
        big = np.inf
        # iterate over relevant pairs
        for dx in S:
            for dy in set(range(size)) - T:
                # find the difference and check if its smaller than any we found before
                weight = matrx[dx, dy]
                alpha = rpotentials[dx] + cpotentials[dy] - weight
                if alpha < big:
                    big = alpha

        # apply difference to potentials as needed
        for dx in S:
            rpotentials[dx] -= big

        for dy in T:
            cpotentials[dy] += big
        
    # Step 4: Loop while our matching is too small
    while len(matching) != size:
        # Step A: Compute neighbours in equality graph
        NS = neighbours(S)
        if set([b[1] for b in NS]) == T:
            # Step B: If all firms are in the tree, update potentials to get a new one
            update_potentials()
            NS = neighbours(S)

        # get the untreed firm
        pair = next(n for n in NS if n[1] not in T)
        if pair[1] not in [m[1] for m in matching]:
            # Step D: Firm is not matched so add it to matching 
            matching.append(pair)
            # Step E: Swap the alternating path in our alternating tree attached to the worker we matched
            source = x_nodes[pair[0]]
            matched = 1
            while source.parent != None:
                above = source.parent
                if matched:
                    # if previously matched, this should be removed from matching
                    matching.remove([source.val, above.val])
                else:
                    # if previous was a remove, this is a match
                    matching.append([above.val, source.val])

                matched = 1 - matched
                source = above

            # Step F: Destroy the tree, go to Step 4 to check completion, and possibly go to Step A
            free = list(set(range(size)) - set([m[0] for m in matching]))
            if len(free):
                tree_root = Node(free[0])
                x_nodes = {free[0]: tree_root}
                S = {free[0]}
                T = set()

        else:
            # Step C: Firm is matched so add it to the tree and go back to Step A
            matching_x = next(m[0] for m in matching if m[1] == pair[1])
            S.add(matching_x)
            T.add(pair[1])
            source = x_nodes[pair[0]]
            y_node = Node(pair[1], source)
            x_node = Node(matching_x, y_node)
            x_nodes[matching_x] = x_node
    
    revenues = [matrx[m[0], m[1]] for m in matching]
    class Result:
        """A simple response object."""

        def __init__(self, match, revenues, row_weights, col_weights, revenue_sum):
            self.match = match
            self.revenues = revenues
            self.row_weights = row_weights
            self.col_weights = col_weights
            self.revenue_sum = revenue_sum

        def __str__(self):
            size = len(self.match)
            maxlen = max(len(str(max(self.revenues))), len(str(min(self.revenues))))
            baselist = [[" "*maxlen for i in range(size)] for j in range(size)]
            for i in range(size):
                entry = self.match[i]
                baselist[entry[0]][entry[1]] = str(self.revenues[i]).rjust(maxlen)

            formatted_list = '\n'.join([str(row) for row in baselist])
            return f"Matching:\n{formatted_list}\n\nRow Potentials: {self.row_weights}\nColumn Potentials: {self.col_weights}"

    return Result(matching, revenues, rpotentials, cpotentials, sum(revenues))