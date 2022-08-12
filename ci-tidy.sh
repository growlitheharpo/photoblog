#!/bin/bash

pushd _tailwind
node purgecss.control.js
popd

cleancss -o assets/css/output.min.css assets/css/output.css
mv -f assets/css/output.min.css assets/css/output.css
