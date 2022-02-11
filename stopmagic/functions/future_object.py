import bpy


def future_object_exists() -> bool:
    for item in bpy.context.view_layer.objects:
        if item.name == "sm_onion_future":
            return True
    return False


def get_future_object(exists: bool) -> bpy.types.Object:
    """Get the future Onion Skin object depending on the provided value. Creates one if it doesn't exists already"""
    if not exists:
        fcache = bpy.data.meshes.new("sm_onion_future")
        fobject = bpy.data.objects.new(name="sm_onion_future", object_data=fcache)
        fobject.hide_select = True
        fobject.display.show_shadows = True
        fobject.hide_render = True
        return fobject
    else:
        return bpy.context.view_layer.objects.get("sm_onion_future")