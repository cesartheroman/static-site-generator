class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag  # string rep of html tag name
        self.value = value  # string rep of html val
        self.children = children  # list of HTMLNode objs
        self.props = props  # a dictionary of of key-val pairs repping the html attrs

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""

        result = []
        for key, val in self.props.items():
            result.append(f'{key}="{val}"')

        return " ".join(result)

    def __repr__(self):
        return f"{self.tag}, {self.value}, {self.children}, {self.props}"
