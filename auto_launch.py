import os
import subprocess
import sys

def run_command(cmd):
    print(f"Executing: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(f"Stdout: {result.stdout}")
    if result.stderr:
        print(f"Stderr: {result.stderr}")
    result.check_returncode()

# 1. Setup Environment
print("🚀 Starting Automated Mac/Linux Setup...")
# Ensure the script runs from its directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

virtual_env_dir = "metformin_env"
pip_path = os.path.join(virtual_env_dir, "bin", "pip")
streamlit_path = os.path.join(virtual_env_dir, "bin", "streamlit")

if not os.path.exists(virtual_env_dir):
    print(f"Creating virtual environment at {virtual_env_dir}...")
    run_command(f"python3 -m venv {virtual_env_dir}")
else:
    print(f"Virtual environment already exists at {virtual_env_dir}.")

# 2. Install dependencies with binary flags to prevent errors
print("📦 Installing/Upgrading libraries...")
run_command(f"{pip_path} install --upgrade pip")
run_command(f"{pip_path} install --only-binary=:all: streamlit pandas scikit-learn joblib numpy")

# 3. Launch App
print("🎉 Launching Dashboard...")
run_command(f"{streamlit_path} run demo_app.py")