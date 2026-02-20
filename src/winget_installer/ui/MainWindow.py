from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

from winget_installer.packages import Package, load_packages
from winget_installer.ui.ListContainer import ListContainer

PACKAGES_FILE = 'packages.json'

class MainWindow(QWidget):
  def __init__(self):
    super().__init__()

    self.packages = sorted(load_packages(PACKAGES_FILE), key=lambda p: p.id)
    self.init_ui()

  def init_ui(self):
    self.setWindowTitle('Winget Installer')
    self.main_layout = QVBoxLayout()
    self.setLayout(self.main_layout)

    self.select = ListContainer(self.packages)
    # self.select.selectionChanged.connect(self.on_selection_changed)
    self.main_layout.addWidget(self.select)

    self.install_button = QPushButton("Install Selected")
    self.install_button.setFixedHeight(64)
    self.install_button.clicked.connect(self.on_install_clicked)
    self.main_layout.addWidget(self.install_button)

  def on_install_clicked(self):
    selected_items = [item.package for item in self.select.list_items if item.selected]
    for item in selected_items:
      print(f"Selected items changed: {item.name}")

  def on_selection_changed(self, selected_items: list[Package]):
    for item in selected_items:
      print(f"Selected items changed: {item.name}")