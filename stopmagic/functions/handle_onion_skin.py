from __future__ import annotations
from typing import Any
import bpy
import bmesh
from stopmagic.functions.get_object_key_values import get_object_key_values
from stopmagic.functions.past_object import *
from stopmagic.functions.future_object import *
from stopmagic.functions.handle_onion_constraints import *
from stopmagic.functions.get_object_keyframes import *


def handle_collections(past: bpy.types.Object, future: bpy.types.Object) -> None:
    if bpy.data.collections.get("Stopmagic"):
        sm_collection = bpy.data.collections["Stopmagic"]
    else:
        sm_collection = bpy.data.collections.new("Stopmagic")
        bpy.context.scene.collection.children.link(sm_collection)
        sm_collection.objects.link(past)
        sm_collection.objects.link(future)
        sm_collection.hide_render = True
    sm_collection.hide_select = True


def handle_onion_skin(dummy):
    """Automatically handles Onion Skin objects and populates them with mesh data"""
    mode_value: str | int | Any = bpy.context.view_layer.objects.active.mode
    mode = ""
    if type(mode_value) == str:
        mode: str = mode_value
    elif type(mode_value) == int:
        modes = [
            "OBJECT",
            "EDIT",
            "POSE",
            "SCULPT",
            "VERTEX_PAINT",
            "WEIGHT_PAINT",
            "TEXTURE_PAINT",
            "PARTICLE_EDIT",
            "EDIT_GPENCIL",
            "SCULPT_GPENCIL",
            "PAINT_GPENCIL",
            "WEIGHT_GPENCIL",
            "VERTEX_GPENCIL",
        ]
        mode: str = modes[mode_value]
    else:
        mode: str = "OBJECT"

    obj = bpy.context.view_layer.objects.active
    if obj.use_dynamic_topology_sculpting is None:
        dyntopo = False
    else:
        dyntopo = obj.use_dynamic_topology_sculpting
    if obj.type == "MESH" and bpy.context.scene.stopmagic_onion_skin_enabled:
        #
        #   Creating or retrieving stopmagic onion skin object data
        #
        past_exists: bool = past_object_exists()
        future_exists: bool = future_object_exists()
        pobject = get_past_object(past_exists)
        fobject = get_future_object(future_exists)
        # Past and Future Offset values from the scene
        poffset = bpy.context.scene.stopmagic_past_offset
        foffset = bpy.context.scene.stopmagic_future_offset

        handle_collections(pobject, fobject)

        # Handle constraints
        handle_onion_constraints(pobject, obj)
        handle_onion_constraints(fobject, obj)

        #
        #   Onion Skin objects visibility
        #
        pobject.color = bpy.context.scene.stopmagic_past_color
        fobject.color = bpy.context.scene.stopmagic_future_color
        pmaterial = bpy.data.materials.get("stopmagic_material_past")
        fmaterial = bpy.data.materials.get("stopmagic_material_future")
        if pmaterial is None:
            pmaterial = bpy.data.materials.new(name="stopmagic_material_past")
            pobject.active_material = pmaterial
            pmaterial.use_nodes = True
            pmat_output = pmaterial.node_tree.nodes.get("Material Output")
            p_principled = pmaterial.node_tree.nodes.get("Principled BSDF")
            pmaterial.node_tree.links.new(
                pmat_output.inputs[0], p_principled.outputs[0]
            )
            p_principled.inputs[
                0
            ].default_value = bpy.context.scene.stopmagic_past_color
            opacity = bpy.context.scene.stopmagic_past_color[3]
            if opacity > 0 and opacity < 1:
                p_principled.inputs[
                    21
                ].default_value = bpy.context.scene.stopmagic_past_color[3]
            else:
                p_principled.inputs[21].default_value = 0.3
            pmaterial.diffuse_color = bpy.context.scene.stopmagic_past_color
            pmaterial.blend_method = "HASHED"
        if fmaterial is None:
            fmaterial = bpy.data.materials.new(name="stopmagic_material_future")
            fobject.active_material = fmaterial
            fmaterial.use_nodes = True
            fmat_output = fmaterial.node_tree.nodes.get("Material Output")
            f_principled = fmaterial.node_tree.nodes.get("Principled BSDF")
            fmaterial.node_tree.links.new(
                fmat_output.inputs[0], f_principled.outputs[0]
            )
            f_principled.inputs[
                0
            ].default_value = bpy.context.scene.stopmagic_future_color
            opacity = bpy.context.scene.stopmagic_future_color[3]
            if opacity > 0 and opacity < 1:
                f_principled.inputs[
                    21
                ].default_value = bpy.context.scene.stopmagic_future_color[3]
            else:
                f_principled.inputs[21].default_value = 0.3
            fmaterial.diffuse_color = bpy.context.scene.stopmagic_future_color
            fmaterial.blend_method = "HASHED"
        #
        #   Check and collect meshes within the range specified by the user
        #
        pmeshes = []
        fmeshes = []
        if obj is not None:
            if obj.get("sm_datablock") is not None:
                name = obj.name
                frame = bpy.context.scene.frame_current
                keyframes = get_object_keyframes(obj)
                key_values = get_object_key_values(obj)
                if len(key_values) > 0:
                    p_frames = []
                    p_key_values = []
                    f_frames = []
                    f_key_values = []
                    index = 0
                    while index < len(keyframes):
                        if keyframes[index] < frame:
                            p_key_values.append(key_values[index])
                            p_frames.append(keyframes[index])
                        elif keyframes[index] > frame:
                            f_key_values.append(key_values[index])
                            f_frames.append(keyframes[index])
                        index += 1
                    # To make sure that the onion for the previous keyframe doesn't
                    # overlay the current mesh
                    if len(p_key_values) > 0 and frame not in keyframes:
                        p_frames.pop(len(p_key_values) - 1)
                        p_key_values.pop(len(p_key_values) - 1)
                    # To make sure that, if there are no previous keyframes then the
                    # onion for the next keyframe doesn't overlay the current mesh
                    elif (
                        len(p_key_values) == 0
                        and len(f_key_values) > 0
                        and frame not in keyframes
                    ):
                        f_frames.pop(0)
                        f_key_values.pop(0)
                    #
                    if bpy.context.scene.stopmagic_onion_display_type == "POSE":
                        p_count = bpy.context.scene.stopmagic_past_count
                        f_count = bpy.context.scene.stopmagic_future_count
                        if len(p_key_values) > p_count:
                            index = 0
                            bound = len(p_key_values) - p_count
                            while index < bound:
                                p_frames.pop(0)
                                p_key_values.pop(0)
                                index += 1
                        if len(f_key_values) > f_count:
                            index = f_count
                            bound = len(f_key_values)
                            while index < bound:
                                f_frames.pop(index)
                                f_key_values.pop(index)
                                index += 1
                    elif bpy.context.scene.stopmagic_onion_display_type == "RANGE":
                        p_result = []
                        f_result = []
                        i = 0
                        while i < len(p_frames):
                            if p_frames[i] > (
                                frame - bpy.context.scene.stopmagic_past_offset
                            ):
                                p_result.append(p_key_values[i])
                            i += 1
                        i = 0
                        while i < len(f_frames):
                            if f_frames[i] < (
                                frame + bpy.context.scene.stopmagic_future_offset
                            ):
                                f_result.append(f_key_values[i])
                            i += 1
                        p_key_values = p_result
                        f_key_values = f_result
                    #
                    if len(p_key_values) > 0:
                        for pkey in p_key_values:
                            pmeshes.append(
                                bpy.data.meshes.get(name + "_sm_" + str(pkey))
                            )
                    if len(f_key_values) > 0:
                        for fkey in f_key_values:
                            fmeshes.append(
                                bpy.data.meshes.get(name + "_sm_" + str(fkey))
                            )
            #
        #
        # Past
        bpy.context.view_layer.objects.active = pobject
        bpy.ops.object.mode_set(mode="EDIT")
        pbmesh: bmesh.types.BMesh = bmesh.from_edit_mesh(pobject.data)
        bmesh.ops.delete(pbmesh, geom=pbmesh.verts, context="VERTS")
        for mesh in pmeshes:
            pbmesh.from_mesh(mesh)
        bmesh.update_edit_mesh(pobject.data)
        bpy.ops.object.mode_set(mode="OBJECT")
        # Future
        bpy.context.view_layer.objects.active = fobject
        bpy.ops.object.mode_set(mode="EDIT")
        fbmesh: bmesh.types.BMesh = bmesh.from_edit_mesh(fobject.data)
        bmesh.ops.delete(fbmesh, geom=fbmesh.verts, context="VERTS")
        for mesh in fmeshes:
            fbmesh.from_mesh(mesh)
        bmesh.update_edit_mesh(fobject.data)
        bpy.ops.object.mode_set(mode="OBJECT")
        # Back to the main control flow
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode=mode, toggle=False)
        if mode == "SCULPT":
            if (
                bpy.context.view_layer.objects.active.get(
                    "use_dynamic_topology_sculpting"
                )
                != dyntopo
            ):
                bpy.ops.sculpt.dynamic_topology_toggle()


def change_onion_color(past: bool, color: bpy.props.FloatVectorProperty):
    past_exists: bool = past_object_exists()
    future_exists: bool = future_object_exists()
    if past:
        pobject = get_past_object(past_exists)
        pobject.color = list(color)
        pmaterial = bpy.data.materials.get("stopmagic_material_past")
        if pmaterial is not None:
            pmaterial.diffuse_color = color
            if not pmaterial.use_nodes:
                pmaterial.use_nodes = True
            if pmaterial.node_tree.get("Principled BSDF") is not None:
                p_principled = pmaterial.node_tree.get("Principled BSDF")
                p_principled.inputs[0] = list(color)
                opacity = color[3]
                if opacity > 0 and opacity < 1:
                    p_principled.inputs[21].default_value = color[3]
                else:
                    p_principled.inputs[21].default_value = 0.3
    else:
        fobject = get_future_object(future_exists)
        fobject.color = list(color)
        fmaterial = bpy.data.materials.get("stopmagic_material_future")
        if fmaterial is not None:
            fmaterial.diffuse_color = color
            if not fmaterial.use_nodes:
                fmaterial.use_nodes = True
            if fmaterial.node_tree.get("Principled BSDF") is not None:
                f_principled = fmaterial.node_tree.get("Principled BSDF")
                f_principled.inputs[0] = list(color)
                opacity = color[3]
                if opacity > 0 and opacity < 1:
                    f_principled.inputs[21].default_value = color[3]
                else:
                    f_principled.inputs[21].default_value = 0.3


def clear_onion_data():
    collection = bpy.data.collections.get("Stopmagic")
    pmaterial = bpy.data.materials.get("stopmagic_material_past")
    fmaterial = bpy.data.materials.get("stopmagic_material_future")
    if pmaterial is not None:
        bpy.data.materials.remove(pmaterial, do_unlink=True)
    if fmaterial is not None:
        bpy.data.materials.remove(fmaterial, do_unlink=True)
    if collection.get("objects") is not None:
        for obj in collection.objects:
            mesh = obj.data
            obj.name = "removed"
            bpy.context.scene.objects.unlink(obj)
            bpy.data.meshes.remove(mesh, do_unlink=True)
            bpy.data.objects.remove(obj, do_unlink=True)
    bpy.data.collections.remove(collection)
    bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=False, do_recursive=False)
