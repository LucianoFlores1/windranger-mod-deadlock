import vpk
from pathlib import Path

CUSTOM_MOD = Path(r"E:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\custom_mod_source")
pak = vpk.open(str(CUSTOM_MOD / r"maps\ui\hero_prefabs\archer.vpk"))

for p in sorted(pak):
    if p.endswith('.vtex_c'):
        outer_file = CUSTOM_MOD / p
        inner_size = len(pak[p].read())
        outer_size = outer_file.stat().st_size if outer_file.exists() else None
        print(f"{p}:")
        print(f"   Inner (archer.vpk): {inner_size:,} bytes")
        outer_str = f"{outer_size:,}" if outer_size else "NOT FOUND"
        print(f"   Outer (custom_mod): {outer_str} bytes")
