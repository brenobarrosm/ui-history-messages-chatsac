import subprocess

subprocess.Popen(["streamlit", "run", "app.py", "--server.port", "8000", "--server.headless", "true"])
