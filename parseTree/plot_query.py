import pydot
from tree_node import TreeNode


def getNumOfPrecedingSpaces(line):
    for i in range(len(line)):
        if line[i] != ' ':
            break  
    return i


def getOperatorFromLine(line):
    # Note that the order of operators is important
    operators = ['HashAggregate', 'Hash Join', 'Nested Loop', 'Index Scan', 'Hash', 'Seq Scan']
    for op in operators:
        if op in line:
            description = line.split(op)[1]
            return op, description
    return 'Unknown Operator', 'Could not find operator'


def parseQuery(result):
    all_nodes = []
    stack = []
    for i, res in enumerate(result):
        line = res[0]
        val = getNumOfPrecedingSpaces(line)
        # signals the start of an operator
        if i == 0 or '->' in line:
            op, description = getOperatorFromLine(line)
            node = TreeNode(op, val, description)

            while len(stack) > 0 and stack[-1].val >= val:
                stack.pop()

            if len(stack) > 0:
                # assign res[0] as a child of stack[-1]
                stack[-1].addChild(node)

            all_nodes.append(node)
            stack.append(node)          

        # if the line is not an operator, it belongs as a description of the previous operator
        else:
            stack[-1].description += '\n'
            line = line.replace(':', '') #pydot doesn't print out semicolons
            stack[-1].description += line[val:]
    return all_nodes


def plotBFS(root, graph):
    frontier = [root]
    i = 0
    while frontier:
        next_level = []
        for u in frontier:
            #print("level {}, val {}, title {}".format(i, n.val, n.title))
            for v in u.children: 
                edge = pydot.Edge(u.pydot_node, v.pydot_node)
                graph.add_edge(edge)
                next_level.append(v)
        frontier = next_level
        i += 1


def plotQueryTree(result, filename='test.png'):
    all_nodes = parseQuery(result)
    graph = pydot.Dot(graph_type='graph')
    for node in all_nodes:
        node.pydot_node = pydot.Node(node.to_string(), shape='box')
        graph.add_node(node.pydot_node)
    plotBFS(all_nodes[0], graph)
    graph.write_png(filename)
    return filename
