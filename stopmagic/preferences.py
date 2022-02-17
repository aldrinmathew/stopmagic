import bpy

from stopmagic.functions import (
    get_preferences,
    change_onion_color,
    clear_onion_data,
    handle_onion_skin,
)


def handle_onion_enable(self, value) -> None:
    if bpy.context.scene.stopmagic_onion_skin_enabled:
        handle_onion_skin(bpy.context.scene)
    else:
        clear_onion_data()


def handle_past_color(self, value) -> None:
    change_onion_color(True, bpy.context.scene.stopmagic_past_color)


def handle_future_color(self, value) -> None:
    change_onion_color(False, bpy.context.scene.stopmagic_future_color)


def handle_display(self, value) -> None:
    handle_onion_skin(bpy.context.scene)


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
    onion_skin_enabled: bpy.props.BoolProperty(
        name="Enable Onion Skin",
        description="Whether onion skins should be displayed",
        options=set(),
        default=False,
    )
    past_color: bpy.props.FloatVectorProperty(
        name="Color",
        description="Color to be used for past frames of the Onion Skin",
        subtype="COLOR_GAMMA",
        size=4,
        default=(1.0, 0.0, 0.0, 0.3),
    )
    future_color: bpy.props.FloatVectorProperty(
        name="Color",
        description="Color to be used for future frames of the Onion Skin",
        subtype="COLOR_GAMMA",
        size=4,
        default=(0.0, 0.0, 1.0, 0.3),
    )
    onion_display_type: bpy.props.EnumProperty(
        items=[
            (
                "POSE",
                "Pose",
                "Display a specific number of poses before or after the current frame",
                "CON_ACTION",
                0,
            ),
            (
                "RANGE",
                "Range",
                "Display all poses within a range before or after the current frame",
                "ARROW_LEFTRIGHT",
                1,
            ),
        ],
        name="Display Type",
        description="Change the type of display for the onion skin",
        options=set(),
        default="POSE",
    )
    past_offset: bpy.props.IntProperty(
        name="Offset",
        description="Show onion skins for these many frames before the current frame",
        subtype="NONE",
        options=set(),
        default=10,
        min=0,
        max=200,
        soft_min=0,
        soft_max=100,
        step=1,
    )
    past_count: bpy.props.IntProperty(
        name="Past Count",
        description="Show onion skins for this many mesh poses, before the current frame",
        subtype="NONE",
        options=set(),
        default=1,
        min=1,
        max=100,
        soft_min=1,
        soft_max=10,
        step=1,
    )
    future_offset: bpy.props.IntProperty(
        name="Offset",
        description="Show onion skins for these many frames after the current frame",
        subtype="NONE",
        options=set(),
        default=10,
        min=0,
        max=200,
        soft_min=0,
        soft_max=100,
        step=1,
    )
    future_count: bpy.props.IntProperty(
        name="Future Count",
        description="Show onion skins for this many mesh poses, after the current frame",
        subtype="NONE",
        options=set(),
        default=1,
        min=1,
        max=100,
        soft_min=1,
        soft_max=10,
        step=1,
    )

    def draw(self, context: bpy.types.Context):
        self.layout.label(text="These settings will be used when you create a new file")
        self.layout.prop(self, "insert_keyframe_after_skip")
        row = self.layout.row()
        column = row.column()
        column.prop(self, "frame_skip_count")
        column.separator()
        column = self.layout.column()
        column.label(text="Onion Skin Options")
        column.prop(self, "onion_skin_enabled")
        column.prop(self, "onion_display_type")
        row = column.row()
        lcolumn = row.column()
        lcolumn.label(text="Past")
        lcolumn.prop(self, "past_count")
        lcolumn.prop(self, "past_offset")
        lcolumn.prop(self, "past_color")
        rcolumn = row.column()
        rcolumn.label(text="Future")
        rcolumn.prop(self, "future_count")
        rcolumn.prop(self, "future_offset")
        rcolumn.prop(self, "future_color")


def register_properties() -> None:
    bpy.types.Scene.stopmagic_frame_skip_count = bpy.props.IntProperty(
        name="Frame Count",
        description="Skip this many frames forwards or backwards",
        subtype="NONE",
        options=set(),
        default=get_preferences(__package__).frame_skip_count,
        min=1,
        max=2**31 - 1,
        soft_min=1,
        soft_max=100,
        step=1,
    )
    bpy.types.Scene.stopmagic_onion_display_type = bpy.props.EnumProperty(
        items=[
            (
                "POSE",
                "Pose",
                "Display a specific number of poses before or after the current frame",
                "CON_ACTION",
                0,
            ),
            (
                "RANGE",
                "Range",
                "Display all poses within a range before or after the current frame",
                "ARROW_LEFTRIGHT",
                1,
            ),
        ],
        name="Display",
        description="Change the type of display for the onion skin",
        options=set(),
        default=get_preferences(__package__).onion_display_type,
        update=handle_display,
    )
    bpy.types.Scene.stopmagic_past_count = bpy.props.IntProperty(
        name="Poses",
        description="Show onion skins for this many mesh poses, before the current frame",
        subtype="NONE",
        options=set(),
        default=get_preferences(__package__).past_count,
        min=1,
        max=100,
        soft_min=1,
        soft_max=10,
        step=1,
        update=handle_display,
    )
    bpy.types.Scene.stopmagic_past_offset = bpy.props.IntProperty(
        name="Offset",
        description="Show keyed meshes in these many frames before the current frame",
        subtype="NONE",
        options=set(),
        default=get_preferences(__package__).past_offset,
        min=0,
        max=200,
        soft_min=0,
        soft_max=100,
        step=1,
        update=handle_display,
    )
    bpy.types.Scene.stopmagic_future_count = bpy.props.IntProperty(
        name="Poses",
        description="Show onion skins for this many mesh poses, after the current frame",
        subtype="NONE",
        options=set(),
        default=get_preferences(__package__).future_count,
        min=1,
        max=100,
        soft_min=1,
        soft_max=10,
        step=1,
        update=handle_display,
    )
    bpy.types.Scene.stopmagic_future_offset = bpy.props.IntProperty(
        name="Offset",
        description="Show keyed meshes in these many frames after the current frame",
        subtype="NONE",
        options=set(),
        default=get_preferences(__package__).future_offset,
        min=0,
        max=200,
        soft_min=0,
        soft_max=100,
        step=1,
        update=handle_display,
    )
    bpy.types.Scene.stopmagic_past_color = bpy.props.FloatVectorProperty(
        name="",
        description="Color for past frames of the Onion Skin",
        subtype="COLOR_GAMMA",
        size=4,
        default=get_preferences(__package__).past_color,
        update=handle_past_color,
    )
    bpy.types.Scene.stopmagic_future_color = bpy.props.FloatVectorProperty(
        name="",
        description="Color for future frames of the Onion State",
        subtype="COLOR_GAMMA",
        size=4,
        default=get_preferences(__package__).future_color,
        update=handle_future_color,
    )
    bpy.types.Scene.stopmagic_onion_skin_enabled = bpy.props.BoolProperty(
        name="Enable (Experimental)",
        description="Whether Onion Skins should be displayed",
        options=set(),
        default=get_preferences(__package__).onion_skin_enabled,
        update=handle_onion_enable,
    )
    bpy.types.Scene.stopmagic_insert_frame_after_skip = bpy.props.BoolProperty(
        name="Insert Keyframe",
        description="Whether to insert keyframe after skipping frames",
        options=set(),
        default=get_preferences(__package__).insert_keyframe_after_skip,
    )
    bpy.types.Scene.stopmagic_expand_find_frame = bpy.props.BoolProperty(
        name="",
        description="",
        options=set(),
        default=True,
    )
    bpy.types.Scene.stopmagic_expand_frame_skip = bpy.props.BoolProperty(
        name="",
        description="",
        options=set(),
        default=True,
    )
    bpy.types.Scene.stopmagic_expand_onion_skin = bpy.props.BoolProperty(
        name="",
        description="",
        options=set(),
        default=False,
    )
    bpy.types.Scene.stopmagic_expand_contributions = bpy.props.BoolProperty(
        name="",
        description="",
        options=set(),
        default=True,
    )
    bpy.types.Scene.stopmagic_expand_status_options = bpy.props.BoolProperty(
        name="",
        description="",
        options=set(),
        default=False,
    )


def unregister_properties() -> None:
    del bpy.types.Scene.stopmagic_frame_skip_count
    del bpy.types.Scene.stopmagic_insert_frame_after_skip
    del bpy.types.Scene.stopmagic_past_offset
    del bpy.types.Scene.stopmagic_past_count
    del bpy.types.Scene.stopmagic_future_offset
    del bpy.types.Scene.stopmagic_future_count
    del bpy.types.Scene.stopmagic_past_color
    del bpy.types.Scene.stopmagic_future_color
    del bpy.types.Scene.stopmagic_onion_skin_enabled
    del bpy.types.Scene.stopmagic_expand_find_frame
    del bpy.types.Scene.stopmagic_expand_frame_skip
    del bpy.types.Scene.stopmagic_expand_onion_skin
    del bpy.types.Scene.stopmagic_expand_contributions
    del bpy.types.Scene.stopmagic_expand_status_options


def register() -> None:
    bpy.utils.register_class(StopmagicPreferences)
    register_properties()


def unregister() -> None:
    bpy.utils.unregister_class(StopmagicPreferences)
    unregister_properties()


if __name__ == "__main__":
    register()
