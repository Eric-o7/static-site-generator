
from enum import Enum

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
    return block_type_convert(revised)
    
block_markdown = """
###### heading

This is a **bolded** paragraph

This is another paragraph with *italic* text and `inline code` here
This is the same paragraph on a new line

-testing
-another list

```This is a block of code```

> This is a quote!

1. This is a numbered
2. List

* This is a list
* with items"""
print(markdown_to_blocks(block_markdown))