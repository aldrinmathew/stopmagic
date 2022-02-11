import bpy


def past_object_exists() -> bool:
    for item in bpy.context.view_layer.objects:
        if item.name == "sm_onion_past":
            return True
    return False


def get_past_object(exists: bool) -> bpy.types.Object:
    """Get the past Onion Skin object depending on the provided value. Creates one if it doesn't exists already"""
    if not exists:
        pcache = bpy.data.meshes.new("sm_onion_past")
        pobject = bpy.data.objects.new(name="sm_onion_past", object_data=pcache)
        pobject.hide_select = True
        pobject.display.show_shadows = False
        pobject.hide_render = True
        return pobject
    else:
        return bpy.context.view_layer.objects.get("sm_onion_past")