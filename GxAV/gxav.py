import bpy




def draw(panel, idv):
    context = bpy.context
    layout = panel.layout
    scene = context.scene
    row = layout.row()

    show_properties = _prop(idv, 'hide')

    split = row.split(percentage=0.5)
    split.label(text=_prop(idv, 'name'), icon='SOUND')

    split = split.split(percentage=0.8)
    split.prop(scene, _prop_name(idv, 'hide'), icon="LINKED" if show_properties else "UNLINKED", text='properties')

    split.operator("object.remove_visualization", icon="PANEL_CLOSE", text='').idv = idv

    if show_properties:
        box = layout.box()
        row = box.row()
        row.prop(scene, _prop_name(idv, "name"), text='name')
        row = box.row()
        row.prop(scene, _prop_name(idv, "object"), text='object')


def _prop_name(idv: int, x: str) -> str:
    return f"gxav_{idv}_{x}"


def _prop(idv: int, x: str):
    return getattr(bpy.context.scene, _prop_name(idv, x))


def create(idv):
    setattr(
        bpy.types.Scene, _prop_name(idv, 'center_space'),
        bpy.props.FloatProperty(
            name="Center Space",
            default=2.0,
            min=0,
            description="Enter an float",
            # update=update_space_x)
        )
    )
    setattr(
        bpy.types.Scene, _prop_name(idv, 'hide'),
        bpy.props.BoolProperty(
            default=True,
        )
    )
    setattr(
        bpy.types.Scene, _prop_name(idv, 'name'),
        bpy.props.StringProperty(
            default=f'Visualization #{idv}'
        )
    )
    setattr(
        bpy.types.Scene, _prop_name(idv, 'object'),
        bpy.props.PointerProperty(name="My Pointer", type=bpy.types.Object)
    )

    # set default values
    setattr(
        bpy.context.scene, _prop_name(idv, 'center_space'), 2.0
    )
    setattr(
        bpy.context.scene, _prop_name(idv, 'hide'), True
    )
    setattr(
        bpy.context.scene, _prop_name(idv, 'name'), f'Visualization #{idv}'
    )




def remove(idv):
    props = [_prop_name(idv, name) for name in ('hide', 'name', 'center_space', 'object')]

    for attr in props:
        print(f'>> remove {attr} attribute')
        delattr(bpy.types.Scene, attr)
        # delattr(bpy.context.scene, attr)