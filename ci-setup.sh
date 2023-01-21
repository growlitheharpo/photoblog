#!/bin/bash

pushd _tailwind/
npm install tailwindcss@^3.2.0

popd
python ./buildtags.py

pushd _tailwind/
npx tailwindcss -i ./base.css -o ../assets/css/output.css --minify
