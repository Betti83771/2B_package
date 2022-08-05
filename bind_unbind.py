import bpy


def bind_all(cage, all_objs, unbind=False):

    arm_mod = next((mod for mod in cage.modifiers if mod.type == 'ARMATURE'), None)

    if arm_mod:
        corr_arm = arm_mod.object

    noarm = False

    if arm_mod == None:
        noarm = True
        print("FW Bind/Unbind: No armature modifier found for rest pose check!")
    elif corr_arm == None:
        noarm = True
        print("FW Bind/Unbind: No armature found for rest pose check!")
    elif corr_arm.data.pose_position == 'REST':
        starting_pose_rest = True
        print("FW Bind/Unbind: Armature found in rest position!")
    else:
        starting_pose_rest = False
        corr_arm.data.pose_position = 'REST'
        print("FW Bind/Unbind: Armature found in pose position! I'm putting it in rest pose then pose position again after I finish binding/unbinding!")
         

    for obj in all_objs:
        s_deform_list = [mod for mod in obj.modifiers if mod.type == 'SURFACE_DEFORM' and mod.target == cage]
        for s_deform in s_deform_list:
            bpy.context.view_layer.objects.active = obj
            if s_deform.is_bound != unbind:
                continue
            bpy.ops.object.surfacedeform_bind(modifier=s_deform.name)

    if not noarm:
        if not starting_pose_rest:
           corr_arm.data.pose_position = 'POSE'
    bpy.context.view_layer.objects.active = cage

    #print("done!")

def bind_menu_func(self, context):
    self.layout.operator(BindAll.bl_idname, icon='MESH_CUBE')


class BindAll(bpy.types.Operator):
    """Bind or unbind all geometry that refers to the active mesh cage as target."""
    bl_idname = "object.bind_all"
    bl_label = "Toggle Bind all"
    bl_options = {'REGISTER', 'UNDO'}

    other_buttons = True

    unbind: bpy.props.BoolProperty(
        name="Unbind",
        default=False,
    )

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.mode == 'OBJECT'

    def execute(self, context):
        bind_all(bpy.context.active_object, context.view_layer.objects, self.unbind)
        if self.unbind:
            self.report({'INFO'}, "Geometry unbinded")
        else:
            self.report({'INFO'}, "Geometry binded")
        return {'FINISHED'}

def fw_register():
    bpy.utils.register_class(BindAll)
    bpy.types.VIEW3D_MT_object.append(bind_menu_func)


def fw_unregister():
    bpy.types.VIEW3D_MT_object.remove(bind_menu_func)
    bpy.utils.unregister_class(BindAll)


if __name__ == "__main__":
    fw_register()