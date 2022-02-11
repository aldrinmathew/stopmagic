from __future__ import annotations
import bpy
from typing import Tuple


def handle_onion_constraints(
    obj: bpy.types.Object, active: bpy.types.Object
) -> Tuple[
    bpy.types.CopyLocationConstraint,
    bpy.types.CopyRotationConstraint,
    bpy.types.CopyScaleConstraint,
    bpy.types.CopyTransformsConstraint,
]:
    """Handle finding constraints for the object. This function expects the object to have four constraints attached to it. If not those will be created. For the addon, this function is only called for the Past and Future variants of the Onion Skin"""
    loc: bpy.types.CopyLocationConstraint | None = None
    rot: bpy.types.CopyRotationConstraint | None = None
    scl: bpy.types.CopyScaleConstraint | None = None
    tra: bpy.types.CopyTransformsConstraint | None = None

    def check_constraints():
        nonlocal loc
        nonlocal rot
        nonlocal scl
        nonlocal tra
        for item in obj.constraints:
            if item.type == "COPY_LOCATION":
                loc = item
            elif item.type == "COPY_ROTATION":
                rot = item
            elif item.type == "COPY_SCALE":
                scl = item
            elif item.type == "COPY_TRANSFORMS":
                tra = item

    check_constraints()
    bpy.context.view_layer.objects.active = obj
    if loc is None or rot is None or scl is None or tra is None:
        if loc is None:
            bpy.ops.object.constraint_add(type="COPY_LOCATION")
        if rot is None:
            bpy.ops.object.constraint_add(type="COPY_ROTATION")
        if scl is None:
            bpy.ops.object.constraint_add(type="COPY_SCALE")
        if tra is None:
            bpy.ops.object.constraint_add(type="COPY_TRANSFORMS")
        loc, rot, scl, tra = handle_onion_constraints(obj, active)
        loc.target = active
        rot.target = active
        scl.target = active
        tra.target = active
        bpy.context.view_layer.objects.active = active
    else:
        return loc, rot, scl, tra
