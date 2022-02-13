import sys

sys.path.append("./")
if "bpy" in locals():
    import importlib

    importlib.reload(preferences)
    importlib.reload(operators)
    importlib.reload(functions)
    importlib.reload(panel)
else:
    from stopmagic import preferences
    from stopmagic import operators
    from stopmagic import functions
    from stopmagic import panel

from typing import List, Tuple
import bpy
import re
from os.path import basename, dirname

__package__ = "stopmagic"

bl_info = {
    "name": "Stopmagic",
    "author": "Aldrin Mathew",
    "version": (0, 3, 1),
    "blender": (2, 91, 0),
    "location": "Sidebar > Stopmagic",
    "warning": "beta",
    "category": "Animation",
    "description": "Improve your Stop motion workflow. Use shortcuts 'Ctrl Shift X' & 'Ctrl Shift Z' for faster workflows.",
    "doc_url": "https://github.com/aldrinsartfactory/stopmagic/wiki",
}


addon_keymaps: List[Tuple[bpy.types.KeyMap, bpy.types.KeyMapItem]] = []


def register() -> None:
    global addon_keymaps
    preferences.register()
    panel.StopmagicPanel.bl_info = bl_info
    panel.register()
    operators.add_mesh_keyframe.register()
    operators.skip_frame_forward.register()
    operators.skip_frame_backward.register()
    operators.purge_unused_data.register()
    operators.initialize_handler.register()
    operators.keyed_frame_next.register()
    operators.keyed_frame_previous.register()
    operators.upgrade_addon.register()
    bpy.app.handlers.load_post.append(functions.frame_handler)
    bpy.app.handlers.load_post.append(functions.handle_onion_skin)
    bpy.app.handlers.frame_change_post.clear()
    bpy.app.handlers.frame_change_post.append(functions.update_stopmagic)
    bpy.app.handlers.frame_change_pre.clear()
    bpy.app.handlers.frame_change_pre.append(functions.handle_onion_skin)
    addon_keymaps = functions.key_config()


def unregister() -> None:
    preferences.unregister()
    operators.add_mesh_keyframe.unregister()
    operators.skip_frame_backward.unregister()
    operators.skip_frame_forward.unregister()
    operators.purge_unused_data.unregister()
    operators.initialize_handler.unregister()
    operators.keyed_frame_next.unregister()
    operators.keyed_frame_previous.unregister()
    operators.upgrade_addon.unregister()
    panel.unregister()
    bpy.app.handlers.load_post.clear()
    bpy.app.handlers.load_post.clear()
    bpy.app.handlers.frame_change_post.clear()
    bpy.app.handlers.frame_change_pre.clear()
    addon_keymaps.clear()


if __name__ == "__main__":
    register()
