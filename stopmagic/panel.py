from __future__ import annotations
from typing import Any
import bpy
from stopmagic import functions
import requests
from stopmagic.operators import UpgradeAddon
from stopmagic.icons import AddonIcons


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
    expand_find_frame = True
    expand_frame_skip = True
    expand_onion_skin = True
    expand_status_options = False

    @staticmethod
    def set_info(info: "dict[str, Any]"):
        StopmagicPanel.bl_info = info

    def draw(self, context: bpy.context):
        if addon_remote_version() is not None:
            if "v" + functions.addon_version(self.bl_info) != addon_remote_version():
                column = self.layout.column()
                box = column.box()
                box.label(
                    text="v"
                    + functions.addon_version(StopmagicPanel.bl_info)
                    + "   >>   "
                    + addon_remote_version()
                )
                box.operator(
                    "stopmagic.upgrade_addon", text="Upgrade Addon", icon="URL"
                )
                self.layout.separator()
        # SECTION :: Keyframe Mesh
        column = self.layout.column()
        column.scale_y = 1.5
        column.operator("object.keyframe_mesh", text="Keyframe Mesh")
        self.layout.separator()
        # SECTION :: Find Keyed Frame
        column = self.layout.column()
        box = column.box()
        row = box.row()
        row.label(text="Find Keyed Frame", icon="ZOOM_PREVIOUS")
        row.prop(
            context.scene,
            "stopmagic_expand_find_frame",
            icon="TRIA_UP"
            if context.scene.stopmagic_expand_find_frame
            else "TRIA_DOWN",
            emboss=False,
        )
        if context.scene.stopmagic_expand_find_frame:
            row = box.row()
            row.operator("object.keyed_frame_previous", text="Previous", icon_value=499)
            row.operator("object.keyed_frame_next", text="Next", icon_value=500)
        self.layout.separator()
        # SECTION :: Frame Skip
        column = self.layout.column()
        box = column.box()
        row = box.row()
        row.label(text="Frame Skip", icon="TRACKING_FORWARDS")
        row.prop(
            context.scene,
            "stopmagic_expand_frame_skip",
            icon="TRIA_UP"
            if context.scene.stopmagic_expand_frame_skip
            else "TRIA_DOWN",
            emboss=False,
        )
        if context.scene.stopmagic_expand_frame_skip:
            box.prop(context.scene, "stopmagic_insert_frame_after_skip")
            box.prop(context.scene, "stopmagic_frame_skip_count")
            column = box.column()
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
        self.layout.separator()
        # SECTION :: Onion Skin
        column = self.layout.column()
        box = column.box()
        row = box.row()
        row.label(text="Onion Skin", icon="GHOST_ENABLED")
        row.prop(
            context.scene,
            "stopmagic_expand_onion_skin",
            icon="TRIA_UP"
            if context.scene.stopmagic_expand_onion_skin
            else "TRIA_DOWN",
            emboss=False,
        )
        if context.scene.stopmagic_expand_onion_skin:
            box.prop(context.scene, "stopmagic_onion_skin_enabled")
            if context.scene.stopmagic_onion_skin_enabled:
                box.prop(context.scene, "stopmagic_onion_display_type")
                row = box.row()
                lcolumn = row.column()
                lcolumn.label(text="Past")
                if context.scene.stopmagic_onion_display_type == "POSE":
                    lcolumn.prop(context.scene, "stopmagic_past_count")
                else:
                    lcolumn.prop(context.scene, "stopmagic_past_offset")
                lcolumn.prop(context.scene, "stopmagic_past_color")
                rcolumn = row.column()
                rcolumn.label(text="Future")
                if context.scene.stopmagic_onion_display_type == "POSE":
                    rcolumn.prop(context.scene, "stopmagic_future_count")
                else:
                    rcolumn.prop(context.scene, "stopmagic_future_offset")
                rcolumn.prop(context.scene, "stopmagic_future_color")
        self.layout.separator()
        # SECTION :: Contribution
        column = self.layout.column()
        box = column.box()
        row = box.row()
        row.label(text="Make a contribution", icon="FUND")
        row.prop(
            context.scene,
            "stopmagic_expand_contributions",
            icon="TRIA_UP"
            if context.scene.stopmagic_expand_contributions
            else "TRIA_DOWN",
            emboss=False,
        )
        if context.scene.stopmagic_expand_contributions:
            row = box.row()
            row.operator(
                "stopmagic.contribution_paypal",
                text="PayPal",
                icon_value=AddonIcons.paypal_color().icon_id,
            )
            row.operator(
                "stopmagic.contribution_kofi",
                text="Ko-Fi",
                icon_value=AddonIcons.kofi_color().icon_id,
            )
            box.operator(
                "stopmagic.contribution_github",
                text="Github",
                icon_value=AddonIcons.github_color().icon_id,
            )
        self.layout.separator()
        # SECTION :: Status Options
        column = self.layout.column()
        box = column.box()
        row = box.row()
        row.label(text="Status Options", icon="TOOL_SETTINGS")
        row.prop(
            context.scene,
            "stopmagic_expand_status_options",
            icon="TRIA_UP"
            if context.scene.stopmagic_expand_status_options
            else "TRIA_DOWN",
            emboss=False,
        )
        if context.scene.stopmagic_expand_status_options:
            box.operator(
                "object.purge_unused_data", text="Purge Unused Data", icon="TRASH"
            )
            box.operator(
                "object.initialize_handler",
                text="Initialize Frame Handler",
                icon="FILE_REFRESH",
            )
        # Fallback upgrade button in case of connectivity issues or invalid responses
        if addon_remote_version() is None:
            self.layout.separator()
            column = self.layout.column()
            box = column.box()
            box.label(text="v" + functions.addon_version(StopmagicPanel.bl_info))
            box.operator("stopmagic.upgrade_addon", text="Upgrade Addon", icon="URL")


def register() -> None:
    global addon_info
    bpy.utils.register_class(StopmagicPanel)
    try:
        resp = requests.get(
            url="https://api.github.com/repos/aldrinsartfactory/stopmagic/releases/latest",
            timeout=5,
        )
        if resp.status_code == 200:
            addon_info = resp.json()
            if addon_remote_version() is not None:
                UpgradeAddon.set_tag_name(addon_remote_version())
    except:
        print("Exception while fetching addon data")


def unregister() -> None:
    bpy.utils.unregister_class(StopmagicPanel)
