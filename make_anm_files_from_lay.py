import bpy
from os import sep
from .misc_operators import rename_all_paths_with_filename

def saveas_cut_file(base_filename:str, destination_path:str, cut_name:str):
    """destination_path: 3D_ANM_SCE000 folder, in which to create the anm cut blends
        cut_name : CUT000"""
    bpy.ops.wm.save_as_mainfile(filepath=destination_path + sep + base_filename + "_" + cut_name + ".blend")

def make_markers_dict(scene:bpy.types.Scene):
    marker_dict = {}
    for marker in scene.timeline_markers:
            marker_dict[marker.name] = marker.frame
    return marker_dict

def clear_markers(scene:bpy.types.Scene):
    for marker in reversed(scene.timeline_markers): 
        scene.timeline_markers.remove(marker)

def frame_from_marker(marker):
    return marker.frame

def get_cut_names_and_duration(scene:bpy.types.Scene, roll_frames:int):
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
            frame_end = int(frame_sorted_markers[i + 1].frame) + roll_frames
            next_cut_name = frame_sorted_markers[i + 1].name.replace("_START", "")
        dict[marker.name.replace("_START", "")] = (int(marker.frame) - roll_frames, frame_end, next_cut_name)
    return dict

def make_anm_files_func(scene_name, destination_path, roll_frames):
    scene = bpy.data.scenes[scene_name]
    lay_filepath = bpy.data.filepath
    base_filename = bpy.path.basename(lay_filepath).replace("LAY", "ANM").replace(".blend", "")
    original_frame_start = scene.frame_start
    original_frame_end = scene.frame_end
    #original_markers = make_markers_dict(scene)
    cut_dict = get_cut_names_and_duration(scene, roll_frames)
    prev_file_name = bpy.path.basename(lay_filepath)
    for key, value in cut_dict.items():
        clear_markers(scene)
        scene.frame_start = value[0]
        scene.frame_end = value[1]
        scene.timeline_markers.new("START", frame=value[0] + roll_frames)
        scene.timeline_markers.new("PRE", frame=value[0])
        if value[2]:
            scene.timeline_markers.new("END", frame=value[1] - roll_frames) 
            scene.timeline_markers.new("POST", frame=value[1]) 
        else:
            scene.timeline_markers.new("END", frame=original_frame_end)
        rename_all_paths_with_filename(old_file_name=prev_file_name)
        saveas_cut_file(base_filename, bpy.path.abspath(destination_path), key)
        prev_file_name = bpy.path.basename(bpy.data.filepath)
    bpy.ops.wm.open_mainfile(filepath=lay_filepath )
    scene = bpy.data.scenes[scene_name]
    scene.frame_start =   original_frame_start
    scene.frame_end = original_frame_end
        

class TwoBAnmFromLayout(bpy.types.Operator):
    """Crea un file ANM per ogni cut da questo file di LAUYOUT"""
    bl_idname = "twob.make_anm_files_from_lay"
    bl_label = "Make ANM files from LAYOUT"
    bl_options = {'UNDO'}

    folder_path: bpy.props.StringProperty(subtype='DIR_PATH', name="Destination folder")
    pre_and_post_frames: bpy.props.IntProperty(
        default=3, name="Pre/post roll frames", min =0)

    def execute(self, context):
        make_anm_files_func(context.scene.name, self.folder_path, self.pre_and_post_frames)
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
        layout.row().prop(context.window_manager, "twob_anm_cut_number_of_pre_and_post_frames")
        layout.row().label(text="Reset the timelines first!", icon="INFO")
        layout.row().label(text="Also, save this file first.", icon="GHOST_ENABLED")
        layout.row().label(text="Any unsaved changes will be lost.")
        op = layout.row().operator( "twob.make_anm_files_from_lay")
        op.folder_path = context.window_manager.twob_anm_destination_folder
        op.pre_and_post_frames = context.window_manager.twob_anm_cut_number_of_pre_and_post_frames