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

import bpy
import math

#__author__ = "Xevaquor"

base = math.pow(2, (1. / 3))

def compute(xarg):
    """
    Computes value of tercja function ignoring set bounds
    :param xarg: x argument for func
    :return: computed y value
    """
    return base ** xarg

def compute_inverse(yarg):
    """
    Computes inverse of tercja
    :param yarg: y argument for func
    :return: corresponding x value
    """
    # non positive numbers are out of domain of log func
    #we are silently ignoring it
    if yarg <= 0:
        return 0
    return math.log(yarg, base)


def get_value_from_x(xx, minimum_x, maximum_x):
    """
    Computes value from percentage in interval. For more details please see:
    https://github.com/Xevaquor/GXAudioVisualisation/wiki/Tercja
    Eg: .42 means 42%
    :param xx: Percent in interval. Must be in range [0,1]
    :param minimum_x: Lower x bound
    :param maximum_x: Upper x bound
    :return: corresponding value of Tercja func
    """
    assert (0 <= xx <= 1)
    return compute(xx * (maximum_x - minimum_x) + minimum_x)

#\__author__ = "Xevaquor"

def initprop():
    bpy.types.Scene.gx_slash_rotate = bpy.props.BoolProperty(
        name = "Rotation",
        description = "Slash Rotation",
        update=update_slash)
    
    bpy.types.Scene.gx_slash = bpy.props.FloatProperty(
        name = "Slash",
        default = 0.0,
        description = "Enter an float",
        update=update_slash)   
            
    bpy.types.Scene.gx_zenit = bpy.props.BoolProperty(
        name = "Zenit",
        description = "Zenit")
            
    bpy.types.Scene.gx_accumulate = bpy.props.BoolProperty(
        name = "Accumulate",
        description = "Accumulate")

    bpy.types.Scene.gx_additive = bpy.props.BoolProperty(
        name = "Use additive",
        description = "Use additive")

    bpy.types.Scene.gx_square = bpy.props.BoolProperty(
        name = "Square",
        description = "Square")

    bpy.types.Scene.gx_sthreshold = bpy.props.FloatProperty(
        name = "Sthreshold",
        default = 0.1)    

    bpy.types.Scene.gx_threshold = bpy.props.FloatProperty(
        name = "Threshold",
        default = 0.0)    

    bpy.types.Scene.gx_release = bpy.props.FloatProperty(
        name = "Release",
        default = 0.2)    

    bpy.types.Scene.gx_attack = bpy.props.FloatProperty(
        name = "Attack",
        default = 0.005)    

    bpy.types.Scene.gx_cube_scale_x = bpy.props.FloatProperty(
        name = "Scale X",
        default = 1.0,
        min = 0, 
        step = 1,
        precision = 2,
        description = "Enter an float",
        update=update_scale)    

    bpy.types.Scene.gx_cube_scale_y = bpy.props.FloatProperty(
        name = "Scale Y",
        default = 1.0,
        min = 0, 
        step = 1,
        precision = 2,
        description = "Enter an float",
        update=update_scale)   

    bpy.types.Scene.gx_cube_scale_z = bpy.props.FloatProperty(
        name = "Scale Z",
        default = 5.6,
        min = 0, 
        step = 1,
        precision = 2,
        description = "Enter an float",
        update=update_scale)       

    bpy.types.Scene.gx_type = bpy.props.EnumProperty(
        items = [('0', 'Array', 'array'),
                 ('1', 'Object scaling', 'object'),
                 ('2', 'Center object scaling', 'center_object')],
        name = "Visualisation Type",
        update=update_channels)      

    bpy.types.Scene.gx_freq_debug = bpy.props.BoolProperty(
        name = "Freq Debug",
        description = "Enter an bool lul")

    bpy.types.Scene.gx_driver_power = bpy.props.FloatProperty(
        name = "Driver Power",
        default = 20.0,
        min = 0, 
        step = 5,
        precision = 2,
        description = "Enter an float",
        update=update_drivers3)     
    
    bpy.types.Scene.gx_mode = bpy.props.EnumProperty(
        items = [('0', 'Logarithm', 'log'),
                 ('1', 'Linear', 'linear'),
                 ('2', 'Tercja (recomended)', 'tercja')],
        name = "Frequency Mode")  
    
    bpy.types.Scene.gx_min_freq = bpy.props.FloatProperty(
        name = "Min Freq",
        default = 100.0,
        min = 0, 
        step = 1000,
        precision = 2,
        description = "Enter an float")    
            
    bpy.types.Scene.gx_max_freq = bpy.props.FloatProperty(
        name = "Max Freq",
        default = 20000.0,
        min = 0, 
        step = 1000,
        precision = 2,
        description = "Enter an float")        
    
    bpy.types.Scene.gx_space_array = bpy.props.FloatProperty(
        name = "Space Array",
        default = 1.5,
        min = 0, 
        step = 1,
        precision = 2,
        description = "Enter an float",
        update=update_space_array)        
    
    bpy.types.Scene.gx_start = bpy.props.IntProperty(
        name = "Start Frame",
        default = 1,
        min = 1,
        description = "Enter an integer")
    
    bpy.types.Scene.gx_left_file = bpy.props.StringProperty(
        name = "Left File",
        #default = "",
        description = "Define path of the left channel file",
        subtype = 'FILE_PATH')

    bpy.types.Scene.gx_right_file = bpy.props.StringProperty(
        name = "Right File",
        #default = "",
        description = "Define path of the right channel file",
        subtype = 'FILE_PATH')    

    bpy.types.Scene.gx_scale_x = bpy.props.FloatProperty(
        name = "Scale X",
        default = 0.7,
        min = 0, 
        step = 1,
        precision = 2,
        description = "Enter an float",
        update=update_scale)    

    bpy.types.Scene.gx_scale_y = bpy.props.FloatProperty(
        name = "Scale Y",
        default = 0.6,
        min = 0, 
        step = 1,
        precision = 2,
        description = "Enter an float",
        update=update_scale)   

    bpy.types.Scene.gx_scale_z = bpy.props.FloatProperty(
        name = "Scale Z",
        default = 0.4,
        min = 0, 
        step = 1,
        precision = 2,
        description = "Enter an float",
        update=update_scale)                   
    
    bpy.types.Scene.gx_channels = bpy.props.EnumProperty(
        items = [('0', 'Stereo', 'Left and Right channel'),
                 ('1', 'Left', 'Left channel'),
                 ('2', 'Right', 'Right channel')],
        name = "Channels",
        update=update_channels)
        
    bpy.types.Scene.gx_center_space = bpy.props.FloatProperty(
        name = "Center Space",
        default = 2.0,
        min = 0, 
        description = "Enter an float",
        update=update_space_x)    
    
    bpy.types.Scene.gx_space_x = bpy.props.FloatProperty(
        name = "Space X",
        default = 2.0,
        min = 0, 
        step = 1,
        precision = 2,
        description = "Enter an float",
        update=update_space_x)
    
    bpy.types.Scene.gx_count_x = bpy.props.IntProperty(
        name = "Count X",
        default = 5,
        min = 1,
        options={'ANIMATABLE'},
        description = "Enter an integer",
        update=update_count)
    
def initpropvalues():
    bpy.context.scene['gx_space_x'] = 0.2
    bpy.context.scene['gx_count_x'] = 32
    bpy.context.scene['gx_center_space'] = 0.2
    bpy.context.scene['gx_channels'] = 2
    bpy.context.scene['gx_scale_x'] = 0.07
    bpy.context.scene['gx_scale_y'] = 0.06
    bpy.context.scene['gx_scale_z'] = 0.04
    bpy.context.scene['gx_start'] = 100
    bpy.context.scene['gx_space_array'] = 1.7
    bpy.context.scene['gx_min_freq'] = 10.0
    bpy.context.scene['gx_max_freq'] = 20000.0  
    bpy.context.scene['gx_mode'] = 2
    bpy.context.scene['gx_driver_power'] = 20.0
    bpy.context.scene['gx_freq_debug'] = False
    bpy.context.scene['gx_type'] = 0    
    bpy.context.scene['gx_cube_scale_x'] = 0.07
    bpy.context.scene['gx_cube_scale_y'] = 0.06
    bpy.context.scene['gx_cube_scale_z'] = 0.20
    bpy.context.scene['gx_zenit'] = False
    bpy.context.scene['gx_slash'] = 0.0
    bpy.context.scene['gx_slash_rotate'] = True
    
    bpy.context.scene['gx_attack'] = 0.005 
    bpy.context.scene['gx_release'] = 0.2 
    bpy.context.scene['gx_threshold'] = 0.0
    bpy.context.scene['gx_accumulate'] = False
    bpy.context.scene['gx_additive'] = False
    bpy.context.scene['gx_square'] = False
    bpy.context.scene['gx_sthreshold'] = 0.1
    
    bpy.context.scene['gx_init'] = 1

calc = 1

class GXAVPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "GXAudioVisualisation"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        row = layout.row()
        row.operator("object.gx_create_base", icon="MODIFIER", text="(re)Create Visualizer Base")
        try:
            if bpy.context.scene['gx_init'] == 1:
                layout.label(text="Parameters:", icon="UI")
                row = layout.row()
                row.prop(scene, "gx_center_space") 
                row = layout.row(align=True)
                row.prop(scene, "gx_count_x")        
                row.prop(scene, "gx_space_x")
                row = layout.row() 
                row.prop(scene, "gx_slash")
                row.prop(scene, "gx_slash_rotate", icon="MAN_ROT")  


                try:
                    if bpy.context.scene['gx_type'] == 0:
                        row = layout.row()
                        row.prop(scene, "gx_type", icon="MOD_ARRAY", text="Mode")                         
                        split = layout.split()
                        col = split.column()
                        col.label(text="Object Scale:", icon="MANIPUL")
                        col = split.column(align=True)
                        col.prop(scene, 'gx_scale_x', text="X")
                        col.prop(scene, 'gx_scale_y', text="Y")
                        col.prop(scene, 'gx_scale_z', text="Z")
                        row = layout.row()
                        row.label(text="Array modifier space:", icon="UNLINKED")
                        row.prop(scene, "gx_space_array")
                    else:
                        row = layout.row()
                        row.prop(scene, "gx_type", icon="MESH_CUBE", text="Mode")                             
                        split = layout.split()
                        col = split.column()
                        col.label(text="Object Scale:", icon="MANIPUL")
                        col = split.column(align=True)
                        col.prop(scene, 'gx_cube_scale_x', text="X")
                        col.prop(scene, 'gx_cube_scale_y', text="Y")
                        #col.prop(scene, 'gx_cube_scale_z', text="Z")
                        col.label(text="") 
                        row = layout.row()
                        row.label(text="")                          
                except:
                    layout.label(text="Missing variables, please report bug")

                row = layout.row()
                row = layout.row()
                row.prop(scene, "gx_driver_power")        
                
                row = layout.row()
                box = layout.box()
                box.label("Channels to bake and audio files path:", icon="SOUND")
                if bpy.context.scene['gx_channels'] == 0:
                    box.prop(scene, "gx_channels", icon="ARROW_LEFTRIGHT")
                elif bpy.context.scene['gx_channels'] == 1:
                    box.prop(scene, "gx_channels", icon="BACK")
                elif bpy.context.scene['gx_channels'] == 2:
                    box.prop(scene, "gx_channels", icon="FORWARD")
                box.prop(scene, "gx_left_file")
                box.prop(scene, "gx_right_file")     
                row = layout.row()    
                row.prop(scene, "gx_mode", icon="RNDCURVE")
                row = layout.row()  
                row.prop(scene, "gx_start")
                row = layout.row()        
                row.prop(scene, "gx_min_freq")                       
                row.prop(scene, "gx_max_freq")      
                #row = layout.row()
                #row.prop(scene, "gx_freq_debug")  
                row = layout.row()
                row.operator("object.gx_bake", icon="RADIO", text="(re)Bake animation data")    
                row = layout.row() 
                row.label(text="")

                box = layout.box()
                box.label(text="'Bake Sound to F-Curves' options:", icon="UI")
                split = box.split()
                col = split.column(align=True)    
                col.prop(scene, 'gx_attack')
                col.prop(scene, 'gx_release')
                col = split.column(align=True)  
                col.prop(scene, 'gx_threshold')
                col.prop(scene, 'gx_sthreshold')
                split = box.split()
                col = split.column()
           
                col.prop(scene, 'gx_accumulate')
                col = split.column()
                col.prop(scene, 'gx_additive')
                col = split.column()        
                col.prop(scene, 'gx_square')
                #row = layout.row()
                #row.prop(scene, 'gx_zenit')
                row = layout.row()
                row.operator("object.gx_init_variables", icon="COLOR", text="Init/Reset Variables")   
        except:
            False

def gxstart():
    try: 
        bpy.context.scene['gx_init']
    except:
        initpropvalues()        
   
    bpy.ops.object.select_all(action="DESELECT")
    try:
        for i in range(bpy.context.scene['gx_count_x']):
            name = "bar_r_" + str(i+1)
            bpy.data.objects[name].select = True  
        bpy.ops.object.delete()    
    except:
        False
    try:
        for i in range(bpy.context.scene['gx_count_x']):  
            name = "bar_l_" + str(i+1)      
            bpy.data.objects[name].select = True          
        bpy.ops.object.delete()
    except:
        False
        
    for i in range(bpy.context.scene['gx_count_x']):
        generate_objects(i)
        
        
    if bpy.context.scene['gx_channels'] == 1 or bpy.context.scene['gx_channels'] == 0:    
        bpy.context.scene.objects.active = bpy.data.objects["bar_l_" + str(bpy.context.scene['gx_count_x'])]
        bpy.ops.object.select_pattern(pattern="bar_l_" + str(bpy.context.scene['gx_count_x']))
    if bpy.context.scene['gx_channels'] == 2 or bpy.context.scene['gx_channels'] == 0:
        bpy.context.scene.objects.active = bpy.data.objects["bar_r_" + str(bpy.context.scene['gx_count_x'])]
        bpy.ops.object.select_pattern(pattern="bar_r_" + str(bpy.context.scene['gx_count_x']))   
            
    bpy.types.Scene.allobjects = bpy.context.scene['gx_count_x']
    update_drivers()  
    update_slash(True, True)
    update_space_x(True, True)

def gxbake():
    ### calculate for tercja
    tercja_x_min = compute_inverse(bpy.context.scene['gx_min_freq'])
    tercja_x_max = compute_inverse(bpy.context.scene['gx_max_freq'])
    tercja_step = (1/bpy.context.scene['gx_count_x'])
    ###

    try:
        bpy.types.Scene.bakedobjects
    except:
        bpy.types.Scene.bakedobjects = 0
        
    bpy.ops.object.select_all(action="DESELECT")
    try:
        for i in range(bpy.types.Scene.bakedobjects):
            name = "obj_r_" + str(i+1)
            bpy.data.objects[name].select = True  
        bpy.ops.object.delete()    
    except:
        False
    try:
        for i in range(bpy.types.Scene.bakedobjects):  
            name = "obj_l_" + str(i+1)      
            bpy.data.objects[name].select = True          
        bpy.ops.object.delete()
    except:
        False 

    b = bpy.context.scene['gx_min_freq']
    c = (bpy.context.scene['gx_max_freq']-bpy.context.scene['gx_min_freq'])/bpy.context.scene['gx_count_x']
    
    bpy.context.window_manager.progress_begin(0, 100)
    bpy.context.window_manager.progress_update(0)
    for i in range(bpy.context.scene['gx_count_x']):
        if bpy.context.scene['gx_mode'] == 2:
            a = b
            b = get_value_from_x((i+1)*tercja_step, tercja_x_min, tercja_x_max)    
        elif bpy.context.scene['gx_mode'] == 1:
            b = ((bpy.context.scene['gx_max_freq']-bpy.context.scene['gx_min_freq'])-c*(bpy.context.scene['gx_count_x']-i-1)) + bpy.context.scene['gx_min_freq']
            a = ((bpy.context.scene['gx_max_freq']-bpy.context.scene['gx_min_freq'])-c*(bpy.context.scene['gx_count_x']-i)) + bpy.context.scene['gx_min_freq']
        elif bpy.context.scene['gx_mode'] == 0:
            b = ((1 - math.log(bpy.context.scene['gx_count_x']-i, bpy.context.scene['gx_count_x']+1)) * (bpy.context.scene['gx_max_freq']-bpy.context.scene['gx_min_freq'])) + bpy.context.scene['gx_min_freq']
            a = ((1 - math.log(bpy.context.scene['gx_count_x']-i+1, bpy.context.scene['gx_count_x']+1)) * (bpy.context.scene['gx_max_freq']-bpy.context.scene['gx_min_freq'])) + bpy.context.scene['gx_min_freq']

        print(str(i) + ": " + str(round(a, 1)) + " Hz - " + str(round(b, 1)) + " Hz")
        if bpy.context.scene['gx_channels'] == 1 or bpy.context.scene['gx_channels'] == 0:
            bpy.context.scene.frame_current = bpy.context.scene['gx_start']
            bpy.ops.object.add(location=(-(i*bpy.context.scene['gx_space_x'] + bpy.context.scene['gx_center_space']/2), bpy.context.scene['gx_slash'] * i, -2))
            name = "obj_l_" + str(i+1)            
            bpy.context.active_object.name = name
            
            bpy.ops.anim.keyframe_insert_menu(type='Scaling')
            if calc == 1:
                bpy.context.area.type = 'GRAPH_EDITOR'
                try:
                    bpy.ops.graph.sound_bake(filepath=bpy.context.scene['gx_left_file'],
                        low=a, high=b,
                        attack = bpy.context.scene['gx_attack'],
                        release = bpy.context.scene['gx_release'],
                        threshold = bpy.context.scene['gx_threshold'],
                        use_accumulate = bpy.context.scene['gx_accumulate'],
                        use_additive = bpy.context.scene['gx_additive'],
                        use_square = bpy.context.scene['gx_square'],
                        sthreshold = bpy.context.scene['gx_sthreshold']) 
                except:
                    False
                bpy.context.area.type = 'PROPERTIES'
            
            if bpy.context.scene['gx_channels'] == 0:
                bpy.context.window_manager.progress_update((i+0.5)/bpy.context.scene['gx_count_x'])

            if bpy.context.scene['gx_freq_debug'] == 1:
                bpy.ops.object.add(location=(-(i*bpy.context.scene['gx_space_x'] + bpy.context.scene['gx_center_space']/2), bpy.context.scene['gx_slash'] * i, -4))
                name = (str(i) + ": " + str(round(a, 1)) + " Hz - " + str(round(b, 1)) + " Hz")
                bpy.context.active_object.name = name            
            
        if bpy.context.scene['gx_channels'] == 2 or bpy.context.scene['gx_channels'] == 0:
            bpy.context.scene.frame_current = bpy.context.scene['gx_start']
            bpy.ops.object.add(location=(i*bpy.context.scene['gx_space_x'] + bpy.context.scene['gx_center_space']/2, bpy.context.scene['gx_slash'] * i, -2))
            name = "obj_r_" + str(i+1)
            bpy.context.active_object.name = name
            
            bpy.ops.anim.keyframe_insert_menu(type='Scaling')
            if calc == 1:
                bpy.context.area.type = 'GRAPH_EDITOR'
                try:
                    bpy.ops.graph.sound_bake(filepath=bpy.context.scene['gx_right_file'],
                        low=a, high=b,
                        attack = bpy.context.scene['gx_attack'],
                        release = bpy.context.scene['gx_release'],
                        threshold = bpy.context.scene['gx_threshold'],
                        use_accumulate = bpy.context.scene['gx_accumulate'],
                        use_additive = bpy.context.scene['gx_additive'],
                        use_square = bpy.context.scene['gx_square'],
                        sthreshold = bpy.context.scene['gx_sthreshold']) 
                except:
                    False
                bpy.context.area.type = 'PROPERTIES'

            if bpy.context.scene['gx_channels'] == 0:
                bpy.context.window_manager.progress_update((i+1)/bpy.context.scene['gx_count_x'])

            if bpy.context.scene['gx_freq_debug'] == 1:
                bpy.ops.object.add(location=(i*bpy.context.scene['gx_space_x'] + bpy.context.scene['gx_center_space']/2, bpy.context.scene['gx_slash'] * i, -4))
                name = (str(i) + ": " + str(round(a, 1)) + " Hz - " + str(round(b, 1)) + " Hz")
                bpy.context.active_object.name = name

        if bpy.context.scene['gx_channels'] == 1 or bpy.context.scene['gx_channels'] == 2:
            bpy.context.window_manager.progress_update((i+1)/bpy.context.scene['gx_count_x'])        

    bpy.context.window_manager.progress_end()
    bpy.types.Scene.bakedobjects = bpy.context.scene['gx_count_x']    

class GxInitVariables(bpy.types.Operator):
 
    bl_idname = "object.gx_init_variables"
    bl_label = "GxInitVariables"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        initpropvalues()
        return {'FINISHED'}
    
class GxCreateBase(bpy.types.Operator):
 
    bl_idname = "object.gx_create_base"
    bl_label = "GxCreateBase"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        gxstart()
        return {'FINISHED'}
    
class GxBake(bpy.types.Operator):
 
    bl_idname = "object.gx_bake"
    bl_label = "GxBake"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        gxbake()
        update_drivers()

        return {'FINISHED'}
    
def update_space_array(self, context):
    for i in range(bpy.context.scene['gx_count_x']):
        if bpy.context.scene['gx_channels'] == 1 or bpy.context.scene['gx_channels'] == 0:        
            name = "bar_l_" + str(i+1)
            bpy.data.objects[name].modifiers['Array'].relative_offset_displace[2] = bpy.context.scene['gx_space_array']            
        if bpy.context.scene['gx_channels'] == 2 or bpy.context.scene['gx_channels'] == 0:
            name = "bar_r_" + str(i+1)
            bpy.data.objects[name].modifiers['Array'].relative_offset_displace[2] = bpy.context.scene['gx_space_array']

def update_slash(self, context):    
    for i in range(bpy.context.scene['gx_count_x']):
        if bpy.context.scene['gx_channels'] == 1 or bpy.context.scene['gx_channels'] == 0:        
            name = "bar_l_" + str(i+1)
            bpy.data.objects[name].location[1] = bpy.context.scene['gx_slash'] * i
            if bpy.context.scene['gx_slash_rotate'] == True:
                bpy.data.objects[name].rotation_euler[2] = -math.asin(bpy.context.scene['gx_slash']/math.sqrt(math.pow(bpy.context.scene['gx_space_x'],2) + math.pow(bpy.context.scene['gx_slash'],2)))
            else:
                bpy.data.objects[name].rotation_euler[2] = 0
        if bpy.context.scene['gx_channels'] == 2 or bpy.context.scene['gx_channels'] == 0:
            name = "bar_r_" + str(i+1)
            bpy.data.objects[name].location[1] = bpy.context.scene['gx_slash'] * i
            if bpy.context.scene['gx_slash_rotate'] == True:
                bpy.data.objects[name].rotation_euler[2] = math.asin(bpy.context.scene['gx_slash']/math.sqrt(math.pow(bpy.context.scene['gx_space_x'],2) + math.pow(bpy.context.scene['gx_slash'],2)))  
            else:
                bpy.data.objects[name].rotation_euler[2] = 0      
    try:
        bpy.types.Scene.bakedobjects
        for i in range(bpy.types.Scene.bakedobjects):
            if bpy.context.scene['gx_channels'] == 1 or bpy.context.scene['gx_channels'] == 0:        
                name = "obj_l_" + str(i+1)
                bpy.data.objects[name].location[1] = bpy.context.scene['gx_slash'] * i
            if bpy.context.scene['gx_channels'] == 2 or bpy.context.scene['gx_channels'] == 0:
                name = "obj_r_" + str(i+1)
                bpy.data.objects[name].location[1] = bpy.context.scene['gx_slash']  * i
    except:
        False                

def drivering(i):
    if bpy.context.scene['gx_channels'] == 1 or bpy.context.scene['gx_channels'] == 0:         
        name = "bar_l_" + str(i+1)
        name2 = "obj_l_" + str(i+1)
        try:
            bpy.data.objects[name2]
            if bpy.context.scene['gx_type'] == 0:
                try:
                    bpy.data.objects[name].modifiers['Array'].driver_remove('count')
                except:
                    False   
                obj = bpy.data.objects[name] #def drivering
                mdf = obj.modifiers['Array'].driver_add('count')
                drv = mdf.driver
                drv.type = 'AVERAGE'
                var = drv.variables.new()
                var.name = 'name'
                var.type = 'TRANSFORMS'
                targ = var.targets[0]
                targ.id = bpy.data.objects[name2]
                targ.transform_type = 'SCALE_Z'
                targ.bone_target = 'Driver'
                fmod = mdf.modifiers[0]
                fmod.poly_order = 1
                fmod.coefficients = (0.0, bpy.context.scene['gx_driver_power'])

            elif bpy.context.scene['gx_type'] == 1 or bpy.context.scene['gx_type'] == 2:
                try:
                    bpy.data.objects[name].driver_remove('scale', 2)
                except:
                    False   
                obj = bpy.data.objects[name] #def drivering
                mdf = obj.driver_add('scale', 2)
                drv = mdf.driver
                drv.type = 'AVERAGE'
                var = drv.variables.new()
                var.name = 'name'
                var.type = 'TRANSFORMS'
                targ = var.targets[0]
                targ.id = bpy.data.objects[name2]
                targ.transform_type = 'SCALE_Z'
                targ.bone_target = 'Driver'
                fmod = mdf.modifiers[0]
                fmod.poly_order = 1
                fmod.coefficients = (0.0, bpy.context.scene['gx_driver_power'])
        except:
            False

    if bpy.context.scene['gx_channels'] == 2 or bpy.context.scene['gx_channels'] == 0:            
        name = "bar_r_" + str(i+1)     
        name2 = "obj_r_" + str(i+1)  
        try:
            bpy.data.objects[name2]
            if bpy.context.scene['gx_type'] == 0:
                try:
                    bpy.data.objects[name].modifiers['Array'].driver_remove('count')
                except:
                    False    
                obj = bpy.data.objects[name] #def drivering
                mdf = obj.modifiers['Array'].driver_add('count')
                drv = mdf.driver
                drv.type = 'AVERAGE'
                var = drv.variables.new()
                var.name = 'name'
                var.type = 'TRANSFORMS'
                targ = var.targets[0]
                targ.id = bpy.data.objects[name2]
                targ.transform_type = 'SCALE_Z'
                targ.bone_target = 'Driver'
                fmod = mdf.modifiers[0]
                fmod.poly_order = 1
                fmod.coefficients = (0.0, bpy.context.scene['gx_driver_power'])

            elif bpy.context.scene['gx_type'] == 1 or bpy.context.scene['gx_type'] == 2:
                try:
                    bpy.data.objects[name].driver_remove('scale', 2)
                except:
                    False    
                obj = bpy.data.objects[name] #def drivering
                mdf = obj.driver_add('scale', 2)
                drv = mdf.driver
                drv.type = 'AVERAGE'
                var = drv.variables.new()
                var.name = 'name'
                var.type = 'TRANSFORMS'
                targ = var.targets[0]
                targ.id = bpy.data.objects[name2]
                targ.transform_type = 'SCALE_Z'
                targ.bone_target = 'Driver'
                fmod = mdf.modifiers[0]
                fmod.poly_order = 1
                fmod.coefficients = (0.0, bpy.context.scene['gx_driver_power'])
        except:
            False

def update_drivers():
    try:
        bpy.types.Scene.bakedobjects
        for i in range(bpy.types.Scene.bakedobjects):
            drivering(i)
    except:
        False

def update_drivers3(self, context):
    try:
        bpy.types.Scene.bakedobjects
        for i in range(bpy.types.Scene.bakedobjects):
            drivering(i)
    except:
        False
        
def update_drivers2():
    try:
        bpy.types.Scene.bakedobjects
        for i in range(bpy.types.Scene.allobjects, bpy.types.Scene.bakedobjects):
            drivering(i)
    except:
        False       

def update_channels(self, context):
    gxstart()

def update_space_x(self, context):
    for i in range(bpy.context.scene['gx_count_x']):
        if bpy.context.scene['gx_channels'] == 1 or bpy.context.scene['gx_channels'] == 0:        
            name = "bar_l_" + str(i+1)
            bpy.data.objects[name].location[0] = -(i*bpy.context.scene['gx_space_x'] + bpy.context.scene['gx_center_space']/2)
            if bpy.context.scene['gx_slash_rotate'] == True and (bpy.context.scene['gx_space_x'] + bpy.context.scene['gx_slash']) != 0:
                bpy.data.objects[name].rotation_euler[2] = -math.asin(bpy.context.scene['gx_slash']/math.sqrt(math.pow(bpy.context.scene['gx_space_x'],2) + math.pow(bpy.context.scene['gx_slash'],2)))  
            else:
                bpy.data.objects[name].rotation_euler[2] = 0    
        if bpy.context.scene['gx_channels'] == 2 or bpy.context.scene['gx_channels'] == 0:
            name = "bar_r_" + str(i+1)
            bpy.data.objects[name].location[0] = i*bpy.context.scene['gx_space_x'] + bpy.context.scene['gx_center_space']/2
            if bpy.context.scene['gx_slash_rotate'] == True and (bpy.context.scene['gx_space_x'] + bpy.context.scene['gx_slash']) != 0:
                bpy.data.objects[name].rotation_euler[2] = math.asin(bpy.context.scene['gx_slash']/math.sqrt(math.pow(bpy.context.scene['gx_space_x'],2) + math.pow(bpy.context.scene['gx_slash'],2)))  
            else:
                bpy.data.objects[name].rotation_euler[2] = 0                
    try:
        bpy.types.Scene.bakedobjects
        for i in range(bpy.types.Scene.bakedobjects):
            if bpy.context.scene['gx_channels'] == 1 or bpy.context.scene['gx_channels'] == 0:        
                name = "obj_l_" + str(i+1)
                bpy.data.objects[name].location[0] = -(i*bpy.context.scene['gx_space_x'] + bpy.context.scene['gx_center_space']/2)
            if bpy.context.scene['gx_channels'] == 2 or bpy.context.scene['gx_channels'] == 0:
                name = "obj_r_" + str(i+1)
                bpy.data.objects[name].location[0] = i*bpy.context.scene['gx_space_x'] + bpy.context.scene['gx_center_space']/2            
    except:
        False
            
def update_scale(self, context):
    for i in range(bpy.context.scene['gx_count_x']):
        if bpy.context.scene['gx_channels'] == 1 or bpy.context.scene['gx_channels'] == 0:        
            name = "bar_l_" + str(i+1)
            if bpy.context.scene['gx_type'] == 0:
                bpy.data.objects[name].scale = (bpy.context.scene['gx_scale_x'], bpy.context.scene['gx_scale_y'], bpy.context.scene['gx_scale_z'])
            elif bpy.context.scene['gx_type'] == 1:
                bpy.data.objects[name].scale = (bpy.context.scene['gx_cube_scale_x'], bpy.context.scene['gx_cube_scale_y'], bpy.context.scene['gx_cube_scale_z'])
                #bpy.ops.object.transform_apply(scale=True)
            elif bpy.context.scene['gx_type'] == 2:
                bpy.data.objects[name].scale = (bpy.context.scene['gx_cube_scale_x'], bpy.context.scene['gx_cube_scale_y'], bpy.context.scene['gx_cube_scale_z']*2) 
                #bpy.ops.object.transform_apply(scale=True)
        if bpy.context.scene['gx_channels'] == 2 or bpy.context.scene['gx_channels'] == 0:
            name = "bar_r_" + str(i+1)
            if bpy.context.scene['gx_type'] == 0:
                bpy.data.objects[name].scale = (bpy.context.scene['gx_scale_x'], bpy.context.scene['gx_scale_y'], bpy.context.scene['gx_scale_z'])
            elif bpy.context.scene['gx_type'] == 1:
                bpy.data.objects[name].scale = (bpy.context.scene['gx_cube_scale_x'], bpy.context.scene['gx_cube_scale_y'], bpy.context.scene['gx_cube_scale_z'])
                #bpy.ops.object.transform_apply(scale=True)
            elif bpy.context.scene['gx_type'] == 2:
                bpy.data.objects[name].scale = (bpy.context.scene['gx_cube_scale_x'], bpy.context.scene['gx_cube_scale_y'], bpy.context.scene['gx_cube_scale_z']*2) 
                #bpy.ops.object.transform_apply(scale=True)

def generate_objects(i):
    gx_save = bpy.context.scene.cursor_location.copy()
    if bpy.context.scene['gx_channels'] == 1 or bpy.context.scene['gx_channels'] == 0:
        bpy.ops.mesh.primitive_cube_add(location=(-(i*bpy.context.scene['gx_space_x'] + bpy.context.scene['gx_center_space']/2), bpy.context.scene['gx_slash'] * i, 0))
        if bpy.context.scene['gx_slash_rotate'] == True:
            bpy.context.active_object.rotation_euler[2] = -math.asin(bpy.context.scene['gx_slash']/math.sqrt(math.pow(bpy.context.scene['gx_space_x'],2) + math.pow(bpy.context.scene['gx_slash'],2)))  
            
        if bpy.context.scene['gx_type'] == 0:
            bpy.context.active_object.scale = (bpy.context.scene['gx_scale_x'], bpy.context.scene['gx_scale_y'], bpy.context.scene['gx_scale_z'])
        elif bpy.context.scene['gx_type'] == 1:
            bpy.context.active_object.scale = (1, 1, 0.06)
            bpy.ops.object.transform_apply(scale=True)
            bpy.context.active_object.location[2] = 0.06
            bpy.context.scene.cursor_location = (-(i*bpy.context.scene['gx_space_x'] + bpy.context.scene['gx_center_space']/2), bpy.context.scene['gx_slash'] * i, 0)  
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR') 
            bpy.context.active_object.scale = (bpy.context.scene['gx_cube_scale_x'], bpy.context.scene['gx_cube_scale_y'], bpy.context.scene['gx_cube_scale_z'])
        elif bpy.context.scene['gx_type'] == 2:
            bpy.context.active_object.scale = (1, 1, 0.06*2)
            bpy.ops.object.transform_apply(scale=True)
            bpy.context.active_object.scale = (bpy.context.scene['gx_cube_scale_x'], bpy.context.scene['gx_cube_scale_y'], bpy.context.scene['gx_cube_scale_z']*2)
                
        name = "bar_l_" + str(i+1)
        bpy.context.active_object.name = name

        if bpy.context.scene['gx_type'] == 0:
            bpy.ops.object.modifier_add(type='ARRAY')
            bpy.context.active_object.modifiers['Array'].count = 10                
            bpy.context.active_object.modifiers['Array'].relative_offset_displace[0] = 0
            bpy.context.active_object.modifiers['Array'].relative_offset_displace[2] = bpy.context.scene['gx_space_array']
                
    if bpy.context.scene['gx_channels'] == 2 or bpy.context.scene['gx_channels'] == 0:
        bpy.ops.mesh.primitive_cube_add(location=(i*bpy.context.scene['gx_space_x'] + bpy.context.scene['gx_center_space']/2, bpy.context.scene['gx_slash'] * i, 0))
        if bpy.context.scene['gx_slash_rotate'] == True:
            bpy.context.active_object.rotation_euler[2] = math.asin(bpy.context.scene['gx_slash']/math.sqrt(math.pow(bpy.context.scene['gx_space_x'],2) + math.pow(bpy.context.scene['gx_slash'],2)))  
            
        if bpy.context.scene['gx_type'] == 0:
            bpy.context.active_object.scale = (bpy.context.scene['gx_scale_x'], bpy.context.scene['gx_scale_y'], bpy.context.scene['gx_scale_z'])
        elif bpy.context.scene['gx_type'] == 1:
            bpy.context.active_object.scale = (1, 1, 0.06)
            bpy.ops.object.transform_apply(scale=True)
            bpy.context.active_object.location[2] = 0.06
            bpy.context.scene.cursor_location = (i*bpy.context.scene['gx_space_x'] + bpy.context.scene['gx_center_space']/2, bpy.context.scene['gx_slash'] * i, 0)
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')      
            bpy.context.active_object.scale = (bpy.context.scene['gx_cube_scale_x'], bpy.context.scene['gx_cube_scale_y'], bpy.context.scene['gx_cube_scale_z'])       
        elif bpy.context.scene['gx_type'] == 2:
            bpy.context.active_object.scale = (1, 1, 0.06*2)
            bpy.ops.object.transform_apply(scale=True)
            bpy.context.active_object.scale = (bpy.context.scene['gx_cube_scale_x'], bpy.context.scene['gx_cube_scale_y'], bpy.context.scene['gx_cube_scale_z']*2)

        name = "bar_r_" + str(i+1)
        bpy.context.active_object.name = name
               
        if bpy.context.scene['gx_type'] == 0:
            bpy.ops.object.modifier_add(type='ARRAY')
            bpy.context.active_object.modifiers['Array'].count = 10                     
            bpy.context.active_object.modifiers['Array'].relative_offset_displace[0] = 0
            bpy.context.active_object.modifiers['Array'].relative_offset_displace[2] = bpy.context.scene['gx_space_array']
    bpy.context.scene.cursor_location = gx_save  
        
def update_count(self, context):
    if bpy.types.Scene.allobjects > bpy.context.scene['gx_count_x']:
        bpy.ops.object.select_all(action="DESELECT")
        for i in range(bpy.context.scene['gx_count_x'], bpy.types.Scene.allobjects):
            if bpy.context.scene['gx_channels'] == 1 or bpy.context.scene['gx_channels'] == 0:            
                name = "bar_l_" + str(i+1)
                bpy.data.objects[name].select = True     
            if bpy.context.scene['gx_channels'] == 2 or bpy.context.scene['gx_channels'] == 0:
                name = "bar_r_" + str(i+1)
                bpy.data.objects[name].select = True
        bpy.ops.object.delete()
        
        if bpy.context.scene['gx_channels'] == 1 or bpy.context.scene['gx_channels'] == 0:    
            bpy.context.scene.objects.active = bpy.data.objects["bar_l_" + str(bpy.context.scene['gx_count_x'])]
            bpy.ops.object.select_pattern(pattern="bar_l_" + str(bpy.context.scene['gx_count_x']))
        if bpy.context.scene['gx_channels'] == 2 or bpy.context.scene['gx_channels'] == 0:
            bpy.context.scene.objects.active = bpy.data.objects["bar_r_" + str(bpy.context.scene['gx_count_x'])]
            bpy.ops.object.select_pattern(pattern="bar_r_" + str(bpy.context.scene['gx_count_x']))            
            
        bpy.types.Scene.allobjects = bpy.context.scene['gx_count_x']
    elif bpy.types.Scene.allobjects < bpy.context.scene['gx_count_x']:
        for i in range(bpy.types.Scene.allobjects, bpy.context.scene['gx_count_x']):
            
            generate_objects(i)
            try:
                if bpy.types.Scene.allobjects < bpy.types.Scene.bakedobjects:
                    update_drivers2()
            except:
                False
     
        if bpy.context.scene['gx_channels'] == 1 or bpy.context.scene['gx_channels'] == 0:    
            bpy.context.scene.objects.active = bpy.data.objects["bar_l_" + str(bpy.context.scene['gx_count_x'])]
            bpy.ops.object.select_pattern(pattern="bar_l_" + str(bpy.context.scene['gx_count_x']))
        if bpy.context.scene['gx_channels'] == 2 or bpy.context.scene['gx_channels'] == 0:
            bpy.context.scene.objects.active = bpy.data.objects["bar_r_" + str(bpy.context.scene['gx_count_x'])]
            bpy.ops.object.select_pattern(pattern="bar_r_" + str(bpy.context.scene['gx_count_x']))                   

        bpy.types.Scene.allobjects = bpy.context.scene['gx_count_x']
    else:
        False
        
def register():
    bpy.utils.register_class(GxCreateBase)
    bpy.utils.register_class(GxInitVariables)
    bpy.utils.register_class(GxBake)    
    bpy.utils.register_class(GXAVPanel)
    initprop()
def unregister():
    bpy.utils.unregister_class(GxCreateBase)
    bpy.utils.unregister_class(GxInitVariables)
    bpy.utils.unregister_class(GxBake)    
    bpy.utils.unregister_class(GXAVPanel)

if __name__ == "__main__":
    register()










