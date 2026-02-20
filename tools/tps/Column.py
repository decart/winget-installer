from typing import NotRequired, TypedDict

class Column(TypedDict):
  title: str
  start: int
  end: NotRequired[int]