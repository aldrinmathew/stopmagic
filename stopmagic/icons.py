import bpy
import os.path
import bpy.utils.previews


addon_icons: bpy.utils.previews.ImagePreviewCollection = None


class AddonIcons:
    @classmethod
    def paypal_color(cls):
        global addon_icons
        return addon_icons["PAYPAL_COLOR"]

    @classmethod
    def kofi_color(cls):
        global addon_icons
        return addon_icons["KOFI_COLOR"]
    
    @classmethod
    def github_color(cls):
        global addon_icons
        return addon_icons["GITHUB_COLOR"]


def register():
    global addon_icons
    addon_icons = bpy.utils.previews.new()
    icons_dir = os.path.join(os.path.dirname(__file__), "icons")
    addon_icons.load("PAYPAL_COLOR", os.path.join(icons_dir, "paypal.png"), "IMAGE")
    addon_icons.load("KOFI_COLOR", os.path.join(icons_dir, "kofi.png"), "IMAGE")
    addon_icons.load("GITHUB_COLOR", os.path.join(icons_dir, "github.png"), "IMAGE")


def unregister():
    global addon_icons
    bpy.utils.previews.remove(addon_icons)
