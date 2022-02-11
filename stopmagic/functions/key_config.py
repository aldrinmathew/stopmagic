from typing import List, Tuple
import bpy


def key_config() -> List[Tuple[bpy.types.KeyMap, bpy.types.KeyMapItem]]:
    result: List[Tuple[bpy.types.KeyMap, bpy.types.KeyMapItem]] = []
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        keyMapView = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
        keyMapItem = keyMapView.keymap_items.new(
            "object.keyframe_mesh", type="A", value="PRESS", shift=True, ctrl=True
        )
        result.append((keyMapView, keyMapItem))
        keyMapItem = keyMapView.keymap_items.new(
            "object.frame_backward_keyframe_mesh",
            type="Z",
            value="PRESS",
            shift=True,
            ctrl=True,
        )
        result.append((keyMapView, keyMapItem))
        keyMapItem = keyMapView.keymap_items.new(
            "object.frame_forward_keyframe_mesh",
            type="X",
            value="PRESS",
            shift=True,
            ctrl=True,
        )
        result.append((keyMapView, keyMapItem))
        keyMapItem = keyMapView.keymap_items.new(
            "object.keyed_frame_previous",
            type="C",
            value="PRESS",
            shift=True,
            ctrl=True,
        )
        result.append((keyMapView, keyMapItem))
        keyMapItem = keyMapView.keymap_items.new(
            "object.keyed_frame_next",
            type="V",
            value="PRESS",
            shift=True,
            ctrl=True,
        )
        result.append((keyMapView, keyMapItem))
    return result
