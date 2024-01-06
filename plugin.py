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

class ExportPresetsPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Export Presets"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        
        # Big render button
        layout.label(text="Test Render:")
        row = layout.row()
        row.operator("render.render")

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
        bpy.data.scenes["Scene"].render.resolution_x = 1080;
        bpy.data.scenes["Scene"].render.resolution_y = 1080;
        return {"FINISHED"}

class EXPORT_OPTIONS_set_1080p_vertical(bpy.types.Operator):
    bl_idname = "export_options.set_1080p_vertical"
    bl_label = "1080p Vertical"
    bl_description = "Sets Resolution to 1080p x 1920p"
    bl_options = {"UNDO"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        bpy.data.scenes["Scene"].render.resolution_x = 1080;
        bpy.data.scenes["Scene"].render.resolution_y = 1920;
        return {"FINISHED"}

class EXPORT_OPTIONS_set_1080p_widescreen(bpy.types.Operator):
    bl_idname = "export_options.set_1080p_widescreen"
    bl_label = "1080p Widescreen"
    bl_description = "Sets Resolution to 1920p x 1080p"
    bl_options = {"UNDO"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        bpy.data.scenes["Scene"].render.resolution_x = 1920;
        bpy.data.scenes["Scene"].render.resolution_y = 1080;
        return {"FINISHED"}

class EXPORT_OPTIONS_set_4k_square(bpy.types.Operator):
    bl_idname = "export_options.set_4k_square"
    bl_label = "4k Square"
    bl_description = "Sets Resolution to 3840px x 3840px"
    bl_options = {"UNDO"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        bpy.data.scenes["Scene"].render.resolution_x = 3840;
        bpy.data.scenes["Scene"].render.resolution_y = 3840;
        return {"FINISHED"}

class EXPORT_OPTIONS_set_4k_widescreen(bpy.types.Operator):
    bl_idname = "export_options.set_4k_widescreen"
    bl_label = "4k Widescreen"
    bl_description = "Sets Resolution to 3840px x 2160px"
    bl_options = {"UNDO"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        bpy.data.scenes["Scene"].render.resolution_x = 3840;
        bpy.data.scenes["Scene"].render.resolution_y = 2160;
        return {"FINISHED"}

class EXPORT_OPTIONS_set_4k_vertical(bpy.types.Operator):
    bl_idname = "export_options.set_4k_vertical"
    bl_label = "4k Vertical"
    bl_description = "Sets Resolution to 2160px x 3840px"
    bl_options = {"UNDO"}

    def execute(self, context: bpy.types.Context) -> set[str]:
        bpy.data.scenes["Scene"].render.resolution_x = 2160;
        bpy.data.scenes["Scene"].render.resolution_y = 3840;
        return {"FINISHED"}

classes = (
    ExportPresetsPanel,
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


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    # bpy.utils.register_classes_factory(classes)


if __name__ == "__main__":
    register()
