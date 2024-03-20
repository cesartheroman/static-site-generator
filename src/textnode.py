class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def eq(self, text_node_1, text_node_2):
        return (
            (text_node_1.text == text_node_2.text)
            and (text_node_1.text_type == text_node_2.text_type)
            and (text_node_1.url == text_node_2.url)
        )

    def repr(self):
        return f"TextNode('{self.text}','{self.text_type}', '{self.url}' )"
