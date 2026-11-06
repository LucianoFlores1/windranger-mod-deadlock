from PIL import Image

im1 = Image.open(r"C:\Program Files (x86)\Steam\userdata\210661329\760\remote\1422450\screenshots\20261105213456_1.jpg")
im2 = Image.open(r"C:\Program Files (x86)\Steam\userdata\210661329\760\remote\1422450\screenshots\20261105213530_1.jpg")

# In im1 (aiming): crop her torso, arms, quiver
# (approx 1920x1080)
w, h = im1.size
crop1 = im1.crop((int(w*0.3), int(h*0.4), int(w*0.55), int(h*0.85)))
crop1.save(r"extracted\crop_aim_arm.png")

# In im2 (idle): crop her upper body and arms
crop2 = im2.crop((int(w*0.35), int(h*0.25), int(w*0.65), int(h*0.8)))
crop2.save(r"extracted\crop_idle_upper.png")

print("Cropped successfully!")

