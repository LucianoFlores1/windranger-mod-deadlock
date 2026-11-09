from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from pathlib import Path

out_dir = Path(r"extracted\new_classic_pano")
out_dir.mkdir(parents=True, exist_ok=True)

wr_full = Image.open(r"extracted\dota_wr_pano\panorama\images\econ\sets\v2\npc_dota_hero_windrunner_0_png.png")
wr_sel = Image.open(r"extracted\dota_wr_pano\panorama\images\heroes\selection\npc_dota_hero_windrunner_png.png")
orig_bg = Image.open(r"extracted\dl_orig_pano\panorama\images\heroes\backgrounds\grey_talon_bg_psd.png")

# 1. Main Hero Card (280 x 380)
def generate_card(style="normal"):
    # Target 280 x 380
    canvas = Image.new("RGBA", (280, 380), (0, 0, 0, 0))
    
    # Atmospheric dark background with gradient
    bg = Image.new("RGBA", (280, 380), (0, 0, 0, 0))
    draw_bg = ImageDraw.Draw(bg)
    for y in range(380):
        alpha = int(min(255, (y / 380.0) ** 1.5 * 255))
        if style == "critical":
            color = (35, 10, 10, alpha)
        elif style == "gloat":
            color = (30, 25, 10, alpha)
        else:
            color = (12, 22, 18, alpha)
        draw_bg.line([(0, y), (280, y)], fill=color)
        
    canvas.alpha_composite(bg)
    
    # Scale WR: full is 448x678
    # Scale so width ~ 330
    scale = 320.0 / wr_full.width
    new_w = int(wr_full.width * scale)
    new_h = int(wr_full.height * scale)
    scaled_wr = wr_full.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # Apply style tints if needed
    if style == "critical":
        r, g, b, a = scaled_wr.split()
        r = ImageEnhance.Brightness(r).enhance(1.3)
        g = ImageEnhance.Brightness(g).enhance(0.8)
        b = ImageEnhance.Brightness(b).enhance(0.8)
        scaled_wr = Image.merge("RGBA", (r, g, b, a))
    elif style == "gloat":
        r, g, b, a = scaled_wr.split()
        r = ImageEnhance.Brightness(r).enhance(1.15)
        g = ImageEnhance.Brightness(g).enhance(1.1)
        b = ImageEnhance.Brightness(b).enhance(0.9)
        scaled_wr = Image.merge("RGBA", (r, g, b, a))
        
    # Place on canvas: centered X, top offset -15
    canvas.alpha_composite(scaled_wr, ((280 - new_w) // 2 + 10, -10))
    
    # Bottom fade mask to blend seamlessly into UI
    fade = Image.new("L", (280, 380), 255)
    draw_fade = ImageDraw.Draw(fade)
    for y in range(320, 380):
        val = int(255 * (1.0 - (y - 320) / 60.0))
        draw_fade.line([(0, y), (280, y)], fill=val)
    canvas.putalpha(Image.composite(canvas.split()[3], Image.new("L", (280, 380), 0), fade))
    
    return canvas

card_normal = generate_card("normal")
card_normal.save(out_dir / "archer_card_psd.png")

card_crit = generate_card("critical")
card_crit.save(out_dir / "archer_card_critical_psd.png")

card_gloat = generate_card("gloat")
card_gloat.save(out_dir / "archer_card_gloat_psd.png")

# 2. Vertical Slot Card (120 x 200)
def generate_vertical():
    canvas = Image.new("RGBA", (120, 200), (0, 0, 0, 0))
    # Background
    bg = Image.new("RGBA", (120, 200), (14, 24, 20, 220))
    canvas.alpha_composite(bg)
    
    # Crop head and shoulders: around X=70..370, Y=60..400
    crop_box = (60, 60, 380, 420)
    cropped = wr_full.crop(crop_box)
    
    scale = 200.0 / cropped.height
    new_w = int(cropped.width * scale)
    new_h = 200
    resized = cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)
    canvas.alpha_composite(resized, ((120 - new_w) // 2, 0))
    return canvas

vert = generate_vertical()
vert.save(out_dir / "archer_vertical_psd.png")

# 3. Small Avatar (128 x 128)
def generate_small():
    canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    # Background subtle dark teal
    bg = Image.new("RGBA", (128, 128), (16, 26, 22, 255))
    canvas.alpha_composite(bg)
    
    # Crop face: around X=120..320, Y=70..270
    crop_face = (110, 65, 330, 285)
    face = wr_full.crop(crop_face)
    face_resized = face.resize((128, 128), Image.Resampling.LANCZOS)
    canvas.alpha_composite(face_resized, (0, 0))
    return canvas

sm = generate_small()
sm.save(out_dir / "archer_sm_psd.png")
sm.save(out_dir / "archer_sm_psd_1ba0ed8b.png")

# 4. Minimap Icon (50 x 50)
def generate_minimap():
    canvas = Image.new("RGBA", (50, 50), (0, 0, 0, 0))
    # Circle mask
    mask = Image.new("L", (50, 50), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse([(1, 1), (48, 48)], fill=255)
    
    # Background
    bg = Image.new("RGBA", (50, 50), (20, 60, 35, 255))
    
    # Crop face close-up: X=140..300, Y=75..235
    face = wr_full.crop((130, 70, 310, 250))
    face_resized = face.resize((50, 50), Image.Resampling.LANCZOS)
    
    bg.alpha_composite(face_resized)
    bg.putalpha(mask)
    return bg

mm = generate_minimap()
mm.save(out_dir / "archer_mm_psd.png")

# 5. Background banner (4096 x 2312)
# Save clean high-res original Deadlock background
orig_bg.save(out_dir / "grey_talon_bg_psd.png")

print("[OK] All 7 classic panorama images generated successfully!")
