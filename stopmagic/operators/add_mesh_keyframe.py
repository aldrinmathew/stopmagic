import bpy
from ..functions.insert_mesh_keyframe import *

class AddMeshKeyframe(bpy.types.Operator):
    """Adds a Keyframe to the currently selected Mesh, after which you can edit the mesh to keep the changes"""

    bl_idname = "object.keyframe_mesh"
    bl_label = "Keyframe Mesh"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.view_layer.objects.active is not None

    def execute(self, context: bpy.types.Context):
        ob = context.view_layer.objects.active
        insert_mesh_keyframe(ob)
        return {"FINISHED"}


def register():
    bpy.utils.register_class(AddMeshKeyframe)


def unregister():
    bpy.utils.unregister_class(AddMeshKeyframe)