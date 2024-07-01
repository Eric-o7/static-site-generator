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
