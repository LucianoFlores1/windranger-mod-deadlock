from PIL import Image

im = Image.open(r"C:\Program Files (x86)\Steam\userdata\210661329\760\remote\1422450\screenshots\20261105220422_1.jpg")
w, h = im.size
# Crop around the bow hand and grip (approx center of character)
crop = im.crop((int(w * 0.40), int(h * 0.38), int(w * 0.55), int(h * 0.60)))
crop.save(r"extracted\crop_bow_hand.png")
print("Cropped bow hand successfully!")

