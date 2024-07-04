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
        #utilize polymorphism to call the correct to_html method on the appropriate node
    
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

#LeafNode method that formats a string of text into an HTML Node based on the tag
#uses HTMLNode props_to_html() method to format props appropriately
    def to_html(self):
        if self.value is None:
            raise ValueError(f"Invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __eq__(self, other):
        if not isinstance(other, LeafNode):
            return False
        return(
            self.tag == other.tag and
            self.value == other.value and
            self.props == other.props
        )
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        #constructor doesn't take a value arg, and children arg not optional


#recursively formats a Parent node and its children.
#treats input as a tree structure with unknown width and depth
    def to_html(self):
        if self.tag is None:
            raise ValueError(f"Invalid HTML: Tag is needed")
        if self.children is None:
            raise ValueError(f"Invalid HTML: Childless")
        listed = [f"<{self.tag}>"]
        for child in self.children:
            listed.append(child.to_html())
            #child.to_html() will call the appropriate Class to_html() method
            #this is considered recursion - LeafNode.to_html() is the base case
            #polymorphism in action
        listed.append(f"</{self.tag}>")
        return "".join(listed)

        
    