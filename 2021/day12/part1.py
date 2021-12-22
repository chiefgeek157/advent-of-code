from anytree import NodeMixin, RenderTree
import colorama
from colorama import Fore
from colorama import Back
from colorama import Style
from functools import total_ordering
import sys
from typing import Any, List, TextIO

#filename = "test1.txt"
#filename = "test2.txt"
#filename = "test3.txt"
filename = "input.txt"

@total_ordering
class GNode():

    unlimited = sys.maxsize

    def __init__(self, name:str):
        self.name = name
        self.neighbors = []
        self.reset_max_visits()

    def add(self, node:"GNode"):
        # print(f"{self} adding {node}")
        return self.neighbors.append(node)

    def set_max_visits(self, max_visits:int):
        self.max_visits = max_visits
    
    def reset_max_visits(self):
        self.max_visits = (1 if self.name.lower() == self.name else GNode.unlimited)

    def __eq__(self, other:Any):
        if isinstance(other, GNode):
            return (self.name == other.name)
        elif isinstance(other, str):
            return (self.name == other)
        return NotImplemented
         
    def __lt__(self, other:Any):
        if isinstance(other, GNode):
            return (self.name < other.name)
        elif isinstance(other, str):
            return (self.name < other.name)
        return NotImplemented

    def __repr__(self):
        str = ""
        if self.max_visits == GNode.unlimited:
            str += f"{Fore.BLUE}"
        elif self.max_visits == 2:
            str += f"{Fore.GREEN}"
        str += f"{self.name}{Style.RESET_ALL}"
        return str

    def __str__(self):
        return self.__repr__()

@total_ordering
class TNode(NodeMixin):

    def __init__(self, gnode:GNode, parent:"TNode"):
        self.gnode = gnode
        self.parent = parent

    # Return a list of GNodes that are neighbors of
    # this TNode's GNode AND can be visited
    def visitables(self):
        v = []
        for neighbor in self.gnode.neighbors:
            if neighbor.max_visits == GNode.unlimited:
                v.append(neighbor)
            else:
                count = 1
                can_visit = True
                for ancestor in self.iter_path_reverse():
                    if ancestor.gnode == neighbor:
                        count += 1
                        if count > neighbor.max_visits:
                            can_visit = False
                            break
                if can_visit:
                    v.append(neighbor)
        return v

    def __eq__(self, other:Any):
        if isinstance(other, TNode):
            return (self.gnode == other.gnode)
        elif isinstance(other, GNode) or isinstance(other, str):
            return (self.gnode == other)
        return NotImplemented

    def __lt__(self, other:Any):
        if isinstance(other, TNode):
            return (self.gnode < other.gnode)
        elif isinstance(other, GNode) or isinstance(other, str):
            return (self.gnode < other)
        return NotImplemented

    def __repr__(self):
        return f"{self.gnode}"

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return hash((self.parent, self.gnode.name))

    
class Graph:

    start_name = "start"
    end_name = "end"

    def __init__(self):
        self.gnodes = []
        self.start = None
        self.end = None

    def read(self, f:TextIO):
        line = f.readline()
        while line:
            values = line.strip().split("-")
            name1 = values[0]
            name2 = values[1]
            node1 = self.get(name1)
            if node1 is None:
                node1 = GNode(name1)
                # print(f"Created {node1}")
                self.gnodes.append(node1)
                if name1 == Graph.start_name:
                    self.start = node1
                elif name1 == Graph.end_name:
                    self.end = node1
            node2 = self.get(values[1])
            if node2 is None:
                node2 = GNode(values[1])
                # print(f"Created {node2}")
                self.gnodes.append(node2)
                if name2 == Graph.start_name:
                    self.start = node2
                elif name2 == Graph.end_name:
                    self.end = node2
            node1.add(node2)
            node2.add(node1)

            line = f.readline()

    def get(self, name:str):
        for gnode in self.gnodes:
            if gnode == name:
                # print(f"Found Node({node.name})")
                return gnode
        return None

    # Get the nodes with max_visits = 1 except the start and end
    def singles(self):
        return [gnode for gnode in self.gnodes if
            gnode.max_visits == 1 and
            gnode != self.start and
            gnode != self.end]

    # Return a list of strings that represent valid paths, e.g. "a-b-C-d"
    def paths(self):
        root = TNode(self.start, None)
        work = set([root])
        while len(work) > 0:
            # print(f"work={work}")
            print(f"work length={len(work)}")
            # print(f"{RenderTree(root)}")
            parent = work.pop()
            # print(f"Visiting {parent} with ancestors {parent.ancestors}")
            # input("Press enter to continue...")
            # Check if adding this node as a child is allowed
            for gnode in parent.visitables():
                # print(f"Adding child {gnode} to {parent}")
                child = TNode(gnode, parent=parent)
                if gnode != self.end:
                    work.add(child)
        
        # print(f"{RenderTree(root)}")

        # Cull paths that do not reach 'end'
        paths = []
        leaves = root.leaves
        for i in range(len(leaves)):
            leaf = leaves[i]
            # print(f"Checking leaf {leaf}")
            if leaf.gnode == self.end:
                path = leaf.gnode.name
                parent = leaf.parent
                while parent is not None:
                    path = f"{parent.gnode.name}-{path}"
                    parent = parent.parent
                # print(f"Path: {path}")
                paths.append(path)
            print(f"paths length: {len(paths)} out of {len(leaves)}")

        return paths

    def override_paths(self):
        all_paths = []
        singles = self.singles()
        print(f"singles {singles}")
        # input("Press enter to continue...")
        for single in singles:
            single.max_visits = 2
            print(f"Computing paths for {single} set to 2 visits...")
            paths = self.paths()
            # paths.sort()
            for path in paths:
                # print(f"Checking if path {path} is in all paths")
                if path not in all_paths:
                    print(f"Adding new path: {path}")
                    all_paths.append(path)
            single.reset_max_visits()
            # all_paths.sort()
            print_paths(all_paths)
            # input("Press enter to continue...")
        return all_paths

    def __str__(self):
        str = f"Graph: num nodes {len(self.gnodes)}"
        for gnode in self.gnodes:
            str += f"\n{gnode}"
        return str

def print_paths(paths:List[List]):
    print(f"\nTotal paths: {len(paths)}")
    for path in paths:
        print(f"{path}")

graph = Graph()
with open(filename, "r") as f:
    graph.read(f)

print(f"Graph: {graph}")

# paths = graph.paths()

all_paths = graph.override_paths()

# print(f"Answer: {len(paths)}")
print(f"Answer: {len(all_paths)}")