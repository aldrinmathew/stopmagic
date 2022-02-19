import bpy
from stopmagic.functions import insert_mesh_keyframe, is_candidate_object


class AddMeshKeyframe(bpy.types.Operator):
    """Adds a Keyframe to the currently selected Mesh, after which you can edit the mesh to keep the changes"""

    bl_idname = "object.keyframe_mesh"
    bl_label = "Keyframe Mesh"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return is_candidate_object(context)

    def execute(self, context: bpy.types.Context):
        if bpy.context.view_layer.objects.active is not None:
            ob = context.view_layer.objects.active
            insert_mesh_keyframe(ob)
        return {"FINISHED"}


def register():
    bpy.utils.register_class(AddMeshKeyframe)


def unregister():
    bpy.utils.unregister_class(AddMeshKeyframe)
