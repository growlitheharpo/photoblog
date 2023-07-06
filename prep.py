#!/usr/bin/env python

import argparse
import os
import json
from datetime import datetime
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path
import cv2

EXPORTED_IMAGE_FOLDER = "M:\FOTO-AFTER"

ArgParser = argparse.ArgumentParser()
ArgParser.add_argument("--any-missing-json", action='store_true', default=False)

def get_exif_tag(exifObject, tagName):
  for (k, v) in exifObject.items():
     if TAGS.get(k) == tagName:
        return v

def replace_first_in_string(haystack, needle, replacement):
    index = haystack.find(needle)
    return haystack[:index] + replacement + haystack[index + 1:]

def get_id_for_file(entry):
    extensionIndex = entry.name.find('.')
    photoId = entry.name[:extensionIndex]
    thumbName = photoId + "_thumb" + entry.name[extensionIndex:]
    return (photoId, thumbName)

def thumbnail_exists(folder, thumbName):
    return folder.joinpath(thumbName).exists()

def json_entry_exists(jsonData, photoId):
    return len([entry for entry in jsonData["entries"] if entry["id"] == photoId]) > 0

def get_date_taken(folder, entry, jsonData):
    sourceImage = Image.open(folder.joinpath(entry.name))
    dateTakenStr = get_exif_tag(sourceImage.getexif(), "DateTimeOriginal")

    if dateTakenStr is None:
        fallbackIndex = len(jsonData["entries"]) % 60
        dateTaken = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 12, 0, fallbackIndex)
    else:
        dateTaken = datetime.strptime(dateTakenStr, "%Y:%m:%d %H:%M:%S")

    return dateTaken

def get_title_tags(photoId):
    skip = False
    stop = False
    title = ''
    tags = ''

    while True:
        print(f"Enter title for {photoId}: ", end='')
        title = str(input())

        if title == "skip":
            skip = True
            break

        if title == "stop":
            stop = True
            break

        print(f"Enter tags for {photoId}: ", end='')
        tags = str(input())

        if tags == "skip":
            skip = True
            break

        if tags == "stop":
            stop = True
            break

        if tags == "retry":
            continue

        print(f"Title: {title}, tags: '{tags}'. Retry? (Enter to confirm)")
        lastChance = str(input())
        if (len(lastChance) == 0):
            break

    return (skip, stop, title, tags)

def create_thumbnail(folder, entry, thumbName):
    print(f"Creating {thumbName}")
    cvimage = cv2.resize(cv2.imread(str(entry)), None, fx = 0.3, fy = 0.3)
    cv2.imwrite(str(folder.joinpath(thumbName)), cvimage, [cv2.IMWRITE_JPEG_QUALITY, 92])

def main():
    createdList = []

    args = ArgParser.parse_args()
    cwd = os.getcwd()
    jsPath = Path(cwd).joinpath("assets/js/scraped.json")
    with open(str(jsPath), 'r') as f:
        existingEntries = json.load(f)

    imgFolderPath = Path(EXPORTED_IMAGE_FOLDER)
    for entry in imgFolderPath.iterdir():
        if not entry.is_file():
            continue

        if entry.name.endswith("_thumb.jpg") or not entry.name.endswith(".jpg"):
            continue

        photoId, thumbName = get_id_for_file(entry)

        # photo already exists
        if json_entry_exists(existingEntries, photoId):
            continue

        # it is missing from the json:
        # if it has a thumbnail and we didn't pass the flag, skip it
        if thumbnail_exists(imgFolderPath, thumbName) and not args.any_missing_json:
            print(f"Skipping missing image {photoId} because it already has a thumbnail")
            continue

        # it's a new file!
        dateTaken = get_date_taken(imgFolderPath, entry, existingEntries)
        shouldSkip, shouldStop, title, tags = get_title_tags(photoId)

        if shouldSkip:
            continue

        if shouldStop:
            break

        create_thumbnail(imgFolderPath, entry, thumbName)

        # TODO: AWS bindings, upload to S3?
        awsFolder = f"{dateTaken.year}-{dateTaken.strftime('%m')}-xx"

        newEntry = {
            "id": photoId,
            "title": title,
            "date": dateTaken.strftime("%Y-%m-%d %H:%M:%S"),
            "tags": tags,
            "thumb": f"https://com-jameskeats-photo.s3.amazonaws.com/{awsFolder}/{photoId}_thumb.jpg",
            "fullsize": f"https://com-jameskeats-photo.s3.amazonaws.com/{awsFolder}/{photoId}.jpg",
        }

        createdList.append(f"{photoId} in {awsFolder}")
        existingEntries["entries"].append(newEntry)

    with open(str(jsPath), 'w') as output:
        json.dump(existingEntries, output, indent=2, default=str)

    print("Newly created items:")
    for item in createdList:
        print(f"\t{item}")

if __name__ == "__main__":
    main()
