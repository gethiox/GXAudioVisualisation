# License: GPLv3
# Version: 0.5
# Relase Date: 11.02.2014

import bpy
from bpy.props import *
from math import *  
#from bpy.types import Operator
#from bpy.props import FloatVectorProperty, FloatProperty

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
    "name": "GXAudioVisualisation",
    "author": "Sławomir Kur (Gethiox)",
    "version": (0, 5),
    "blender": (2, 6, 0),
    "location": "View3D > Tools menu",
    "description": "Bake Spectrum Visualizer with sound file",
    "category": "Animation",
    "wiki_url": "https://github.com/gethiox/GXAudioVisualisation/wiki",
    "tracker_url": ""}

def initSceneProperties(scn):
    bpy.types.Scene.Bake = BoolProperty(
        name = "Bake",
        description = "Bake animation from file")
    scn['Bake'] = False

    bpy.types.Scene.Debug = BoolProperty(
        name = "Freq Info",
        description = "Create additional emptys with frequency information")
    scn['Debug'] = False

    bpy.types.Scene.Channels = EnumProperty(
        items = [('0', 'Both', 'Left and Right channel'),
                 ('1', 'Left', 'Left channel'),
                 ('2', 'Right', 'Right channel')],
        name = "Channels")
    scn['Channels'] = 0

    bpy.types.Scene.Mode = EnumProperty(
        items = [('0', 'Array', 'Array modifier visualisation based'),
                 ('1', 'Cube Scale', 'Cube with scaling in bottom'),
                 ('2', 'Center Cube Scale', 'Cube with scaling in center')],
        name = "Based-Mode")
    scn['Mode'] = 0

    bpy.types.Scene.LeftFile = StringProperty(
        name = "Left File",
        #default = "",
        description = "Define path of the left channel file",
        subtype = 'FILE_PATH')

    bpy.types.Scene.RightFile = StringProperty(
        name = "Right File",
        #default = "",
        description = "Define path of the right channel file",
        subtype = 'FILE_PATH')

    bpy.types.Scene.value_x = IntProperty(
        name = "Count X",
        default = 8,
        soft_min = 1,
        soft_max = 32,
        description = "Enter an integer")
    scn['value_x'] = 8

    bpy.types.Scene.value_y = IntProperty(
        name = "Count Y",
        default = 1,
        soft_min = 1,
        soft_max = 32,
        description = "Enter an integer")
    scn['value_y'] = 1
        
    bpy.types.Scene.space_x = FloatProperty(
        name = "Space X",
        description = "Space between objects orgins in X axis",
        default = 3.0,
        min = 0,)
    scn['space_x'] = 3.0

    bpy.types.Scene.space_y = FloatProperty(
        name = "Space Y",
        description = "Space between objects orgins in Y axis",
        default = 3.0,
        min = 0,)
    scn['space_y'] = 3.0
    
    bpy.types.Scene.space_array = FloatProperty(
        name = "Array Relative Offet",
        description = "Array  Modifier Relative Offet",
        default = 1.3,
        min = 0,)
    scn['space_array'] = 1.3
    
    bpy.types.Scene.scale_x = FloatProperty(
        name = "X",
        description = "Dimensions of the cube (default object)",
        default = 1.0,
        min = 0,)
    scn['scale_x'] = 1.0  
    
    bpy.types.Scene.scale_y = FloatProperty(
        name = "Y",
        description = "Dimensions of the cube (default object)",
        default = 0.8,
        min = 0,)
    scn['scale_y'] = 0.8  
    
    bpy.types.Scene.scale_z = FloatProperty(
        name = "Z",
        description = "Dimensions of the cube (default object)",
        default = 0.5,
        min = 0,)
    scn['scale_z'] = 0.5
    
    bpy.types.Scene.start_frame = IntProperty(
        name = "Start Frame",
        default = 1,
        soft_min = 0,
        description = "Start frame of isualization")
    scn['start_frame'] = 1        


    bpy.types.Scene.attack = FloatProperty(
        name = "attack",
        description = "attack",
        default = 0.005,
        min = 0,)
    scn['attack'] = 0.005

    bpy.types.Scene.release = FloatProperty(
        name = "release",
        description = "release",
        default = 0.2,
        min = 0,)
    scn['release'] = 0.2
    
    bpy.types.Scene.threshold = FloatProperty(
        name = "threshold",
        description = "threshold",
        default = 0.0,
        min = 0,)
    scn['threshold'] = 0.0
    
    bpy.types.Scene.sthreshold = FloatProperty(
        name = "sthreshold",
        description = "sthreshold",
        default = 0.5,
        min = 0,)
    scn['sthreshold'] = 0.5
    
    bpy.types.Scene.use_accumulate = BoolProperty(
        name = "accumulate",
        description = "accumulate")
    scn['use_accumulate'] = False
    
    bpy.types.Scene.use_additive = BoolProperty(
        name = "additive",
        description = "additive")
    scn['use_additive'] = False
    
    bpy.types.Scene.use_square = BoolProperty(
        name = "square",
        description = "square")
    scn['use_square'] = False      
    
    bpy.types.Scene.offset = IntProperty(
        name = "Jumps Frames",
        default = 1,
        soft_min = 1,
        description = "delay in frames between changes 'count' value of array modificator (jumps, strobe effect)")
    scn['offset'] = 1           
    
    bpy.types.Scene.center_space = FloatProperty(
        name = "Segments Space",
        default = 1.0,
        min = 0,
        description = "Additional space between left and right channel segments")
    scn['center_space'] = 1.0     
    
    bpy.types.Scene.FreqMode = EnumProperty(
        items = [('0', 'Logarithm', 'log'),
                 ('1', 'Linear', 'linear')],
        name = "Frequency Mode")
    scn['FreqMode'] = 0

    bpy.types.Scene.drivmod = FloatProperty(
        name = "Driver Power",
        description = "driver 'amplifier' - Imprecise column height",
        default = 20.0,
        min = 1,)
    scn['drivmod'] = 20.0
    
    bpy.types.Scene.slash = FloatProperty(
        name = "Slash",
        default = 0.0,
        min = 0,
        description = "additional transform for objects in X axis line, looks like 'V' char")
    scn['slash'] = 0.0       
    
    bpy.types.Scene.max_herz = IntProperty(
        name = "Maximum Frequency",
        default = 20000,
        soft_min = 0,
        description = "max frequency value to analyze, dafault 20000")
    scn['max_herz'] = 20000
    
    bpy.types.Scene.slash_rotate = BoolProperty(
        name = "slash rotate",
        description = "additional rotation for object when slash option is used")
    scn['slash_rotate'] = False      
        

class GXAudioVisualisationPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "GXAudioVisualisation"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

    def draw(self, context):
        scene = context.scene

        layout = self.layout
        row = layout.row()
        row.operator("scene.bake_visualisation", text="Create Visualizer", icon="RADIO")
        row = layout.row()
        row.prop(scn, 'Bake')
        row.prop(scn, 'Debug')
                
        box = layout.box()
        box.label("Channels to bake and audio files path:")
        box.prop(scn, 'Channels')
        box.prop(scn, 'LeftFile')
        box.prop(scn, 'RightFile')

        row = layout.row()
        row = layout.row() 
        row.prop(scn, 'Mode')
        row = layout.row()  
        row.prop(scn, 'FreqMode')        

        split = layout.split()

        col = split.column(align=True)
        col.label(text="Objects Grid")
        col.prop(scn, 'value_x')
        col.prop(scn, 'value_y') 

        col = split.column(align=True)
        col.label(text="Space Between Objects")
        col.prop(scn, 'space_x')
        col.prop(scn, 'space_y')
        
        split = layout.split()
        row = layout.row()
        row.prop(scn, 'center_space')
        row = layout.row()
        row.prop(scn, 'slash')
        row.prop(scn, 'slash_rotate')     

        row = layout.row(align=True)
        row.label(text="Object Scale:")
        row.prop(scn, 'scale_x')
        row.prop(scn, 'scale_y')
        row.prop(scn, 'scale_z')

        row = layout.row()
        row.prop(scn, 'space_array')
        
        row = layout.row()
        row.prop(scn, 'start_frame')
        row.prop(scn, 'offset')
        
        row = layout.row()  
        row.prop(scn, 'drivmod')
        row = layout.row()  
        row.prop(scn, 'max_herz')
        
        row = layout.row()
        box = layout.box()
        box.label(text="'Bake Sound to F-Curves' function options:")
        split = box.split()
        col = split.column(align=True)    
        col.prop(scn, 'attack')
        col.prop(scn, 'release')
        col = split.column(align=True)  
        col.prop(scn, 'threshold')
        col.prop(scn, 'sthreshold')
        split = box.split()
        col = split.column()
           
        col.prop(scn, 'use_accumulate')
        col = split.column()
        col.prop(scn, 'use_additive')
        col = split.column()        
        col.prop(scn, 'use_square')

scn = bpy.context.scene
initSceneProperties(bpy.context.scene);

class GXAudioVisualisation(bpy.types.Operator):
    bl_idname = 'scene.bake_visualisation'
    bl_label = 'bake_visualisation'
    bl_description = 'bake_visualisation'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bake();
        return{'FINISHED'}

def bake():
    low = 0           # min freq, doesn't work yet (removed broken code, disabled)
    ouu = -2            # offset for emptys in Z axis range (nothing important to modify)

    if scn['Channels'] == 1:
        loop_count = 1; kanau = 1
    elif scn['Channels'] == 2:
        loop_count = 1; kanau = 2
    elif scn['Channels'] == 0:
        loop_count = 2;

    stereo_memory = scn['Channels']
    for loop in range(0, loop_count):
        if scn['Channels'] == 0 and loop == 0: kanau = 1
        if scn['Channels'] == 0 and loop == 1: kanau = 2

        float_rx = 0 + scn['center_space']
        float_ry = 0
        start = scn['start_frame']
        for ry in range(0, scn['value_y']):
            step2 = low
            for rx in range(0, scn['value_x']):
                bpy.context.scene.frame_current = start
                if kanau == 1: bpy.ops.object.empty_add(type='SPHERE', location=(-float_rx - scn['space_x']/2, float_ry, ouu));
                elif kanau == 2: bpy.ops.object.empty_add(type='SPHERE', location=(float_rx + scn['space_x']/2, float_ry, ouu));
                bpy.ops.anim.keyframe_insert_menu(type='Scaling')
                step1 = step2
                if scn['FreqMode'] == 0:
                    step2 = scn['max_herz']
                    for what in range (0, scn['value_x']-rx-1):
                        step2 = step2 / ((8/scn['value_x'])+1)
                        if rx == 0: #additional module for correct math range problem, but not so fine
                            step1 = step2 / ((8/scn['value_x'])+1)
                        #step2 = step2 / 2
                elif scn['FreqMode'] == 1:
                    step2 = (rx+1)*(scn['max_herz']/scn['value_x'])
                if scn['Bake'] == True:
                    bpy.context.area.type = 'GRAPH_EDITOR'
                    if kanau == 1: bpy.ops.graph.sound_bake(filepath=scn['LeftFile'],\
                                                                      low=step1,\
                                                                      high=step2,\
                                                                      attack=scn['attack'],\
                                                                      release=scn['release'],\
                                                                      threshold=scn['threshold'],\
                                                                      use_accumulate=scn['use_accumulate'],\
                                                                      use_additive=scn['use_additive'],\
                                                                      use_square=scn['use_square'],\
                                                                      sthreshold=scn['sthreshold'])
                    elif kanau == 2: bpy.ops.graph.sound_bake(filepath=scn['RightFile'],\
                                                                        low=step1,\
                                                                        high=step2,\
                                                                        attack=scn['attack'],\
                                                                        release=scn['release'],\
                                                                        threshold=scn['threshold'],\
                                                                        use_accumulate=scn['use_accumulate'],\
                                                                        use_additive=scn['use_additive'],\
                                                                        use_square=scn['use_square'],\
                                                                        sthreshold=scn['sthreshold'])                                                                        
                    bpy.context.area.type = 'VIEW_3D'
                nx = rx + 1; nx = str(nx)
                ny = ry + 1; ny = str(ny)
                if kanau == 1: no = "obj_L"
                elif kanau == 2: no = "obj_R"
                bpy.context.active_object.name = (no + "_"  + ny + "_" + nx)
                bpy.data.objects[no + "_"  + ny + "_" + nx].animation_data.action.fcurves[0].hide = True
                bpy.data.objects[no + "_"  + ny + "_" + nx].animation_data.action.fcurves[1].hide = True

                if scn['Mode'] == 0:
                    if kanau == 1: bpy.ops.mesh.primitive_cube_add(location=(-float_rx - scn['space_x']/2, float_ry, 0))
                    elif kanau == 2: bpy.ops.mesh.primitive_cube_add(location=(float_rx + scn['space_x']/2, float_ry, 0))
                    bpy.ops.transform.resize(value=(scn['scale_x'],scn['scale_y'],scn['scale_z']))
                    bpy.ops.object.transform_apply(scale=True)
                    if scn['slash'] >= 0.0 and scn['slash_rotate'] == True:
                        face = pow(scn['space_x'],2) + pow(scn['slash'],2)
                        face = sqrt(face)
                        iks = scn['slash']/face
                        iks = asin(iks)
                        if kanau == 1: bpy.ops.transform.rotate(value=-iks, axis=(0,0,1))   
                        elif kanau == 2: bpy.ops.transform.rotate(value=iks, axis=(0,0,1))   
                    if kanau == 1: nc = "cub_L"
                    elif kanau == 2: nc = "cub_R"
                    bpy.context.active_object.name = (nc + "_" + ny + "_" + nx)
                    bpy.ops.object.modifier_add(type='ARRAY')
                    bpy.context.active_object.modifiers['Array'].relative_offset_displace[0] = 0
                    bpy.context.active_object.modifiers['Array'].relative_offset_displace[2] = scn['space_array']
                    obj = bpy.data.objects[nc + "_" + ny + "_" + nx] #def drivering
                    mdf = obj.modifiers['Array'].driver_add('count')
                    drv = mdf.driver
                    drv.type = 'AVERAGE'
                    var = drv.variables.new()
                    var.name = 'name'
                    var.type = 'TRANSFORMS'
                    targ = var.targets[0]
                    targ.id = bpy.data.objects[no + "_"  + ny + "_" + nx]
                    targ.transform_type = 'SCALE_Z'
                    targ.bone_target = 'Driver'
                    fmod = mdf.modifiers[0]
                    fmod.poly_order = 1
                    if scn['FreqMode'] == 0:
                        fmod.coefficients = (0.0, scn['drivmod'])
                    elif scn['FreqMode'] == 1:
                        #fmod.coefficients = (0.0, scn['drivmod']+(2*(rx+1))):
                        fmod.coefficients = (0.0, scn['drivmod'])
                elif scn['Mode'] == 1 or scn['Mode'] == 2:
                    if kanau == 1: bpy.ops.mesh.primitive_cube_add(location=(-float_rx - scn['space_x']/2, float_ry, 0))
                    elif kanau == 2: bpy.ops.mesh.primitive_cube_add(location=(float_rx + scn['space_x']/2, float_ry, 0))
                    bpy.context.scene.cursor_location = bpy.context.active_object.location
                    bpy.ops.transform.resize(value=(scn['scale_x'],scn['scale_y'],scn['scale_z']))
                    if scn['slash'] >= 0.0 and scn['slash_rotate'] == True:
                        face = pow(scn['space_x'],2) + pow(scn['slash'],2)
                        face = sqrt(face)
                        iks = scn['slash']/face
                        iks = asin(iks)
                        if kanau == 1: bpy.ops.transform.rotate(value=-iks, axis=(0,0,1))   
                        elif kanau == 2: bpy.ops.transform.rotate(value=iks, axis=(0,0,1))                     
                    bpy.ops.object.transform_apply(scale=True)
                    if scn['Mode'] == 1:
                        bpy.ops.transform.transform(value=(0, 0, scn['scale_z'], 0))
                        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
                    if kanau == 1: nc = "cub_L"
                    elif kanau == 2: nc = "cub_R"
                    bpy.context.active_object.name = (nc + "_" + ny + "_" + nx)
                    obj = bpy.data.objects[nc + "_" + ny + "_" + nx] #def drivering
                    mdf = obj.driver_add('scale', 2)
                    drv = mdf.driver
                    drv.type = 'AVERAGE'
                    var = drv.variables.new()
                    var.name = 'name'
                    var.type = 'TRANSFORMS'
                    targ = var.targets[0]
                    targ.id = bpy.data.objects[no + "_"  + ny + "_" + nx]
                    targ.transform_type = 'SCALE_Z'
                    targ.bone_target = 'Driver'
                    fmod = mdf.modifiers[0]
                    fmod.poly_order = 1
                    if scn['FreqMode'] == 0:
                        fmod.coefficients = (0.0, scn['drivmod'])
                    elif scn['FreqMode'] == 1:
                        #fmod.coefficients = (0.0, scn['drivmod']+(2*(rx+1))):
                        fmod.coefficients = (0.0, scn['drivmod'])

                if scn['offset'] >= 2:
                    bpy.data.objects[no + "_"  + ny + "_" + nx].animation_data.action.fcurves[2].modifiers.new('STEPPED')
                    bpy.data.objects[no + "_"  + ny + "_" + nx].animation_data.action.fcurves[2].modifiers.active.frame_step = scn['offset']

                if scn['Debug'] == True and ry == 0:
                    ds1 = round(step1,2); ds1 = str(ds1)
                    ds2 = round(step2,2); ds2 = str(ds2)
                    if kanau == 1:
                        bpy.ops.object.empty_add(location=(-float_rx - scn['space_x']/2, float_ry, ouu*2));
                        bpy.context.active_object.name = ("L " + ds1 + "Hz - " + ds2 + "Hz");
                    elif kanau == 2:
                        bpy.ops.object.empty_add(location=(float_rx + scn['space_x']/2, float_ry, ouu*2));
                        bpy.context.active_object.name = ("R "+ ds1 + "Hz - " + ds2 + "Hz");
                
                float_rx = float_rx+scn['space_x']
                float_ry = float_ry+scn['slash']
            float_ry = float_ry+scn['space_y']-(scn['slash']*scn['value_x'])
            float_rx = float_rx - scn['space_x'] * scn['value_x']
            start = start + scn['offset']

def register():
    bpy.utils.register_class(GXAudioVisualisationPanel)
    bpy.utils.register_class(GXAudioVisualisation)

def unregister():
    bpy.utils.unregister_class(GXAudioVisualisationPanel)
    bpy.utils.unregister_class(GXAudioVisualisation)

if __name__ == "__main__":
    register()
