import vpk
from pathlib import Path
import itertools

DOTA_VPK = r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\dota\pak01_dir.vpk"
CUSTOM_VO = Path(r"custom_mod_source\sounds\vo\orion")

dota = vpk.open(DOTA_VPK)

def get_dota_lines(prefix):
    return [p for p in dota if p.lower().startswith(f"sounds/vo/windrunner/wind_{prefix}")]

# Define pools of authentic classic Windrunner lines
pools = {
    'angry': get_dota_lines('anger_') + get_dota_lines('pain_'),
    'be_careful': get_dota_lines('underattack_') + get_dota_lines('missing_'),
    'congrats': get_dota_lines('happy_') + get_dota_lines('thanks_'),
    'enemy_gets_rejuv': get_dota_lines('lose_'),
    'happy': get_dota_lines('happy_') + get_dota_lines('laugh_'),
    'kill_anyhero': get_dota_lines('kill_') + get_dota_lines('firstblood_') + get_dota_lines('killspecial_'),
    'parry': get_dota_lines('deny_'),
    'pick_up_rejuv': get_dota_lines('immort_') + get_dota_lines('haste_') + get_dota_lines('doubdam_') + get_dota_lines('regen_'),
    'select': get_dota_lines('spawn_') + get_dota_lines('battlebegins_') + get_dota_lines('move_'),
    'unselect': get_dota_lines('acknow_') + get_dota_lines('attack_'),
    'upgrade_power1': get_dota_lines('level_') + get_dota_lines('purch_'),
    'upgrade_power2': get_dota_lines('level_') + get_dota_lines('purch_'),
    'upgrade_power3': get_dota_lines('level_') + get_dota_lines('purch_'),
    'upgrade_power4': get_dota_lines('scepter_') + get_dota_lines('inthebag_') + get_dota_lines('level_'),
    'use_power1': get_dota_lines('ability_powershot_') + get_dota_lines('powershot_'),
    'use_power2': get_dota_lines('ability_windrun_') + get_dota_lines('blink_'),
    'use_power3': get_dota_lines('ability_shackleshot_') + get_dota_lines('shackl_'),
    'use_power4': get_dota_lines('ability_focusfire_') + get_dota_lines('rival_'),
}

# Cycle iterators for each pool
iterators = {}
for k, flist in pools.items():
    if not flist:
        print(f"[WARNING] Pool '{k}' is empty! Using generic lines.")
        flist = get_dota_lines('move_')
    iterators[k] = itertools.cycle(flist)

target_files = sorted(CUSTOM_VO.glob("*.vsnd_c"))
print(f"Replacing {len(target_files)} Grey Talon voice lines with Classic Dota 2 Windrunner voice lines...")

replaced_count = 0
for tf in target_files:
    fname = tf.stem # e.g. orion_use_power1_03
    name_clean = fname.replace("orion_", "")
    
    # Determine which pool matches best
    matched_pool = None
    for pool_name in sorted(pools.keys(), key=len, reverse=True):
        if name_clean.startswith(pool_name):
            matched_pool = pool_name
            break
            
    if not matched_pool:
        # Fallback by first word
        prefix = name_clean.split('_')[0]
        matched_pool = prefix if prefix in pools else 'select'
        
    src_dota_path = next(iterators[matched_pool])
    audio_data = dota[src_dota_path].read()
    tf.write_bytes(audio_data)
    replaced_count += 1

print(f"[SUCCESS] Replaced {replaced_count} voice lines with classic Windrunner voice lines from Dota 2!")

