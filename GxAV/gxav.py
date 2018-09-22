import bpy

from GxAV.interface import VisualizationInterface as VisualizationInterface


class Visualization(VisualizationInterface):
    def __init__(self, id: int):
        self.id: int = id
        self.name: str = f"#{self.id}"

        self.__init_props()

    def clean_up(self):
        props = [self.prop_name(name) for name in ('hide', 'name', 'center_space', 'object')]


        for attr in props:
            print(f'>> remove {attr} attribute')
            delattr(bpy.types.Scene, attr)
            # delattr(bpy.context.scene, attr)


    def prepare_data(self):
        pass

    def draw(self, context, panel):
        layout = panel.layout
        scene = context.scene
        row = layout.row()

        show_properties = self.prop('hide')

        split = row.split(percentage=0.5)
        split.label(text=self.prop('name'), icon='SOUND')

        split = split.split(percentage=0.8)
        split.prop(scene, self.prop_name('hide'), icon="LINKED" if show_properties else "UNLINKED", text='properties')

        split.operator("object.remove_visualization", icon="PANEL_CLOSE", text='').idx = self.id

        if show_properties:
            box = layout.box()
            row = box.row()
            row.prop(scene, self.prop_name("name"), text='name')
            row = box.row()
            row.prop(scene, self.prop_name("object"), text='object')

    def prop_name(self, x: str) -> str:
        return f"viz_{self.id}_{x}"

    def prop(self, x: str):
        return getattr(bpy.context.scene, self.prop_name(x))

    def __init_props(self):
        setattr(
            bpy.types.Scene, self.prop_name('center_space'),
            bpy.props.FloatProperty(
                name="Center Space",
                default=2.0,
                min=0,
                description="Enter an float",
                # update=update_space_x)
            )
        )
        setattr(
            bpy.types.Scene, self.prop_name('hide'),
            bpy.props.BoolProperty(
                default=True,
            )
        )
        setattr(
            bpy.types.Scene, self.prop_name('name'),
            bpy.props.StringProperty(
                default=f'Visualization #{self.id}'
            )
        )
        setattr(
            bpy.types.Scene, self.prop_name('object'),
            bpy.props.PointerProperty(name="My Pointer", type=bpy.types.Object)
        )
