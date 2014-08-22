# little thanks for <mfoxdogg> from #blender
# zmień sobie tylko ścieżki do pliku oraz "value_x" i "value_y" dla kolejno: ilości słupków w rzędzie i ilość rzędów, polecam zacząć od np, 8x4
"""
# comment for you    */ < who wrote this? :V
### comment for me
"""

import bpy

#############
### FILES ###
#############

# dla kanalu lewego,
file_l = "/media/gx-data/Gethiox/Blender/BlenderWork/wizualizator v2/music_left.ogg"
# dla kanalu prawego,
file_r = "/media/gx-data/Gethiox/Blender/BlenderWork/wizualizator v2/music_right.ogg"
#


#################
# basic options #
#################

value_x = 32        # 14 ilosc slupkow w rzedzie dla kazdego z kanalow,
value_y = 16        # 4 ilosc slupkow w kolumnie

bake = 1            # bake sound? 0-no, 1-yes
question = 1        # 1-parabolic, 2-linear
herz = 20000        # max frequency
space_x = 3         # space x
space_y = 3         # space y 
space_array = 1.2   # array "z" parametr
ouu = -1            # offset for empty
pow = (8/value_x)+1 ### parabolic "/' value: 2, 1.8, 1.6 etc

### pow for value_x==32 = 1.25
### pow for value_x==16 = 1.5
### pow for value_x==8 = 2

scale = [1,0.8,0.5] # xyz cube scale
s = 1               # start keyframe
offset = 1          # delay for animation next columns (1 looks the best)
center_space = 1    # additional center space - left and right chanel

################
# Bake details #
################

filter_blender=False
filter_image=False
filter_movie=True
filter_python=False
filter_font=False
filter_sound=True
filter_text=False
filter_btx=False
filter_collada=False
filter_folder=True
filemode=9
attack=0.5 ###
release=0.2
threshold=0.0
accumulate=False
use_additive=False
square=False
sthreshold=0.1

"""
DEFAULT:

filter_blender=False
filter_image=False
filter_movie=True
filter_python=False
filter_font=False
filter_sound=True
filter_text=False
filter_btx=False
filter_collada=False
filter_folder=True
filemode=9
attack=0.015
release=0.2
threshold=0.0
accumulate=False
use_additive=False
square=False
sthreshold=0.1
"""

############# 
# Podprogram #
#############

def drivering():
    rig = bpy.data.objects[nc + "_" + ny + "_" + nx]
    fcurve = rig.modifiers['Array'].driver_add('count')
    drv = fcurve.driver
    drv.type = 'AVERAGE'
    
    var = drv.variables.new()
    var.name = 'name'
    var.type = 'TRANSFORMS'
    
    targ = var.targets[0]
    targ.id = bpy.data.objects[no + "_"  + ny + "_" + nx]
    targ.transform_type = 'SCALE_Z'
    targ.bone_target = 'Driver'
    
    
    fmod = fcurve.modifiers[0]
    
    fmod.poly_order = 1
    
    
    fmod.coefficients = (0.0, 100.0)


############# 
# zerowanie #
#############

float_rx = 0 + center_space
float_ry = 0
step = 0
start = s

for ry in range(0, value_y):
    for rx in range(0, value_x):
        bpy.context.scene.frame_current = start #
        
        bpy.ops.object.add(location=(float_rx + space_x/2, float_ry, ouu), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        bpy.ops.anim.keyframe_insert_menu(type='Scaling')
        
        bpy.context.area.type = 'GRAPH_EDITOR'
        
        step2 = step
        if bake == 1:
            if question == 1:
                step = herz
                for what in range (0, value_x-rx):
                    step = step / pow
                
                bpy.ops.graph.sound_bake(filepath=file_r, low=(step2+1), high=step, filter_blender=filter_blender, filter_image=filter_image, filter_movie=filter_movie, filter_python=filter_python, filter_font=filter_font, filter_sound=filter_sound, filter_text=filter_text, filter_btx=filter_btx, filter_collada=filter_collada, filter_folder=filter_folder, filemode=filemode, attack=attack, release=release, threshold=threshold, accumulate=accumulate, use_additive=use_additive, square=square, sthreshold=sthreshold)
            elif question == 2:
                step = (rx+1)*(herz/value_x)
                bpy.ops.graph.sound_bake(filepath=file_r, low=(step2+1), high=step, filter_blender=filter_blender, filter_image=filter_image, filter_movie=filter_movie, filter_python=filter_python, filter_font=filter_font, filter_sound=filter_sound, filter_text=filter_text, filter_btx=filter_btx, filter_collada=filter_collada, filter_folder=filter_folder, filemode=filemode, attack=attack, release=release, threshold=threshold, accumulate=accumulate, use_additive=use_additive, square=square, sthreshold=sthreshold)
            else:
                error
                
        bpy.context.area.type = 'TEXT_EDITOR'
        
        nx = rx + 1; nx = str(nx)
        ny = ry + 1; ny = str(ny)
        no = "obj_R"
        bpy.context.active_object.name = (no + "_"  + ny + "_" + nx)
        
        bpy.ops.mesh.primitive_cube_add(location=(float_rx + space_x/2, float_ry, 0), layers=(False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        bpy.ops.transform.resize(value=(scale[0],scale[1],scale[2]))
        bpy.ops.object.transform_apply(scale=True)
        
        nc = "cub_R"
        bpy.context.active_object.name = (nc + "_" + ny + "_" + nx)
        
        bpy.ops.object.modifier_add(type='ARRAY')
        bpy.context.active_object.modifiers['Array'].relative_offset_displace[0] = 0
        bpy.context.active_object.modifiers['Array'].relative_offset_displace[2] = space_array
        drivering()
        
        ###################
        bpy.context.area.type = 'GRAPH_EDITOR'
        bpy.context.area.type = 'TEXT_EDITOR'
        ###################       
        
        float_rx = float_rx+space_x
        ####
    float_ry = float_ry+space_y
    float_rx = float_rx - space_x * value_x
    start = start+offset
    step = 0

######################################
######################################

float_rx = 0 + center_space
float_ry = 0
step = 0
start = s

for ry in range(0, value_y):
    for rx in range(0, value_x):
        bpy.context.scene.frame_current = start #
        
        bpy.ops.object.add(location=(-float_rx - space_x/2, float_ry, ouu), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        bpy.ops.anim.keyframe_insert_menu(type='Scaling')
        
        bpy.context.area.type = 'GRAPH_EDITOR'
        
        step2 = step
        if bake == 1:
            if question == 1:
                step = herz
                for what in range (0, value_x-rx):
                    step = step / pow
                
                bpy.ops.graph.sound_bake(filepath=file_l, low=(step2+1), high=step, filter_blender=filter_blender, filter_image=filter_image, filter_movie=filter_movie, filter_python=filter_python, filter_font=filter_font, filter_sound=filter_sound, filter_text=filter_text, filter_btx=filter_btx, filter_collada=filter_collada, filter_folder=filter_folder, filemode=filemode, attack=attack, release=release, threshold=threshold, accumulate=accumulate, use_additive=use_additive, square=square, sthreshold=sthreshold)
            elif question == 2:
                step = (rx+1)*(herz/value_x)
                bpy.ops.graph.sound_bake(filepath=file_l, low=(step2+1), high=step, filter_blender=filter_blender, filter_image=filter_image, filter_movie=filter_movie, filter_python=filter_python, filter_font=filter_font, filter_sound=filter_sound, filter_text=filter_text, filter_btx=filter_btx, filter_collada=filter_collada, filter_folder=filter_folder, filemode=filemode, attack=attack, release=release, threshold=threshold, accumulate=accumulate, use_additive=use_additive, square=square, sthreshold=sthreshold)
            else:
                error
                
        bpy.context.area.type = 'TEXT_EDITOR'
        
        nx = rx + 1; nx = str(nx)
        ny = ry + 1; ny = str(ny)
        no = "obj_L"
        bpy.context.active_object.name = (no + "_" + ny + "_" + nx)
        
        bpy.ops.mesh.primitive_cube_add(location=(-float_rx - space_x/2, float_ry, 0), layers=(False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        bpy.ops.transform.resize(value=(scale[0],scale[1],scale[2]))
        bpy.ops.object.transform_apply(scale=True)
        
        nc = "cub_L"
        bpy.context.active_object.name = (nc + "_" + ny + "_" + nx) ## thanks for this to <mfoxdogg> from #blender
        
        bpy.ops.object.modifier_add(type='ARRAY')
        bpy.context.active_object.modifiers['Array'].relative_offset_displace[0] = 0
        bpy.context.active_object.modifiers['Array'].relative_offset_displace[2] = space_array
        drivering()
        
        ###################
        bpy.context.area.type = 'GRAPH_EDITOR'
        bpy.context.area.type = 'TEXT_EDITOR'
        ###################       
        
        float_rx = float_rx+space_x
        ####
    float_ry = float_ry+space_y
    float_rx = float_rx - space_x * value_x
    start = start+offset
    step = 0

step = 0
start = s
float_rx = 0 + center_space
float_ry = 0

