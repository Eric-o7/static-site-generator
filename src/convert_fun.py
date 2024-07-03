from textnode import Text_Type, TextNode
from htmlnode import HTMLNode,ParentNode,LeafNode
import re

def split_nodes_delimiter(old_nodes, delimiter, type):
    delimited_nodes = [] #create empty list for delimited nodes to append to
    text = old_nodes #create new variable for easier parsing
    delim1_pos = text.find(delimiter) #find first delimiter for slicing
    if delim1_pos == -1:
        delimited_nodes.append(node) #no delimiter found - add node as is
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
    image_slicer(presplit_nodes)
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
    link_slicer(presplit_nodes)
    return split_nodes


def markdown_to_text_nodes(text):
    if not isinstance(text, TextNode):
        text = TextNode(Text_Type.no_value, text) #converts input to text node for recursive evaluation
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
        
    return split_nodes
   
   
def markdown_to_blocks(markdown):
    lines =  markdown.splitlines()
    revised_blocks = []
    unordered_list = []
    for block in lines:
        if len(block) >= 2:
            revised_blocks.append(block)      
    for i in range(0,len(revised_blocks)):
        if revised_blocks[i].startswith("*"):
            unordered_list.append(i)
    revised_blocks[unordered_list[0]:unordered_list[-1]+1] = [' '.join(revised_blocks[unordered_list[0]:unordered_list[-1]+1])]
    return revised_blocks


block_markdown = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items"""
print(markdown_to_blocks(block_markdown))