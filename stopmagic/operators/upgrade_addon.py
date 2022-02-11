from __future__ import annotations
from typing import Set
import webbrowser
import bpy


class UpgradeAddon(bpy.types.Operator):
    """Gets you to the page with the latest version of the addon"""

    bl_idname = "stopmagic.upgrade_addon"
    bl_label = "Check Updates"
    bl_description = "Tries to download the latest version of the addon via the browser. If that's not available, this will open the Releases page of the addon"

    tag_name = None

    @staticmethod
    def set_tag_name(value: str) -> None:
        UpgradeAddon.tag_name = value

    @classmethod
    def poll(cls, context: bpy.types.context) -> bool:
        return True

    def execute(self, context: bpy.types.Context) -> Set[int] | Set[str]:
        if self.tag_name is None:
            webbrowser.open_new_tab(
                "https://github.com/aldrinsartfactory/stopmagic/releases"
            )
        else:
            webbrowser.open_new_tab(
                "https://github.com/aldrinsartfactory/stopmagic/releases/download/"
                + self.tag_name
                + "/stopmagic.zip"
            )
        return {"FINISHED"}


def register():
    bpy.utils.register_class(UpgradeAddon)


def unregister():
    bpy.utils.unregister_class(UpgradeAddon)
