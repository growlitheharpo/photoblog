@echo off
pushd %~dp0
cd _tailwind
call node purgecss.control.js
call cleancss -o ..\assets\css\output.min.css ..\assets\css\output.css
move /y "..\assets\css\output.min.css" "..\assets\css\output.css"
popd
