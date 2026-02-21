import sys
from PySide6.QtWidgets import QApplication

from winget_installer.ui.MainWindow import MainWindow


def main() -> None:
  app = QApplication(sys.argv)

  main_window = MainWindow()
  main_window.show()

  with open('styles.qss', 'r') as f:
    style = f.read()
    app.setStyleSheet(style)

  sys.exit(app.exec())

if __name__ == "__main__":
  main()