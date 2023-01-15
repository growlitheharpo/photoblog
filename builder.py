#!/usr/bin/env python

import os
from datetime import datetime
from pathlib import Path

def main():
    cwd = os.getcwd()
    postsPath = Path(cwd).joinpath("_posts")

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

        with postsPath.joinpath(f"{year}-{month}-{day}-{count}-{title}.md").open("w") as f:
            f.writelines('\n'.join([
                f"---",
                f"title: {title}",
                f"layout: blogpost",
                f"author: James Keats",
                f"date: {year}-{month}-{day} 12:00:{count:02d}",
                f"tags: {tags}",
                f"thumb: https://com-jameskeats-photo.s3.amazonaws.com/{year}-{month}-xx/DSC_{photo_num}_thumb.jpg",
                f"fullsize: https://com-jameskeats-photo.s3.amazonaws.com/{year}-{month}-xx/DSC_{photo_num}.jpg",
                f"---",
                f"",
            ]))

if __name__ == "__main__":
    main()
