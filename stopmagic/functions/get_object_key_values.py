import bpy
from typing import List


def get_object_key_values(obj: bpy.types.Object) -> List[int]:
    values: List[int] = []
    if obj.get("sm_id") is not None:
        for action in bpy.data.actions:
            if obj.user_of_id(action.id_data):
                fcurves = action.fcurves
                if fcurves is not None:
                    for item in fcurves:
                        fcurve: bpy.types.FCurve = item
                        if fcurve.data_path != '["sm_datablock"]':
                            continue
                        #
                        keyframe_points = fcurve.keyframe_points
                        for item in keyframe_points:
                            i = 1
                            while i < len(item.co):
                                values.append(int(item.co[i]))
                                i += 2
                        return values
    return values
