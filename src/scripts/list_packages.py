import subprocess
import json
from os import makedirs, path
from typing import NotRequired, TypedDict

## === Constants ===

CACHE_FILE = '.tmp/installed_packages.txt'

PACKAGE_FIELDS_MAPPING = {
  "Имя": "name",
  "ИД": "id",
  "Версия": "version",
  "Доступно": "available",
  "Источник": "source",
}

## === Types ===

class Column(TypedDict):
  title: str
  start: int
  end: NotRequired[int]

class Package(TypedDict):
  name: str
  id: str
  version: str
  available: str
  source: str

## === Functions ===

def get_installed_packages():
  makedirs('.tmp', exist_ok=True)
  if (path.exists(CACHE_FILE)):
    return open(CACHE_FILE, 'r', encoding='utf-8').read()

  cmd_result = subprocess.run(['winget', 'list'], stdout=subprocess.PIPE)
  cache = cmd_result.stdout.decode('utf-8')

  open(CACHE_FILE, 'w', encoding='utf-8', newline='\n').write(cache)

  return cache

def find_table_header_index(lines: list[str]):
  for i, line in enumerate(lines):
    if line.startswith("---"):
      return i - 1
  return -1

def get_columns_titles(header_line: str) -> list[Column]:
  columns: list[Column] = []
  i = 0
  while i < len(header_line):
    if header_line[i] != ' ':
      start = i
      while i < len(header_line) and header_line[i] != ' ':
        i += 1

      columns.append({
        'title': header_line[start:i].strip(),
        'start': start,
      })

      if (len(columns) > 1):
        columns[-2]['end'] = start - 1
    else:
      i += 1

  return columns

def get_packages():
  packages_list = get_installed_packages().splitlines()
  header_index = find_table_header_index(packages_list)

  if (header_index == -1):
    print("🔴 Failed to find the table header in the winget list output.")
    exit(1)

  header_line = packages_list[header_index]
  columns = get_columns_titles(header_line)

  packages: dict[str, Package] = {}
  for package in packages_list[header_index + 2:]:
    line = package.strip()
    if line == "":
      continue

    packages_item: Package = {
      'name': '',
      'id': '',
      'version': '',
      'available': '',
      'source': '',
    }

    for column in columns:
      start = column['start']
      end = column.get('end', len(line))

      value = line[start:end].strip()
      package_field = PACKAGE_FIELDS_MAPPING.get(column['title'])

      if (package_field is not None):
        packages_item[package_field] = value

    packages[packages_item['id']] = packages_item

  return packages

## === Main ===

def main():
  packages = [p for p in get_packages().values() if p['source'] == 'winget']
  with open('packages.json', 'w', encoding='utf-8', newline='\n') as f:
    json.dump(packages, f, indent=2, ensure_ascii=False)