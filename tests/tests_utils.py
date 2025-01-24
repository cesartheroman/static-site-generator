import unittest

from src.utils import extract_title


class TestUtils(unittest.TestCase):
    def test_util(self):
        md = """
## This is a second header

#  This is a header

this is a regular paragraph
"""
        actual = extract_title(md)
        expected = "This is a header"
        self.assertEqual(
            actual, expected, f"Expected: {expected} to equal actual: {actual}"
        )

    def test_exception_handling(self):
        md = "hi there"
        with self.assertRaises(Exception) as context:
            extract_title(md)

            self.assertEqual(
                str(context.exception),
                "No header!",
                f"Expected 'No header!' to equal actual: {str(context.exception)}",
            )

    def test_edgecase(self):
        md = """
## This is a second header

# Tricky # Tricky

this is a regular paragraph
"""
        actual = extract_title(md)
        expected = "Tricky # Tricky"
        self.assertEqual(
            actual, expected, f"Expected: {expected} to equal actual: {actual}"
        )


if __name__ == "__main__":
    unittest.main()
