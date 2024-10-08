import unittest

from textnode import TextNode, Text_Type
from htmlnode import LeafNode
from convert_fun import split_nodes_delimiter, text_node_to_leafhtml_node, extract_md_links, extract_md_img

class TestTexttoLeaf(unittest.TestCase):
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

class TestNodeDelimSplit(unittest.TestCase):
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

class TestExtractionMethods(unittest.TestCase):
    def test_extract_img(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        conversion = [('image', 'https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png'), ('another', 'https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png')]
        self.assertEqual(extract_md_img(text), conversion)

    def test_extract_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        conversion = [('link', 'https://www.example.com'), ('another', 'https://www.example.com/another')]
        self.assertEqual(extract_md_links(text), conversion)

class TestMarkdownToText(unittest.TestCase):
    #tested on convert_fun.py by comparing expected result to system output
    pass


if __name__ == "__main__":
    unittest.main()