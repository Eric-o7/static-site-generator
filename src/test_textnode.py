import unittest

from textnode import TextNode, Text_Type, text_node_to_leafhtml_node
from htmlnode import LeafNode

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

    def test_no_value(self):
        text_node = TextNode(Text_Type.no_value, text="Plain text")
        leaf_node = text_node_to_leafhtml_node(text_node)
        self.assertEqual(leaf_node, LeafNode(None, "Plain text"))

    def test_bold(self):
        text_node = TextNode(Text_Type.bold, text="Bold text")
        leaf_node = text_node_to_leafhtml_node(text_node)
        self.assertEqual(leaf_node, LeafNode("b", "Bold text"))

    def test_italic(self):
        text_node = TextNode(Text_Type.italic, text="Italic text")
        leaf_node = text_node_to_leafhtml_node(text_node)
        self.assertEqual(leaf_node, LeafNode("i", "Italic text"))
    
    def test_code(self):
        text_node = TextNode(Text_Type.code, text="Code text")
        leaf_node = text_node_to_leafhtml_node(text_node)
        self.assertEqual(leaf_node, LeafNode("code", "Code text"))

    def test_link(self):
        text_node = TextNode(Text_Type.link, text="Click here", url="https://example.com")
        leaf_node = text_node_to_leafhtml_node(text_node)
        self.assertEqual(leaf_node, LeafNode("a", "Click here", props={"href": "https://example.com"}))

    def test_image(self):
        text_node = TextNode(Text_Type.image, url="https://example.com/image.png", alt="An image")
        leaf_node = text_node_to_leafhtml_node(text_node)
        self.assertEqual(leaf_node, LeafNode("img", "", props={"src": "https://example.com/image.png", "alt": "An image"}))


if __name__ == "__main__":
    unittest.main()