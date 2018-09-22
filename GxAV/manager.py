import json
from typing import List, Optional, Dict

import bpy

from GxAV import gxav

ID = int


class GxAVProperties(bpy.types.PropertyGroup):
    # keeps configuration in json format
    configuration = bpy.props.StringProperty()

    @property
    def visualizations(self) -> List[ID]:
        if self.configuration:
            try:
                return json.loads(self.configuration)['vizualizations']
            except KeyError:
                return []
        return []

    @visualizations.setter
    def visualizations(self, value):
        try:
            configuration = json.loads(self.configuration)
        except json.JSONDecodeError:
            configuration = {}

        configuration['vizualizations'] = value
        self.configuration = json.dumps(configuration)



class Panel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "GXAudioVisualisation"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("object.add_visualization", icon="ZOOMIN")

        for vis_id in context.scene.gxav.visualizations:
            gxav.draw(self, vis_id)


class AddVisualization(bpy.types.Operator):
    bl_idname = "object.add_visualization"
    bl_label = "Add Visualization"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        idv = self._get_available_id(context)
        current_visualizations = context.scene.gxav.visualizations
        current_visualizations.append(idv)
        context.scene.gxav.visualizations = current_visualizations
        gxav.create(idv)
        print(f'>>> Visualization "{idv}" added!')
        return {'FINISHED'}

    def _get_available_id(self, context) -> ID:
        """
        Returns first free/available ID for visualization instance  on current scene
        """

        current_ids = [idv for idv in context.scene.gxav.visualizations]

        idv = 0
        while True:
            if idv not in current_ids:
                return idv
            idv += 1


class RemoveVisualization(bpy.types.Operator):
    bl_idname = "object.remove_visualization"
    bl_label = "Remove Visualization"
    bl_options = {'UNDO'}

    idv = bpy.props.IntProperty(name="vizualization idx to remove", default=-1)

    def execute(self, context):
        current_visualizations = context.scene.gxav.visualizations
        current_visualizations.remove(self.idv)
        context.scene.gxav.visualizations = current_visualizations
        gxav.remove(self.idv)
        print(f'>>> Visualization {self.idv} removed!')
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


def register():
    bpy.utils.register_class(GxAVProperties)
    bpy.utils.register_class(Panel)
    bpy.utils.register_class(AddVisualization)
    bpy.utils.register_class(RemoveVisualization)

    try:
        getattr(bpy.types.Scene, 'gxav')
        print('>>> data already existing')
    except AttributeError:
        bpy.types.Scene.gxav = bpy.props.PointerProperty(type=GxAVProperties)
        print('>>> new data created')


def unregister():
    bpy.utils.unregister_class(GxAVProperties)
    bpy.utils.unregister_class(Panel)
    bpy.utils.unregister_class(AddVisualization)
    bpy.utils.unregister_class(RemoveVisualization)
