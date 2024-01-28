import bpy

print("==== START ====")

total_frame = bpy.data.scenes[0].frame_end
height = 20
acceleration_const = -0.06
bounce_const = 0.7

bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, -1))
bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, height))

traversed_since_last_bounce = 0

def get_vertical_pos(relative_x: float, current_max_height: float, acceleration: float):
    return acceleration * (relative_x ** 2) + current_max_height

for i in range(total_frame):
    z = get_vertical_pos(traversed_since_last_bounce, height, acceleration_const)
    # print(f"frame {i}, height: {z}")
    if z < 0:
        print("height before: " + str(height))
        height *= bounce_const
        print("height after: " + str(height))
        traversed_since_last_bounce = ((-4 * acceleration_const * height) ** 0.5) / (2 * acceleration_const)
        print("traversed since last bounce: " + str(traversed_since_last_bounce))
        z = get_vertical_pos(traversed_since_last_bounce, height, acceleration_const)
    bpy.context.selected_objects[0].location[2] = z
    bpy.context.selected_objects[0].keyframe_insert(data_path="location", frame=i)
    traversed_since_last_bounce += 1
