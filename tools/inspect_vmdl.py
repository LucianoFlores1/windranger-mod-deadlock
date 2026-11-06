import vpk

dl_pak = vpk.open(r'E:\SteamLibrary\steamapps\common\Deadlock\game\citadel\pak01_dir.vpk')
dota_pak = vpk.open(r'C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\dota\pak01_dir.vpk')

archer_vmdl = dl_pak['models/heroes_staging/archer/archer.vmdl_c'].read()
wr_vmdl = dota_pak['models/heroes/windrunner/windrunner.vmdl_c'].read()

print("Deadlock Archer vmdl size:", len(archer_vmdl))
print("Dota Windranger vmdl size:", len(wr_vmdl))

# In Source 2 compiled files (KV3 / binary resource format):
# First 4 bytes are usually resource type or block header
# Magic: 0x55CC895b or similar
print("Archer magic / header:", archer_vmdl[:16])
print("Windranger magic / header:", wr_vmdl[:16])
