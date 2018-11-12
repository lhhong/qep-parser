class TreeNode(object):
    def __init__(self, title, val, description):
        self.title = title
        self.val = val
        self.description = description
        self.parent = None
        self.children = []
        self.pydot_node = None

    def setParent(self, node):
        self.parent = node
        
    def addChild(self, node):
        self.children.append(node)
        node.setParent(self)
    
    def to_string(self):
        return self.title + '\n' + self.description
