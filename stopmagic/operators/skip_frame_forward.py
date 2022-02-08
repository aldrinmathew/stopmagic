import bpy
from ..functions.insert_mesh_keyframe import *


class SkipFrameForward(bpy.types.Operator):
    """Skips frames forward based on the number of frames entered by the user."""

    bl_idname = "object.frame_forward_keyframe_mesh"
    bl_label = "Skip Frame"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        count = 3
        try:
            count = context.scene.stopmagic_frame_skip_count
        except Exception as e:
            print("KEYMESH :: Fetching frame skip count :: ", e)
            count = 3
        ob = context.active_object
        bpy.context.scene.frame_current += count
        if context.scene.stopmagic_insert_frame_after_skip:
            insert_mesh_keyframe(ob)
        return {"FINISHED"}


def register():
    bpy.utils.register_class(SkipFrameForward)


def unregister():
    bpy.utils.unregister_class(SkipFrameForward)