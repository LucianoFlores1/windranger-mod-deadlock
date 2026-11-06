import bpy

bpy.ops.wm.open_mainfile(filepath=r"extracted\windrunner_on_archer.blend")
obj = bpy.data.objects['windrunner_classic_body']
me = obj.data
xs = [v.co.x for v in me.vertices]
ys = [v.co.y for v in me.vertices]
zs = [v.co.z for v in me.vertices]
print(f"windrunner_classic_body in blend:")
print(f"  X: [{min(xs):.2f}, {max(xs):.2f}]")
print(f"  Y: [{min(ys):.2f}, {max(ys):.2f}]")
print(f"  Z: [{min(zs):.2f}, {max(zs):.2f}]")

