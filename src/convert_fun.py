from textnode import Text_Type, TextNode
from htmlnode import HTMLNode,ParentNode,LeafNode
import re

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
        

def extract_md_img(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_md_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_img(presplit_nodes):
    split_nodes = []
    def image_slicer(text):
        if len(text) <=3:
            return
        before_img = text.find("![")
        if before_img == -1:
            if len(text.strip()) > 0:
                split_nodes.append(TextNode(Text_Type.no_value, text))
            return
        if before_img != -1:
            if len(text[:before_img].strip()) > 0:
                split_nodes.append(TextNode(Text_Type.no_value, text[:before_img]))
        post_image_sep = text.find(')')
        image_tup = extract_md_img(text[before_img : post_image_sep +1])
        split_nodes.append(TextNode(Text_Type.image, None, image_tup[0][0], image_tup[0][1]))
        next_img = text.find('![', post_image_sep)
        if next_img == -1:
            if len(text[post_image_sep:]) >= 2:
                split_nodes.append(TextNode(Text_Type.no_value, text[post_image_sep+1:]))
        if next_img != -1:    
            if len(text[post_image_sep:next_img]) >=2:
                split_nodes.append(TextNode(Text_Type.no_value, text[post_image_sep+1:next_img]))
            return image_slicer(text[next_img:])
        return
    if isinstance(presplit_nodes, TextNode):
        presplit_nodes = [presplit_nodes]    
    for node in presplit_nodes:
        if len(node.text) <=1:
            continue 
        image_slicer(node.text)
    return split_nodes


def split_nodes_link(presplit_nodes):
    split_nodes = []
    def link_slicer(text):
        if len(text) <=3:
            return
        before_lnk = text.find("[")
        if before_lnk == -1:
            if len(text.strip()) > 0:
                split_nodes.append(TextNode(Text_Type.no_value, text))
            return
        if before_lnk != -1:
            if len(text[:before_lnk].strip()) > 0:
                split_nodes.append(TextNode(Text_Type.no_value, text[:before_lnk]))
        post_link_sep = text.find(')')
        link_tup = extract_md_links(text[before_lnk : post_link_sep +1])
        split_nodes.append(TextNode(Text_Type.link, link_tup[0][0], None, link_tup[0][1]))
        next_link = text.find('[', post_link_sep)
        if next_link == -1:
            if len(text[post_link_sep:]) >= 2:
                split_nodes.append(TextNode(Text_Type.no_value, text[post_link_sep+1:]))
        if next_link != -1:    
            if len(text[post_link_sep:next_link]) >=2:
                split_nodes.append(TextNode(Text_Type.no_value, text[post_link_sep+1:next_link]))
            return link_slicer(text[next_link:])
        return

    if isinstance(presplit_nodes, TextNode):
        presplit_nodes = [presplit_nodes]    
    for node in presplit_nodes:
        if len(node.text) <=1:
            continue 
        link_slicer(node.text)
    return split_nodes
    
node = [
    TextNode(Text_Type.no_value, "Text without link"),
    TextNode(Text_Type.no_value, "Text with a [link](https://example.com/image1.png) inside it [and another](link.com) plus one more [linky](poop.org) inside the text")
]
split_nodes_link(node)
   