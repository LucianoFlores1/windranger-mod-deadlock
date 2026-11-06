import re

data = open(r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\content\dota_addons\windrunner_classic\models\heroes_staging\archer\archer.vnmskel", "rb").read()
# Let's search for bow_string in the skeleton file
strings = [s.decode('latin1') for s in re.findall(rb'[a-zA-Z0-9_]{3,}', data)]
idx = [i for i, s in enumerate(strings) if 'bow_string' in s]
print("bow_string occurrences:", idx)
for i in idx:
    print(strings[max(0, i-5):min(len(strings), i+6)])

