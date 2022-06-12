import bpy

def uniform_timelines(from_scene:bpy.types.Scene, overwrite_markers=True):
    """si copia anche i marker (da leggere con il tono della musica del latte e caffe')"""
    if overwrite_markers:
        marker_dict = {}
        for marker in from_scene.timeline_markers:
            marker_dict[marker.name] = marker.frame

    for scene in bpy.data.scenes:
        if scene.name.endswith("anm"): continue
        scene.frame_set(from_scene.frame_current)
        scene.frame_start = from_scene.frame_start
        scene.frame_end = from_scene.frame_end
        if overwrite_markers:
            for marker in reversed(scene.timeline_markers): 
                scene.timeline_markers.remove(marker)
            for name, frame in marker_dict.items():
                scene.timeline_markers.new(name, frame=frame)
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
        uniform_timelines(bpy.data.scenes[anm_scene], overwrite_markers=False)
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