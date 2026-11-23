#!/usr/bin/env bash
# Linux → Windows 64-bit cross build (needs: apt install g++-mingw-w64-x86-64-posix)
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p build dist
x86_64-w64-mingw32-windres res/app.rc -O coff -o build/app.res
x86_64-w64-mingw32-g++-posix -std=c++17 -O2 -municode -mwindows -static -static-libgcc -static-libstdc++ \
  -Wall -Wno-missing-field-initializers -Wno-cast-function-type \
  src/main.cpp build/app.res -o dist/SOSprintWidget.exe \
  -lgdiplus -ldwmapi -lcomctl32 -lshell32 -luser32 -lgdi32 -ladvapi32 -lole32 -s
ls -la dist/SOSprintWidget.exe
