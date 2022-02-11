import bpy


def new_object_id() -> int:
    max_id = 0
    for item in bpy.data.objects:
        if item.get("sm_id") is None:
            continue
        object_sm_id = item["sm_id"]
        if object_sm_id > max_id:
            max_id = object_sm_id
    return max_id + 1