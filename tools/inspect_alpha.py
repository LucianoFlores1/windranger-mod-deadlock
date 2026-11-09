from PIL import Image

im = Image.open(r"extracted\dl_orig_pano\panorama\images\heroes\archer_card_psd.png")
print("Has transparency?", im.getextrema()[3]) # alpha min/max
im_sm = Image.open(r"extracted\dl_orig_pano\panorama\images\heroes\archer_sm_psd.png")
print("sm Has transparency?", im_sm.getextrema()[3])
im_mm = Image.open(r"extracted\dl_orig_pano\panorama\images\heroes\archer_mm_psd.png")
print("mm Has transparency?", im_mm.getextrema()[3])
