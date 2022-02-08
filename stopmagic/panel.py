from typing import Any
import bpy
from stopmagic import functions


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
        column.label(
            text=("Version: " + functions.addon_version(StopmagicPanel.bl_info))
        )
        column = self.layout.column()
        column.scale_y = 1.5
        column.separator()
        column.operator("object.keyframe_mesh", text="Keyframe Mesh")
        self.layout.separator()
        column = self.layout.column()
        column.label(text="Frame Skip Options")
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
        column.label(text="Use shortcuts for faster & easier workflows")
        column.separator()
        column = self.layout.column()
        column.label(text="Status Options")
        column.operator("object.purge_unused_data", text="Purge Unused Data")
        column.operator("object.initialize_handler", text="Initialize Frame Handler")


def register() -> None:
    bpy.utils.register_class(StopmagicPanel)


def unregister() -> None:
    bpy.utils.unregister_class(StopmagicPanel)