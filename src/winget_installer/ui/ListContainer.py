from PySide6.QtWidgets import QScrollArea, QWidget, QVBoxLayout
from PySide6.QtCore import Qt, Signal

from winget_installer.packages import Package, PackageState
from winget_installer.ui.CheckBox import CheckBox 

class ListContainer(QScrollArea):
  selectionChanged = Signal(list)

  def __init__(self, items: list[Package] | None = None, parent:QWidget | None = None):
    super(ListContainer, self).__init__(parent)
    self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
    self.setWidgetResizable(True)

    self.list_items = [PackageState(item) for item in (items if items else [])]
    self.list_checkboxes: list[CheckBox] = []

    self.init_ui()
    self.setProperty("class", "package_list")

  def init_ui(self):
    container = QWidget()
    self.setWidget(container)

    layout = QVBoxLayout(container)
    layout.setSpacing(0)
    for idx, item in enumerate(self.list_items):
      self.list_checkboxes.append(CheckBox(f"{item.package.name} [{item.package.id}]", item))
      self.list_checkboxes[idx].packageStateChanged.connect(self.on_state_changed)
      self.list_checkboxes[idx].setChecked(False)
      self.list_checkboxes[idx].setProperty('isEven', idx % 2 == 0)

      layout.addWidget(self.list_checkboxes[-1])

  def on_state_changed(self, state: Qt.CheckState, item: PackageState):
    item.selected = state == Qt.CheckState.Checked
    self.selectionChanged.emit([item.package for item in self.list_items if item.selected])