bl_info = {
    "name": "Render Buddy",
    "description": "",
    "author": "whoisryosuke",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "Properties > Output",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "Development"
}

import bpy

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )

# Global plugin properties
class PluginProperties(PropertyGroup):

    test_resolution: IntProperty(
        name = "Test Resolution",
        description="Temporary resolution for test renders",
        default = 50,
        min = 10,
        max = 100
        )

# The UI Panel in Render View
class ExportPresetsPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Render Buddy"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        state = scene.render_buddy

        row = layout.row()
        row.prop(scene, "camera")

        # Big render button
        layout.label(text="Test Render:")
        row = layout.row()
        row.operator("export_options.test_render")
        row = layout.row()
        row.prop(state, "test_resolution")

        layout.label(text="Export Presets")
        # Create two columns, by using a split layout.
        split = layout.split()

        # First column
        col = split.column()
        col.label(text="1080p:")
        col.operator("export_options.set_1080p_square")
        col.operator("export_options.set_1080p_vertical")
        col.operator("export_options.set_1080p_widescreen")

        # Second column, aligned
        col = split.column()
        col.label(text="4k:")
        col.operator("export_options.set_4k_square")
        col.operator("export_options.set_4k_vertical")
        col.operator("export_options.set_4k_widescreen")



class EXPORT_OPTIONS_set_1080p_square(bpy.types.Operator):
    bl_idname = "export_options.set_1080p_square"
    bl_label = "1080p Square"
    bl_description = "Sets Resolution to 1080p"
    bl_options = {"UNDO"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        bpy.context.scene.render.resolution_x = 1080;
        bpy.context.scene.render.resolution_y = 1080;
        return {"FINISHED"}

class EXPORT_OPTIONS_set_1080p_vertical(bpy.types.Operator):
    bl_idname = "export_options.set_1080p_vertical"
    bl_label = "1080p Vertical"
    bl_description = "Sets Resolution to 1080p x 1920p"
    bl_options = {"UNDO"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        bpy.context.scene.render.resolution_x = 1080;
        bpy.context.scene.render.resolution_y = 1920;
        return {"FINISHED"}

class EXPORT_OPTIONS_set_1080p_widescreen(bpy.types.Operator):
    bl_idname = "export_options.set_1080p_widescreen"
    bl_label = "1080p Widescreen"
    bl_description = "Sets Resolution to 1920p x 1080p"
    bl_options = {"UNDO"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        bpy.context.scene.render.resolution_x = 1920;
        bpy.context.scene.render.resolution_y = 1080;
        return {"FINISHED"}

class EXPORT_OPTIONS_set_4k_square(bpy.types.Operator):
    bl_idname = "export_options.set_4k_square"
    bl_label = "4k Square"
    bl_description = "Sets Resolution to 3840px x 3840px"
    bl_options = {"UNDO"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        bpy.context.scene.render.resolution_x = 3840;
        bpy.context.scene.render.resolution_y = 3840;
        return {"FINISHED"}

class EXPORT_OPTIONS_set_4k_widescreen(bpy.types.Operator):
    bl_idname = "export_options.set_4k_widescreen"
    bl_label = "4k Widescreen"
    bl_description = "Sets Resolution to 3840px x 2160px"
    bl_options = {"UNDO"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        bpy.context.scene.render.resolution_x = 3840;
        bpy.context.scene.render.resolution_y = 2160;
        return {"FINISHED"}

class EXPORT_OPTIONS_set_4k_vertical(bpy.types.Operator):
    bl_idname = "export_options.set_4k_vertical"
    bl_label = "4k Vertical"
    bl_description = "Sets Resolution to 2160px x 3840px"
    bl_options = {"UNDO"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        bpy.context.scene.render.resolution_x = 2160;
        bpy.context.scene.render.resolution_y = 3840;
        return {"FINISHED"}

class EXPORT_OPTIONS_test_render(bpy.types.Operator):
    bl_idname = "export_options.test_render"
    bl_label = "Test Render"
    bl_description = "Renders at 50% then returns prev. settings"

    def execute(self, context: bpy.types.Context) -> set[str]:
        # Preserve prev settings
        # Make sure to copy any properties of classes
        import copy
        prev_reso_percent = copy.copy(bpy.context.scene.render.resolution_percentage)
        prev_file_path = copy.copy(bpy.context.scene.render.filepath)
        
        # Set to 50%
        bpy.context.scene.render.resolution_percentage = 50

        # Make a filename based on current `.blend` file
        import os
        output_dir = os.path.dirname(bpy.data.filepath)
        filename_dirty = os.path.basename(bpy.data.filepath)
        filename = filename_dirty.replace(".blend", "")
        file_type = bpy.context.scene.render.image_settings.file_format
        output_file_pattern_string = filename + "-%s." + file_type

        # Get the current time to append to filename
        from datetime import datetime
        now = datetime.now() # current date and time
        time = now.strftime("%H-%M-%S")

        # Render and save to file
        bpy.context.scene.render.filepath = os.path.join(output_dir, (output_file_pattern_string % time))
        bpy.ops.render.render(write_still = bpy.data.is_saved)

        # Return settings
        bpy.context.scene.render.resolution_percentage = prev_reso_percent
        bpy.context.scene.render.filepath = prev_file_path
        
        return {"FINISHED"}

classes = (
    PluginProperties,
    ExportPresetsPanel,
    EXPORT_OPTIONS_test_render,
    EXPORT_OPTIONS_set_1080p_square,
    EXPORT_OPTIONS_set_1080p_vertical,
    EXPORT_OPTIONS_set_1080p_widescreen,
    EXPORT_OPTIONS_set_4k_square,
    EXPORT_OPTIONS_set_4k_widescreen,
    EXPORT_OPTIONS_set_4k_vertical
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    # bpy.utils.register_classes_factory(classes)
        
    bpy.types.Scene.render_buddy = PointerProperty(type=PluginProperties)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    # bpy.utils.register_classes_factory(classes)
        
    del bpy.types.Scene.render_buddy


if __name__ == "__main__":
    register()
