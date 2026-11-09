from PIL import Image, ImageEnhance, ImageFilter

wr_full = Image.open(r"extracted\dota_wr_pano\panorama\images\econ\sets\v2\npc_dota_hero_windrunner_0_png.png")

# Let's inspect the upper body portion:
# WR full is 448x678.
# Head is around Y=60..250, Torso Y=250..500.
# For 280x380 card:
# Let's crop from Y=50 to Y=450 (height 400), width from X=30 to X=430 (width 400)
# Then resize to fit nicely in 280x380.

def make_card(tint=None):
    card = Image.new("RGBA", (280, 380), (0, 0, 0, 0))
    
    # Scale wr_full
    # We want the bust/torso to fill the card nicely
    scale = 380.0 / 480.0 # scale factor
    new_w = int(wr_full.width * scale)
    new_h = int(wr_full.height * scale)
    resized = wr_full.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # Position: center horizontally, align upper part
    x_offset = (280 - new_w) // 2 + 15
    y_offset = -10
    
    # Background soft dark radial gradient or subtle green glow
    bg = Image.new("RGBA", (280, 380), (15, 25, 20, 220))
    card.alpha_composite(bg)
    card.alpha_composite(resized, (x_offset, y_offset))
    
    if tint == "red":
        r, g, b, a = card.split()
        r = ImageEnhance.Brightness(r).enhance(1.4)
        g = ImageEnhance.Brightness(g).enhance(0.7)
        b = ImageEnhance.Brightness(b).enhance(0.7)
        card = Image.merge("RGBA", (r, g, b, a))
    elif tint == "gold":
        r, g, b, a = card.split()
        r = ImageEnhance.Brightness(r).enhance(1.2)
        g = ImageEnhance.Brightness(g).enhance(1.15)
        card = Image.merge("RGBA", (r, g, b, a))
        
    return card

c_normal = make_card()
c_normal.save(r"extracted\test_card_classic.png")
print("Saved test_card_classic.png")
