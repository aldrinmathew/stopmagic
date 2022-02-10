from typing import List
import bpy


def get_object_keyframes() -> List[int]:
    """Get all keyframes that has mesh keyframes, associated with the active object"""
    obj = bpy.context.view_layer.objects.active
    keyframes: List[int] = []
    if obj is not None:
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
                                for val in item.co:
                                    keyframes.append(int(val))
                            return keyframes
    return keyframes
