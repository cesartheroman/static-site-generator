class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def eq(self, text_node_1, text_node_2):
        print("to do")

    def repr(self):
        return "TextNode(TEXT, TEXT_TYPE, URL)"
