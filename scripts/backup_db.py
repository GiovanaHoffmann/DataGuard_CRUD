import subprocess
from datetime import datetime

def backup():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    cmd = f"pg_dump -U postgres client_governance > backup_{timestamp}.sql"
    subprocess.run(cmd, shell=True)