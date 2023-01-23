import bpy
from os import sep

from .rigaprop_script import *



def rename_all_paths_with_filename_2():
    """filewise"""
    to_replace_with_SCE = "SCE" + bpy.path.basename(bpy.data.filepath).split("SCE")[-1][:3]
    to_replace_with_CUT = "CUT" + bpy.path.basename(bpy.data.filepath).split("CUT")[-1][:3]
    if to_replace_with_SCE == "nopatt" or to_replace_with_CUT == "nopatt":
        return
    for scene in bpy.data.scenes:
        if scene.library != None: continue # se la scena è linkata, non fare niente
        for node in scene.node_tree.nodes: # per ogni nodo nel compositor node tree della scena:
            existing_base_path = getattr(node, "base_path", None) # prendi il base path del nodo
            if not existing_base_path: continue # se non c'è il base path, non fare più niente
            to_be_replaced_SCE_list = ["SCE" + tbr[:3] for tbr in node.base_path.split("SCE") if tbr[2].isdigit()]
            to_be_replaced_CUT_list = ["CUT" + tbr[:3] for tbr in node.base_path.split("CUT") if tbr[2].isdigit()]
            for to_be_replaced_SCE in to_be_replaced_SCE_list:
                node.base_path = node.base_path.replace(to_be_replaced_SCE, to_replace_with_SCE) 
            for to_be_replaced_CUT in to_be_replaced_CUT_list:
                node.base_path = node.base_path.replace(to_be_replaced_CUT, to_replace_with_CUT) 
            
        ren_to_be_replaced_SCE = "SCE" + scene.render.filepath.split("SCE")[-1][:3]
        ren_to_be_replaced_CUT = "CUT" + scene.render.filepath.split("CUT")[-1][:3]
        scene.render.filepath = scene.render.filepath.replace(ren_to_be_replaced_SCE, to_replace_with_SCE)
        scene.render.filepath = scene.render.filepath.replace(ren_to_be_replaced_CUT, to_replace_with_CUT)

def relocate_library_paths(old_path, new_path):
    old_path = old_path.replace("//", "")
    new_path = new_path.replace("//", "")
    relocated_libraries = []
    for library in bpy.data.libraries:
        old_filepath = library.filepath
        library.filepath = library.filepath.replace(old_path, new_path)
        if library.filepath != old_filepath:
            relocated_libraries.append(library.name)
    return relocated_libraries


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
    """Replaces the old path with the new one in every library."""
    bl_idname = "twob.relocate_paths"
    bl_label = "Relocate library paths"
    bl_options = {'UNDO'}

    old_path: bpy.props.StringProperty(subtype='FILE_PATH')
    new_path: bpy.props.StringProperty(subtype='FILE_PATH')


    def execute(self, context):
        relocated_libraries = relocate_library_paths(self.old_path, self.new_path)
        if len(relocated_libraries):
            self.report(type={"INFO"}, message=f"Relocated Libraries:{str(relocated_libraries)}")
        else:
            self.report(type={"WARNING"}, message="No libraries found o relocate!")
        return  {'FINISHED'}




class TwoBRigaprop(bpy.types.Operator):
    """aaa."""
    bl_idname = "twob.make_proprig_collections_and_metarig"
    bl_label = "Make collections and metarig"
    bl_options = {'UNDO'}

    def execute(self, context):
        rigaprop(context)
        return  {'FINISHED'}