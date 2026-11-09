import shutil
from pathlib import Path
from PIL import Image

src_dir = Path(r"extracted\orig_mod_pano")
dst_dir = Path(r"extracted\new_classic_pano")
dst_dir.mkdir(parents=True, exist_ok=True)

# 1. Base static portrait (the clean, beautiful Windranger bust)
card_static = Image.open(src_dir / "archer_card_psd.png")

# Use this EXACT same static face for normal, critical, and gloat!
card_static.save(dst_dir / "archer_card_psd.png")
card_static.save(dst_dir / "archer_card_critical_psd.png")
card_static.save(dst_dir / "archer_card_gloat_psd.png")
print("[OK] archer_card_psd, critical, and gloat set to unified static Windranger face!")

# 2. Vertical slot (120 x 200)
shutil.copy2(src_dir / "archer_vertical_psd.png", dst_dir / "archer_vertical_psd.png")
print("[OK] archer_vertical_psd copied!")

# 3. Small HUD avatar (128 x 128)
shutil.copy2(src_dir / "archer_sm_psd.png", dst_dir / "archer_sm_psd.png")
shutil.copy2(src_dir / "archer_sm_psd_1ba0ed8b.png", dst_dir / "archer_sm_psd_1ba0ed8b.png")
print("[OK] archer_sm_psd & hash copied!")

# 4. Minimap icon (50 x 50)
shutil.copy2(src_dir / "archer_mm_psd.png", dst_dir / "archer_mm_psd.png")
print("[OK] archer_mm_psd copied!")

print("\nAll UI textures prepared with unified static Windranger face.")
