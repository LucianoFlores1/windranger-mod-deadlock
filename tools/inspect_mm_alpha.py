from PIL import Image

im = Image.open(r"extracted\dl_orig_pano\panorama\images\heroes\archer_mm_psd.png")
a = im.split()[3]
print("Corners alpha:", a.getpixel((0,0)), a.getpixel((49,0)), a.getpixel((0,49)), a.getpixel((49,49)))
print("Center alpha:", a.getpixel((25,25)))
