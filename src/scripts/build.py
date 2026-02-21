import subprocess, shutil, sys

EXECUTABLE_NAME = "winget-installer"

def main():
  print("Building executable with PyInstaller...")

  shutil.rmtree("dist", ignore_errors=True)
  shutil.rmtree("build", ignore_errors=True)
  subprocess.run([
      sys.executable, "-m", "PyInstaller",
      # "--onefile",
      "--name", EXECUTABLE_NAME,
      "src/winget_installer/__init__.py"
  ], check=True)

  shutil.copy("./packages.json", f"./dist/{EXECUTABLE_NAME}/packages.json")
  shutil.copy("./styles.qss", f"./dist/{EXECUTABLE_NAME}/styles.qss")