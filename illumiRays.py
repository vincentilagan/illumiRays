import bpy
import random

class ILLUMIRAYS_OT_create_scene(bpy.types.Operator):
    bl_idname = "illumirays.create_scene"
    bl_label = "Create Scene"

    def execute(self, context):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        bpy.ops.mesh.primitive_plane_add(size=6, location=(0,0,0))
        bpy.context.active_object.name = "IllumiFloor"
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0,0,0.5))
        bpy.context.active_object.name = "IllumiBox"
        world = bpy.data.worlds["World"]
        world.use_nodes = True
        bg = world.node_tree.nodes["Background"]
        bg.inputs[0].default_value = (0.9,0.9,0.9,1)
        bpy.ops.object.light_add(type='SUN', radius=1, location=(3,3,5))
        bpy.context.active_object.name = "IllumiSun"
        return {'FINISHED'}

class IllumiRaysProperties(bpy.types.PropertyGroup):
    render_style: bpy.props.EnumProperty(
        name="Render Style",
        items=[
            ('CARTOON', "2D Cartoon", ""),
            ('PAINTING', "Painting", ""),
            ('WATERCOLOR', "Watercolor", ""),
            ('REALISM', "Hyper Realism", ""),
        ],
        default='REALISM'
    )
    light_dir: bpy.props.EnumProperty(
        name="Light Direction",
        items=[
            ('TOP', "Top Light", ""),
            ('RIGHT', "Right Light", ""),
            ('LEFT', "Left Light", ""),
            ('SUN', "Sun Light", ""),
        ],
        default='SUN'
    )

class ILLUMIRAYS_OT_apply_style(bpy.types.Operator):
    bl_idname = "illumirays.apply_style"
    bl_label = "Apply Render Style"

    def execute(self, context):
        props = context.scene.illumirays_props
        mat = bpy.data.materials.new(name="IllumiMat")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        bsdf = nodes.get("Principled BSDF")
        if props.render_style == 'CARTOON':
            bsdf.inputs[7].default_value = 1.0
            bsdf.inputs[9].default_value = 0.0
        elif props.render_style == 'PAINTING':
            bsdf.inputs[7].default_value = 0.6
        elif props.render_style == 'WATERCOLOR':
            bsdf.inputs[7].default_value = 0.9
        elif props.render_style == 'REALISM':
            bsdf.inputs[7].default_value = 0.3
        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                obj.data.materials.clear()
                obj.data.materials.append(mat)
        light = next((obj for obj in bpy.data.objects if obj.type == 'LIGHT'), None)
        if light:
            if props.light_dir == 'TOP':
                light.location = (0,0,5)
            elif props.light_dir == 'RIGHT':
                light.location = (5,0,3)
            elif props.light_dir == 'LEFT':
                light.location = (-5,0,3)
            elif props.light_dir == 'SUN':
                light.location = (3,3,5)
        return {'FINISHED'}

class ILLUMIRAYS_PT_panel(bpy.types.Panel):
    bl_label = "IllumiRays"
    bl_idname = "ILLUMIRAYS_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "IllumiRays"

    def draw(self, context):
        layout = self.layout
        props = context.scene.illumirays_props
        layout.operator("illumirays.create_scene", icon="MESH_CUBE")
        layout.prop(props, "render_style")
        layout.prop(props, "light_dir")
        layout.operator("illumirays.apply_style", icon="RENDER_STILL")

classes = [ILLUMIRAYS_OT_create_scene, IllumiRaysProperties, ILLUMIRAYS_OT_apply_style, ILLUMIRAYS_PT_panel]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.illumirays_props = bpy.props.PointerProperty(type=IllumiRaysProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.illumirays_props

if __name__ == "__main__":
    register()
