import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        testdict1 = {"href": "https://www.google.com", "target": "_blank"}
        node1 = HTMLNode.props_to_html(testdict1)
        node2 = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node1, node2)

if __name__ == "__main__":
    unittest.main()