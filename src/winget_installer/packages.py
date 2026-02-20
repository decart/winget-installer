import json
from typing import cast

class Package:
  def __init__(self, name: str, id: str, version: str, available: str, source: str):
    self.name = name
    self.id = id
    self.version = version
    self.available = available
    self.source = source

def load_packages(file_path: str):
  with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f, object_hook=lambda d: Package(**d))
    return cast(list[Package], data)

class PackageState():
  def __init__(self, package: Package):
    self.package = package
    self.selected = False