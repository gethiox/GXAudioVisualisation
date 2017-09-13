#!/usr/bin/env bash

if [ -d "./GxAV" ]; then
  project_dir="./GxAV"
elif [ -d "./../GxAV" ]; then
  project_dir="./../GxAV"
else
  echo "Build failed, make sure you are sitting in the right place (project directory)"
  exit 1
fi

build_date=$(date +%d-%m-%Y_%H:%M:%S)
filename=GxAV_$build_date.zip

zip -r $filename $project_dir && echo "Build successes, you can now install $filename as blender addon"