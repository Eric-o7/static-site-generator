import unittest

from textnode import TextNode, Text_Type
from htmlnode import LeafNode
from convert_fun import split_nodes_delimiter, text_node_to_leafhtml_node, extract_md_links, extract_md_img, split_nodes_img

#text node properties: Type, Text=None, Alt=None, URL=None

class TestTextNode(unittest.TestCase):
    def test_text_type(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_url(self):
        node = TextNode("sample text", "underline", "potato.com")
        node2 = TextNode("sample text", "underline", "potato.com")
        self.assertEqual(node, node2)

    def test_text(self):
        node = TextNode("sample text", "italic")
        node2 = TextNode("sample text", "italic")
        self.assertEqual(node, node2)

    def test_same(self):
        node = TextNode("same", "same", "same")
        node2 = TextNode("same", "same", "same")
        self.assertEqual(node, node2)

    




if __name__ == "__main__":
    unittest.main()