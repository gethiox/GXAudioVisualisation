#!/usr/bin/env bash

set -u
set -e

if ! [ -d "./GxAV" ] && ! [ -f "./GxAV/gxav.py" ]; then
  echo "Build failed, make sure you are sitting in the right place (project directory)"
  exit 1
fi

builds_dir="./builds"


build_date=$(date +%d-%m-%Y_%H:%M:%S_%s)
filename="GxAV_${build_date}.zip"

if ! [ -d "${builds_dir}" ]; then
    mkdir "${builds_dir}"
fi

sync
zip -r "${builds_dir}/${filename}" "GxAV" && echo "Build successes, you can now install ${filename} as blender addon"
ln -sf "${builds_dir}/${filename}" "build_latest.zip"