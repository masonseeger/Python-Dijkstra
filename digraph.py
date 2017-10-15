from math import inf
from terminaltables import AsciiTable
from timeit import default_timer as timer

def get_min_dist(node_to_dist, S):
    temp_result = -1
    temp_min = inf
    for node in node_to_dist:
        if (node not in S) and (temp_min > node_to_dist[node]):
            temp_result = node
            temp_min = node_to_dist[node]

    return temp_result

def generate_table(node_set, node_to_pred, node_to_dist):
    table_data = [["v", "pred(v)", "dis(v)"]]
    for node in node_set:
        table_data.append([node, node_to_pred[node], node_to_dist[node]])

    return list(map(list, zip(*table_data)))

class DiGraph:
    def __init__(self, edge_to_cost={}):
        self.edge_to_cost = edge_to_cost

        self.node_to_neighbor = {}
        self.node_set = set()
        for tail, head in edge_to_cost:
            self.node_set.add(tail)
            self.node_set.add(head)

            if tail not in self.node_to_neighbor:
                self.node_to_neighbor[tail] = {head}
            else:
                self.node_to_neighbor[tail].add(head)

    def dijkstra_iteration(self, S, node_to_pred, node_to_dist):
        temp_node = get_min_dist(node_to_dist, S)

        if temp_node not in self.node_to_neighbor:
            print("Error: There is not an edge going out from", temp_node)
            return False

        S.add(temp_node)
        for node in self.node_to_neighbor[temp_node]:
            #print(node_to_dist)
            #print(self.edge_to_cost)
            temp_dist = node_to_dist[temp_node] + self.edge_to_cost[(temp_node, node)]
            if temp_dist < node_to_dist[node]:
                node_to_pred[node] = temp_node
                node_to_dist[node] = temp_dist

        return S, node_to_pred, node_to_dist

    def dijkstra(self, source, terminus, early_stop=True, file_name="output.txt"):
        start = timer()

        # checking for invalid source or terminus
        invalid_source = True
        invalid_terminus = True
        for node in self.node_to_neighbor:
            if source == node: invalid_source = False
            if terminus in self.node_to_neighbor[node]: invalid_terminus = False
        if invalid_source:
            print("Error: Invalid source")
            return False
        if invalid_terminus:
            print("Error: Invalid terminus")
            return False

        # initializing set S and vertex table
        S = set()
        node_to_pred = {}
        node_to_dist = {}
        for node in self.node_set:
            node_to_pred[node] = source
            node_to_dist[node] = inf
        node_to_dist[source] = 0

        # individual iteration
        my_file = open(file_name, "w")
        table_data = generate_table(self.node_set, node_to_pred, node_to_dist)
        table = AsciiTable(table_data)
        my_file.write(table.table)
        my_file.write("\n")

        if early_stop:
            while terminus not in S:
                try:
                    S, node_to_pred, node_to_dist = self.dijkstra_iteration(S, node_to_pred, node_to_dist)
                    table_data = generate_table(self.node_set, node_to_pred, node_to_dist)
                    table = AsciiTable(table_data)
                    my_file.write(table.table)
                    my_file.write("\n")
                except Exception as exc:
                    print("Error in iteration,", exc)
                    break
        else:
            for i in range(len(self.node_set)):
                try:
                    S, node_to_pred, node_to_dist = self.dijkstra_iteration(S, node_to_pred, node_to_dist)
                    table_data = generate_table(self.node_set, node_to_pred, node_to_dist)
                    table = AsciiTable(table_data)
                    my_file.write(table.table)
                    my_file.write("\n")
                except Exception as exc:
                    print("Error in iteration,", exc)
                    break

        time = timer() - start
        my_file.write("Took %f seconds." % time)
        my_file.close()
