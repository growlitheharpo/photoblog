#!/usr/bin/env python

import json
import os
import yaml

from pathlib import Path

def main():
    cwd = os.getcwd()
    postsPath = Path(cwd).joinpath("_posts")

    allobjects = []

    for entry in postsPath.iterdir():
        if not entry.is_file():
            continue

        with open(str(entry), "r") as stream:
            lines = stream.readlines()
            lines = lines[1: len(lines) - 1]
            try:
                header = yaml.safe_load('\n'.join(lines))
                del header["author"]
                allobjects.append(header)
            except yaml.YAMLError as exc:
                print(exc)

    rootobject = {}
    rootobject["entries"] = allobjects

    with open(postsPath.joinpath("scraped.json"), "w") as output:
        output.write(json.dumps(rootobject, indent = 2, default=str))
    #with open(postsPath.joinpath("scraped.yaml"), "w") as output:
    #    yaml.dump(rootobject, output)

if __name__ == "__main__":
    main()
