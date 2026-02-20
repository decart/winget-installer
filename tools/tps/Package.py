from typing import TypedDict

package_fields_mapping = {
  "Имя": "name",
  "ИД": "id",
  "Версия": "version",
  "Доступно": "available",
  "Источник": "source",
}


class Package(TypedDict):
  name: str
  id: str
  version: str
  available: str
  source: str