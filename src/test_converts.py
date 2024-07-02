import unittest

from textnode import TextNode, Text_Type
from htmlnode import LeafNode
from convert_fun import split_nodes_delimiter, split_nodes_link, text_node_to_leafhtml_node, extract_md_links, extract_md_img, split_nodes_img

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

class TestImgAndLinkSplit(unittest.TestCase):
    def test_single_textnode_with_one_image(self):
        node = TextNode(
            Text_Type.no_value,
            "This is text with an ![image](https://example.com/image1.png)"
        )
        result = split_nodes_img(node)
        expected = [
            TextNode(Text_Type.no_value, "This is text with an "),
            TextNode(Text_Type.image, None, "image", "https://example.com/image1.png")
        ]
        self.assertEqual(result, expected, "not equal")

    def test_single_textnode_with_multiple_images(self):
        node = TextNode(
            Text_Type.no_value,
            "Text with ![first](https://example.com/first.png) and ![second](https://example.com/second.png)"
        )
        result = split_nodes_img([node])
        expected = [
            TextNode(Text_Type.no_value, "Text with "),
            TextNode(Text_Type.image, None, "first", "https://example.com/first.png"),
            TextNode(Text_Type.no_value, " and "),
            TextNode(Text_Type.image, None, "second", "https://example.com/second.png")
        ]
        self.assertEqual(result, expected)

    def test_single_textnode_with_no_images(self):
        node = TextNode(
            Text_Type.no_value,
            "This is text with no images"
        )
        result = split_nodes_img([node])
        expected = [node]  # Since there's no image, the input should be the same as output.
        self.assertEqual(result, expected)

    def test_images_at_start_and_end(self):
        node = TextNode(
            Text_Type.no_value,
            "![start](https://example.com/start.png) Text in the middle ![end](https://example.com/end.png)"
        )
        result = split_nodes_img([node])
        expected = [
            TextNode(Text_Type.image, None, "start", "https://example.com/start.png"),
            TextNode(Text_Type.no_value, " Text in the middle "),
            TextNode(Text_Type.image, None, "end", "https://example.com/end.png")
        ]
        self.assertEqual(result, expected)

    def test_only_an_image(self):
        node = TextNode(
            Text_Type.no_value,
            "![only](https://example.com/only.png)"
        )
        result = split_nodes_img([node])
        expected = [
            TextNode(Text_Type.image, None, "only", "https://example.com/only.png")
        ]
        self.assertEqual(result, expected)

    def test_single_textnode_with_one_link(self):
        node = TextNode(
            Text_Type.no_value,
            "This is text with a [link](https://example.com)"
        )
        result = split_nodes_link([node])
        expected = [
            TextNode(Text_Type.no_value, "This is text with a "),
            TextNode(Text_Type.link, "link", None, "https://example.com")
        ]
        self.assertEqual(result, expected)

    def test_single_textnode_with_only_link(self):
        node = TextNode(
            Text_Type.no_value,
            "[link](https://example.com)"
        )
        result = split_nodes_link([node])
        expected = [
            TextNode(Text_Type.link, "link", None, "https://example.com")
        ]
        self.assertEqual(result, expected)

    def test_single_textnode_with_only_links(self):
        node = TextNode(
            Text_Type.no_value,
            "[link](https://example.com)[link2](www.link2.com)"
        )
        result = split_nodes_link([node])
        expected = [
            TextNode(Text_Type.link, "link", None, "https://example.com"),
            TextNode(Text_Type.link, "link2", None, "www.link2.com")
        ]
        self.assertEqual(result, expected)
    

if __name__ == "__main__":
    unittest.main()