class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self is None:
            return ""
        result = ""
        for x,y in self.items():
            join = f' {x}="{y}"'
            result += join
        return result
    
    def __repr__(self):
        return f"TAG = {self.tag}, VALUE = {self.value}, CHILDREN = {self.children}, PROPS = {self.props}"
    
class LeafNode(HTMLNode):
    def __init__(self):
        super().__init__()

    def to_html(self):
        if self.tag is None:
            return 
    