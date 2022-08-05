
from posixpath import split
import bpy
from os import sep
from .update_comp_node_tree import *
from .timeline_operators import *
from .make_anm_files_from_lay import *
from .misc_operators import *
from .enable_render_nodes import *
from .bind_unbind import * 
from .operators_refresh_drivers import *

class NewMistPanel(bpy.types.Panel):
    bl_label = "Mist"
    bl_idname = "TWOB_PT_newmist"
    bl_space_type = 'VIEW_3D'
    bl_category = "2B"
    bl_region_type = 'UI'
    bl_parent_id = "TWOB_PT_renderpanel"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        world = context.scene.world

        col = layout.column(align=True)
        col.prop(world.mist_settings, "start")
        col.prop(world.mist_settings, "depth")

        col = layout.column()
        col.prop(world.mist_settings, "falloff")

class TwoBUpdateComp(bpy.types.Operator):
    """Update compositor node tree from specified file zero"""
    bl_idname = "twob.update_compositor_nodes"
    bl_label = "Update compositor node tree"
    bl_options = {'REGISTER', 'UNDO'}

    file_zero: bpy.props.StringProperty(
        name="file_zero"
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        updated_scenes = update_comp_node_tree_func(context.window_manager.twob_file_zero)
        if updated_scenes == "file_not_found": 
            self.report({'ERROR'}, f"File not found: {context.window_manager.twob_file_zero}")
            return {'FINISHED'}
        self.report({'INFO'}, f"Following scenes node trees updated: {updated_scenes}")
        return {'FINISHED'}

class TwoBRenamePaths(bpy.types.Operator):
    """Rinomina tutti i percorsi del file che contengono il nome del file base, con il nome del file corrente"""
    bl_idname = "twob.rename_paths_filename"
    bl_label = "Rename Paths with file name"
    bl_options = {'REGISTER', 'UNDO'}

   # file_zero_name: bpy.props.StringProperty(
    #    name="file_zero"
    #)

    #@classmethod
    #def poll(cls, context):
     #   return cls.file_zero_name != ""

    def execute(self, context):
        rename_all_paths_with_filename()
        return{'FINISHED'}

class TwoBCompositingPanel(bpy.types.Panel):
    """Panel for useful operations in the 2B production"""
    bl_label = "Compositing"
    bl_idname = "TWOB_PT_comppanel"
    bl_space_type = 'VIEW_3D'
    bl_category = "2B"
    bl_region_type = 'UI'
    def draw(self, context):
        layout = self.layout
        layout.row().prop(context.window_manager, "twob_file_zero")
        layout.row().operator( "twob.update_compositor_nodes")
        layout.row().label(text="Update the Scenes and Layers names first, otherwise this may fail.", icon='INFO')
        layout.row().separator
        layout.row().operator( "twob.rename_paths_filename")
        layout.row().separator


class TwoBTimelinePanel(bpy.types.Panel):
    """Panel for useful operations in the 2B production"""
    bl_label = "Timeline Operations"
    bl_idname = "TWOB_PT_timelinepanel"
    bl_space_type = 'VIEW_3D'
    bl_category = "2B"
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        layout.row().operator( "twob.timeline_reset")
        layout.row().operator( "twob.timeline_uniform")

class TwoBRelocatePathPanel(bpy.types.Panel):
    """Panel for useful operations in the 2B production"""
    bl_label = "Relocate library paths"
    bl_idname = "TWOB_PT_relocpanel"
    bl_space_type = 'VIEW_3D'
    bl_category = "2B"
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        layout.row().prop(context.window_manager, "twob_relocate_paths_old_path")
        layout.row().prop(context.window_manager, "twob_relocate_paths_new_path")
        op =layout.row().operator( "twob.relocate_paths")
        op.old_path = context.window_manager.twob_relocate_paths_old_path
        op.new_path = context.window_manager.twob_relocate_paths_new_path

class TwoBMiscPanel(bpy.types.Panel):
    """Panel for useful operations in the 2B production"""
    bl_label = "Other"
    bl_idname = "TWOB_PT_miscpanel"
    bl_space_type = 'VIEW_3D'
    bl_category = "2B"
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        layout.row().operator( "twob.make_rig_animatable")
        layout.row().operator( "object.bind_all")
        layout.row().operator( "object.remobe_broken_drivers")
        layout.row().operator( "object.refresh_drivers")
        

    

class TwoBRenderPanel(bpy.types.Panel):
    """Panel for useful operations in the 2B production"""
    bl_label = "Render"
    bl_idname = "TWOB_PT_renderpanel"
    bl_space_type = 'VIEW_3D'
    bl_category = "2B"
    bl_region_type = 'UI'

    
    def draw(self, context):
        layout = self.layout

classes = [
    BindAll,
    RemoveBrokenDrivers,
    RefreshDrivers,
    TwoBTimelineUniform,
    TwoBTimelineReset,
    TwoBUpdateComp,
    TwoBEnableRenderNodesGenerateProps,
    TwoBEnableRenderNodesReset,
    TwoBMakeRigAnimatable,
    TwoBRelocatePaths,
    TwoBAnmFromLayout,
    TwoBRenamePaths,
    TwoBCompositingPanel,
    TwoBTimelinePanel,
    TwoBMiscPanel,
    TwoBRelocatePathPanel,
    TwoBRenderPanel,
    TwoBMakeAnmFilesSubpanel,
    TwoBEnableRenderNodesPanel,
    NewMistPanel

]

     
def twoB_ui_register():
    bpy.types.WindowManager.twob_file_zero = bpy.props.StringProperty(subtype='FILE_PATH',
                        name="File zero",
                        default=f"//..{sep}3D_ANM_SCE000{sep}3D_ANM_SCE000_CUT000.blend")
    bpy.types.WindowManager.twob_anm_destination_folder = bpy.props.StringProperty(subtype='DIR_PATH',
                        name="Destination folder",
                        default=f"//")
    bpy.types.WindowManager.twob_relocate_paths_old_path = bpy.props.StringProperty(subtype='FILE_PATH',
                        name="Old path",
                        default=f"//")
    bpy.types.WindowManager.twob_relocate_paths_new_path = bpy.props.StringProperty(subtype='FILE_PATH',
                        name="New path",
                        default=f"//")
    bpy.types.WindowManager.twob_anm_cut_number_of_pre_and_post_frames = bpy.props.IntProperty(
        default=3, name="Pre/post roll frames", min =0)
    bpy.types.Scene.twob_not_yet_generated_props = bpy.props.BoolProperty(default=True)
    for cls in classes:
        bpy.utils.register_class(cls)


def twoB_ui_unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.WindowManager.twob_file_zero
    del bpy.types.WindowManager.twob_anm_destination_folder
    del bpy.types.WindowManager.twob_relocate_paths_old_path
    del bpy.types.WindowManager.twob_relocate_paths_new_path
    del bpy.types.WindowManager.twob_anm_cut_number_of_pre_and_post_frames
    del  bpy.types.WindowManager.twob_not_yet_generated_props
    
    