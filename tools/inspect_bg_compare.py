from PIL import Image

orig_bg = Image.open(r"extracted\dl_orig_pano\panorama\images\heroes\backgrounds\grey_talon_bg_psd.png")
print("Original bg size:", orig_bg.size)

mod_bg = Image.open(r"extracted\decompiled_pano\grey_talon_bg_psd.png")
print("Mod bg size:", mod_bg.size)
