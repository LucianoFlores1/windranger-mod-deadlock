from PIL import Image
from pathlib import Path

orig_dir = Path(r"extracted\dl_orig_pano\panorama\images\heroes")
for p in orig_dir.glob("*.png"):
    im = Image.open(p)
    print(p.name, im.size, im.mode)
