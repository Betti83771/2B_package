import bpy

def uniform_timelines(from_scene:bpy.types.Scene):
    for scene in bpy.data.scenes:
        if scene.name.endswith("anm"): continue
        scene.frame_start = from_scene.frame_start
        scene.frame_end = from_scene.frame_end
    return

def put_cursor_at_starting_frame():
    for scene in bpy.data.scenes:
        scene.frame_set(scene.frame_start)
    return

class TwoBTimelineReset(bpy.types.Operator):
    """Uniform all timelines to the anm Scene; also move the timeline cursors to the starting frames"""
    bl_idname = "twob.timeline_reset"
    bl_label = "Reset timelines"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        anm_scene = next((sce for sce in bpy.data.scenes.keys() if "ANM" in sce), None)
        return  anm_scene

    def execute(self, context):
        anm_scene = next((sce for sce in bpy.data.scenes.keys() if "ANM" in sce), None)
        uniform_timelines(bpy.data.scenes[anm_scene])
        put_cursor_at_starting_frame()
        return  {'FINISHED'}

class TwoBTimelineUniform(bpy.types.Operator):
    """Uniform all timelines to the current Scene's timeline"""
    bl_idname = "twob.timeline_uniform"
    bl_label = "Uniform timelines"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        return  True

    def execute(self, context):
        uniform_timelines(context.scene)
        return  {'FINISHED'}