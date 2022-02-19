from __future__ import annotations
from typing import Any, List
import bpy

from .get_object_keyframes import *
from .handle_onion_skin import *
from .next_qualified_frame import *
from .new_object_id import *
from .update_stopmagic import *


def insert_mesh_keyframe(obj: bpy.types.Object | Any) -> None:

    if obj.type == "MESH":
        # Gets the data that's not persistent when the Keyframe is added to the mesh
        remesh_voxel_size = obj.data.remesh_voxel_size
        remesh_voxel_adaptivity = obj.data.remesh_voxel_adaptivity
        symmetry_x = obj.data.use_mirror_x
        symmetry_y = obj.data.use_mirror_y
        symmetry_z = obj.data.use_mirror_z

    is_done = insert_mesh_keyframe_ex(obj)
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


def insert_mesh_keyframe_ex(obj: bpy.types.Object) -> bool:
    if obj.get("sm_id") is None:
        obj["sm_id"] = new_object_id()
    #
    object_sm_id = obj["sm_id"]
    ob_name_full = obj.name_full
    mesh_index = get_next_mesh_index(obj)
    mesh_name = ob_name_full + "_sm_" + str(mesh_index)
    del_mesh = []
    new_mesh = bpy.data.meshes.new_from_object(obj)
    new_mesh.name = mesh_name
    new_mesh["sm_id"] = object_sm_id
    new_mesh["sm_datablock"] = mesh_index
    obj.data = new_mesh
    obj.data.use_fake_user = True
    obj["sm_datablock"] = mesh_index
    obj.keyframe_insert(
        data_path='["sm_datablock"]', frame=bpy.context.scene.frame_current
    )
    for mesh in del_mesh:
        mesh.use_fake_user = False
    update_stopmagic(bpy.context.scene)
    for mesh in del_mesh:
        if mesh.users == 0:
            bpy.data.meshes.remove(mesh)
    #
    return True


# Get the appropriate index for the mesh about to be created
def get_next_mesh_index(obj: bpy.types.Object) -> int:
    if obj.get("sm_datablock") is not None:
        values = get_object_key_values(obj)
        if len(values) > 0:
            largest = values[0]
            for val in values:
                largest = val if val > largest else largest
            return largest + 1
        else:
            return 0
    else:
        return 0
