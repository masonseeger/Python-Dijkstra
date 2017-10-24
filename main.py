from digraph import DiGraph

def read_input(file_name):
    '''
    `file_name` is formatted as a csv file
    in the form of `tail,head,cost` in each line
    '''
    my_file = open(file_name, "r")
    lines = my_file.read().split("\n")
    my_file.close()

    del lines[-1]

    edge_to_cost = {}
    for line in lines:
        tail, head, cost = map(int, line.split(","))
        edge_to_cost[(tail, head)] = cost

    return edge_to_cost

# To change input file and output file,
# change the arguments in line 25 and line 31
# and change the terminus in line 31
def main():
    edge_to_cost = read_input("input2.txt")
    my_digraph = DiGraph(edge_to_cost)
    #print(my_digraph.node_set)
    #print(my_digraph.node_to_neighbor)
    #print(my_digraph.edge_to_cost)

    my_digraph.dijkstra(1, 12, early_stop=False, file_name="output2.txt")

if __name__ == "__main__":
    main()
