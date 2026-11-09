from PIL import Image

im = Image.open(r"extracted\dl_orig_pano\panorama\images\heroes\archer_card_psd.png")
print("Top-left pixel:", im.getpixel((0,0)))
print("Bottom-left pixel:", im.getpixel((0,379)))
print("Center pixel:", im.getpixel((140, 190)))
print("Top-center pixel:", im.getpixel((140, 10)))
