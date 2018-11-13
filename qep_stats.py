from tree_node import TreeNode


def markLargestNode(all_nodes):
    row_switch = 'Plan Rows'
    if 'Actual Rows' in all_nodes[0].description_dict:
        row_switch = 'Actual Rows'
    all_nodes_rows = [n.description_dict[row_switch] for n in all_nodes]
    largest = max(all_nodes_rows)
    label = '*Largest Node (by rows)'
    for n in all_nodes:
        n.description_dict[label] = False
        if n.description_dict[row_switch] == largest:
            n.description_dict[label] = True
    return largest

def calculateActualCost(all_nodes):
    for n in all_nodes:
        children_cost = sum([c.description_dict['Total Cost'] for c in n.children])
        n.description_dict['*Actual Cost'] = n.description_dict['Total Cost'] - children_cost
        
def markCostliestNode(all_nodes):
    all_nodes_cost = [n.description_dict['*Actual Cost'] for n in all_nodes]
    largest = max(all_nodes_cost)
    label = '*Costiest Node (by cost)'
    for n in all_nodes:
        n.description_dict[label] = False
        if n.description_dict['*Actual Cost'] == largest:
            n.description_dict[label] = True 
    return largest

def calculateActualDuration(all_nodes):
    if 'Actual Total Time' not in all_nodes[0].description_dict:
        for n in all_nodes:
            n.description_dict['*Actual Duration'] = 0
        return
        
    for n in all_nodes:
        children_cost = sum([c.description_dict['Actual Total Time'] for c in n.children])
        n.description_dict['*Actual Duration'] = n.description_dict['Actual Total Time'] - children_cost
        
def markSlowestNode(all_nodes):
    if 'Actual Total Time' not in all_nodes[0].description_dict:
        for n in all_nodes:
            n.description_dict['*Slowest Node (by duration)'] = False
        return
    
    all_nodes_cost = [n.description_dict['*Actual Duration'] for n in all_nodes]
    largest = max(all_nodes_cost)
    label = '*Slowest Node (by duration)'
    for n in all_nodes:
        n.description_dict[label] = False
        if n.description_dict['*Actual Duration'] == largest:
            n.description_dict[label] = True 
    return largest

def calculatePercentDuration(all_nodes, total_duration):
    if total_duration is None:
        for n in all_nodes:
            n.description_dict['*Percent Duration'] = None
        return
        
    for n in all_nodes:
        n.description_dict['*Percent Duration'] = round(n.description_dict['*Actual Duration'] / total_duration * 100)