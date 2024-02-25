bl_info = {
    "name": "Bounscripting Ball",
    "author": "Bahana Alana Khansa",
    "version": "(0, 1, 0)",
    "blender": "(4, 0)",
    "description": "Bouncing Ball Generator",
}

from typing import Set
import bpy
from bpy import props
from bpy.types import Context, Event, Operator, Panel, PropertyGroup


class BOUNSCRIPTINGBALL_OT_GenBall(Operator):
    bl_idname = "object.gen_ball"
    bl_label = "Generate Ball"

    height: props.FloatProperty(name="height", default=20, min=0)  # type: ignore
    acceleration_const: props.FloatProperty(
        name="acceleration const",
        default=-0.1,
        max=0,
    )  # type: ignore
    bounce_const: props.FloatProperty(
        name="bounce const", default=0.7, min=0
    )  # type: ignore

    def execute(self, context: Context) -> Set[int] | Set[str]:
        print(str(self.height) + str(self.acceleration_const), str(self.bounce_const))

        total_frame = bpy.data.scenes[0].frame_end
        height = self.height
        acceleration_const = self.acceleration_const
        bounce_const = self.bounce_const

        bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, -1))
        bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, height))

        traversed_since_last_bounce = 0

        def get_vertical_pos(
            relative_x: float, current_max_height: float, acceleration: float
        ):
            return acceleration * (relative_x**2) + current_max_height

        for i in range(total_frame):
            z = get_vertical_pos(
                traversed_since_last_bounce, height, acceleration_const
            )
            # print(f"frame {i}, height: {z}")
            if z < 0:
                print("height before: " + str(height))
                height *= bounce_const
                print("height after: " + str(height))
                traversed_since_last_bounce = (
                    (-4 * acceleration_const * height) ** 0.5
                ) / (2 * acceleration_const)
                print(
                    "traversed since last bounce: " + str(traversed_since_last_bounce)
                )
                z = get_vertical_pos(
                    traversed_since_last_bounce, height, acceleration_const
                )
            bpy.context.selected_objects[0].location[2] = z
            bpy.context.selected_objects[0].keyframe_insert(
                data_path="location", frame=i
            )
            traversed_since_last_bounce += 1

        return {"FINISHED"}

    def invoke(self, context: Context, event: Event) -> Set[int] | Set[str]:
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


class BOUNSCRIPTINGBALL_PT_MainPanel(Panel):
    bl_label = "Bounscripting Ball"
    bl_idname = "OBJECT_PT_MainPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Bounscripting Ball"

    def draw(self, context):
        layout = self.layout

        layout.operator("object.gen_ball")


classes = [BOUNSCRIPTINGBALL_OT_GenBall, BOUNSCRIPTINGBALL_PT_MainPanel]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
