class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def eq(self, other_node):
        return (
            (self.text == other_node.text)
            and (self.text == other_node.text_type)
            and (self.url == other_node.url)
        )

    def repr(self):
        print(f"TextNode({self.text}, {self.text_type}, {self.url})")
