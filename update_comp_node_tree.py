import bpy
from .ExtraSettingComp import *
from .misc_operators import rename_all_paths_with_filename



def  overwrite_tree(scene_to_be_overwritten:bpy.types.Scene, scene_to_copy_from:bpy.types.Scene):
    for node in reversed(scene_to_be_overwritten.node_tree.nodes):
        scene_to_be_overwritten.node_tree.nodes.remove(node)
    links_dict_list = []
    for node_to_copy in scene_to_copy_from.node_tree.nodes:
        new_node = scene_to_be_overwritten.node_tree.nodes.new(node_to_copy.bl_idname)
        if new_node.bl_idname == 'CompositorNodeOutputFile':
            new_node.format.file_format = node_to_copy.format.file_format
            new_node.format.color_mode = node_to_copy.format.color_mode
            new_node.format.color_depth = node_to_copy.format.color_depth
            new_node.format.compression = node_to_copy.format.compression
            new_node.format.quality = node_to_copy.format.quality
            new_node.file_slots.clear()
            for file_slot in node_to_copy.file_slots:
                new_slot = new_node.file_slots.new(file_slot.path)

        for i, input in enumerate(node_to_copy.inputs):
            if input.is_linked: continue
            new_node.inputs[i].default_value = input.default_value
        empty_dict = {}
        settings_dict = writeExtraSettings(empty_dict, node_to_copy, node_to_copy.type, "", "betti")
        new_node.name =  settings_dict["name"]
        new_node.location = settings_dict["location"]
        new_node.hide = settings_dict["hide"]
        new_node.height=  settings_dict["height"]
        new_node.width=  settings_dict["width"]
        if settings_dict["extra_settings"][0][0] == -1: break
        readExtraSettings(settings_dict["extra_settings"], new_node)


        if(len(node_to_copy.inputs) < 1): continue
        for index, input in enumerate(node_to_copy.inputs):
            if not input.is_linked: continue
            temp_socket = str(input.links[0].from_socket.path_from_id()).split('outputs[')[-1]
            temp_socket = temp_socket.split(']')[0]
            links_dict_list.append({
                'output_node': input.links[0].from_node.name, 
                'output_socket': int(temp_socket),
                'input_node': node_to_copy.name,
                'input_socket': index,
            })
        
    for link in links_dict_list:
        from_socket = scene_to_be_overwritten.node_tree.nodes[link['output_node']].outputs[link['output_socket']]
        to_socket = scene_to_be_overwritten.node_tree.nodes[link['input_node']].inputs[link['input_socket']]
        new_link = scene_to_be_overwritten.node_tree.links.new(to_socket, from_socket)


    
def update_comp_node_tree_func(file_zero_path):
    linked_scenes = []
    local_scenes = []
    initial_linked_scenes = []
    try:
        with bpy.data.libraries.load(file_zero_path, link=True) as (data_from, data_to):
            data_to.scenes = [scene for scene in data_from.scenes if scene in bpy.data.scenes.keys()]
            for scene in data_to.scenes: initial_linked_scenes.append(scene)
    except OSError:
        return "file_not_found"

    for scene in bpy.data.scenes:
        if scene.library != None: 
            linked_scenes.append(scene)
        else:
            local_scenes.append(scene)

    for local_scene in local_scenes:
        for linked_scene in reversed(linked_scenes):
            if local_scene.name == linked_scene.name: 
                local_scene.use_nodes = True
                overwrite_tree(local_scene, linked_scene)
                bpy.data.scenes.remove(linked_scene, do_unlink=True)
                linked_scenes.remove(linked_scene)
                break
    rename_all_paths_with_filename()
    return str(initial_linked_scenes)
            