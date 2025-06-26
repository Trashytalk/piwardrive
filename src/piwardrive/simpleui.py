from __future__ import annotations

from typing import Any, Callable, Iterable


class Label:
    def __init__(
        self, text: str = "", halign: str = "center", valign: str = "middle", **_kwargs: Any
    ) -> None:
        self.text: str = text
        self.halign: str = halign
        self.valign: str = valign
        self.text_size: tuple[int, int] = (0, 0)
        self.texture_size: list[int] = [0, 0]
        self.height: int = 0

    def bind(self, **_kwargs: Callable[[Any, Any], None]) -> None:
        pass


class Card:
    def __init__(
        self,
        orientation: str = "vertical",
        padding: int | float = 0,
        radius: Iterable[int] | None = None,
        **_kwargs: Any,
    ) -> None:
        self.orientation: str = orientation
        self.padding: int | float = padding
        self.radius: list[int] = list(radius or [])
        self.children: list[Any] = []

    def add_widget(self, widget: Any) -> None:
        self.children.append(widget)


class BoxLayout:
    def __init__(self, **_kwargs: Any) -> None:
        self.children: list[Any] = []

    def add_widget(self, widget: Any) -> None:
        self.children.append(widget)

    def bind(self, **kwargs: Callable[[Any, Any], None]) -> None:
        for cb in kwargs.values():
            cb(self, None)


class ScrollView:
    def __init__(self, **_kwargs: Any) -> None:
        self.width: int = 0
        self.children: list[Any] = []
        self.scroll_y: float = 0.0

    def add_widget(self, widget: Any) -> None:
        self.children.append(widget)

    def bind(self, **kwargs: Callable[[Any, Any], None]) -> None:
        for cb in kwargs.values():
            cb(self, None)


def dp(val: int | float) -> int | float:
    return val


class Image:
    def __init__(self, **_kwargs: Any) -> None:
        self.source: str = ""
        self.size_hint_y: float | None = None
        self.height: int = 0

    def reload(self) -> None:
        pass


class DropdownMenu:
    def __init__(self, **kwargs: Any) -> None:
        self.kwargs: dict[str, Any] = kwargs

    def open(self) -> None:
        pass

    def dismiss(self) -> None:
        pass
