from PIL import Image

img = Image.open(r"C:\Program Files (x86)\Steam\userdata\210661329\760\remote\1422450\screenshots\20261103073757_1.jpg")
w, h = img.size
crop = img.crop((w*0.35, h*0.3, w*0.65, h*0.95))
crop.save("extracted/crop_073757.png")
print("Saved crop_073757.png")

img_aim = Image.open(r"C:\Program Files (x86)\Steam\userdata\210661329\760\remote\1422450\screenshots\20261103073747_1.jpg")
w, h = img_aim.size
crop_aim = img_aim.crop((w*0.25, h*0.3, w*0.60, h*0.95))
crop_aim.save("extracted/crop_073747.png")
print("Saved crop_073747.png")

