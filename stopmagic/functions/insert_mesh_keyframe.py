from __future__ import annotations
from typing import Any, List
import bpy

from .handle_onion_skin import *
from .next_qualified_frame import *
from .new_object_id import *
from .update_stopmagic import *


def insert_mesh_keyframe(obj: bpy.types.Object | Any) -> None:
    new_keyframe_index: int = bpy.context.scene.frame_current

    if obj.type == "MESH":
        # Gets the data that's not persistent when the Keyframe is added to the mesh
        remesh_voxel_size = obj.data.remesh_voxel_size
        remesh_voxel_adaptivity = obj.data.remesh_voxel_adaptivity
        symmetry_x = obj.data.use_mirror_x
        symmetry_y = obj.data.use_mirror_y
        symmetry_z = obj.data.use_mirror_z

    is_done = insert_mesh_keyframe_ex(obj, new_keyframe_index)
    if is_done:
        fcurves = obj.animation_data.action.fcurves
        for fcurve in fcurves:
            if fcurve.data_path != '["sm_datablock"]':
                continue
            for kf in fcurve.keyframe_points:
                kf.interpolation = "CONSTANT"
        #
        if obj.type == "MESH":
            # Restores the values of the variables that are not persistent, from before the keyframe was added.
            obj.data.remesh_voxel_size = remesh_voxel_size
            obj.data.remesh_voxel_adaptivity = remesh_voxel_adaptivity
            bpy.context.object.data.use_mirror_x = symmetry_x
            bpy.context.object.data.use_mirror_y = symmetry_y
            bpy.context.object.data.use_mirror_z = symmetry_z
        #
        bpy.app.handlers.frame_change_post.clear()
        bpy.app.handlers.frame_change_post.append(update_stopmagic)
        handle_onion_skin(obj)


def insert_mesh_keyframe_ex(obj: bpy.types.Object, frame_index: int) -> bool:
    if obj.get("sm_id") is None:
        obj["sm_id"] = new_object_id()
    #
    object_sm_id = obj["sm_id"]
    ob_name_full = obj.name_full
    new_mesh_name = ob_name_full + "_sm_" + str(frame_index)
    del_mesh = []
    proceed = False
    for mesh in bpy.data.meshes:
        if mesh.name is not None:
            if mesh.name != new_mesh_name:
                proceed = True
            else:
                return False
    #
    new_mesh = bpy.data.meshes.new_from_object(obj)
    new_mesh.name = new_mesh_name
    new_mesh["sm_id"] = object_sm_id
    new_mesh["sm_datablock"] = frame_index
    if proceed:
        if obj.get("sm_datablock") is not None:
            num = obj.get("sm_datablock")
            if num != bpy.context.scene.frame_current:
                proceed = True
        else:
            proceed = True
    else:
        return proceed
    #
    if proceed:
        obj.data = new_mesh
        obj.data.use_fake_user = True
        current_frame = bpy.context.scene.frame_current
        obj["sm_datablock"] = current_frame
        obj.keyframe_insert(data_path='["sm_datablock"]', frame=current_frame)
        for mesh in del_mesh:
            mesh.use_fake_user = False
        update_stopmagic(bpy.context.scene)
        for mesh in del_mesh:
            if mesh.users == 0:
                bpy.data.meshes.remove(mesh)
    #
    return proceed
