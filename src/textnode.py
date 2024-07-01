from enum import Enum
from htmlnode import LeafNode

class Text_Type(Enum):
    no_value = 1
    bold = 2
    italic = 3
    code = 4
    link = 5
    image = 6

class TextNode():
    def __init__(self,  type, text=None, alt=None, url=None):
        self.text = text
        self.type = type
        self.url = url
        self.alt = alt

    def __eq__(self, other):
        return (
            self.type == other.type
            and self.text == other.text
            and self.url == other.url
            and self.alt == other.alt
        )
    
    def __repr__(self):
        return f"TextNode(TEXT = {self.text}, TEXT_TYPE = {self.type}, URL = {self.url}), ALT = {self.alt}"



def split_nodes_delimiter(old_nodes, delimiter, type):
    delimited_nodes = [] #create empty list for delimited nodes to append to
    for node in old_nodes:
        if not isinstance(node, TextNode):
            delimited_nodes.append(node)
            continue
        text = node.text #create new variable for easier parsing
        delim1_pos = text.find(delimiter) #find first delimiter for slicing
        if delim1_pos == -1:
            delimited_nodes.append(node)
            continue #no delimiter found - add node as is
        delim2_pos = text.find(delimiter, delim1_pos + len(delimiter)) #second delim position for slicing
        if delim2_pos == -1:
            raise Exception(f"Invalid markdown syntax, must include matching delimiter")
        #append nodes before, between, and after delim
        if delim1_pos > 0: #if there is text before first delimiter
            delimited_nodes.append(TextNode(Text_Type.no_value, text[:delim1_pos]))
        delimited_nodes.append(TextNode(type, text[delim1_pos + len(delimiter):delim2_pos]))
        if delim2_pos + len(delimiter) < len(text):
            delimited_nodes.append(TextNode(Text_Type.no_value, text[delim2_pos+len(delimiter):]))

    return delimited_nodes

    

def text_node_to_leafhtml_node(text_node):
    match text_node.type:
        case Text_Type.no_value:
            return LeafNode(None, text_node.text)
        case Text_Type.bold:
            return LeafNode("b", text_node.text)
        case Text_Type.italic:
            return LeafNode("i", text_node.text)
        case Text_Type.code:
            return LeafNode("code", text_node.text)
        case Text_Type.link:
            if text_node.url is None:
                raise ValueError(f"URL is required for link")
            return LeafNode("a", text_node.text, props={"href": text_node.url})
        case Text_Type.image:
            if text_node.url is None or text_node.alt is None:
                raise ValueError(f"URL and Alt text needed for image")
            return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.alt})
        case _:
            raise Exception(f"Invalid type")
