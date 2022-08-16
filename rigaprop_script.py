import bpy

def rigaprop(collection):
    """Run this script with the collection above the linking collection active in the outliner (the one that has the same name of file name)"""

    filename = bpy.path.basename(bpy.data.filepath).replace(".blend", "")

    current_coll = collection

    obj_coll = next(coll for coll in current_coll.children if filename in coll.name)

    for coll_suffix in ("_RIG", "_GEO", "_DEFORM" ):


        if filename + coll_suffix in bpy.data.collections.keys(): continue

        coll = bpy.data.collections.new(filename  + "_RIG")


        obj_coll.children.link(coll)

    metarig_coll =  bpy.data.collections.new(filename + "_METARIG" )

    current_coll.children.link(metarig_coll)

    new_rig_data = bpy.data.armatures.new(filename + "_METARIG" )
    new_rig = bpy.data.objects.new(filename + "_METARIG" ,new_rig_data)
    metarig_coll.objects.link(new_rig)