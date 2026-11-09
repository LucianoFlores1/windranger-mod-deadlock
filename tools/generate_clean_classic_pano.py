from PIL import Image, ImageFilter, ImageOps
import numpy as np
from pathlib import Path

# Load classic portrait
src_path = Path(r"extracted\dota_wr_pano\panorama\images\heroes\selection\npc_dota_hero_windrunner_png.png")
src = Image.open(src_path).convert("RGBA")

# Upscale with high quality Lanczos filter
# The original is 142 x 188.
print("Source size:", src.size)

# Output directory
out_dir = Path(r"extracted\new_classic_pano")
out_dir.mkdir(parents=True, exist_ok=True)

# 1. ARCHER_CARD_PSD (280 x 380)
# We want the bust of Windranger nicely framed in 280x380 with her classic green vignette background
# Crop src to match aspect ratio 280 / 380 = 0.7368
# Current aspect ratio = 142 / 188 = 0.7553 (almost exact!)
target_w, target_h = 280, 380
# Scale src to fill 280 x 380
card_img = src.resize((target_w, int(target_w * (src.height / src.width))), Image.Resampling.LANCZOS)
# If height is less than 380 or more, pad/crop
if card_img.height < target_h:
    # Scale by height
    card_img = src.resize((int(target_h * (src.width / src.height)), target_h), Image.Resampling.LANCZOS)

# Crop center/top
left = (card_img.width - target_w) // 2
top = 0
card_final = card_img.crop((left, top, left + target_w, top + target_h))

# Sharpen slightly for crispness
card_final = card_final.filter(ImageFilter.UnsharpMask(radius=1.2, percent=120, threshold=3))
card_final.save(out_dir / "archer_card_psd.png")
card_final.save(out_dir / "archer_card_critical_psd.png")
card_final.save(out_dir / "archer_card_gloat_psd.png")
print("[OK] archer_card_psd, critical, gloat saved (280x380)")

# 2. ARCHER_VERTICAL_PSD (120 x 200)
# Aspect ratio = 120 / 200 = 0.60
vert_h = 200
vert_w = int(vert_h * (src.width / src.height)) # 151
vert_img = src.resize((vert_w, vert_h), Image.Resampling.LANCZOS)
left = (vert_img.width - 120) // 2
vert_final = vert_img.crop((left, 0, left + 120, 200))
vert_final = vert_final.filter(ImageFilter.UnsharpMask(radius=1.0, percent=110, threshold=3))
vert_final.save(out_dir / "archer_vertical_psd.png")
print("[OK] archer_vertical_psd saved (120x200)")

# 3. ARCHER_SM_PSD (128 x 128) - Top Bar HUD Avatar
# For the HUD avatar, let's look at how Deadlock avatars are:
# Deadlock avatars are the hero's head/face on a transparent background, with a subtle dark outline.
# In src (142 x 188), let's crop the head/face:
# Head is roughly from Y=5 to Y=130, X=15 to X=125
head_crop = src.crop((12, 4, 130, 134)) # 118 x 130
# Now let's remove the greenish background outside the hair and hood to make it a transparent avatar:
# The background is dark olive/green (RGB around (45-75, 55-85, 20-50))
arr = np.array(head_crop)
r, g, b, a = arr[:,:,0], arr[:,:,1], arr[:,:,2], arr[:,:,3]

# In Dota 2 portraits, we can create a clean circular/soft mask or threshold:
# Better yet, let's inspect the pixels or create a clean vignette circular mask with subtle dark border:
# Wait, let's see how original Deadlock archer_sm_psd looks:
orig_sm = Image.open(r"extracted\dl_orig_pano\panorama\images\heroes\archer_sm_psd.png")
print("Original SM size:", orig_sm.size, "mode:", orig_sm.mode)

# Let's create a beautiful circular/badge headshot on transparent:
sm_size = 128
mask = Image.new('L', (sm_size, sm_size), 0)
from PIL import ImageDraw
draw = ImageDraw.Draw(mask)
# Draw an oval/circle that fills most of the frame
draw.ellipse((4, 4, 124, 124), fill=255)

# Resize head crop to 120x120
head_resized = head_crop.resize((120, 120), Image.Resampling.LANCZOS)
head_resized = head_resized.filter(ImageFilter.UnsharpMask(radius=1.0, percent=120, threshold=3))

sm_final = Image.new("RGBA", (sm_size, sm_size), (0, 0, 0, 0))
# Create circular background with subtle dark green/black backing
bg_circle = Image.new("RGBA", (sm_size, sm_size), (0, 0, 0, 0))
draw_bg = ImageDraw.Draw(bg_circle)
draw_bg.ellipse((4, 4, 124, 124), fill=(18, 32, 20, 255), outline=(35, 60, 40, 255), width=2)

# Paste head into center
sm_final.paste(bg_circle, (0, 0), bg_circle)
head_masked = Image.new("RGBA", (120, 120), (0, 0, 0, 0))
head_mask = Image.new('L', (120, 120), 0)
draw_hm = ImageDraw.Draw(head_mask)
draw_hm.ellipse((0, 0, 120, 120), fill=255)
sm_final.paste(head_resized, (4, 4), head_mask)

# Save sm and hash
sm_final.save(out_dir / "archer_sm_psd.png")
sm_final.save(out_dir / "archer_sm_psd_1ba0ed8b.png")
print("[OK] archer_sm_psd saved (128x128)")

# 4. ARCHER_MM_PSD (50 x 50) - Minimap Icon
mm_final = sm_final.resize((50, 50), Image.Resampling.LANCZOS)
mm_final.save(out_dir / "archer_mm_psd.png")
print("[OK] archer_mm_psd saved (50x50)")
