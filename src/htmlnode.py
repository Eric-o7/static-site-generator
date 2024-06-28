class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        #tag = string representing the HTML tag name
        #value = string representing the value of the HTML tag, text inside p
        #children = list of HTMLNode objects representing the children of the node
        #props = dictionary of key:value pairs representing attributes of the HTML tag

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        result = ""
        for x,y in self.props.items():
            result +=  f' {x}="{y}"'
        return result
    
    def __repr__(self):
        return f"TAG = {self.tag}, VALUE = {self.value}, CHILDREN = {self.children}, PROPS = {self.props}"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        #constructor doesn't allow for children, value and tag now required

    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
    