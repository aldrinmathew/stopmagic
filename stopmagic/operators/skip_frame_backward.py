from __future__ import annotations
from typing import Set
import bpy
from stopmagic.functions import insert_mesh_keyframe, is_candidate_object


class SkipFrameBackward(bpy.types.Operator):
    """Skips frames backward based on the number of frames entered by the user."""

    bl_idname = "object.frame_backward_keyframe_mesh"
    bl_label = "Skip Frame"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        return is_candidate_object(context)

    def execute(self, context: bpy.types.Context) -> Set[int] | Set[str]:
        count = 3
        try:
            count = context.scene.stopmagic_frame_skip_count
        except Exception as _:
            count = 3
        if bpy.context.view_layer.objects.active is not None:
            active = context.view_layer.objects.active
            if active is not None:
                bpy.context.scene.frame_current -= count
                if context.scene.stopmagic_insert_frame_after_skip:
                    insert_mesh_keyframe(active)
        return {"FINISHED"}


def register():
    bpy.utils.register_class(SkipFrameBackward)


def unregister():
    bpy.utils.unregister_class(SkipFrameBackward)
