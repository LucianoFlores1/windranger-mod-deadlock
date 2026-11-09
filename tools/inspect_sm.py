from PIL import Image

im = Image.open(r"extracted\dl_orig_pano\panorama\images\heroes\archer_sm_psd.png")
print("DL sm center:", im.getpixel((64, 64)))
print("DL sm top-left:", im.getpixel((0, 0)))

mod_sm = Image.open(r"extracted\decompiled_pano\archer_sm_psd.png")
print("Mod sm center:", mod_sm.getpixel((64, 64)))
print("Mod sm top-left:", mod_sm.getpixel((0, 0)))
