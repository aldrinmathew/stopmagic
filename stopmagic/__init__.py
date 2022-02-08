import bpy
import re
from bpy.app.handlers import persistent
from os.path import basename, dirname

__package__ = "stopmagic"

bl_info = {
    "name": "Stopmagic",
    "author": "Aldrin Mathew",
    "version": (0, 2, 1),
    "blender": (2, 91, 0),
    "location": "Sidebar > Stopmagic",
    "warning": "Experimental",
    "category": "Animation",
    "description": "Improve your Stop motion workflow. Use shortcuts 'Ctrl Shift X' & 'Ctrl Shift Z' for faster workflows.",
    "doc_url": "https://github.com/aldrinsartfactory/stopmagic/wiki",
}


def get_preferences(context: bpy.context):
    return context.preferences.addons[__package__].preferences


def next_available_object_id():
    max_id = 0
    for ob in bpy.data.objects:
        if ob.get("sm_id") is None:
            continue
        object_sm_id = ob["sm_id"]
        if object_sm_id > max_id:
            max_id = object_sm_id
    return max_id + 1


def next_available_stopmagic_frame(ob):
    if ob.get("sm_id") is None:
        return 0
    object_sm_id = ob["sm_id"]
    max_index = 0
    object_name_full = ob.name_full
    for mesh in bpy.data.meshes:
        if mesh.get("sm_id") is None:
            continue
        mesh_sm_id = mesh["sm_id"]
        mesh_sm_datablock = mesh["sm_datablock"]
        if mesh_sm_id != object_sm_id:
            continue
        keyframe_index = mesh_sm_datablock
        if keyframe_index > max_index:
            max_index = keyframe_index
    return max_index + 1


def insert_mesh_keyframe_ex(object, frame_index):
    if object.get("sm_id") is None:
        object["sm_id"] = next_available_object_id()
    object_sm_id = object["sm_id"]
    new_mesh = bpy.data.meshes.new_from_object(object)
    ob_name_full = object.name_full
    new_mesh_name = ob_name_full + "_sm_" + str(frame_index)
    new_mesh.name = new_mesh_name
    new_mesh["sm_id"] = object_sm_id
    new_mesh["sm_datablock"] = frame_index
    object.data = new_mesh
    object.data.use_fake_user = True
    current_frame = bpy.context.scene.frame_current
    object["sm_datablock"] = frame_index
    object.keyframe_insert(data_path='["sm_datablock"]', frame=current_frame)


def insert_mesh_keyframe(object):
    new_keyframe_index = next_available_stopmagic_frame(object)

    # Gets the data that's not persistent when the Keyframe is added to the mesh
    remesh_voxel_size = object.data.remesh_voxel_size
    remesh_voxel_adaptivity = object.data.remesh_voxel_adaptivity
    symmetry_x = object.data.use_mirror_x
    symmetry_y = object.data.use_mirror_y
    symmetry_z = object.data.use_mirror_z

    insert_mesh_keyframe_ex(object, new_keyframe_index)

    fcurves = object.animation_data.action.fcurves
    for fcurve in fcurves:
        if fcurve.data_path != '["sm_datablock"]':
            continue
        for kf in fcurve.keyframe_points:
            kf.interpolation = "CONSTANT"

    # Restores the values of the variables that are not persistent, from before the keyframe was added.
    object.data.remesh_voxel_size = remesh_voxel_size
    object.data.remesh_voxel_adaptivity = remesh_voxel_adaptivity
    bpy.context.object.data.use_mirror_x = symmetry_x
    bpy.context.object.data.use_mirror_y = symmetry_y
    bpy.context.object.data.use_mirror_z = symmetry_z

    bpy.app.handlers.frame_change_post.clear()
    bpy.app.handlers.frame_change_post.append(updateStopmagic)


class StopmagicPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    frame_skip_count: bpy.props.IntProperty(
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
    insert_keyframe_after_skip: bpy.props.BoolProperty(
        name="Insert Keyframe after Skip",
        description="Whether to insert keyframe after skipping frames",
        options=set(),
        default=True,
    )

    def draw(self, context):
        self.layout.label(text="Frame Skip Options")
        self.layout.prop(self, "insert_keyframe_after_skip")
        row = self.layout.row()
        column = row.column()
        column.prop(self, "frame_skip_count")
        column = row.column()


class SkipFrameForward(bpy.types.Operator):
    """Skips frames forward based on the number of frames entered by the user."""

    bl_idname = "object.frame_forward_keyframe_mesh"
    bl_label = "Skip Frame"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        count = 3
        try:
            count = context.scene.stopmagic_frame_skip_count
        except Exception as e:
            print("KEYMESH :: Fetching frame skip count :: ", e)
            count = 3
        ob = context.active_object
        bpy.context.scene.frame_current += count
        if context.scene.stopmagic_insert_frame_after_skip:
            insert_mesh_keyframe(ob)
        return {"FINISHED"}


class SkipFrameBackward(bpy.types.Operator):
    """Skips frames backward based on the number of frames entered by the user."""

    bl_idname = "object.frame_backward_keyframe_mesh"
    bl_label = "Skip Frame"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        count = 3
        try:
            count = context.scene.stopmagic_frame_skip_count
        except Exception as e:
            print("KEYMESH :: Fetching frame skip count :: ", e)
            count = 3
        ob = context.active_object
        bpy.context.scene.frame_current -= count
        if context.scene.stopmagic_insert_frame_after_skip:
            insert_mesh_keyframe(ob)
        return {"FINISHED"}


class AddMeshKeyframe(bpy.types.Operator):
    """Adds a Keyframe to the currently selected Mesh, after which you can edit the mesh to keep the changes."""

    bl_idname = "object.keyframe_mesh"
    bl_label = "Keyframe Mesh"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        ob = context.active_object
        insert_mesh_keyframe(ob)
        return {"FINISHED"}


def updateStopmagic(scene):
    for object in scene.objects:
        if object.get("sm_datablock") is None:
            continue

        object_sm_id = object["sm_id"]
        object_sm_datablock = object["sm_datablock"]

        final_mesh = None
        for mesh in bpy.data.meshes:

            # No stopmagic Datablock
            if mesh.get("sm_id") is None:
                continue
            mesh_sm_id = mesh["sm_id"]
            mesh_sm_datablock = mesh["sm_datablock"]

            # No stopmagic data for this object
            if mesh_sm_id != object_sm_id:
                continue

            # No stopmagic data for this frame
            if mesh_sm_datablock != object_sm_datablock:
                continue

            final_mesh = mesh

        if not final_mesh:
            continue

        object.data = final_mesh


class PurgeStopmagicData(bpy.types.Operator):
    """Deletes all unushed Mesh data."""

    bl_idname = "object.purge_unused_data"
    bl_label = "Purge Unused Data"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        used_sm_mesh = {}

        for ob in bpy.data.objects:
            if ob.get("sm_id") is None:
                continue

            sm_id = ob.get("sm_id")
            used_sm_mesh[sm_id] = []

            fcurves = ob.animation_data.action.fcurves
            for fcurve in fcurves:
                if fcurve.data_path != '["sm_datablock"]':
                    continue

                keyframePoints = fcurve.keyframe_points
                for keyframe in keyframePoints:
                    used_sm_mesh[sm_id].append(keyframe.co.y)

        delete_mesh = []

        for mesh in bpy.data.meshes:
            if mesh.get("sm_id") is None:
                continue

            mesh_sm_id = mesh.get("sm_id")

            if mesh_sm_id not in used_sm_mesh:
                delete_mesh.append(mesh)
                continue

            mesh_sm_datablock = mesh.get("sm_datablock")

            if mesh_sm_datablock not in used_sm_mesh[mesh_sm_id]:
                delete_mesh.append(mesh)
                continue

        print("purged")
        for mesh in delete_mesh:
            print(mesh.name)
            mesh.use_fake_user = False

        updateStopmagic(bpy.context.scene)

        for mesh in delete_mesh:
            if mesh.users == 0:
                bpy.data.meshes.remove(mesh)

        return {"FINISHED"}


@persistent
def sm_frame_handler(dummy):  #
    obs = bpy.context.scene.objects
    for o in obs:
        if "sm_datablock" and "sm_id" in o:  # It's a Stopmagic scene
            bpy.app.handlers.frame_change_post.clear()
            bpy.app.handlers.frame_change_post.append(updateStopmagic)
            break


class InitializeHandler(bpy.types.Operator):
    """If Stopmagic stops working try using this function to re-initialize it's frame handler"""

    bl_idname = "object.initialize_handler"
    bl_label = "Initialize Handler"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.app.handlers.frame_change_post.clear()
        bpy.app.handlers.frame_change_post.append(updateStopmagic)
        return {"FINISHED"}


def register_properties():
    bpy.utils.register_class(StopmagicPreferences)
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
        default=True,
    )


def unregister_properties():
    del bpy.types.Scene.stopmagic_frame_skip_count
    del bpy.types.Scene.stopmagic_insert_frame_after_skip
    bpy.utils.unregister_class(StopmagicPreferences)


def addon_version():
    """Gets the string form of the addon version"""
    result = ""
    i = 0
    length = len(bl_info["version"])
    while i < length:
        result += str(bl_info["version"][i])
        if i + 1 != length:
            result += "."
        i += 1
    if "warning" in bl_info:
        result += " " + bl_info["warning"]
    return result


class StopmagicPanel(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_stopmagic_panel"
    bl_label = "Stopmagic"
    bl_category = "Stopmagic"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context: bpy.context):
        column = self.layout.column()
        column.label(text=("Version: " + addon_version()))
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


addon_keymaps = []


def register():
    bpy.utils.register_classes_factory([StopmagicPreferences])
    register_properties()
    bpy.utils.register_class(AddMeshKeyframe)
    bpy.utils.register_class(SkipFrameForward)
    bpy.utils.register_class(SkipFrameBackward)
    bpy.utils.register_class(PurgeStopmagicData)
    bpy.utils.register_class(InitializeHandler)
    bpy.utils.register_class(StopmagicPanel)
    bpy.app.handlers.load_post.append(sm_frame_handler)
    bpy.app.handlers.frame_change_post.clear()
    bpy.app.handlers.frame_change_post.append(updateStopmagic)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        keyMapView = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
        keyMapItem = keyMapView.keymap_items.new(
            "object.keyframe_mesh", type="A", value="PRESS", shift=True, ctrl=True
        )
        addon_keymaps.append((keyMapView, keyMapItem))
        keyMapItem = keyMapView.keymap_items.new(
            "object.frame_backward_keyframe_mesh",
            type="Z",
            value="PRESS",
            shift=True,
            ctrl=True,
        )
        addon_keymaps.append((keyMapView, keyMapItem))
        keyMapItem = keyMapView.keymap_items.new(
            "object.frame_forward_keyframe_mesh",
            type="X",
            value="PRESS",
            shift=True,
            ctrl=True,
        )
        addon_keymaps.append((keyMapView, keyMapItem))


def unregister():
    bpy.utils.register_classes_factory([StopmagicPreferences])
    unregister_properties()
    bpy.utils.unregister_class(AddMeshKeyframe)
    bpy.utils.unregister_class(SkipFrameForward)
    bpy.utils.unregister_class(SkipFrameBackward)
    bpy.utils.unregister_class(PurgeStopmagicData)
    bpy.utils.unregister_class(InitializeHandler)
    bpy.utils.unregister_class(StopmagicPanel)
    bpy.app.handlers.load_post.remove(sm_frame_handler)
    bpy.app.handlers.frame_change_post.clear()
    addon_keymaps.clear()


if __name__ == "__main__":
    register()
