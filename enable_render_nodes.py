import bpy


def followLinks(node_in:bpy.types.Node, node_list):
    for n_outputs in node_in.outputs:
        for node_links in n_outputs.links:
            node_list.append(node_links.to_node.name)
          #  print("going to " + node_links.to_node.name)
            node_list = followLinks(node_links.to_node, node_list)
    return node_list


def erngp_prop_update(self, context:bpy.types.Context):
    layer_node = next(node for node in context.scene.node_tree.nodes if node.bl_idname == "CompositorNodeRLayers" and node.layer == self.prop.name)
    empty_list = []
    given_node_companions = followLinks(layer_node, empty_list)
    for node_comp in given_node_companions:
        if self.prop:
            node_comp.mute = False
            context.scene.view_layers[self.prop.name].use = False
        else:
            node_comp.mute = True
            context.scene.view_layers[self.prop.name].use = True


def erngp_generate_boolprops(context:bpy.types.Context):
    """
    only current scene"""
    for layer in context.scene.view_layers:
        layer_name =layer.name
        exec(f"""
def erngp_prop_update_{layer_name}(self, context):
    layer_node = next(node for node in context.scene.node_tree.nodes if node.bl_idname == "CompositorNodeRLayers" and node.layer == "{layer_name}")
    empty_list = []
    given_node_companions = followLinks(layer_node, empty_list)
    for node_comp in given_node_companions:
        if self.twob_renderboolprop_{layer_name}:
            context.scene.node_tree.nodes[node_comp].mute = False
            context.scene.view_layers["{layer_name}"].use = True
        else:
            context.scene.node_tree.nodes[node_comp].mute = True
            context.scene.view_layers["{layer_name}"].use = False
bpy.types.Scene.twob_renderboolprop_{layer_name} = bpy.props.BoolProperty(name="twob_renderboolprop_{layer_name}", default=True, update=erngp_prop_update_{layer_name})""")
    
def  erngp_delete_boolprops(context):
    for name, prop in context.window_manager.items():
        if name.startswith("twob_renderboolprop_"): del prop

class TwoBEnableRenderNodesGenerateProps(bpy.types.Operator):
    """Click here to start"""
    bl_idname = "twob.generate_render_nodes_boolprops"
    bl_label = "Initialize switches"
    bl_options = {'UNDO'}


    def execute(self, context):
        erngp_generate_boolprops(context)
        context.scene.twob_not_yet_generated_props = False
        return  {'FINISHED'}

class TwoBEnableRenderNodesReset(bpy.types.Operator):
    """Delete all properties for a fresh start in this scene, something changes or the props break for whatever reason"""
    bl_idname = "twob.delete_render_nodes_boolprops"
    bl_label = "Reset"
    bl_options = {'UNDO'}


    def execute(self, context):
        erngp_delete_boolprops(context)
        context.scene.twob_not_yet_generated_props = True
        return  {'FINISHED'}

class TwoBEnableRenderNodesPanel(bpy.types.Panel):
    """Panel for useful operations in the 2B production"""
    bl_label = "Enable / disable render nodes"
    bl_idname = "TWOB_PT_enablerendernodespanel"
    bl_space_type = 'VIEW_3D'
    bl_category = "2B"
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        
        if context.scene.twob_not_yet_generated_props:
            layout.row().operator( "twob.generate_render_nodes_boolprops")
        else:
            col = layout.column(align=True)
            col.row().label(text="BKG")
            for layer in context.scene.view_layers:
                if "BKG" not in layer.name: continue
                col.row().prop(context.scene, "twob_renderboolprop_" + layer.name, text=layer.name)
            col = layout.column(align=True)
            col.row().label(text="CHR")
            for layer in context.scene.view_layers:
                if "CHR" not in layer.name: continue
                col.row().prop(context.scene, "twob_renderboolprop_" + layer.name, text=layer.name)
            col = layout.column(align=True)
            col.row().operator("twob.delete_render_nodes_boolprops")

        
