
import bpy
from os import sep
from .update_comp_node_tree import *
from bl_ui.properties_world import EEVEE_WORLD_PT_mist

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
        self.report({'INFO'}, f"Following scenes node trees updated: {updated_scenes}")
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

    

class TwoBRenderPanel(bpy.types.Panel):
    """Panel for useful operations in the 2B production"""
    bl_label = "Render"
    bl_idname = "TWOB_PT_renderpanel"
    bl_space_type = 'VIEW_3D'
    bl_category = "2B"
    bl_region_type = 'UI'

    
    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.prop(context.scene.world.node_tree.nodes["Background"].inputs[1], "default_value", text="World strength")
        
     
def twoB_ui_register():
    bpy.types.WindowManager.twob_file_zero = bpy.props.StringProperty(subtype='FILE_PATH',
                        name="File zero",
                        default=f"//3D_ANMs{sep}3D_ANM_SCE000{sep}3D_ANM_SCE000_CUT000")
    bpy.utils.register_class(TwoBUpdateComp)
    bpy.utils.register_class(TwoBCompositingPanel)
    bpy.utils.register_class(TwoBRenderPanel)
    bpy.utils.register_class(NewMistPanel)


def twoB_ui_unregister():
    bpy.utils.unregister_class(TwoBUpdateComp)
    bpy.utils.unregister_class(TwoBCompositingPanel)
    bpy.utils.unregister_class(NewMistPanel)
    bpy.utils.unregister_class(TwoBRenderPanel)
    
    