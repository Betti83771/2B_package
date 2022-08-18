import bpy

def rigaprop(context):
    """Run this script with the collection above the linking collection active in the outliner (the one that has the same name of file name)"""

    filename = bpy.path.basename(bpy.data.filepath).replace(".blend", "")

    current_coll = context.collection

    obj_coll = next(coll for coll in current_coll.children if filename in coll.name)

    for coll_suffix in ("_RIG", "_GEO", "_DEFORM" ):


        if filename + coll_suffix in bpy.data.collections.keys(): continue

        coll = bpy.data.collections.new(filename  + coll_suffix)


        obj_coll.children.link(coll)

    metarig_coll =  bpy.data.collections.new(filename + "_METARIG" )

    current_coll.children.link(metarig_coll)

    bpy.ops.object.armature_add(enter_editmode=False, align='WORLD', location=(0.00266746, -0.19931, 0.734643), scale=(1, 1, 1))


    metarig_coll.objects.link(context.active_object)
    current_coll.objects.unlink(context.active_object)