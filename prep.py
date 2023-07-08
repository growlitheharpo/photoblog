#!/usr/bin/env python

import argparse
import boto3
import cv2
import json
import os

from datetime import datetime
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS

EXPORTED_IMAGE_FOLDER = "M:\FOTO-AFTER"
S3_BUCKET = "com-jameskeats-photo"

ArgParser = argparse.ArgumentParser()
ArgParser.add_argument("--any-missing-json", action='store_true', default=False)
ArgParser.add_argument("-patch-times", action='store_true', default=False)
args = ArgParser.parse_args()

def json_entry_exists(entryList, photoId):
    return len([entry for entry in entryList if entry["id"] == photoId]) > 0

def get_exif_tag(exifObject, tagName):
  for (k, v) in exifObject.items():
     if TAGS.get(k) == tagName:
        return v

def get_date_taken(fullImageFile, entryList):
    sourceImage = Image.open(str(fullImageFile))
    dateTakenStr = get_exif_tag(sourceImage.getexif(), "DateTimeOriginal")

    if dateTakenStr is None:
        fallbackIndex = len(entryList) % 60
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

def create_thumbnail(fullImageFile, thumbnailFile):
    print(f"Creating {thumbnailFile.name}")

    srcImage = cv2.imread(str(fullImageFile))
    resizedImage = cv2.resize(srcImage, None, fx = 0.3, fy = 0.3)
    cv2.imwrite(str(thumbnailFile), resizedImage, [cv2.IMWRITE_JPEG_QUALITY, 92])

def upload_file(s3, localFile, s3Path):
    if s3 is not None:
        print(f"Uploading {localFile} to {s3Path}")
        s3.upload_file(localFile, S3_BUCKET, s3Path)

def load_json():
    cwd = os.getcwd()
    jsPath = Path(cwd).joinpath("assets/js/scraped.json")
    with open(str(jsPath), 'r') as f:
        existingEntries = json.load(f)

    return existingEntries

def save_json(jsonData):
    cwd = os.getcwd()
    jsPath = Path(cwd).joinpath("assets/js/scraped.json")
    jsonData["entries"].sort(key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d %H:%M:%S"))
    with open(str(jsPath), 'w') as output:
        json.dump(jsonData, output, indent=2, default=str)

def patch_times():
    existingEntries = load_json()
    entryList = existingEntries["entries"]

    for jsonEntry in entryList:
        id = jsonEntry["id"]
        imagePath = Path(f"{EXPORTED_IMAGE_FOLDER}\{id}.jpg")
        if not imagePath.exists():
            print(f"Could not find {imagePath}")
            continue

        dateTaken = get_date_taken(imagePath, entryList)
        jsonEntry["date"] = dateTaken.strftime("%Y-%m-%d %H:%M:%S")

    save_json(existingEntries)

def add_missing_entries():
    createdList = []

    # assume the user has installed the AWS CLI and set up an IAM user - we're not going to
    # even attempt any sort of authentication here
    s3 = boto3.client("s3")

    existingEntries = load_json()
    entryList = existingEntries["entries"]

    imgFolderPath = Path(EXPORTED_IMAGE_FOLDER)
    for fullImageFile in imgFolderPath.iterdir():
        if not fullImageFile.is_file():
            continue

        if fullImageFile.name.endswith("_thumb.jpg") or not fullImageFile.name.endswith(".jpg"):
            continue

        photoId = fullImageFile.stem
        thumbnailFile = fullImageFile.with_name(f"{fullImageFile.stem}_thumb{fullImageFile.suffix}")
        thumbnailName = thumbnailFile.stem

        # photo already exists
        if json_entry_exists(entryList, photoId):
            continue

        # it is missing from the json:
        # if it has a thumbnail and we didn't pass the flag, skip it
        if thumbnailFile.exists() and not args.any_missing_json:
            print(f"Skipping missing image {photoId} because it already has a thumbnail")
            continue

        # it's a new file!
        dateTaken = get_date_taken(fullImageFile, entryList)
        shouldSkip, shouldStop, title, tags = get_title_tags(photoId)

        if shouldSkip:
            continue

        if shouldStop:
            break

        if not thumbnailFile.exists():
            create_thumbnail(fullImageFile, thumbnailFile)

        awsFolder = f"{dateTaken.year}-{dateTaken.strftime('%m')}-xx"
        fullFileAwsKey = f"{awsFolder}/{fullImageFile.name}"
        thumbnailFileAwsKey = f"{awsFolder}/{thumbnailFile.name}"

        upload_file(s3, str(fullImageFile), fullFileAwsKey)
        upload_file(s3, str(thumbnailFile), thumbnailFileAwsKey)

        newJsonEntry = {
            "id": photoId,
            "title": title,
            "date": dateTaken.strftime("%Y-%m-%d %H:%M:%S"),
            "tags": tags,
            "fullsize": f"https://com-jameskeats-photo.s3.amazonaws.com/{fullFileAwsKey}",
            "thumb": f"https://com-jameskeats-photo.s3.amazonaws.com/{thumbnailFileAwsKey}",
        }

        createdList.append(f"{photoId} in {awsFolder}")
        entryList.append(newJsonEntry)

    save_json(existingEntries)

    print("Newly created items:")
    for item in createdList:
        print(f"\t{item}")

if __name__ == "__main__":
    if (args.patch_times):
        patch_times()
    else:
        add_missing_entries()
