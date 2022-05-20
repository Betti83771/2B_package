
import bpy
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
    bpy.utils.register_class(TwoBRenderPanel)
    
    bpy.utils.register_class(NewMistPanel)


def twoB_ui_unregister():
    bpy.utils.unregister_class(NewMistPanel)
    bpy.utils.unregister_class(TwoBRenderPanel)
    
    