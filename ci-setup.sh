#!/bin/bash

pushd _tailwind/
npm install tailwindcss@1.2.0
npm install purgecss@^1.4.0
npm install clean-css
npm install -g clean-css-cli

popd
python ./buildtags.py

pushd _tailwind/
npx tailwind build base.css -o ../assets/css/output.css

