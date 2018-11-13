import json
from tree_node import TreeNode
from qep_stats import *


def parseJsonNode(json_node):
    title = json_node["Node Type"]
    # If Plans not in dict, return empty list
    node_children = json_node.get("Plans", [])
    description_dict = {k: v for k,v in json_node.items() if k not in ["Plans", "Node Type"]}
    return TreeNode(title, node_children, description_dict)


def getTreeBFS(root):
    # root is a TreeNode
    all_nodes = [root]
    frontier = [root]
    i = 0
    while frontier:
        next_level = []
        for u in frontier:
            for v in u.children_text:
                node = parseJsonNode(v)
                u.addChild(node)
                all_nodes.append(node)
                next_level.append(node)
        frontier = next_level
        i += 1
    return all_nodes


def plotQueryTree(qep):
    """
    Args:
        - qep: json object, may need to perform json.load
    Returns:
        - stats: json object
        - all_nodes: json object representing the annotated qep 
    """
    assert 'Plan' in qep[0], "Invalid JSON was given"
    root = parseJsonNode(qep[0]['Plan'])
    all_nodes = getTreeBFS(root)
    
    # Compute statistics
    execution_time = qep[0].get('Execution Time', None)
    planning_time = qep[0].get('Planning Time', None)
    calculateActualCost(all_nodes)
    calculateActualDuration(all_nodes)
    largest_row = markLargestNode(all_nodes)
    largest_cost = markCostliestNode(all_nodes)
    largest_duration = markSlowestNode(all_nodes)
    calculatePercentDuration(all_nodes, execution_time)
    
    stats = {'execution_time': execution_time, 
             'planning_time': planning_time,
             'largest_row': largest_row, 
             'largest_cost': largest_cost, 
             'largest_duration': largest_duration}

    return json.dump(stats), json.dump(all_nodes[0].to_json())
