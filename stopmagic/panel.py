from __future__ import annotations
from typing import Any
import bpy
from stopmagic import functions
import requests
from stopmagic.operators import UpgradeAddon


addon_info = {}


def addon_remote_version() -> str | None:
    global addon_info
    if addon_info is not None:
        if addon_info.get("tag_name") is not None:
            return addon_info.get("tag_name")
    return None


class StopmagicPanel(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_stopmagic_panel"
    bl_label = "Stopmagic"
    bl_category = "Stopmagic"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    # For showing version to the user
    bl_info: "dict[str, Any]" = {}

    @staticmethod
    def set_info(info: "dict[str, Any]"):
        StopmagicPanel.bl_info = info

    def draw(self, context: bpy.context):
        column = self.layout.column()
        column.scale_y = 1.5
        column.separator()
        column.operator("object.keyframe_mesh", text="Keyframe Mesh")
        column.separator()
        column = self.layout.column()
        column.label(text="Find Keyed Frame")
        row = column.row()
        row.operator(
            "object.keyed_frame_previous", text="Previous", icon_value=499
        )
        row.operator("object.keyed_frame_next", text="Next", icon_value=500)
        self.layout.separator()
        column = self.layout.column()
        column.label(text="Frame Skip")
        column.prop(context.scene, "stopmagic_insert_frame_after_skip")
        column.prop(context.scene, "stopmagic_frame_skip_count")
        column = self.layout.column()
        column.scale_y = 1.5
        row = column.row(align=False)
        row.alignment = "EXPAND"
        row.operator(
            "object.frame_backward_keyframe_mesh",
            text=r"Backward",
            emboss=True,
            depress=False,
            icon_value=6,
        )
        row.operator(
            "object.frame_forward_keyframe_mesh",
            text=r"Forward",
            emboss=True,
            depress=False,
            icon_value=4,
        )
        column.separator()
        column = self.layout.column()
        column.label(text="Onion Skin (Experimental)")
        column.prop(context.scene, "stopmagic_onion_skin_enabled")
        if context.scene.stopmagic_onion_skin_enabled:
            row = column.row()
            lcolumn = row.column()
            lcolumn.label(text="Past")
            lcolumn.prop(context.scene, "stopmagic_past_offset")
            lcolumn.prop(context.scene, "stopmagic_past_color")
            rcolumn = row.column()
            rcolumn.label(text="Future")
            rcolumn.prop(context.scene, "stopmagic_future_offset")
            rcolumn.prop(context.scene, "stopmagic_future_color")
        column.separator()
        column = self.layout.column()
        column.label(text="Status Options")
        column.operator(
            "object.purge_unused_data", text="Purge Unused Data", icon="TRASH"
        )
        column.operator(
            "object.initialize_handler",
            text="Initialize Frame Handler",
            icon="FILE_REFRESH",
        )
        if addon_remote_version() is not None:
            if "v" + functions.addon_version(self.bl_info) != addon_remote_version():
                column.separator()
                column.label(
                    text="v"
                    + functions.addon_version(StopmagicPanel.bl_info)
                    + "   >>   "
                    + addon_remote_version()
                )
                column.operator(
                    "stopmagic.upgrade_addon", text="Upgrade Addon", icon="URL"
                )
        else:
            column.separator()
            column.label(text="v" + functions.addon_version(StopmagicPanel.bl_info))
            column.operator("stopmagic.upgrade_addon", text="Upgrade Addon", icon="URL")


def register() -> None:
    global addon_info
    bpy.utils.register_class(StopmagicPanel)
    resp = requests.get(
        "https://api.github.com/repos/aldrinsartfactory/stopmagic/releases/latest"
    )
    if resp.status_code == 200:
        addon_info = resp.json()
        if addon_remote_version() is not None:
            UpgradeAddon.set_tag_name(addon_remote_version())


def unregister() -> None:
    bpy.utils.unregister_class(StopmagicPanel)
