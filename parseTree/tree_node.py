import copy


class TreeNode(object):
    def __init__(self, title, children_text, description_dict):
        self.title = title
        self.children_text = children_text # List
        self.description_dict = description_dict
        self.parent = None
        self.children = []
        self.pydot_node = None

    def setParent(self, node):
        self.parent = node
        
    def addChild(self, node):
        self.children.append(node)
        node.setParent(self)
    
    def to_string(self):
        description = ["{} = {}".format(k,v) for k,v in self.description_dict.items()]
        description = "\n".join(description)
        description = description.replace(':', '')
        return self.title + '\n' + description
    
    def to_json(self):
        data = copy.deepcopy(self.description_dict)
        data['Node Type'] = self.title
        data['Children'] = [c.to_json() for c in self.children]
        return data