from __future__ import annotations
import bpy


def is_candidate_object(context: bpy.types.Context | None) -> bool:
    if context is None:
        context = bpy.context
    if context.view_layer.objects.active is None:
        return False
    else:
        return context.view_layer.objects.active.type == "MESH"
