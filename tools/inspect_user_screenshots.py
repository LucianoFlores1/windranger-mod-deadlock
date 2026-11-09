from PIL import Image

s1 = Image.open(r"C:\Program Files (x86)\Steam\userdata\210661329\760\remote\1422450\screenshots\20261109124619_1.jpg")
s2 = Image.open(r"C:\Program Files (x86)\Steam\userdata\210661329\760\remote\1422450\screenshots\20261109124631_1.jpg")

print("Screenshot 1 size:", s1.size)
print("Screenshot 2 size:", s2.size)

# Let's save smaller previews or inspect crops
s1.resize((960, 540)).save(r"extracted\preview_s1.jpg")
s2.resize((960, 540)).save(r"extracted\preview_s2.jpg")
