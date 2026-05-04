import sys
import subprocess

try:
    from PIL import Image
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image

import os

png_path = "icon.png"
ico_path = "icon.ico"

if os.path.exists(png_path):
    img = Image.open(png_path)
    img.save(ico_path, format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    print("Icon converted successfully.")
else:
    print("icon.png not found.")
