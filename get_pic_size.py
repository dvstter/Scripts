#!/usr/local/bin/python3
from PIL import Image
import sys


if __name__ == "__main__":
    try:
        width, height = Image.open(sys.argv[1]).size
        print(f"{width}*{height}")
    except Exception:
        print(f"Error: Please check parameter.")
