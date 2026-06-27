import subprocess, sys, os
if __name__ == "__main__":
    print("Iniciando PU_BOLIVIA_PERPLEXI...")
    ui = os.path.join(os.path.dirname(__file__), "app", "ui.py")
    subprocess.run([sys.executable, "-m", "streamlit", "run", ui])
