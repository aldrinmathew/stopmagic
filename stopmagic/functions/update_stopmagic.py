import bpy


def update_stopmagic(scene: bpy.types.Scene) -> None:
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