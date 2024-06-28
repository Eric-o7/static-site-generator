import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "div",
            "hello, world",
            None,
            {"class": "greeting", "href": "https://boot.dev"}
        )
        self.assertEqual(node.props_to_html(),
                         ' class="greeting" href="https://boot.dev"')
        
    def test_to_html(self):
        node = HTMLNode(
            "div",
            ("a", "Click me!", {"href": "https://www.google.com"}),
            None,
            None
        )
        self.assertEqual(LeafNode.to_html(self), '<a href="https://www.google.com">Click me!</a>')

if __name__ == "__main__":
    unittest.main()