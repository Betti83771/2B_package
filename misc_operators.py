import bpy

def relocate_library_paths(old_path, new_path):
    old_path = old_path.replace("//", "")
    new_path = new_path.replace("//", "")
    for library in bpy.data.libraries:
        library.filepath = library.filepath.replace(old_path, new_path)

def turn_off_widgets_collections(layer_coll:bpy.types.LayerCollection):
    """scenewise"""
    for coll in layer_coll.children:
        if "WGTS" in coll.name:
            coll.hide_viewport = True 
        turn_off_widgets_collections(coll)

def recursively_find_rig(collection:bpy.types.Collection):
    rig = None
    for obj in collection.objects:
        if obj.type == 'ARMATURE': return obj
    for coll in collection.children:
        rig = recursively_find_rig(coll)
    return rig

def make_linked_rig_animatable(rig:bpy.types.Object, scene:bpy.types.Scene, view_layer: bpy.types.ViewLayer):
    override_hierarchy = rig.instance_collection.override_hierarchy_create(scene, view_layer)
    bpy.data.objects.remove(rig)
    turn_off_widgets_collections(view_layer.layer_collection)
    rig = recursively_find_rig(override_hierarchy)
    rig.show_in_front = True
    return

class TwoBMakeRigAnimatable(bpy.types.Operator):
    """Crea library override del rig selezionato e lo rende In front"""
    bl_idname = "twob.make_rig_animatable"
    bl_label = "Rendi animabile"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        if context.object:
            if context.object.instance_collection: return True
        return  False

    def execute(self, context):
        make_linked_rig_animatable(context.object, context.scene, context.window.view_layer)
        return  {'FINISHED'}

class TwoBRelocatePaths(bpy.types.Operator):
    """Replaces the old path with the new one in every library."""
    bl_idname = "twob.relocate_paths"
    bl_label = "Relocate paths"
    bl_options = {'UNDO'}

    old_path: bpy.props.StringProperty(subtype='FILE_PATH')
    new_path: bpy.props.StringProperty(subtype='FILE_PATH')


    def execute(self, context):
        relocate_library_paths(self.old_path, self.new_path)
        return  {'FINISHED'}