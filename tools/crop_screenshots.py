from PIL import Image

img = Image.open(r"C:\Program Files (x86)\Steam\userdata\210661329\760\remote\1422450\screenshots\20261103014918_1.jpg")
w, h = img.size
print("Size:", w, h)

# Crop around Windranger
# In 1080p, she's centered slightly to the left: x: 700..1200, y: 300..1000
crop1 = img.crop((w*0.35, h*0.3, w*0.65, h*0.95))
crop1.save("extracted/crop_14918.png")
print("Saved crop_14918.png")

img2 = Image.open(r"C:\Program Files (x86)\Steam\userdata\210661329\760\remote\1422450\screenshots\20261103014922_1.jpg")
crop2 = img2.crop((w*0.35, h*0.3, w*0.65, h*0.95))
crop2.save("extracted/crop_14922.png")
print("Saved crop_14922.png")

