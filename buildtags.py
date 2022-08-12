#!/usr/bin/env python

# Inspired by https://github.com/qian256/qian256.github.io/blob/master/tag_generator.py

import os
import shutil
from pathlib import Path

FrontMatterMarker = "---"
TagsMarker = "tags: "

def getTags(rootDir):
    postPath = Path(rootDir).joinpath("_posts")
    postFiles = postPath.rglob("*.md")
    allTags = set()
    for p in postFiles:
        with p.open(encoding="utf8") as f:
            while True:
                curLine = f.readline().rstrip("\n")
                if (curLine == FrontMatterMarker):
                    break

            while True:
                curLine = f.readline().rstrip("\n")
                if (curLine.startswith(TagsMarker)):
                    curTags = curLine.strip(TagsMarker).split(" ")
                    allTags = allTags.union(curTags)
                    break
                elif (curLine == FrontMatterMarker):
                    break

    return allTags

def deleteExisting(rootDir):
    tagsPath = Path(rootDir).joinpath("tags")
    for child in tagsPath.rglob("*.md"):
        if (child.is_file()):
            child.unlink()

def createPosts(rootDir, tags):
    tagsPath = Path(rootDir).joinpath("tags")
    tagsPath.mkdir(parents=True, exist_ok=True)
    for tag in tags:
        with tagsPath.joinpath(f"{tag}.md").open("w") as f:
            f.writelines([
                f"---\n",
                f"layout: postlist\n",
                f"selectedurl: Blog\n"
                f"title: Posts Tagged \"{tag}\" - Perfect and Absolute Blank\n",
                f"tag: {tag}\n",
                f"---\n",
            ])

if __name__ == "__main__":
    cwd = os.getcwd()
    tags = getTags(cwd)
    if (len(tags) > 0):
        deleteExisting(cwd)
        createPosts(cwd, tags)
    print(f"Generated {len(tags)} tag pages.")
