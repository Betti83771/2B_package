import bpy
from os import sep

def saveas_cut_file(destination_path:str, cut_name:str):
    """destination_path: 3D_ANM_SCE000 folder, in which to create the anm cut blends
        cut_name : CUT000"""
    bpy.ops.wm.save_as_mainfile(filepath=destination_path + sep + cut_name + ".blend")

def frame_from_marker(marker):
    return marker.frame

def get_cut_names_and_duration(scene:bpy.types.Scene):
    """
    {
        cut name: (start int, end int, next cut str or None)
        ...
        }
    """
    frame_sorted_markers = []
    for marker in scene.timeline_markers:
        if not marker.name.endswith("_START"): continue
        frame_sorted_markers.append(marker)
    frame_sorted_markers.sort(key=frame_from_marker)
    len_markers = len(frame_sorted_markers)
    dict = {}
    for i, marker in enumerate(frame_sorted_markers):
        if i+1 == len_markers: 
            frame_end = int(scene.frame_end)
            next_cut_name = None
        else:
            frame_end = int(frame_sorted_markers[i + 1].frame) + 3
            next_cut_name = frame_sorted_markers[i + 1].name.replace("_START", "")
        dict[marker.name.replace("_START", "")] = (int(marker.frame) - 3, frame_end, next_cut_name)
    return dict

def make_anm_files_func(scene, destination_path):
    original_frame_start = scene.frame_start
    original_frame_end = scene.frame_end
    cut_dict = get_cut_names_and_duration(scene)
    for key, value in cut_dict.items():
        scene.frame_start = value[0]
        scene.frame_end = value[1]
        if value[2]:
            scene.timeline_markers[value[2] + "_START"].name = key + "_END"
        saveas_cut_file(destination_path, key)
        if value[2]:
            scene.timeline_markers[key + "_END"].name = value[2] + "_START"
    scene.frame_start =   original_frame_start
    scene.frame_end = original_frame_end
        


class TwoBAnmFromLayout(bpy.types.Operator):
    """Crea un file ANM per ogni cut da questo file di LAUYOUT"""
    bl_idname = "twob.make_anm_files_from_lay"
    bl_label = "Make ANM files from LAYOUT"
    bl_options = {'UNDO'}

    folder_path: bpy.props.StringProperty(subtype='DIR_PATH')

    def execute(self, context):
        make_anm_files_func(context.scene, self.folder_path)
        return  {'FINISHED'}

class TwoBMakeAnmFilesSubpanel(bpy.types.Panel):
    bl_label = "Make ANM files from LAYOUT"
    bl_idname = "TWOB_PT_makeanmfilessubpanel"
    bl_space_type = 'VIEW_3D'
    bl_category = "2B"
    bl_region_type = 'UI'
    bl_parent_id = "TWOB_PT_comppanel"

    def draw(self, context):
        layout = self.layout
        layout.row().prop(context.window_manager, "twob_anm_destination_folder")
        op = layout.row().operator( "twob.make_anm_files_from_lay")
        op.folder_path = context.window_manager.twob_anm_destination_folder