@echo off
echo "NOTE: You must have node and npm on your path for all utilities to work!"
pushd %~dp0
cd _tailwind
call npm install tailwindcss@^3.2.0
popd
