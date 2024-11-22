import re
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import (
    text_to_textnodes
)
from textnode import (
    text_node_to_html_node
)

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"

# Correction BOOT.DEV
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(markdown):
    regex_order = re.findall(r"^[1-9]\d*\.", markdown)
    regex_header = re.findall(r"^\#{1,6}\s", markdown)
    regex_unorder = re.findall(r"^[*\-]{1}\s", markdown)

    if regex_unorder:
        return "unordered_list"
    elif regex_header:
        return "heading"
    elif markdown.startswith("```") and markdown.endswith("```"):
        return "code"
    elif markdown.startswith(">"):
        return "quote"
    elif regex_order:
        return "ordered_list"
    
    return "paragraph"


def block_type_to_nodes(block, block_type):
    if block_type == block_type_heading:
        c = block.count("#")
        return LeafNode(f"h{c}", block, None)
    elif block_type == block_type_code:
        return ParentNode("pre", [ LeafNode("code", block, None) ])
    elif block_type == block_type_quote:
        return LeafNode("blockquote", block, None)
    elif block_type == block_type_olist:
        return ParentNode("ol", [ LeafNode("li", block, None) ])
    elif block_type == block_type_ulist:
        return ParentNode("ul", [ LeafNode("li", block, None) ])
    elif block_type == block_type_paragraph:
        node_list = []
        nodes = text_to_textnodes(block)
        for node in nodes:
            node_list.append(text_node_to_html_node(node))
        return ParentNode("p", node_list)

def text_to_children(text):
    block_type = block_to_block_type(text)
    htmlnodes = block_type_to_nodes(text, block_type)
    return htmlnodes

def markdown_to_html_node(markdown):
    all_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        children = text_to_children(block)
        all_nodes.append(children)
    
    # final_div = final_div.to_html()
    print(ParentNode("div", all_nodes))
    return ParentNode("div", all_nodes)

# md = """
# ## This is a heading

# Then i have a cool paragraph with lots of text. (not so much but ok)

# * What should i do ?
# * Really, help me

# [Here is a link](https://boot.dev)

# ![Now an image](https://boot.dev)

# *now some italic text*

# **then some bold text**
# """
# markdown_to_html_node(md)