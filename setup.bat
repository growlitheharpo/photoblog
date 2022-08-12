@echo off
echo "NOTE: You must have node and npm on your path for all utilities to work!"
pushd %~dp0
cd _tailwind
call npm install tailwindcss@1.2.0
call npm install purgecss@^1.4.0
call npm install clean-css
call npm install -g clean-css-cli
popd
