import bpy

def turn_off_widgets_collections(layer_coll:bpy.types.LayerCollection):
    """scenewise"""
    for coll in layer_coll.children:
        if "WGTS" in coll.name:
            coll.hide_viewport = True 
        turn_off_widgets_collections(coll)

def recursively_find_rig(collection:bpy.types.Collection, rig:bpy.types.Object):
    
    for obj in collection.objects:
        if obj.type == 'ARMATURE': return obj
    for coll in collection.children:
        rig = recursively_find_rig(coll, rig)
    return rig

def make_linked_rig_animatable(context, rig:bpy.types.Object, scene:bpy.types.Scene, view_layer: bpy.types.ViewLayer, override_obj=None, orginal_matrix=None):
    
    if not override_obj:
        override_obj = context.object
        
    if orginal_matrix:
        matrix = orginal_matrix
    else:
        matrix = rig.matrix_world
    coll_name = rig.name
    with context.temp_override(object=override_obj, active_object=override_obj, selected_objects=[override_obj]):
        bpy.ops.object.make_override_library()
    turn_off_widgets_collections(view_layer.layer_collection)
    
    override_hierarchy = next(coll for coll in bpy.data.collections if coll.name ==coll_name and coll.override_library)
    rig = recursively_find_rig(override_hierarchy, None)
    rig.show_in_front = True

    
   # rig.matrix_world = matrix
    rig.pose.bones["root"].matrix = matrix @ rig.matrix_world.inverted()
    if "rig_id" not in rig.data.keys(): return
    for text in bpy.data.texts:
        if rig.data["rig_id"] in text.as_string(): text.as_module()
    return

def make_linked_obj_positionable(obj:bpy.types.Object, scene:bpy.types.Scene, view_layer: bpy.types.ViewLayer):
    coll = next(coll for coll in obj.users_collection if not coll.library)
    matrix_world = obj.matrix_world
    new_empty = bpy.data.objects.new(obj.name + "DUP", None)
    new_empty.instance_type = "COLLECTION"
    new_empty.instance_collection = obj.instance_collection
    coll.objects.link(new_empty)
    bpy.data.objects.remove(obj)
    new_empty.matrix_world = matrix_world

def replace_obj_with_prop(obj:bpy.types.Object):
    matrix_world = obj.matrix_world
    if len(obj.instance_collection.objects):
        obj_library = obj.instance_collection.objects[0].library
    else:
        obj_library = obj.instance_collection.children[0].objects[0].library
    base_file_path = obj_library.name.replace("OBJ", "PROP")
    file_path = obj_library.filepath.replace(obj_library.name, base_file_path)
    coll_name = obj.instance_collection.name.replace("OBJ", "PROP")
    print(file_path)
    try:
        with bpy.data.libraries.load(file_path, link=True, relative=True) as (data_from, data_to):
            data_to.collections = [coll for coll in data_from.collections if coll == coll_name]
            print(data_from.collections, data_to.collections)
    except OSError:
        return "file_not_found"
    
    coll = obj.users_collection[0]
    prop_coll = data_to.collections[0]
    new_empty = bpy.data.objects.new(prop_coll.name, None)
    new_empty.instance_type = "COLLECTION"
    new_empty.instance_collection = prop_coll
    coll.objects.link(new_empty)
    new_empty.matrix_world = matrix_world
    bpy.data.objects.remove(obj)
    return new_empty
    

class TwoBMakeRigAnimatable(bpy.types.Operator):
    """Crea library override del rig selezionato LINKATO MANUALMENTE e lo rende In front
Funziona meglio su Blender 3.1 e 3.3"""
    bl_idname = "twob.make_rig_animatable"
    bl_label = "Rendi animabile"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        if context.object:
            if context.object.instance_collection: return True
        return  False

    def execute(self, context):
        make_linked_rig_animatable(context, context.object, context.scene, context.window.view_layer)
        return  {'FINISHED'}

class TwoBMakeSceneLinkedObjPositionable(bpy.types.Operator):
    """duplica e butta l'altro """
    bl_idname = "twob.make_scene_linked_obj_positionable"
    bl_label = "Rendi posizionabile (OBJ del SET)"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        if not context.object: return False
        if not context.object.instance_collection: return False
        if not context.object.library: return False
        return  True

    def execute(self, context):
        make_linked_obj_positionable(context.object, context.scene, context.window.view_layer)
        return  {'FINISHED'}

class TwoBMakeAnimatableReplaceObjProp(bpy.types.Operator):
    """Importa dal file PROP corrispondente il link e ne fa il library override, buttando l'OBJ;
    effettivamente quindi sostituisce"""
    bl_idname = "twob.make_animatable_replace_obj_prop"
    bl_label = "Rendi animabile (PROP del SET)"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        if not context.object: return False
        if not context.object.instance_collection: return False
        if not context.object.library: return False
        return  True

    def execute(self, context):
        original_matrix = context.object.matrix_world
        prop_return  = replace_obj_with_prop(context.object)
        if prop_return == "file_not_found" : 
            self.report({'ERROR'}, "File PROP non trovato!")
            return  {'FINISHED'}
        make_linked_rig_animatable(context, prop_return, context.scene, context.window.view_layer, override_obj=prop_return, orginal_matrix=original_matrix)
        return  {'FINISHED'}


