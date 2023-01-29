#!/usr/bin/env python

import os
import json
from datetime import datetime
from pathlib import Path

def main():
    cwd = os.getcwd()
    jsPath = Path(cwd).joinpath("assets/js/scraped.json")
    with open(str(jsPath), 'r') as f:
        existingEntries = json.load(f)

    month = datetime.now().strftime('%m')
    year = datetime.now().strftime('%Y')
    day = datetime.now().strftime('%d')
    count = 0

    while True:
        count = count + 1
        print("Enter photo number or 'stop' to exit: ", end='')
        photo_num = str(input())
        if photo_num.lower() == 'stop':
            break

        print("Enter title: ", end='')
        title = str(input())
        print("Enter tags: ", end='')
        tags = str(input())

        newEntry = {
            "title": title,
            "date": f"{year}-{month}-{day} 12:00:{count:02d}",
            "tags": tags,
            "thumb": f"https://com-jameskeats-photo.s3.amazonaws.com/{year}-{month}-xx/DSC_{photo_num}_thumb.jpg",
            "fullsize": f"https://com-jameskeats-photo.s3.amazonaws.com/{year}-{month}-xx/DSC_{photo_num}.jpg",
        }

        existingEntries["entries"].append(newEntry)

    with open(str(jsPath), 'w') as output:
        json.dump(existingEntries, output, indent=2, default=str)

if __name__ == "__main__":
    main()
