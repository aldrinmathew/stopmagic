from __future__ import annotations
from typing import Any
import bpy
import bmesh
from stopmagic.functions.past_object import *
from stopmagic.functions.future_object import *
from stopmagic.functions.handle_onion_constraints import *


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
        for area in bpy.context.screen.areas:
            if area.type == "VIEW_3D":
                for space in area.spaces:
                    if space.type == "VIEW_3D":
                        space.shading.color_type = "OBJECT"

        #
        #   Check and collect meshes within the range specified by the user
        #
        pmeshes = []
        fmeshes = []
        if obj is not None:
            if obj.get("sm_datablock") is not None:
                name = obj.name
                frame = bpy.context.scene.frame_current
                for mesh in bpy.data.meshes:
                    i = frame - poffset
                    while i <= frame:
                        mesh_name: str = mesh.name
                        if mesh_name.find(name + "_sm_" + str(i)) != -1:
                            pmeshes.append(mesh)
                        i += 1
                    i = frame + 1
                    while i <= (frame + foffset):
                        if mesh.name == name + "_sm_" + str(i):
                            fmeshes.append(mesh)
                        i += 1
                    #
                #
                # To make sure that the onion for the previous keyframe doesn't overlay on the current frame
                if len(pmeshes) > 0:
                    pmeshes.pop(len(pmeshes) - 1)
                else:
                    if len(fmeshes) > 0:
                        fmeshes.remove(fmeshes[0])
                #
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
    else:
        fobject = get_future_object(future_exists)
        fobject.color = list(color)


def clear_onion_data():
    collection = bpy.data.collections.get("Stopmagic")
    for obj in collection.objects:
        mesh = obj.data
        bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.meshes.remove(mesh, do_unlink=True)
    bpy.data.collections.remove(collection)
