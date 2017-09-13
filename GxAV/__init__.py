"""
GXAudioVisualisation - Blender Music Visualizer
Copyright (C) 2013 Sławomir Kur (Gethiox)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see http://www.gnu.org/licenses/
"""

bl_info = {
    "name": "GxAV",
    "author": "Sławomir Kur (Gethiox)",
    "version": (1, 0),
    "blender": (2, 7, 1),
    "location": "Properties > Scene",
    "description": "Bake Spectrum Visualizer by sound file",
    "category": "Animation",
    "wiki_url": "https://github.com/gethiox/GXAudioVisualisation/wiki",
    "tracker_url": "https://github.com/gethiox/GXAudioVisualisation/issues"}

from GxAV import gxav


def register():
    gxav.register()


def unregister():
    gxav.unregister()
