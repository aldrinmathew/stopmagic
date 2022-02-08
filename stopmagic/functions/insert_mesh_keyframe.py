import bpy
from .next_qualified_frame import *
from .new_object_id import *
from .update_stopmagic import *

def insert_mesh_keyframe(object: bpy.types.Object) -> None:
    new_keyframe_index : int = next_qualified_frame(object)

    # Gets the data that's not persistent when the Keyframe is added to the mesh
    remesh_voxel_size = object.data.remesh_voxel_size
    remesh_voxel_adaptivity = object.data.remesh_voxel_adaptivity
    symmetry_x = object.data.use_mirror_x
    symmetry_y = object.data.use_mirror_y
    symmetry_z = object.data.use_mirror_z

    insert_mesh_keyframe_ex(object, new_keyframe_index)

    fcurves = object.animation_data.action.fcurves
    for fcurve in fcurves:
        if fcurve.data_path != '["sm_datablock"]':
            continue
        for kf in fcurve.keyframe_points:
            kf.interpolation = "CONSTANT"

    # Restores the values of the variables that are not persistent, from before the keyframe was added.
    object.data.remesh_voxel_size = remesh_voxel_size
    object.data.remesh_voxel_adaptivity = remesh_voxel_adaptivity
    bpy.context.object.data.use_mirror_x = symmetry_x
    bpy.context.object.data.use_mirror_y = symmetry_y
    bpy.context.object.data.use_mirror_z = symmetry_z

    bpy.app.handlers.frame_change_post.clear()
    bpy.app.handlers.frame_change_post.append(update_stopmagic)


def insert_mesh_keyframe_ex(object, frame_index):
    if object.get("sm_id") is None:
        object["sm_id"] = new_object_id()
    object_sm_id = object["sm_id"]
    new_mesh = bpy.data.meshes.new_from_object(object)
    ob_name_full = object.name_full
    new_mesh_name = ob_name_full + "_sm_" + str(frame_index)
    new_mesh.name = new_mesh_name
    new_mesh["sm_id"] = object_sm_id
    new_mesh["sm_datablock"] = frame_index
    object.data = new_mesh
    object.data.use_fake_user = True
    current_frame = bpy.context.scene.frame_current
    object["sm_datablock"] = frame_index
    object.keyframe_insert(data_path='["sm_datablock"]', frame=current_frame)