import json
from collections import OrderedDict
from typing import List, Optional, Dict

import bpy

from GxAV.gxav import Visualization

ID = int
ScenePointer = int

scene_vizualizations: Dict[ScenePointer, List[Visualization]] = {}
scene_vizualizations = {}

class GxAVProperties(bpy.types.PropertyGroup):
    # keeps configuration in json format
    configuration = bpy.props.StringProperty()

    @property
    def visualizations(self) -> Optional[List[ID]]:
        if self.configuration:
            try:
                return json.loads(self.configuration)['vizualizations']
            except KeyError:
                return None

    @visualizations.setter
    def visualizations(self, value):
        try:
            configuration = json.loads(self.configuration)
        except json.JSONDecodeError:
            configuration = {}

        configuration['vizualizations'] = value
        self.configuration = json.dumps(configuration)


def init():
    global scene_vizualizations
    for scene in bpy.data.scenes:
        try:
            getattr(scene, 'gxav')
        except:
            print('>>> Nothing to load')
        else:
            for idx in bpy.context.scene.gxav.visualizations:
                print('>>> recreating existing visualizers')
                scene_vizualizations[scene.as_pointer()] = Visualization(id=idx)


# try:
#     vizualizations = bpy.types.Scene.gxav.state
#     print('>>> addon data already exist')
# except AttributeError:
#     print('>>> initializating addon data')
#     bpy.types.Scene.gxav_vizualizations = OrderedDict()
#     vizualizations = bpy.types.Scene.gxav_vizualizations

to_remove: ID = -1

initializated = False


class Panel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "GXAudioVisualisation"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"


    def draw(self, context):
        global initializated
        if not initializated:
            init()
            initializated = True

        layout = self.layout
        row = layout.row()
        row.operator("object.add_visualization", icon="ZOOMIN")

        for scene_pointer, visuzalizations in scene_vizualizations.items():
            if scene_pointer == context.scene.as_pointer():
                for viz in visuzalizations:
                    viz.draw(context, self)


class AddVisualization(bpy.types.Operator):
    bl_idname = "object.add_visualization"
    bl_label = "Add Visualization"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        viz_id = self._get_available_id(context)
        viz = Visualization(id=viz_id)
        try:
            scene_vizualizations[context.scene.as_pointer()].append(viz)
        except KeyError:
            scene_vizualizations[context.scene.as_pointer()] = [viz]

        print(f'>>> Visualization "{viz_id}" added!')
        return {'FINISHED'}

    def _get_available_id(self, context) -> ID:
        try:
            visualizations = scene_vizualizations[context.scene.as_pointer()]
        except KeyError:
            visualizations = []

        current_ids = [viz.id for viz in visualizations]

        idx = 0
        while True:
            if idx not in current_ids:
                return idx
            idx += 1


class RemoveVisualization(bpy.types.Operator):
    bl_idname = "object.remove_visualization"
    bl_label = "Remove Visualization"
    bl_options = {'UNDO'}

    idx = bpy.props.IntProperty(name="vizualization idx to remove", default=-1)

    def execute(self, context):
        vis = scene_vizualizations[context.scene.as_pointer()].pop(self.idx)
        vis.clean_up()
        del vis
        print(f'>>> Visualization {self.idx} removed!')
        return {'FINISHED'}


def register():
    bpy.utils.register_class(GxAVProperties)
    bpy.utils.register_class(Panel)
    bpy.utils.register_class(AddVisualization)
    bpy.utils.register_class(RemoveVisualization)

    # bpy.types.Scene.gxav = bpy.props.PointerProperty(type=GxAVProperties)
    # for idx in bpy.context.scene.gxav.visualizations:
    #     viz = Visualization(id=idx)
    #     vizualizations[idx] = viz
    #     print(f'>>> Visualization "{idx}" added!')
    #     print(f'>>> visualizations: {vizualizations}')


def unregister():
    bpy.utils.unregister_class(GxAVProperties)
    bpy.utils.unregister_class(Panel)
    bpy.utils.unregister_class(AddVisualization)
    bpy.utils.unregister_class(RemoveVisualization)
