from PIL import Image

im = Image.open(r"C:\Program Files (x86)\Steam\userdata\210661329\760\remote\1422450\screenshots\20261109124631_1.jpg")
# Crop around Windranger: center bottom-left
# Resolution is 1600x900
crop = im.crop((450, 480, 850, 900))
crop.save(r"extracted\crop_ultimate_arm.png")
print("Saved crop_ultimate_arm.png")
