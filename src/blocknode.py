
from enum import Enum
from htmlnode import ParentNode
import re
from convert_fun import markdown_to_text_nodes, text_node_to_leafhtml_node
from textnode import Text_Type, TextNode

class Block_Type(Enum):
    paragraph = 1
    heading = 2
    code = 3
    quote = 4
    unordered_list = 5
    ordered_list = 6

class BlockNode():
    def __init__(self, type=None, contents=None):
        self.type = type
        self.contents = contents
        
    def __repr__(self):
        return f"BlockNode(TYPE={self.type}, CONTENTS={self.contents})"

#converts a list of unformatted strings with blocknode 
#Markdown text into BlockNode(s) with appropriate types
def block_type_convert(list):
    converted_types = []
    for block in list:
        if block.startswith("#"):
            converted_types.append(BlockNode(Block_Type.heading, block))
        elif block.startswith("```") and block.endswith('```'):
            converted_types.append(BlockNode(Block_Type.code, block))
        elif block.startswith(">"):
            converted_types.append(BlockNode(Block_Type.quote, block))
        elif block.startswith("*") | block.startswith("-"):
            converted_types.append(BlockNode(Block_Type.unordered_list, block))
        elif block.startswith("1"):
            converted_types.append(BlockNode(Block_Type.ordered_list, block))
        else:
            converted_types.append(BlockNode(Block_Type.paragraph, block))
    return converted_types

#splits incoming text into a list of string and feeds that list into the function above
def markdown_to_blocks(block_text):
    split_new_line =  block_text.split('\n\n')
    revised = []
    for line in split_new_line:
        revised.append(line.strip('\n'))
    return blocknode_to_htmlnode(block_type_convert(revised))

#all of these should be Parent Nodes because the leaf nodes may have more Markdown in them
def blocknode_to_htmlnode(blocknode):
    split_nodes = []
    if isinstance(blocknode, BlockNode):
        blocknode = [blocknode]
    #first we need to make a <div> HTMLNode (Parent) and each child is a separate block
    top_level = ParentNode("div", split_nodes)
    for block in blocknode:
        if block.type == Block_Type.unordered_list:
            split_nodes.append(unordered_list_to_html(block.contents))
        elif block.type == Block_Type.ordered_list:
            split_nodes.append(ordered_list_to_html(block.contents))
        elif block.type == Block_Type.code:
            split_nodes.append(code_to_html(block.contents))
        elif block.type == Block_Type.quote:
            split_nodes.append(quotes_to_html(block.contents))
        elif block.type == Block_Type.heading:
            split_nodes.append(heading_to_html(block.contents))
        else:
            split_nodes.append(ParentNode("p", [block.contents]))
    if top_level.children[0].tag == "h1":
        for child in top_level.children:
            if child.tag == "pre":
                print(child.children[0])
                child.children[0] = ParentNode("code", child_to_leaf((markdown_to_text_nodes(child.children[0]))))
            elif child.tag == "ol" or child.tag == "ul":
                child.children[0] = ParentNode("li", child_to_leaf(markdown_to_text_nodes(child.children[0])))
            else:
                child.children = child_to_leaf(markdown_to_text_nodes(child.children))
        return top_level.to_html()
    else:
        raise Exception (f"all pages need a header")
    
def child_to_leaf(list):
    leaves = []
    for child in list:
        leaves.append(text_node_to_leafhtml_node(child))
    return leaves

#<ul> and <li> are both parent nodes with content as children for further processing
def unordered_list_to_html(blocknode):
    node_list = []
    top_level = ParentNode("ul", node_list)
    for li in re.split("[-*]", blocknode):
        if len(li) >= 2:
            node_list.append(ParentNode("li", [li]))
    #Parentnode <ul> has the <li> children
    return top_level

#<ol> and <li> are both parent nodes with content as children for further processing
def ordered_list_to_html(blocknode):
    node_list = []
    top_level = ParentNode("ol", node_list)
    for li in re.split("(\d+\.)",blocknode):
        if len(li) > 2:
            node_list.append(ParentNode("li", [li]))
    #Parentnode <ol> has the <li> children
    # print(top_level)
    return top_level

#content needs to be surrounded by <blockquote>
def quotes_to_html(blocknode):
    top_level = ParentNode("blockquote", [blocknode.strip(">")])
    return top_level

def code_to_html(blocknode):
    top_level = ParentNode("pre", [(ParentNode("code", [blocknode.strip("`")]))])
    return top_level

#determine the number of # each heading has and then use <h1> - <h6>
def heading_to_html(blocknode):
    sep_head_level = blocknode.split(" ")
    x = 0
    for s in sep_head_level[0]:
        if s == "#":
            x+=1
    if x <= 6:
        top_level = ParentNode(f"h{x}", [blocknode.strip("#")])
        # print(top_level)
        return top_level
    else:
        return ParentNode("p", [blocknode])
    
block_markdown = """
# heading

1. This is a numbered
2. List

This is some **bolded** and *italic* text with `code as well`

"This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)

This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)

```
def code_to_html()
    top_level = ParentNode(what_about, )
    return top_level
```

* This is a list
* with items"""
print(markdown_to_blocks(block_markdown))