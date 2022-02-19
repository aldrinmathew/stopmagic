from __future__ import annotations
from typing import List, Set
import bpy

from stopmagic.functions import get_object_keyframes


class KeyedFrameNext(bpy.types.Operator):
    """Find and jump to the next frame that has a mesh keyframe for the current object"""

    bl_idname = "object.keyed_frame_next"
    bl_label = "Jump Next"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        return context.view_layer.objects.active is not None

    def execute(self, context: bpy.types.Context) -> Set[int] | Set[str]:
        if bpy.context.view_layer.objects.active is not None:
            keyframes = get_object_keyframes(context.view_layer.objects.active)
            if len(keyframes) > 0:
                frame = bpy.context.scene.frame_current
                keyframes = [k for k in keyframes if k > frame]
            if len(keyframes) > 0:
                lowest = keyframes[0]
                for num in keyframes:
                    if num < lowest:
                        lowest = num
                context.scene.frame_current = lowest
        return {"FINISHED"}


def register() -> None:
    bpy.utils.register_class(KeyedFrameNext)


def unregister() -> None:
    bpy.utils.unregister_class(KeyedFrameNext)
