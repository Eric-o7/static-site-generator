import unittest

from textnode import TextNode

#goal is to fail 3/4 tests to make sure each object property is correctly evaluated
class TestTextNode(unittest.TestCase):
    def test_text_type(self):
        node = TextNode("This is a text node", "italic")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_url(self):
        node = TextNode("sample text", "underline", None)
        node2 = TextNode("sample text", "underline", "potato.com")
        self.assertEqual(node, node2)

    def test_text(self):
        node = TextNode("sample text", "italic")
        node2 = TextNode("sampler text", "italic")
        self.assertEqual(node, node2)

    def test_same(self):
        node = TextNode("same", "same", "same")
        node2 = TextNode("same", "same", "same")
        self.assertEqual(node, node2)



if __name__ == "__main__":
    unittest.main()