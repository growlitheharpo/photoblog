@echo off
pushd %~dp0
cd _tailwind
call npx tailwind build base.css -o ../assets/css/output.css
popd
