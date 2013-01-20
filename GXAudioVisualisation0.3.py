# by Gethiox, CC-BY, pre-beta-alpha version

import bpy

#############
### FILES ###
#############

"""
we have two files because blender "not see" mutli chanels in audio files.
You can insert here two chanels, before separate it in e.g. audacity,
or insert original file for two chanel (mono visulation)

please testing with "bake = 0" - it is faster,
or "bake = 1" for testing bake parametrs and final work.
"""

# left file chanel ("C:\Folder\music.flac" or "/media/music.ogg") 
file_l = "/media/music.ogg"
# right file chanel
file_r = "/media/music.ogg"

#################
# basic options #
#################

bake = 1            # bake sound? 0-no, 1-yes ("no" for testing "how it looks in space?")

value_x = 8         # cubes in X axis for one chanel
value_y = 1         # cubes in Y axis for one chanel (must be over 0!)

space_x = 3         # space for any objects in X axis
space_y = 3         # space for any objects in Y axis

space_array = 1.2   # array space :) (for new, "copying" objects of array, Z axis)
scale = [1,0.8,0.5] # cube scale

s = 1               # what frame is starting animation?
offset = 2          # delay (frames) for next changes of array (jumps)
center_space = 1    # add center space, left chanel move to left, right move to right direction
slash = 0           # add move for objects in X axis line, like char "V" looks
drivmod = 20.0      # driver "amplifier" (Imprecise column height)

herz = 20000        # max frequency value, dafault 20000
pow = (8/value_x)+1 # parametr for "parabolic with frequency"

### less important settings
ouu = -1            # offset for emptys in Z axis range
question = 1        # 1-parabolic frequency, 2-linear (doesn't work yet!)


# add driver and change properties
def drivering():
    obj = bpy.data.objects[nc + "_" + ny + "_" + nx]
    mdf = obj.modifiers['Array'].driver_add('count')
    drv = mdf.driver
    
    drv.type = 'AVERAGE'
    
    var = drv.variables.new()
    
    # change Variable name
    var.name = 'name'
    # change Variable type
    var.type = 'TRANSFORMS'
    
    targ = var.targets[0]
    targ.id = bpy.data.objects[no + "_"  + ny + "_" + nx]
    
    # change variable transform type
    targ.transform_type = 'SCALE_Z'
    # change variable target
    targ.bone_target = 'Driver'
    
    fmod = mdf.modifiers[0]

    # change first modifier parametr "Poly Prder"
    fmod.poly_order = 1
    
    # parabolic power for linear bake question
    if question == 2:
        fmod.coefficients = (0.0, 100+(20*(rx+1)))
    
    # standard value
    else:
        fmod.coefficients = (0.0, drivmod)

# add "stepped" modifier for curve "Z" from sound baking
def curve_modifier():
    bpy.data.objects[no + "_"  + ny + "_" + nx].animation_data.action.fcurves[2].modifiers.new('STEPPED')
    bpy.data.objects[no + "_"  + ny + "_" + nx].animation_data.action.fcurves[2].modifiers.active.frame_step = offset
    

# float_rx - value X axis for insert objects + canter_space - insert "extra" space in center
float_rx = 0 + center_space
# float_ry - value Y axis for insert objects
float_ry = 0
# reset value
step = 0
# set start frame value for float value
start = s

for ry in range(0, value_y):
    for rx in range(0, value_x):
        # set start frame for scene
        bpy.context.scene.frame_current = start
        # add Empty in first layer
        bpy.ops.object.add(location=(float_rx + space_x/2, float_ry, ouu))
        # add scaling keyframe for active scene frame
        bpy.ops.anim.keyframe_insert_menu(type='Scaling')
        
        # change to "graph editro" for baking
        bpy.context.area.type = 'GRAPH_EDITOR'
        
        # (bake sound parametrs) step2 for first freq value, step for second freq value
        step2 = step
        
        # bake question
        if bake == 1:
            # parabolic with frequency
            if question == 1:
                step = herz
                for what in range (0, value_x-rx):
                    step = step / pow
                bpy.ops.graph.sound_bake(filepath=file_r, low=(step2), high=step)
            # linear (later with parabolic power in "def drivering():"
            elif question == 2: 
                step = (rx+1)*(herz/value_x)
                bpy.ops.graph.sound_bake(filepath=file_r, low=(step2), high=step)
                    
        # back to this text editor        
        bpy.context.area.type = 'TEXT_EDITOR'
        
        # create parametrs for name generating
        nx = rx + 1; nx = str(nx)
        ny = ry + 1; ny = str(ny)
        no = "obj_R"
        # change active empty name
        bpy.context.active_object.name = (no + "_"  + ny + "_" + nx)
        
        # hide curve X and Y
        bpy.data.objects[no + "_"  + ny + "_" + nx].animation_data.action.fcurves[0].hide = True
        bpy.data.objects[no + "_"  + ny + "_" + nx].animation_data.action.fcurves[1].hide = True
        
        # add new cube, scond layer
        bpy.ops.mesh.primitive_cube_add(location=(float_rx + space_x/2, float_ry, 0))
        # scaling cube, (scale float parametrs)
        bpy.ops.transform.resize(value=(scale[0],scale[1],scale[2]))
        # apply scaling (active size is changing for default value 1 in object editor)
        bpy.ops.object.transform_apply(scale=True)
        
        # add nev name parametrs for cube
        nc = "cub_R"
        # change active cube name
        bpy.context.active_object.name = (nc + "_" + ny + "_" + nx)
        
        # add "array" modifier, change "copying" parametr for Z axis, set array space
        if bake == 1:
            bpy.ops.object.modifier_add(type='ARRAY')
            bpy.context.active_object.modifiers['Array'].relative_offset_displace[0] = 0
            bpy.context.active_object.modifiers['Array'].relative_offset_displace[2] = space_array
            drivering()
            
        
        if offset >= 2:
            curve_modifier()
        
        # adding space for loop end (X axis)
        float_rx = float_rx+space_x
        float_ry = float_ry+slash
        
    # adding space for loop end (Y axis)
    float_ry = float_ry+space_y-(slash*value_x)
    # reset float value for next line of objects
    float_rx = float_rx - space_x * value_x
    # add "frames" value for next line of objects
    start = start+offset
    step = 0

######################################

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

step = 0
start = s
float_rx = 0 + center_space
float_ry = 0

