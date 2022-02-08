import bpy


def next_qualified_frame(ob: bpy.types.Object) -> int:
    if ob.get("sm_id") is None:
        return 0
    object_sm_id = ob["sm_id"]
    max_index = 0
    object_name_full: str = ob.name_full
    for mesh in bpy.data.meshes:
        if mesh.get("sm_id") is None:
            continue
        mesh_sm_id = mesh["sm_id"]
        mesh_sm_datablock = mesh["sm_datablock"]
        if mesh_sm_id != object_sm_id:
            continue
        keyframe_index = mesh_sm_datablock
        if keyframe_index > max_index:
            max_index = keyframe_index
    return max_index + 1
