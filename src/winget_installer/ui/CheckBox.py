from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Signal, Qt

from winget_installer.packages import PackageState

class CheckBox(QPushButton):
  packageStateChanged = Signal(Qt.CheckState, object)

  def __init__(self, label: str, package: PackageState):
    super().__init__()
    self.package = package
    self.label = label

    self.setFixedHeight(40)
    self.clicked.connect(self.toggleCheckState)
    self.setProperty("class", "package_checkbox")
    self.initUI()

  def initUI(self):
    layout = QHBoxLayout(self)

    self.checkbox = QCheckBox(self.package.package.name)
    self.checkbox.checkStateChanged.connect(self.on_state_changed)
    layout.addWidget(self.checkbox)

    self.subtitle = QLabel(self.package.package.id)
    layout.addWidget(self.subtitle)

  def toggleCheckState(self):
    new_state = Qt.CheckState.Checked if self.checkbox.checkState() == Qt.CheckState.Unchecked else Qt.CheckState.Unchecked
    self.checkbox.setCheckState(new_state)

  def setChecked(self, state: bool):
    self.checkbox.setChecked(state)

  def on_state_changed(self, state: Qt.CheckState):
    self.packageStateChanged.emit(state, self.package)