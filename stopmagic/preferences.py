import bpy

from stopmagic.functions import get_preferences


class StopmagicPreferences(bpy.types.AddonPreferences):
    """Preferences for the Stopmagic addon"""

    bl_idname = __package__

    frame_skip_count: bpy.props.IntProperty(
        name="Frame Skip Count",
        description="Skip this many frames forwards or backwards",
        subtype="NONE",
        options=set(),
        default=3,
        min=1,
        max=2**31 - 1,
        soft_min=1,
        soft_max=100,
        step=1,
    )
    insert_keyframe_after_skip: bpy.props.BoolProperty(
        name="Insert Keyframe after Skip",
        description="Whether to insert keyframe after skipping frames",
        options=set(),
        default=True,
    )

    def draw(self, context):
        self.layout.label(text="These settings will be used when you create a new file")
        self.layout.prop(self, "insert_keyframe_after_skip")
        row = self.layout.row()
        column = row.column()
        column.prop(self, "frame_skip_count")
        column = row.column()


def register_properties() -> None:
    bpy.types.Scene.stopmagic_frame_skip_count = bpy.props.IntProperty(
        name="Frame Count",
        description="Skip this many frames forwards or backwards",
        subtype="NONE",
        options=set(),
        default=3,
        min=1,
        max=2**31 - 1,
        soft_min=1,
        soft_max=100,
        step=1,
    )
    bpy.types.Scene.stopmagic_insert_frame_after_skip = bpy.props.BoolProperty(
        name="Insert Keyframe",
        description="Whether to insert keyframe after skipping frames",
        options=set(),
        default=False,
    )


def unregister_properties() -> None:
    del bpy.types.Scene.stopmagic_frame_skip_count
    del bpy.types.Scene.stopmagic_insert_frame_after_skip


def register() -> None:
    bpy.utils.register_class(StopmagicPreferences)
    register_properties()


def unregister() -> None:
    bpy.utils.unregister_class(StopmagicPreferences)
    unregister_properties()
