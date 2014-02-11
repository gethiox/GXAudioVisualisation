# by Gethiox, CC-BY, pre-beta-alpha version
# version 0.31 
# 16.08.2013

import bpy

#############
### FILES ###
#############

"""
# "Bake Sound to F-Curves" doesn't support choosing audio chanels
# from audio files like left or right channel, so if you want to have a
# stereo visualisatnion, then You must separate your stereo audio file 
# to two mono files (e.g. in audacity), or You can use same file for
# left and right channel
"""

# left file chanel ("C:\Folder\music.flac" or "/media/music.ogg") 
file_l = "/media/music.ogg"
# right file chanel
file_r = "/media/music.ogg"

#################
# basic options #
#################

# always when you run script, you must delete
# generated objects before you run script again

bake = 1            # bake sound to f-curves, 1=yes 0=no, useful for tesing
stereo = 3          # channels to bake, 1=only left, 2=only right, 3=stereo

value_x = 8         # value of cubes on X axis (must be over 0!)
value_y = 1         # value of cubes on Y axis (must be over 0!)
space_x = 3         # space between objects in X axis (orgins)
space_y = 3         # space betweeb objects in Y axis (orgins)
space_array = 1.3   # value of "Relative Offset" in array modifier, Z axis
scale = [1,0.8,0.5] # Dimensions of the cube (default object)

s = 1               # Start frame of visualisation
offset = 1          # delay in frames between changes 'count' value of array modificator (jumps, strobe effect)
center_space = 1    # adding some space between right and left row of the visualisation
slash = 0           # adding transform for objects in X axis line, looks like "V" char

drivmod = 20.0      # driver "amplifier" (Imprecise column height)
low = 200           # min freq, doesn't work yet (removed broken code)
herz = 20000        # max frequency value, dafault 20000
question = 1        # 1-exponential frequency, 2-linear frequency

# magic, i don't know how exactly it works
# just kidding, I know but I can't explain it
pow = (8/value_x)+1 # parametr for "parabolic with frequency" (?)

# less important settings
ouu = -1            # offset for emptys in Z axis range

########################
# end of basic options #
########################

def drivering():
    obj = bpy.data.objects[nc + "_" + ny + "_" + nx]
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
    if question == 2:
        fmod.coefficients = (0.0, drivmod+(2*(rx+1)))
    else:
        fmod.coefficients = (0.0, drivmod)

def curve_modifier():
    bpy.data.objects[no + "_"  + ny + "_" + nx].animation_data.action.fcurves[2].modifiers.new('STEPPED')
    bpy.data.objects[no + "_"  + ny + "_" + nx].animation_data.action.fcurves[2].modifiers.active.frame_step = offset

#########
# RIGHT #
#########

if stereo == 2 or stereo == 3:
    float_rx = 0 + center_space
    float_ry = 0
    step = 0
    start = s
    for ry in range(0, value_y):
        for rx in range(0, value_x):
            bpy.context.scene.frame_current = start
            bpy.ops.object.add(location=(float_rx + space_x/2, float_ry, ouu))
            bpy.ops.anim.keyframe_insert_menu(type='Scaling')
            bpy.context.area.type = 'GRAPH_EDITOR'
            step2 = step
            if bake == 1:
                if question == 1:
                    step = herz
                    for what in range (0, value_x-rx):
                        step = step / pow
                    bpy.ops.graph.sound_bake(filepath=file_r, low=(step2), high=step)
                elif question == 2: 
                    step = (rx+1)*(herz/value_x)
                    bpy.ops.graph.sound_bake(filepath=file_r, low=(step2), high=step)
            bpy.context.area.type = 'TEXT_EDITOR'
            nx = rx + 1; nx = str(nx)
            ny = ry + 1; ny = str(ny)
            no = "obj_R"
            bpy.context.active_object.name = (no + "_"  + ny + "_" + nx)
            bpy.data.objects[no + "_"  + ny + "_" + nx].animation_data.action.fcurves[0].hide = True
            bpy.data.objects[no + "_"  + ny + "_" + nx].animation_data.action.fcurves[1].hide = True
            bpy.ops.mesh.primitive_cube_add(location=(float_rx + space_x/2, float_ry, 0))
            bpy.ops.transform.resize(value=(scale[0],scale[1],scale[2]))
            bpy.ops.object.transform_apply(scale=True)
            nc = "cub_R"
            bpy.context.active_object.name = (nc + "_" + ny + "_" + nx)
            if bake == 1:
                bpy.ops.object.modifier_add(type='ARRAY')
                bpy.context.active_object.modifiers['Array'].relative_offset_displace[0] = 0
                bpy.context.active_object.modifiers['Array'].relative_offset_displace[2] = space_array
                drivering()
            if offset >= 2:
                curve_modifier()
            float_rx = float_rx+space_x
            float_ry = float_ry+slash
        float_ry = float_ry+space_y-(slash*value_x)
        float_rx = float_rx - space_x * value_x
        start = start+offset
        step = 0

########
# LEFT #
########

if stereo == 1 or stereo == 3:
    float_rx = 0 + center_space
    float_ry = 0
    step = 0
    start = s
    for ry in range(0, value_y):
        for rx in range(0, value_x):
            bpy.context.scene.frame_current = start
            bpy.ops.object.add(location=(-float_rx - space_x/2, float_ry, ouu))
            bpy.ops.anim.keyframe_insert_menu(type='Scaling')
            bpy.context.area.type = 'GRAPH_EDITOR'
            step2 = step
            if bake == 1:
                if question == 1:
                    step = herz
                    for what in range (0, value_x-rx):
                        step = step / pow
                    bpy.ops.graph.sound_bake(filepath=file_l, low=(step2), high=step)
                elif question == 2:
                    step = (rx+1)*(herz/value_x)
                    bpy.ops.graph.sound_bake(filepath=file_l, low=(step2), high=step)
            bpy.context.area.type = 'TEXT_EDITOR'
            nx = rx + 1; nx = str(nx)
            ny = ry + 1; ny = str(ny)
            no = "obj_L"
            bpy.context.active_object.name = (no + "_" + ny + "_" + nx)
            bpy.data.objects[no + "_"  + ny + "_" + nx].animation_data.action.fcurves[0].hide = True
            bpy.data.objects[no + "_"  + ny + "_" + nx].animation_data.action.fcurves[1].hide = True
            bpy.ops.mesh.primitive_cube_add(location=(-float_rx - space_x/2, float_ry, 0))
            bpy.ops.transform.resize(value=(scale[0],scale[1],scale[2]))
            bpy.ops.object.transform_apply(scale=True)
            nc = "cub_L"
            bpy.context.active_object.name = (nc + "_" + ny + "_" + nx)
            if bake == 1:
                bpy.ops.object.modifier_add(type='ARRAY')
                bpy.context.active_object.modifiers['Array'].relative_offset_displace[0] = 0
                bpy.context.active_object.modifiers['Array'].relative_offset_displace[2] = space_array
                drivering()
            if offset >= 2:
                curve_modifier()
            float_rx = float_rx+space_x
            float_ry = float_ry+slash
        float_ry = float_ry+space_y-(slash*value_x)  
        float_rx = float_rx - space_x * value_x
        start = start+offset
        step = 0
