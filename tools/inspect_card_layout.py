from PIL import Image

orig_card = Image.open(r"extracted\dl_orig_pano\panorama\images\heroes\archer_card_psd.png")
print("Card bbox:", orig_card.getbbox())

wr_art = Image.open(r"extracted\dota_wr_pano\panorama\images\econ\sets\v2\npc_dota_hero_windrunner_0_png.png")
print("WR art bbox:", wr_art.getbbox())
