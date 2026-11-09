from PIL import Image

im = Image.open(r"extracted\decompiled_pano\archer_card_psd.png")
print("Mod card top-left:", im.getpixel((0,0)))
print("Mod card bottom-left:", im.getpixel((0,379)))
print("Mod card center:", im.getpixel((140, 190)))
