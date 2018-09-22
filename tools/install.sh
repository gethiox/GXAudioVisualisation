#!/usr/bin/env bash

set -e
set -u

if [ -z "$1" ]; then
    echo "Provide blender version, eg. 2.79"
    exit 1
fi

version=${1}
package="GxAV"

echo "Removing old package..."
rm -r "/home/endriu/.config/blender/${version}/scripts/addons/${package}"
echo "installing new package..."
unzip build_latest.zip -d "/home/endriu/.config/blender/${version}/scripts/addons/"
echo "installed successfully"