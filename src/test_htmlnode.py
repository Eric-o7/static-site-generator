import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode
from convert_fun import split_nodes_delimiter, text_node_to_leafhtml_node


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )
        
    def test_to_html_no_children(self):
        node = LeafNode('p','Hello, world!')
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, 'Hello, world!')
        self.assertEqual(node.to_html(), 'Hello, world!')

    def test_children_basic(self):
        node3 = LeafNode("a", "Click me!", {"href": "https://www.github.com"})
        node2 = LeafNode("b", "SO BOLD")
        node1 = ParentNode("p",
                        [node2,
                         node3,
                        ]
                        )
        self.assertEqual(node1.to_html(), '<p><b>SO BOLD</b><a href="https://www.github.com">Click me!</a></p>')

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("i", "spoiled grandchildren :)")
        child_node = ParentNode("p", [grandchild_node])
        parent_node = ParentNode("div",[child_node])
        self.assertEqual(parent_node.to_html(), "<div><p><i>spoiled grandchildren :)</i></p></div>")

if __name__ == "__main__":
    unittest.main()