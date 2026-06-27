import subprocess
import sys
import os

if __name__ == "__main__":
    print("Iniciando PU_BOLIVIA_PERPLEXI...")
    ui_path = os.path.join(os.path.dirname(__file__), "app", "ui.py")
    subprocess.run([sys.executable, "-m", "streamlit", "run", ui_path])
