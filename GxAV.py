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
    "version": (0, 91),
    "blender": (2, 7, 1),
    "location": "Properties > Scene",
    "description": "Bake Spectrum Visualizer by sound file",
    "warning": "Still beta, a little bit buggy, stay tuned :v",
    "category": "Animation",
    "wiki_url": "https://github.com/gethiox/GXAudioVisualisation/wiki",
    "tracker_url": "https://github.com/gethiox/GXAudioVisualisation/issues"}



import bpy
import math
  

def initprop():
    bpy.types.Scene.gx_mode = bpy.props.EnumProperty(
        items = [('0', 'Logarithm', 'log'),
                 ('1', 'Linear', 'linear')],
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
        items = [('0', 'Both', 'Left and Right channel'),
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
        description = "Enter an integer",
        update=update_count)
    
def initpropvalues():
    bpy.context.scene['gx_space_x'] = 2.0
    bpy.context.scene['gx_count_x'] = 5
    bpy.context.scene['gx_center_space'] = 2.0
    bpy.context.scene['gx_channels'] = 2
    bpy.context.scene['gx_scale_x'] = 0.7
    bpy.context.scene['gx_scale_y'] = 0.6
    bpy.context.scene['gx_scale_z'] = 0.4
    bpy.context.scene['gx_start'] = 100
    bpy.context.scene['gx_space_array'] = 1.5
    bpy.context.scene['gx_min_freq'] = 100.0
    bpy.context.scene['gx_max_freq'] = 20000.0  
    bpy.context.scene['gx_mode'] = 0
        

class LayoutDemoPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "GXAudioVisualisation"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Big render button
        # layout.label(text="Big Button:")
        row = layout.row()
        row.operator("object.gx_init_variables", icon="COLOR", text="Init/Reset Variables")  
        row = layout.row()
        row.operator("object.gx_create_base", icon="MODIFIER", text="Create Visualizer Base")

        layout.label(text="Parameters:")
        row = layout.row()
        row.prop(scene, "gx_count_x")        
        row.prop(scene, "gx_space_x")
        row = layout.row()
        row.prop(scene, "gx_center_space") 

        row = layout.row(align=True)
        row.label(text="Object Scale:")
        row.prop(scene, 'gx_scale_x')
        row.prop(scene, 'gx_scale_y')
        row.prop(scene, 'gx_scale_z')                
        
        layout.label(text="VisMode Parameters:")
        row = layout.row()
        row.prop(scene, "gx_space_array")            

        layout.label(text="Bake Parameters:")
        box = layout.box()
        box.label("Channels to bake and audio files path:")
        box.prop(scene, "gx_channels")
        box.prop(scene, "gx_left_file")
        box.prop(scene, "gx_right_file")     
        row = layout.row()    
        row.prop(scene, "gx_mode")
        row = layout.row()  
        row.prop(scene, "gx_start")
        row = layout.row()        
        row.prop(scene, "gx_min_freq")                       
        row.prop(scene, "gx_max_freq")        
        row = layout.row()
        row.operator("object.gx_bake", icon="RADIO", text="(re)Bake animation data")     
          
           
        


def gxstart():
    bpy.ops.object.select_all(action="DESELECT")
    try:
        for i in range(bpy.context.scene['gx_count_x']):
            name = "bar_r_" + str(i+1)
            bpy.data.objects[name].select = True  
        bpy.ops.object.delete()    
    except:
        print("Right channel not exist, skip deleting")
    try:
        for i in range(bpy.context.scene['gx_count_x']):  
            name = "bar_l_" + str(i+1)      
            bpy.data.objects[name].select = True          
        bpy.ops.object.delete()
    except:
        print("Left channel not exist, skip deleting")
        
    for i in range(bpy.context.scene['gx_count_x']):
        if bpy.context.scene['gx_channels'] == 1 or bpy.context.scene['gx_channels'] == 0:
            bpy.ops.mesh.primitive_cube_add(location=(-(i*bpy.context.scene['gx_space_x'] + bpy.context.scene['gx_center_space']/2), 0, 0))
            bpy.context.active_object.scale = (bpy.context.scene['gx_scale_x'], bpy.context.scene['gx_scale_y'], bpy.context.scene['gx_scale_z'])

            name = "bar_l_" + str(i+1)            
            bpy.context.active_object.name = name
            
            bpy.ops.object.modifier_add(type='ARRAY')
            bpy.context.active_object.modifiers['Array'].count = 10                 
            bpy.context.active_object.modifiers['Array'].relative_offset_displace[0] = 0
            bpy.context.active_object.modifiers['Array'].relative_offset_displace[2] = bpy.context.scene['gx_space_array']            

        if bpy.context.scene['gx_channels'] == 2 or bpy.context.scene['gx_channels'] == 0:
            bpy.ops.mesh.primitive_cube_add(location=(i*bpy.context.scene['gx_space_x'] + bpy.context.scene['gx_center_space']/2, 0, 0))
            bpy.context.active_object.scale = (bpy.context.scene['gx_scale_x'], bpy.context.scene['gx_scale_y'], bpy.context.scene['gx_scale_z'])

            name = "bar_r_" + str(i+1)
            bpy.context.active_object.name = name
            
            bpy.ops.object.modifier_add(type='ARRAY')
            bpy.context.active_object.modifiers['Array'].count = 10                 
            bpy.context.active_object.modifiers['Array'].relative_offset_displace[0] = 0
            bpy.context.active_object.modifiers['Array'].relative_offset_displace[2] = bpy.context.scene['gx_space_array']

    if bpy.context.scene['gx_channels'] == 1 or bpy.context.scene['gx_channels'] == 0:    
        bpy.context.scene.objects.active = bpy.data.objects["bar_l_" + str(bpy.context.scene['gx_count_x'])]
        bpy.ops.object.select_pattern(pattern="bar_l_" + str(bpy.context.scene['gx_count_x']))
    if bpy.context.scene['gx_channels'] == 2 or bpy.context.scene['gx_channels'] == 0:
        bpy.context.scene.objects.active = bpy.data.objects["bar_r_" + str(bpy.context.scene['gx_count_x'])]
        bpy.ops.object.select_pattern(pattern="bar_r_" + str(bpy.context.scene['gx_count_x']))   
            
    bpy.types.Scene.allobjects = bpy.context.scene['gx_count_x']
    print("Objects: " + str(bpy.types.Scene.allobjects))      
    
    update_drivers()  

def gxbake():
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
        print("Right channel not exist, skip deleting")
    try:
        for i in range(bpy.types.Scene.bakedobjects):  
            name = "obj_l_" + str(i+1)      
            bpy.data.objects[name].select = True          
        bpy.ops.object.delete()
    except:
        print("Left channel not exist, skip deleting")   
        
    print("debug mode kurwa: " + str(bpy.context.scene['gx_count_x'])) 
    
    
    c = (bpy.context.scene['gx_max_freq']-bpy.context.scene['gx_min_freq'])/bpy.context.scene['gx_count_x']
        
    for i in range(bpy.context.scene['gx_count_x']):
        if bpy.context.scene['gx_mode'] == 1:
            b = ((bpy.context.scene['gx_max_freq']-bpy.context.scene['gx_min_freq'])-c*(bpy.context.scene['gx_count_x']-i-1)) + bpy.context.scene['gx_min_freq']
            a = ((bpy.context.scene['gx_max_freq']-bpy.context.scene['gx_min_freq'])-c*(bpy.context.scene['gx_count_x']-i)) + bpy.context.scene['gx_min_freq']
        elif bpy.context.scene['gx_mode'] == 0:
            b = ((1 - math.log(bpy.context.scene['gx_count_x']-i, bpy.context.scene['gx_count_x']+1)) * (bpy.context.scene['gx_max_freq']-bpy.context.scene['gx_min_freq'])) + bpy.context.scene['gx_min_freq']
            a = ((1 - math.log(bpy.context.scene['gx_count_x']-i+1, bpy.context.scene['gx_count_x']+1)) * (bpy.context.scene['gx_max_freq']-bpy.context.scene['gx_min_freq'])) + bpy.context.scene['gx_min_freq']
        print(str(i) + ": " + str(a) + " - " + str(b))
        if bpy.context.scene['gx_channels'] == 1 or bpy.context.scene['gx_channels'] == 0:
            bpy.context.scene.frame_current = bpy.context.scene['gx_start']
            bpy.ops.object.add(location=(-(i*bpy.context.scene['gx_space_x'] + bpy.context.scene['gx_center_space']/2), 0, -2))
            name = "obj_l_" + str(i+1)            
            bpy.context.active_object.name = name
            
            bpy.ops.anim.keyframe_insert_menu(type='Scaling')
            bpy.context.area.type = 'GRAPH_EDITOR'
            bpy.ops.graph.sound_bake(filepath=bpy.context.scene['gx_left_file'], low=a, high=b)
            bpy.context.area.type = 'PROPERTIES'
        if bpy.context.scene['gx_channels'] == 2 or bpy.context.scene['gx_channels'] == 0:
            bpy.context.scene.frame_current = bpy.context.scene['gx_start']
            bpy.ops.object.add(location=(i*bpy.context.scene['gx_space_x'] + bpy.context.scene['gx_center_space']/2, 0, -2))
            name = "obj_r_" + str(i+1)
            bpy.context.active_object.name = name
            
            bpy.ops.anim.keyframe_insert_menu(type='Scaling')
            bpy.context.area.type = 'GRAPH_EDITOR'
            bpy.ops.graph.sound_bake(filepath=bpy.context.scene['gx_right_file'], low=a, high=b)
            bpy.context.area.type = 'PROPERTIES'

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
        print("bake")
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


def update_drivers():
    try:
        bpy.types.Scene.bakedobjects
        for i in range(bpy.types.Scene.bakedobjects):
            if bpy.context.scene['gx_channels'] == 1 or bpy.context.scene['gx_channels'] == 0:         
                name = "bar_l_" + str(i+1)
                name2 = "obj_l_" + str(i+1)
                
                bpy.data.objects[name].modifiers['Array'].driver_remove('count')
                 
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
                fmod.coefficients = (0.0, 40.0)
           
                #bpy.data.objects[name].modifiers['Array'].driver_add('count').driver.type = 'AVERAGE'
                #bpy.data.objects[name].modifiers['Array'].driver_add('count').driver.variables.new().name = 'name'
                #bpy.data.objects[name].modifiers['Array'].driver_add('count').driver.variables.new().type = 'TRANSFORMS'
                #bpy.data.objects[name].modifiers['Array'].driver_add('count').driver.variables.new().targets[0].id = bpy.data.objects[name2]
                #bpy.data.objects[name].modifiers['Array'].driver_add('count').driver.variables.new().targets[0].transform_type = 'SCALE_Z'
                #bpy.data.objects[name].modifiers['Array'].driver_add('count').driver.variables.new().targets[0].bone_target = 'Driver'

            if bpy.context.scene['gx_channels'] == 2 or bpy.context.scene['gx_channels'] == 0:            
                name = "bar_r_" + str(i+1)     
                name2 = "obj_r_" + str(i+1)  
                
                bpy.data.objects[name].modifiers['Array'].driver_remove('count')    
                                  
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
                fmod.coefficients = (0.0, 40.0)
           
                #bpy.data.objects[name].modifiers['Array'].driver_add('count').driver.type = 'AVERAGE'
                #bpy.data.objects[name].modifiers['Array'].driver_add('count').driver.variables.new().name = 'name'
                #bpy.data.objects[name].modifiers['Array'].driver_add('count').driver.variables.new().type = 'TRANSFORMS'
                #bpy.data.objects[name].modifiers['Array'].driver_add('count').driver.variables.new().targets[0].id = bpy.data.objects[name2]
                #bpy.data.objects[name].modifiers['Array'].driver_add('count').driver.variables.new().targets[0].transform_type = 'SCALE_Z'
                #bpy.data.objects[name].modifiers['Array'].driver_add('count').driver.variables.new().targets[0].bone_target = 'Driver'
        
    except:
        print("no drivers connections to update") 
        
def update_drivers2():
    try:
        bpy.types.Scene.bakedobjects
        for i in range(bpy.types.Scene.allobjects, bpy.types.Scene.bakedobjects):
            if bpy.context.scene['gx_channels'] == 1 or bpy.context.scene['gx_channels'] == 0:         
                name = "bar_l_" + str(i+1)
                name2 = "obj_l_" + str(i+1)
                
                bpy.data.objects[name].modifiers['Array'].driver_remove('count')
                 
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
                fmod.coefficients = (0.0, 20.0)
           
                #bpy.data.objects[name].modifiers['Array'].driver_add('count').driver.type = 'AVERAGE'
                #bpy.data.objects[name].modifiers['Array'].driver_add('count').driver.variables.new().name = 'name'
                #bpy.data.objects[name].modifiers['Array'].driver_add('count').driver.variables.new().type = 'TRANSFORMS'
                #bpy.data.objects[name].modifiers['Array'].driver_add('count').driver.variables.new().targets[0].id = bpy.data.objects[name2]
                #bpy.data.objects[name].modifiers['Array'].driver_add('count').driver.variables.new().targets[0].transform_type = 'SCALE_Z'
                #bpy.data.objects[name].modifiers['Array'].driver_add('count').driver.variables.new().targets[0].bone_target = 'Driver'

            if bpy.context.scene['gx_channels'] == 2 or bpy.context.scene['gx_channels'] == 0:            
                name = "bar_r_" + str(i+1)     
                name2 = "obj_r_" + str(i+1)     
                
                bpy.data.objects[name].modifiers['Array'].driver_remove('count') 
                                  
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
                fmod.coefficients = (0.0, 20.0)
           
                #bpy.data.objects[name].modifiers['Array'].driver_add('count').driver.type = 'AVERAGE'
                #bpy.data.objects[name].modifiers['Array'].driver_add('count').driver.variables.new().name = 'name'
                #bpy.data.objects[name].modifiers['Array'].driver_add('count').driver.variables.new().type = 'TRANSFORMS'
                #bpy.data.objects[name].modifiers['Array'].driver_add('count').driver.variables.new().targets[0].id = bpy.data.objects[name2]
                #bpy.data.objects[name].modifiers['Array'].driver_add('count').driver.variables.new().targets[0].transform_type = 'SCALE_Z'
                #bpy.data.objects[name].modifiers['Array'].driver_add('count').driver.variables.new().targets[0].bone_target = 'Driver'
        
    except:
        print("no drivers connections to update")         
                                

    

def update_channels(self, context):
    gxstart()

def update_space_x(self, context):
    for i in range(bpy.context.scene['gx_count_x']):
        if bpy.context.scene['gx_channels'] == 1 or bpy.context.scene['gx_channels'] == 0:        
            name = "bar_l_" + str(i+1)
            bpy.data.objects[name].location[0] = -(i*bpy.context.scene['gx_space_x'] + bpy.context.scene['gx_center_space']/2)
        if bpy.context.scene['gx_channels'] == 2 or bpy.context.scene['gx_channels'] == 0:
            name = "bar_r_" + str(i+1)
            bpy.data.objects[name].location[0] = i*bpy.context.scene['gx_space_x'] + bpy.context.scene['gx_center_space']/2
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
        print("no baked objects to change position")
            
def update_scale(self, context):
    for i in range(bpy.context.scene['gx_count_x']):
        if bpy.context.scene['gx_channels'] == 1 or bpy.context.scene['gx_channels'] == 0:        
            name = "bar_l_" + str(i+1)
            bpy.data.objects[name].scale = (bpy.context.scene['gx_scale_x'], bpy.context.scene['gx_scale_y'], bpy.context.scene['gx_scale_z'])
        if bpy.context.scene['gx_channels'] == 2 or bpy.context.scene['gx_channels'] == 0:
            name = "bar_r_" + str(i+1)
            bpy.data.objects[name].scale = (bpy.context.scene['gx_scale_x'], bpy.context.scene['gx_scale_y'], bpy.context.scene['gx_scale_z'])       
        
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
            if bpy.context.scene['gx_channels'] == 1 or bpy.context.scene['gx_channels'] == 0:
                bpy.ops.mesh.primitive_cube_add(location=(-(i*bpy.context.scene['gx_space_x'] + bpy.context.scene['gx_center_space']/2), 0, 0))
                bpy.context.active_object.scale = (bpy.context.scene['gx_scale_x'], bpy.context.scene['gx_scale_y'], bpy.context.scene['gx_scale_z'])
                
                name = "bar_l_" + str(i+1)
                bpy.context.active_object.name = name
                
                bpy.ops.object.modifier_add(type='ARRAY')
                bpy.context.active_object.modifiers['Array'].count = 10                
                bpy.context.active_object.modifiers['Array'].relative_offset_displace[0] = 0
                bpy.context.active_object.modifiers['Array'].relative_offset_displace[2] = bpy.context.scene['gx_space_array']
                

            if bpy.context.scene['gx_channels'] == 2 or bpy.context.scene['gx_channels'] == 0:
                bpy.ops.mesh.primitive_cube_add(location=(i*bpy.context.scene['gx_space_x'] + bpy.context.scene['gx_center_space']/2, 0, 0))
                bpy.context.active_object.scale = (bpy.context.scene['gx_scale_x'], bpy.context.scene['gx_scale_y'], bpy.context.scene['gx_scale_z'])

                name = "bar_r_" + str(i+1)
                bpy.context.active_object.name = name
                
                bpy.ops.object.modifier_add(type='ARRAY')
                bpy.context.active_object.modifiers['Array'].count = 10                     
                bpy.context.active_object.modifiers['Array'].relative_offset_displace[0] = 0
                bpy.context.active_object.modifiers['Array'].relative_offset_displace[2] = bpy.context.scene['gx_space_array']
                
            try:
                if bpy.types.Scene.allobjects < bpy.types.Scene.bakedobjects:
                    update_drivers2()
            except:
                print("kurwachuj")
     
        if bpy.context.scene['gx_channels'] == 1 or bpy.context.scene['gx_channels'] == 0:    
            bpy.context.scene.objects.active = bpy.data.objects["bar_l_" + str(bpy.context.scene['gx_count_x'])]
            bpy.ops.object.select_pattern(pattern="bar_l_" + str(bpy.context.scene['gx_count_x']))
        if bpy.context.scene['gx_channels'] == 2 or bpy.context.scene['gx_channels'] == 0:
            bpy.context.scene.objects.active = bpy.data.objects["bar_r_" + str(bpy.context.scene['gx_count_x'])]
            bpy.ops.object.select_pattern(pattern="bar_r_" + str(bpy.context.scene['gx_count_x']))                   

        bpy.types.Scene.allobjects = bpy.context.scene['gx_count_x']
    else:
        print("chuj")
        
def register():
    bpy.utils.register_class(GxCreateBase)
    bpy.utils.register_class(GxInitVariables)
    bpy.utils.register_class(GxBake)    
    bpy.utils.register_class(LayoutDemoPanel)
    initprop()
def unregister():
    bpy.utils.unregister_class(GxCreateBase)
    bpy.utils.unregister_class(GxInitVariables)
    bpy.utils.unregister_class(GxBake)    
    bpy.utils.unregister_class(LayoutDemoPanel)

if __name__ == "__main__":
    register()


