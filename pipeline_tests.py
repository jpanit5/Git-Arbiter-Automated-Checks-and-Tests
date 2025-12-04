import subprocess
import sys
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)

SERVER_SCRIPT = Path("C:\\Users\\localadmin\\Desktop\\Automation\\server_check\\main_tester.py")
CLIENT_SCRIPT = Path("C:\\Users\\localadmin\\Desktop\\Automation\\client_checks\\tools\\reporters\\ts_reporter.ts")

def run_python_script(title: str, script_path: Path) -> bool:
    """Run a Python script and return True if it failed."""
    print(f"\n=== {title} ===")
    cwd = script_path.parent 
    result = subprocess.run(
        [sys.executable, str(script_path), "--out", str(REPORTS / "server")],
        text=True,
        cwd=cwd
    )
    if result.returncode != 0:
        print(f"{title} failed!")
        return True
    print(f"{title} passed.")
    return False

def run_ts_script(title: str, ts_path: Path) -> bool:
    """
    Run a TypeScript/Node script using ts-node in a Windows-safe way.
    Returns True if failed.
    """
    print(f"\n=== {title} ===")

    npx_path = shutil.which("npx")
    if not npx_path:
        print("Error: npx not found in PATH. Make sure Node.js and ts-node are installed.")
        return True

    cwd = ts_path.parent  # ✅ Ensure correct working directory

    try:
        result = subprocess.run(
            [npx_path, "ts-node", str(ts_path)],
            cwd=cwd,
            text=True
        )
        if result.returncode != 0:
            print(f"{title} failed!")
            return True
        print(f"{title} passed.")
        return False
    except FileNotFoundError as e:
        print(f"{title} failed: {e}")
        return True

def main():
    failed = False

    # 1️⃣ Server Tests
    if SERVER_SCRIPT.exists():
        failed |= run_python_script("Server Tests", SERVER_SCRIPT)
    else:
        print(f"Server script not found at {SERVER_SCRIPT}, skipping server tests.")

    # 2️⃣ Client/UI Tests
    if CLIENT_SCRIPT.exists():
        failed |= run_ts_script("Client/UI Tests", CLIENT_SCRIPT)
    else:
        print(f"Client/UI script not found at {CLIENT_SCRIPT}, skipping UI tests.")

    # 3️⃣ Exit status
    if failed:
        print("\nOne or more checks failed!")
        sys.exit(1)
    print("\nAll checks passed successfully!")
    sys.exit(0)

if __name__ == "__main__":
    main()
