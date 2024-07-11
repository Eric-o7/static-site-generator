
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
        elif block.startswith("* ") | block.startswith("- "):
            converted_types.append(BlockNode(Block_Type.unordered_list, block))
        elif block.startswith("1"):
            converted_types.append(BlockNode(Block_Type.ordered_list, block))
        else:
            converted_types.append(BlockNode(Block_Type.paragraph, block))
    # print(converted_types)
    return converted_types

#splits incoming text into a list of string and feeds that list into the function above
def markdown_to_blocks(block_text):
    split_new_line =  block_text.split('\n\n')
    revised = []
    for line in split_new_line:
        revised.append(line.strip('\n'))
    # print(revised)
    return blocknode_to_htmlnode(block_type_convert(revised))

#all of these should be Parent Nodes because the leaf nodes may have more Markdown in them
def blocknode_to_htmlnode(blocknode):
    split_nodes = []
    # print(blocknode)
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
                # print(child.children[0])
                child.children[0] = ParentNode("code", child_to_leaf((markdown_to_text_nodes(child.children[0]))))
            elif child.tag == "ol" or child.tag == "ul":
                for i in range(len(child.children)):
                    old_child = child.children[i]
                    new_child = ParentNode("li", child_to_leaf(markdown_to_text_nodes(old_child.children)))
                    child.children[i] = new_child
            else:
                child.children = child_to_leaf(markdown_to_text_nodes(child.children))
        # print(top_level)
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
    # print(blocknode)
    top_level = ParentNode("ul", node_list)
    for li in re.split("-\s|\* ", blocknode):
        if len(li) >= 2:
            node_list.append(ParentNode("li", [li.strip()]))
    #Parentnode <ul> has the <li> children
    return top_level

#<ol> and <li> are both parent nodes with content as children for further processing
def ordered_list_to_html(blocknode):
    node_list = []
    top_level = ParentNode("ol", node_list)
    for li in re.split("(\d+\.)",blocknode):
        if len(li) > 2:
            node_list.append(ParentNode("li", [li.strip()]))
    #Parentnode <ol> has the <li> children
    # print(top_level)
    return top_level

#content needs to be surrounded by <blockquote>
def quotes_to_html(blocknode):
    top_level = ParentNode("blockquote", [blocknode.strip("> ")])
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
        no_space = blocknode.lstrip()
        top_level = ParentNode(f"h{x}", [no_space.strip("# ")])
        return top_level
    else:
        return ParentNode("p", [blocknode])
    
# block_markdown = """
# # The Unparalleled Majesty of "The Lord of the Rings"

# [Back Home](/)

# ![LOTR image artistmonkeys](/images/rivendell.png)

# > "I cordially dislike allegory in all its manifestations, and always have done so since I grew old and wary enough to detect its presence.
# > I much prefer history, true or feigned, with its varied applicability to the thought and experience of readers.
# > I think that many confuse 'applicability' with 'allegory'; but the one resides in the freedom of the reader, and the other in the purposed domination of the author."

# In the annals of fantasy literature and the broader realm of creative world-building, few sagas can rival the intricate tapestry woven by J.R.R. Tolkien in *The Lord of the Rings*. You can find the [wiki here](https://lotr.fandom.com/wiki/Main_Page).

# ## Introduction

# This series, a cornerstone of what I, in my many years as an **Archmage**, have come to recognize as the pinnacle of imaginative creation, stands unrivaled in its depth, complexity, and the sheer scope of its *legendarium*. As we embark on this exploration, let us delve into the reasons why this monumental work is celebrated as the finest in the world.

# ## A Rich Tapestry of Lore

# One cannot simply discuss *The Lord of the Rings* without acknowledging the bedrock upon which it stands: **The Silmarillion**. This compendium of mythopoeic tales sets the stage for Middle-earth's history, from the creation myth of Eä to the epic sagas of the Elder Days. It is a testament to Tolkien's unparalleled skill as a linguist and myth-maker, crafting:

# 1. An elaborate pantheon of deities (the `Valar` and `Maiar`)
# 2. The tragic saga of the Noldor Elves
# 3. The rise and fall of great kingdoms such as Gondolin and Númenor

# ```
# print("Lord")
# print("of")
# print("the")
# print("Rings")
# ```

# ## The Art of **World-Building**

# ### Crafting Middle-earth

# Tolkien's Middle-earth is a realm of breathtaking diversity and realism, brought to life by his meticulous attention to detail. This world is characterized by:

# - **Diverse Cultures and Languages**: Each race, from the noble Elves to the sturdy Dwarves, is endowed with its own rich history, customs, and language. Tolkien, leveraging his expertise in philology, constructed languages such as Quenya and Sindarin, each with its own grammar and lexicon.
# - **Geographical Realism**: The landscape of Middle-earth, from the Shire's pastoral hills to the shadowy depths of Mordor, is depicted with such vividness that it feels as tangible as our own world.
# - **Historical Depth**: The legendarium is imbued with a sense of history, with ruins, artifacts, and lore that hint at bygone eras, giving the world a lived-in, authentic feel.

# ## Themes of *Timeless* Relevance

# ### The *Struggle* of Good vs. Evil

# At its heart, *The Lord of the Rings* is a timeless narrative of the perennial struggle between light and darkness, a theme that resonates deeply with the human experience. The saga explores:

# - The resilience of the human (and hobbit) spirit in the face of overwhelming odds
# - The corrupting influence of power, epitomized by the One Ring
# - The importance of friendship, loyalty, and sacrifice

# These universal themes lend the series a profound philosophical depth, making it a beacon of wisdom and insight for generations of readers.

# ## A Legacy **Unmatched**

# ### The Influence on Modern Fantasy

# The shadow that *The Lord of the Rings* casts over the fantasy genre is both vast and deep, having inspired countless authors, artists, and filmmakers. Its legacy is evident in:

# - The archetypal "hero's journey" that has become a staple of fantasy narratives
# - The trope of the "fellowship," a diverse group banding together to face a common foe
# - The concept of a richly detailed fantasy world, which has become a benchmark for the genre

# ## Conclusion

# As we stand at the threshold of this mystical realm, it is clear that *The Lord of the Rings* is not merely a series but a gateway to a world that continues to enchant and inspire. It is a beacon of imagination, a wellspring of wisdom, and a testament to the power of myth. In the grand tapestry of fantasy literature, Tolkien's masterpiece is the gleaming jewel in the crown, unmatched in its majesty and enduring in its legacy. As an Archmage who has traversed the myriad realms of magic and lore, I declare with utmost conviction: *The Lord of the Rings* reigns supreme as the greatest legendarium our world has ever known.

# Splendid! Then we have an accord: in the realm of fantasy and beyond, Tolkien's creation is unparalleled, a treasure trove of wisdom, wonder, and the indomitable spirit of adventure that dwells within us all.

# """
# print(markdown_to_blocks(block_markdown))