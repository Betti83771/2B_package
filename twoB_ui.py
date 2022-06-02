
import bpy
from os import sep
from .update_comp_node_tree import *
from .timeline_operators import *
from .make_anm_files_from_lay import *
from .misc_operators import *

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
    

class TwoBRenderPanel(bpy.types.Panel):
    """Panel for useful operations in the 2B production"""
    bl_label = "Render"
    bl_idname = "TWOB_PT_renderpanel"
    bl_space_type = 'VIEW_3D'
    bl_category = "2B"
    bl_region_type = 'UI'

    
    def draw(self, context):
        layout = self.layout

     
def twoB_ui_register():
    bpy.types.WindowManager.twob_file_zero = bpy.props.StringProperty(subtype='FILE_PATH',
                        name="File zero",
                        default=f"//..{sep}3D_ANM_SCE000{sep}3D_ANM_SCE000_CUT000.blend")
    bpy.types.WindowManager.twob_anm_destination_folder = bpy.props.StringProperty(subtype='DIR_PATH',
                        name="Destination folder",
                        default=f"")
    bpy.utils.register_class(TwoBTimelineUniform)
    bpy.utils.register_class(TwoBTimelineReset)
    bpy.utils.register_class(TwoBUpdateComp)
    bpy.utils.register_class(TwoBMakeRigAnimatable)
    bpy.utils.register_class(TwoBAnmFromLayout)
    bpy.utils.register_class(TwoBRenamePaths)
    bpy.utils.register_class(TwoBCompositingPanel)
    bpy.utils.register_class(TwoBTimelinePanel)
    bpy.utils.register_class(TwoBMiscPanel)
    bpy.utils.register_class(TwoBRenderPanel)
    bpy.utils.register_class(TwoBMakeAnmFilesSubpanel)
    bpy.utils.register_class(NewMistPanel)


def twoB_ui_unregister():
    bpy.utils.unregister_class(TwoBTimelineUniform)
    bpy.utils.unregister_class(TwoBTimelineReset)
    bpy.utils.unregister_class(TwoBUpdateComp)
    bpy.utils.unregister_class(TwoBAnmFromLayout)
    bpy.utils.unregister_class(TwoBRenamePaths)
    bpy.utils.unregister_class(TwoBMakeRigAnimatable)
    bpy.utils.unregister_class(TwoBCompositingPanel)
    bpy.utils.unregister_class(TwoBTimelinePanel)
    bpy.utils.unregister_class(TwoBMiscPanel)
    bpy.utils.unregister_class(NewMistPanel)
    bpy.utils.unregister_class(TwoBMakeAnmFilesSubpanel)
    bpy.utils.unregister_class(TwoBRenderPanel)
    del bpy.types.WindowManager.twob_file_zero
    del bpy.types.WindowManager.twob_anm_destination_folder
    
    