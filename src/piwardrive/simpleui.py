class Label:
    def __init__(self, text="", halign="center", valign="middle", **_kwargs):
        self.text = text
        self.halign = halign
        self.valign = valign
        self.text_size = (0, 0)
        self.texture_size = [0, 0]
        self.height = 0

    def bind(self, **_kwargs):
        pass


class Card:
    def __init__(self, orientation="vertical", padding=0, radius=None, **_kwargs):
        self.orientation = orientation
        self.padding = padding
        self.radius = radius or []
        self.children = []

    def add_widget(self, widget):
        self.children.append(widget)


class BoxLayout:
    def __init__(self, **_kwargs):
        self.children = []

    def add_widget(self, widget):
        self.children.append(widget)

    def bind(self, **kwargs):
        for cb in kwargs.values():
            cb(self, None)


class ScrollView:
    def __init__(self, **_kwargs):
        self.width = 0
        self.children = []
        self.scroll_y = 0.0

    def add_widget(self, widget):
        self.children.append(widget)

    def bind(self, **kwargs):
        for cb in kwargs.values():
            cb(self, None)


def dp(val):
    return val


class Image:
    def __init__(self, **_kwargs):
        self.source = ""
        self.size_hint_y = None
        self.height = 0

    def reload(self):
        pass


class DropdownMenu:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def open(self):
        pass

    def dismiss(self):
        pass

