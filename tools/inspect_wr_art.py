from PIL import Image

im = Image.open(r"extracted\dota_wr_pano\panorama\images\econ\sets\v2\npc_dota_hero_windrunner_0_png.png")
print("Size:", im.size, "Mode:", im.mode)
print("Alpha min/max:", im.getextrema()[3])
