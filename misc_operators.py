import bpy
from os import sep

from .rigaprop_script import *

def find_parts_to_replace_in_file_path(old_file_path, old_file_name):
    path_splits = old_file_path.split(sep)
    if len(path_splits) < 2:
        print("2B: Separator error while replacing paths. Please use the file zero's native OS or convert its paths.")
        return "wrong os"
    for split in path_splits:
        if old_file_name in split: return split
    return "no_replacement"

def rename_all_paths_with_filename(old_file_name="SCE000"):
    """filewise"""
    name_to_replace = bpy.path.basename(bpy.data.filepath).replace("3D_", "").replace(".blend", "")
    for scene in bpy.data.scenes:
        if scene.library != None: continue
        for node in scene.node_tree.nodes:
            existing_base_path = getattr(node, "base_path", None)
            if not existing_base_path: continue
            to_be_replaced = find_parts_to_replace_in_file_path(existing_base_path, old_file_name)
            if to_be_replaced == "no_replacement": continue
            node.base_path = existing_base_path.replace(to_be_replaced, name_to_replace)
        to_be_replaced_render = find_parts_to_replace_in_file_path(scene.render.filepath, old_file_name)
        if to_be_replaced_render == "no_replacement": continue
        scene.render.filepath = scene.render.filepath.replace(to_be_replaced_render, name_to_replace)




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

class TwoBRelocatePaths(bpy.types.Operator):
    """Replaces the old path with the new one in every library.
    DEPRECATED IN Blender 3.3"""
    bl_idname = "twob.relocate_paths"
    bl_label = "Relocate library paths"
    bl_options = {'UNDO'}

    old_path: bpy.props.StringProperty(subtype='FILE_PATH')
    new_path: bpy.props.StringProperty(subtype='FILE_PATH')


    def execute(self, context):
        relocate_library_paths(self.old_path, self.new_path)
        return  {'FINISHED'}




class TwoBRigaprop(bpy.types.Operator):
    """aaa."""
    bl_idname = "twob.make_proprig_collections_and_metarig"
    bl_label = "Make collections and metarig"
    bl_options = {'UNDO'}

    def execute(self, context):
        rigaprop(context)
        return  {'FINISHED'}