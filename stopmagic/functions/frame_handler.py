import bpy

from stopmagic.functions import handle_onion_skin, update_stopmagic


@bpy.app.handlers.persistent
def frame_handler(dummy) -> None:
    obs = bpy.context.scene.objects
    for o in obs:
        if "sm_datablock" and "sm_id" in o:  # It's a Stopmagic scene
            bpy.app.handlers.frame_change_post.clear()
            bpy.app.handlers.frame_change_post.append(update_stopmagic)
            bpy.app.handlers.frame_change_pre.append(handle_onion_skin)
            break
