from PIL import Image

card = Image.open(r"extracted\decompiled_pano\archer_card_psd.png")
print("card size:", card.size, card.mode)
bg = Image.open(r"extracted\decompiled_pano\grey_talon_bg_psd.png")
print("bg size:", bg.size, bg.mode)
