import bpy

from ..functions.handle_onion_skin import handle_onion_skin
from ..functions.update_stopmagic import update_stopmagic


class InitializeHandler(bpy.types.Operator):
    """If Stopmagic stops working try using this function to re-initialize it's frame handler"""

    bl_idname = "object.initialize_handler"
    bl_label = "Initialize Handler"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.app.handlers.frame_change_post.clear()
        bpy.app.handlers.frame_change_post.append(update_stopmagic)
        bpy.app.handlers.frame_change_pre.clear()
        bpy.app.handlers.frame_change_pre.append(handle_onion_skin)
        return {"FINISHED"}


def register():
    bpy.utils.register_class(InitializeHandler)


def unregister():
    bpy.utils.unregister_class(InitializeHandler)
