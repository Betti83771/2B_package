import bpy


def followLinks(node_in:bpy.types.Node, node_list):
    for n_outputs in node_in.outputs:
        for node_links in n_outputs.links:
            node_list.append(node_links.to_node.name)
          #  print("going to " + node_links.to_node.name)
            node_list = followLinks(node_links.to_node, node_list)
    return node_list

def check_if_use_for_render_has_to_be_disabled(layer:str, display_name:str, node_tree:bpy.types.CompositorNodeTree):
    nodes_that_use_the_layer  = [node for node in node_tree.nodes if  node.bl_idname == 'CompositorNodeRLayers' and node.layer == layer]
    for node in nodes_that_use_the_layer: # if just one has a different frame group, don't disable the layer
        if not node.parent: continue
        if not node.parent.name.startswith(display_name): 
            return False
    return True


def  erngp_delete_boolprops(scene:bpy.types.Scene):
    for name, prop in scene.items():
        if name.startswith("twob_renderboolprop_"): del prop

def  erngp_delete_enumprops(scene:bpy.types.Scene):
    for name, prop in scene.items():
        if name.startswith("twob_renderenumprop_"): del prop


def erngp_generate_props(scene:bpy.types.Scene):
    """only current scene"""
    if not len(scene.twob_layernamedata.items()): return "error"
    for layer_data in scene.twob_layernamedata:
        base_layers = [layerp.layer for layerp in layer_data.base_layers]
        exec(f"""
def erngp_enumprop_update_{layer_data.display_name}(self, context):
    if not context.scene.twob_renderboolprop_{layer_data.display_name}: return
    if self.twob_renderenumprop_{layer_data.display_name} == "2D Lights":
        for node in context.scene.node_tree.nodes:
            if node.parent == context.scene.node_tree.nodes["{layer_data.luci_2D}"]:
                node.mute = True
            elif node.parent == context.scene.node_tree.nodes["{layer_data.luci_3D}"]:
                node.mute = False
    elif self.twob_renderenumprop_{layer_data.display_name} == "3D Lights":
        for node in context.scene.node_tree.nodes:
            if node.parent == context.scene.node_tree.nodes["{layer_data.luci_3D}"]:
                node.mute = True
            elif node.parent == context.scene.node_tree.nodes["{layer_data.luci_2D}"]:
                node.mute = False
    return

def erngp_boolprop_update_{layer_data.display_name}(self, context):
   # frame_data = context.scene.twob_layernamedata[context.scene.twob_layernamedata.find("{layer_data.display_name}")]
    if self.twob_renderboolprop_{layer_data.display_name}:
        for node in context.scene.node_tree.nodes:
            if node.parent == context.scene.node_tree.nodes["{layer_data.base}"]:
                node.mute = False
            if node.parent == context.scene.node_tree.nodes["{layer_data.luci_2D}"] and context.scene.twob_renderenumprop_{layer_data.display_name} == '2D Lights':
                node.mute = False  
            if node.parent == context.scene.node_tree.nodes["{layer_data.luci_3D}"] and context.scene.twob_renderenumprop_{layer_data.display_name} == '3D Lights':
                node.mute = False
        for layer in {base_layers}:
            if layer in context.scene.view_layers.keys():
                context.scene.view_layers[layer].use = True
    else:
        for node in context.scene.node_tree.nodes:
            if node.parent == context.scene.node_tree.nodes["{layer_data.base}"]:
                node.mute = True
            if node.parent == context.scene.node_tree.nodes["{layer_data.luci_2D}"]:
                node.mute = True  
            if node.parent == context.scene.node_tree.nodes["{layer_data.luci_3D}"]:
                node.mute = True
        for layer in {base_layers}:
            if check_if_use_for_render_has_to_be_disabled(layer, "{layer_data.display_name}", context.scene.node_tree):
                context.scene.view_layers[layer].use = False
    return

bpy.types.Scene.twob_renderenumprop_{layer_data.display_name} = bpy.props.EnumProperty(
                                                    items=[('2D Lights', '2D Lights', ""), ('3D Lights', '3D Lights', "")],
                                                    name="twob_renderenumprop_{layer_data.display_name}",
                                                    default='2D Lights',
                                                    update=erngp_enumprop_update_{layer_data.display_name})
bpy.types.Scene.twob_renderboolprop_{layer_data.display_name} = bpy.props.BoolProperty(
                                                    name="{layer_data.display_name}", 
                                                    default=True, 
                                                    update=erngp_boolprop_update_{layer_data.display_name})                                                   

""")

class TwoBLayerName(bpy.types.PropertyGroup):
    layer: bpy.props.StringProperty()
 
    

class TwoBFrameNodeData(bpy.types.PropertyGroup):
    base: bpy.props.StringProperty()
    luci_2D: bpy.props.StringProperty()
    luci_3D: bpy.props.StringProperty()
    display_name: bpy.props.StringProperty()
    base_layers: bpy.props.CollectionProperty(type=TwoBLayerName)

def set_frame_node_data(scene:bpy.types.Scene):
    frames = [node for node in scene.node_tree.nodes if node.bl_idname == 'NodeFrame']
    for frame in frames:
        if not frame.name.endswith("BASE"): continue
        frame_data = scene.twob_layernamedata.add()
        frame_data.display_name = frame.name.replace("_BASE", "")
        frame_data.name = frame_data.display_name
        frame_data.base = frame.name
        frame_data.luci_2D = frame.name.replace("_BASE", "_LUCI_2D")
        frame_data.luci_3D = frame.name.replace("_BASE", "_LUCI_3D")
        for node in scene.node_tree.nodes:
            if node.bl_idname == 'CompositorNodeRLayers':
                if node.parent == frame:
                   frame_data.base_layers.add().layer = node.layer
    



class TwoBEnableRenderNodesGenerateProps(bpy.types.Operator):
    """Click here to start"""
    bl_idname = "twob.generate_render_nodes_props"
    bl_label = "Initialize switches"
    bl_options = {'UNDO'}


    def execute(self, context):
        set_frame_node_data(context.scene)
        ret = erngp_generate_props(context.scene)
        if ret:
            
            return  {'FINISHED'}
        context.scene.twob_not_yet_generated_props = False
        for layer_data in context.scene.twob_layernamedata: # call update functions
            exec(f"context.scene.twob_renderboolprop_{layer_data.display_name} = True") 
            exec(f"context.scene.twob_renderenumprop_{layer_data.display_name} = '2D Lights'") 

        return  {'FINISHED'}

class TwoBEnableRenderNodesReset(bpy.types.Operator):
    """Delete all properties for a fresh start in this scene, something changes or the props break for whatever reason"""
    bl_idname = "twob.delete_render_nodes_props"
    bl_label = "Reset"
    bl_options = {'UNDO'}


    def execute(self, context):
        erngp_delete_boolprops(context.scene)
        erngp_delete_enumprops(context.scene)
        context.scene.twob_layernamedata.clear()
        context.scene.twob_not_yet_generated_props = True
        return  {'FINISHED'}

class TwoBEnableRenderNodesPanel(bpy.types.Panel):
    """Panel for useful operations in the 2B production"""
    bl_label = "Enable / disable render nodes"
    bl_idname = "TWOB_PT_enablerendernodespanel"
    bl_category = "2B"
    bl_region_type = 'UI'
    

    def draw(self, context):
        layout = self.layout

        if context.scene.twob_not_yet_generated_props:
            layout.row().operator( "twob.generate_render_nodes_props")
        else:
            for layer_data in context.scene.twob_layernamedata:
                col = layout.column(align=True)
                col.row().prop(context.scene, "twob_renderboolprop_" + layer_data.display_name)
                col.row().prop(context.scene, "twob_renderenumprop_" + layer_data.display_name,  expand=True)
            
            col = layout.column(align=True)
            col.row().operator("twob.delete_render_nodes_props")

class TwoBEnableRenderNodesPanel_VIEWPORT(TwoBEnableRenderNodesPanel):
    bl_space_type = 'VIEW_3D'
    bl_parent_id = "TWOB_PT_renderpanel"
    bl_idname = "TWOB_PT_enablerendernodespanelVIEWPORT"

class TwoBEnableRenderNodesPanel_COMPOSITOR(TwoBEnableRenderNodesPanel):
    bl_space_type = 'NODE_EDITOR'
    bl_idname = "TWOB_PT_enablerendernodespanelCOMPOSITOR"

    @classmethod
    def poll(cls, context):
        return context.area.ui_type == 'CompositorNodeTree'

def ern_register_props():
    bpy.utils.register_class(TwoBLayerName)
    bpy.utils.register_class(TwoBFrameNodeData)
    bpy.types.Scene.twob_not_yet_generated_props = bpy.props.BoolProperty(default=True)
    bpy.types.Scene.twob_layernamedata = bpy.props.CollectionProperty(type=TwoBFrameNodeData)

def ern_unregister_props():
    del  bpy.types.Scene.twob_layernamedata
    del  bpy.types.WindowManager.twob_not_yet_generated_props