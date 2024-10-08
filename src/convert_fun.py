from textnode import Text_Type, TextNode
from htmlnode import HTMLNode,ParentNode,LeafNode
import re

#helper function - splits text nodes into more text nodes based on Markdown syntax
def split_nodes_delimiter(old_nodes, delimiter, type):
    delimited_nodes = [] #create empty list for delimited nodes to append to
    text = old_nodes #create new variable for easier parsing
    delim1_pos = text.find(delimiter) #find first delimiter for slicing
    if delim1_pos == -1:
        delimited_nodes.append(text) #no delimiter found - add node as is
    delim2_pos = text.find(delimiter, delim1_pos + len(delimiter)) #second delim position for slicing
    if delim2_pos == -1:
        raise Exception(f"Invalid markdown syntax, must include matching delimiter")
    #append nodes before, between, and after delim
    if delim1_pos > 0: #if there is text before first delimiter
        delimited_nodes.append(TextNode(Text_Type.no_value, text[:delim1_pos]))
    delimited_nodes.append(TextNode(type, text[delim1_pos + len(delimiter):delim2_pos]))
    if delim2_pos + len(delimiter) < len(text):
        delimited_nodes.append(TextNode(Text_Type.no_value, text[delim2_pos+len(delimiter):]))
    # print(f" MY DELIM NODES{delimited_nodes}")
    return delimited_nodes

#helper function - turns a text node into an HTML leafnode depending on the Text_Type
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
        
#helper function - identifies where an image is in an unformatted text node
def extract_md_img(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

#helper function - identifies where links are in an unformatted text node
def extract_md_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches

#helper function - splits a text node into more text nodes where an image is found
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
    image_slicer(presplit_nodes)
    return split_nodes

# helper function - splits a text node into more text nodes where a link is found
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
    link_slicer(presplit_nodes)
    return split_nodes

#utilizes a lot of helper functions to split an unformatted text node into
#many individual formatted text nodes based on Markdown syntax
def markdown_to_text_nodes(text):
    if isinstance(text, list):
        text = TextNode(Text_Type.no_value, text[0])
    if isinstance(text, ParentNode):
        text = TextNode(Text_Type.no_value, text.children[0])
    if not isinstance(text, TextNode):
        text = TextNode(Text_Type.no_value, text) #converts input to text node for recursive evaluation
    if isinstance(text.text, ParentNode):
        text = TextNode(Text_Type.no_value, text.text.children[0])
    if not text.text:
        return [] #empty list can help integrate into larger pipeline if needed, or could raise exception if I want to enforce requirements
    elif text.text.find("![") != -1:
        nodes = split_nodes_img(text.text) #returns a list of nodes from helper functions
    elif text.text.find("[") != -1:
        nodes = split_nodes_link(text.text)
    elif text.text.find("**") != -1:
        nodes = split_nodes_delimiter(text.text, "**", Text_Type.bold)
    elif text.text.find("*") != -1:
        nodes = split_nodes_delimiter(text.text, "*", Text_Type.italic)
    elif text.text.find("`") != -1:
        nodes = split_nodes_delimiter(text.text, "`", Text_Type.code)
    else:
        return [text] #base case, returns input as a TextNode to be extended onto split_nodes. Must be a list to be extended.
    split_nodes = []
    for node in nodes:
        if isinstance(node, TextNode) and node.type == Text_Type.no_value:
            split_nodes.extend(markdown_to_text_nodes(node))
        else:
            split_nodes.append(node)
    # print(f" MY SPLIT NODES {split_nodes}")    
    # for node in split_nodes:
    #     print(f" MY SPLIT NODES {split_nodes}")  
    #     leaves = []
    #     leaves.append(text_node_to_leafhtml_node(node))
    #     print(leaves)
    # return leaves
    return split_nodes
    
def split_nodes_to_leaf_list(list):
    leaves = []
    for node in list:
        leaves.append(text_node_to_leafhtml_node(node))
    # print(f"MY LEAVES{leaves}")
    return leaves