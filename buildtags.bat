@echo off
pushd %~dp0
call python buildtags.py
popd
