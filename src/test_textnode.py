import unittest

from textnode import TextNode, Text_Type, text_node_to_leafhtml_node, split_nodes_delimiter
from htmlnode import LeafNode

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

    def test_no_value(self):
        text_node = TextNode(Text_Type.no_value, text="Plain text")
        leaf_node = text_node_to_leafhtml_node(text_node)
        self.assertEqual(leaf_node, LeafNode(None, "Plain text"))

    def test_bold(self):
        text_node = TextNode(Text_Type.bold, text="Bold text")
        leaf_node = text_node_to_leafhtml_node(text_node)
        self.assertEqual(leaf_node, LeafNode("b", "Bold text"))

    def test_italic(self):
        text_node = TextNode(Text_Type.italic, "Italic text")
        leaf_node = text_node_to_leafhtml_node(text_node)
        self.assertEqual(leaf_node, LeafNode("i", "Italic text"))
    
    def test_code(self):
        text_node = TextNode(Text_Type.code, "Code text")
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

    def test_text_delim(self):
        node = TextNode(Text_Type.no_value, "This is text with a `code block` word")
        new_nodes = split_nodes_delimiter([node], "`", Text_Type.code)
        expected_nodes = [
            TextNode(Text_Type.no_value, "This is text with a "),
            TextNode(Text_Type.code, "code block"),
            TextNode(Text_Type.no_value, " word")
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_no_delimiters(self):
        node = TextNode(Text_Type.no_value, "This is plain text with no delimiters")
        new_nodes = split_nodes_delimiter([node], "`", Text_Type.code)
        expected_nodes = [TextNode(Text_Type.no_value, "This is plain text with no delimiters")]
        self.assertEqual(new_nodes, expected_nodes)

    def test_simple_bold_text_delim(self):
        node = TextNode(Text_Type.no_value, "This is some **bold** text")
        new_nodes = split_nodes_delimiter([node], "**", Text_Type.bold)
        expected_nodes = [
            TextNode(Text_Type.no_value, "This is some "),
            TextNode(Text_Type.bold, "bold"),
            TextNode(Text_Type.no_value, " text")
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_multiple_inline_elements(self):
        node = TextNode(Text_Type.no_value, "This is `code` and *italic* and **bold** text")
        new_nodes = split_nodes_delimiter([node], "`", Text_Type.code)
        new_nodes = split_nodes_delimiter(new_nodes, "*", Text_Type.italic)
        new_nodes = split_nodes_delimiter(new_nodes, "**", Text_Type.bold)
        expected_nodes = [
            TextNode(Text_Type.no_value, "This is "),
        TextNode(Text_Type.code, "code"),
        TextNode(Text_Type.no_value, " and "),
        TextNode(Text_Type.italic, "italic"),
        TextNode(Text_Type.no_value, " and "),
        TextNode(Text_Type.bold, "bold"),
        TextNode(Text_Type.no_value, " text"),
    ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_no_matching_closing_delimiter(self):
        node = TextNode(Text_Type.no_value, "This is an *italic text with no closing delimiter")
        # This part checks that an exception is raised when the code is executed
        with self.assertRaises(Exception) as context:
            # Call the function that is expected to raise an exception
            split_nodes_delimiter([node], "*", Text_Type.italic)
        # This part checks that the exception contains the expected error message
        self.assertTrue("Invalid markdown syntax, must include matching delimiter" in str(context.exception))

if __name__ == "__main__":
    unittest.main()