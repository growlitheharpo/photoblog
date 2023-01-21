#!/usr/bin/env python

from PIL import Image
from pathlib import Path
import cv2

def main():
    folder = "M:\FOTO-AFTER"
    folderPath = Path(folder)
    for entry in folderPath.iterdir():
        if not entry.is_file():
            continue

        if entry.name.endswith("_thumb.jpg") or not entry.name.endswith(".jpg"):
            continue

        thumbName = entry.name
        index = thumbName.find('.')
        thumbName = entry.name[:index] + "_thumb" + entry.name[index:]
        if folderPath.joinpath(thumbName).exists():
            continue

        print(f"Creating {thumbName}")
        cvimage = cv2.resize(cv2.imread(str(entry)), None, fx = 0.3, fy = 0.3)
        cv2.imwrite(str(folderPath.joinpath(thumbName)), cvimage, [cv2.IMWRITE_JPEG_QUALITY, 92])

if __name__ == "__main__":
    main()
