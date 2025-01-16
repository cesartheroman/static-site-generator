import unittest

from src.block_markdown import (
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)
from src.htmlnode import HTMLNode, LeafNode, ParentNode


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        raw_markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        actual = markdown_to_blocks(raw_markdown)
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
        ]
        self.assertListEqual(
            actual, expected, f"Expected: {expected} to equal actual: {actual}"
        )

    def test_markdown_to_blocks_newlines(self):
        raw_markdown = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        actual = markdown_to_blocks(raw_markdown)
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items",
        ]
        self.assertListEqual(
            actual, expected, f"Expected: {expected} to be equal to actual: {actual}"
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_basic_heading(self):
        raw_markdown = "# A basic heading"
        actual = block_to_block_type(raw_markdown)
        expected = "heading"
        self.assertEqual(
            actual, expected, f"Expected: {expected} to be equal to actual: {actual}"
        )

    def test_multilevel_heading(self):
        headings = [
            ("## Level Two Heading", "heading"),
            ("### Level Three Heading", "heading"),
        ]
        for raw_markdown, expected in headings:
            with self.subTest(raw_markdown=raw_markdown):
                actual = block_to_block_type(raw_markdown)
                self.assertEqual(
                    actual,
                    expected,
                    f"Expected: {expected} to be equal to actual: {actual}",
                )

    def test_heading_no_space(self):
        md = "##Heading without space"
        actual = block_to_block_type(md)
        expected = "paragraph"
        self.assertEqual(
            actual,
            expected,
            f"Expected: {expected} to be equal to actual: {actual}",
        )

    def test_non_heading_block(self):
        md = "This is a regular paragraph"
        actual = block_to_block_type(md)
        expected = "paragraph"
        self.assertEqual(
            actual,
            expected,
            f"Expected: {expected} to be equal to actual: {actual}",
        )

    def test_excessive_hashes(self):
        md = "####### Too many hashes"
        actual = block_to_block_type(md)
        expected = "paragraph"
        self.assertEqual(
            actual,
            expected,
            f"Expected: {expected} to be equal to actual: {actual}",
        )

    def test_code_block(self):
        md = "```let test = 10```"
        actual = block_to_block_type(md)
        expected = "code"
        self.assertEqual(
            actual, expected, f"Expected: {expected} to be equal to actual: {actual}"
        )

    def test_code_missing_backticks(self):
        headings = [
            ("``` let test = 10", "paragraph"),
            ("``` code block with one missing backtick``", "paragraph"),
        ]
        for raw_markdown, expected in headings:
            with self.subTest(raw_markdown=raw_markdown):
                actual = block_to_block_type(raw_markdown)
                self.assertEqual(
                    actual,
                    expected,
                    f"Expected: {expected} to be equal to actual: {actual}",
                )

    def test_quote_block(self):
        headings = [
            (">This is a quote\n>Second line of it\n>Last line of quote", "quote"),
            (">This is almost a quote\n Second line", "paragraph"),
        ]
        for raw_markdown, expected in headings:
            with self.subTest(raw_markdown=raw_markdown):
                actual = block_to_block_type(raw_markdown)
                self.assertEqual(
                    actual,
                    expected,
                    f"Expected: {expected} to be equal to actual: {actual}",
                )

    def test_unordered_list_block(self):
        headings = [
            ("* This is the first item\n* Second item\n* and third", "unordered_list"),
            (
                "- This is the first item\n- Second item\n- and third just with dashes",
                "unordered_list",
            ),
            (
                "* How about a list\n- that has a mix of asterisk\n- and dashes",
                "unordered_list",
            ),
            (
                "*This is the first item\n*But this won't work because no space after *",
                "paragraph",
            ),
            (
                "-This is the first item\n-But this won't work because no space after -",
                "paragraph",
            ),
        ]
        for raw_markdown, expected in headings:
            with self.subTest(raw_markdown=raw_markdown):
                actual = block_to_block_type(raw_markdown)
                self.assertEqual(
                    actual,
                    expected,
                    f"Expected: {expected} to be equal to actual: {actual}",
                )

    def test_ordered_list_block(self):
        headings = [
            ("1. This is first item\n2. This is second\n3. and third", "ordered_list"),
            ("1. This is first item\n1. This is first\n1. and first", "paragraph"),
            (
                "1. This is first item\n2.This is second with no space after .\n3. and third",
                "paragraph",
            ),
        ]
        for raw_markdown, expected in headings:
            with self.subTest(raw_markdown=raw_markdown):
                actual = block_to_block_type(raw_markdown)
                self.assertEqual(
                    actual,
                    expected,
                    f"Expected: {expected} to be equal to actual: {actual}",
                )


class TestMarkdownToHtmlNodes(unittest.TestCase):
    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""
        actual = markdown_to_html_node(md)
        expected = (
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>"
        )
        self.assertEqual(
            actual.to_html(),
            expected,
            f"Expected: {expected} to equal to actual: {actual}",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here


This is another paragraph with *italic* text and `code` here

"""
        actual = markdown_to_html_node(md)
        expected = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        self.assertEqual(
            actual.to_html(),
            expected,
            f"Expected: {expected} to equal to actual: {actual}",
        )

    # test lists(ordered and unordered), headings, blocquotes
    def test_lists(self):
        md = """
- This is a list
- with a couple of
- *different* items that might have inline styles

1. This is an `ordered` list
2. With a couple of items
3. and some other items

"""
        actual = markdown_to_html_node(md)
        expected = "<div><ul><li>This is a list</li><li>with a couple of</li><li><i>different</i> items that might have inline styles</li></ul><ol><li>This is an <code>ordered</code> list</li><li>With a couple of items</li><li>and some other items</li></ol></div>"

        self.assertEqual(
            actual.to_html(),
            expected,
            f"Expected: {expected} to be equal to actual: {actual}",
        )


#     def test_multi_block_type(self):
#         md = """
# # This is a header
#
# This is a regular paragraph
#
# - List item 1
# - List item 2
#
# *this is in italics*
# **this is in bold**
#         """
#         actual = markdown_to_html_node(md)
#         expected = ParentNode(
#             "div",
#             [
#                 LeafNode("h1", "This is a header"),
#                 LeafNode("p", "This is a regular paragraph"),
#                 ParentNode(
#                     "ul", [LeafNode("li", "List item 1"), LeafNode("li", "List item 2")]
#                 ),
#                 LeafNode("i", "this is in italics"),
#                 LeafNode("b", "this is in bold"),
#             ],
#         )
#         self.assertEqual(
#             actual,
#             expected.to_html(),
#             f"Expected: {expected.to_html()} to be equal to actual: {actual.to_html}",
#         )


if __name__ == "__main__":
    unittest.main()
