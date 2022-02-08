import bpy

def get_preferences(package: str) -> bpy.types.AddonPreferences:
    return bpy.context.preferences.addons[package].preferences