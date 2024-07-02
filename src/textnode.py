from enum import Enum
from htmlnode import LeafNode, ParentNode, HTMLNode

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
        return f"TextNode(TEXT = {self.text}, TEXT_TYPE = {self.type}, URL = {self.url}, ALT = {self.alt})"
