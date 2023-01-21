#!/usr/bin/env python

import os
import signal
import subprocess
import sys
import shutil
import time

from pathlib import Path

cwd = Path(os.getcwd())
tailwindWd = cwd.joinpath("_tailwind")

npxPath = shutil.which("npx")
tailwindProcess = subprocess.Popen(
    f"{npxPath} tailwindcss -i ./base.css -o ../assets/css/output.css --watch",
    cwd=str(tailwindWd))

time.sleep(0.5)

jekyllPath = shutil.which("jekyll")
jekyllProcess = subprocess.Popen(
    f"{jekyllPath} serve --drafts",
    cwd=str(cwd))

def signal_handler(sig, frame):
    tailwindProcess.kill()
    jekyllProcess.kill()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
tailwindProcess.wait()
jekyllProcess.wait()
