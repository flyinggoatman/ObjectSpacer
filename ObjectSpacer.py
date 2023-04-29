bl_info = {
    "name": "ObjectSpacer",
    "blender": (3, 5, 0),
    "author": "flyinggoatman",
    "version": (1, 0),
    "category": "Object",
}

import bpy
from bpy.props import EnumProperty, FloatProperty
from bpy.types import Panel, Operator


class OBJECT_OT_evenly_space_objects(Operator):
    bl_idname = "object.evenly_space_objects"
    bl_label = "Evenly Space Objects"
    bl_options = {'REGISTER', 'UNDO'}

    axis: EnumProperty(
        name="Axis",
        description="Select the axis to distribute objects",
        items=[
            ('X', "X", "Distribute objects along the X axis"),
            ('Y', "Y", "Distribute objects along the Y axis"),
            ('Z', "Z", "Distribute objects along the Z axis")
        ],
        default='X'
    )

    distance: FloatProperty(
        name="Distance",
        description="Distance between objects",
        default=1.0,
        min=0.0
    )

    def execute(self, context):
        selected_objects = context.selected_objects
        start_object = context.active_object

        if start_object in selected_objects:
            selected_objects.remove(start_object)

        axis_index = {'X': 0, 'Y': 1, 'Z': 2}[self.axis]
        selected_objects.sort(key=lambda obj: obj.location[axis_index])

        for i, obj in enumerate(selected_objects, start=1):
            obj.location[axis_index] = start_object.location[axis_index] + self.distance * i

        return {'FINISHED'}


class OBJECT_PT_evenly_space_objects(Panel):
    bl_idname = "OBJECT_PT_evenly_space_objects"
    bl_label = "ObjectSpacer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        col = layout.column(align=True)
        operator = col.operator(OBJECT_OT_evenly_space_objects.bl_idname)

        col.prop(operator, "axis", text="Axis")
        col.prop(operator, "distance", text="Distance")


def menu_func(self, context):
    self.layout.operator(OBJECT_OT_evenly_space_objects.bl_idname)


def register():
    bpy.utils.register_class(OBJECT_OT_evenly_space_objects)
    bpy.utils.register_class(OBJECT_PT_evenly_space_objects)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_evenly_space_objects)
    bpy.utils.unregister_class(OBJECT_PT_evenly_space_objects)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()