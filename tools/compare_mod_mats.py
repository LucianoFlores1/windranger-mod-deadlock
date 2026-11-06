import vpk

# Compare materials in dota2_extracted vs pak22
dota_dir = r'e:\Antigravity-consultas-y-pruebas\windranger-mod-deadlock\dota2_extracted'
mod_pak = vpk.open(r'extracted_mod\pak22_dir.vpk')

print("Materials in mod:")
mod_vmats = [f for f in mod_pak if f.endswith('.vmat_c')]
for m in mod_vmats:
    print("  ", m)

print("\nTextures in mod:")
mod_vtexs = [f for f in mod_pak if f.endswith('.vtex_c')]
for t in mod_vtexs:
    print("  ", t)
