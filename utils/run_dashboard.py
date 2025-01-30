import os
import sys
from subprocess import run

from utils.constants import FRONTEND_PATH  # Importera efter att sys.path är uppdaterat

# Lägg till projektets root-mapp i sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def run_dashboard():
    run(["streamlit", "run", str(FRONTEND_PATH / "dashboard.py")])


if __name__ == "__main__":
    run_dashboard()
