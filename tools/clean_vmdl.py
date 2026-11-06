import sys
from pathlib import Path

sys.path.insert(0, r"E:\creacion-mods\enigma-dynamo")
from pipeline.make_vmdl import _block_span

vmdl_path = Path(r"extracted\archer_windrunner.vmdl")
text = vmdl_path.read_text(encoding="utf-8")

cleaned_bodygroup = '''{
				_class = "BodyGroupList"
				children = 
				[
					{
						_class = "BodyGroup"
						name = "default"
						children = 
						[
							{
								_class = "BodyGroupChoice"
								name = "body"
								meshes = 
								[
									"windrunner_classic",
								]
							},
						]
					},
					{
						_class = "BodyGroup"
						name = "reload_bow_clip"
						children = 
						[
							{
								_class = "BodyGroupChoice"
								name = "bow_clip_off"
								meshes = [  ]
							},
						]
					},
					{
						_class = "BodyGroup"
						name = "reload_quiver_clip"
						children = 
						[
							{
								_class = "BodyGroupChoice"
								name = "quiver_in_hand"
								meshes = [  ]
							},
						]
					},
					{
						_class = "BodyGroup"
						name = "reload_quiverclips"
						children = 
						[
							{
								_class = "BodyGroupChoice"
								name = "empty"
								meshes = [  ]
							},
						]
					},
					{
						_class = "BodyGroup"
						name = "bow_toggle"
						children = 
						[
							{
								_class = "BodyGroupChoice"
								name = "Bow_off"
								meshes = [  ]
							},
						]
					},
					{
						_class = "BodyGroup"
						name = "owl"
						children = 
						[
							{
								_class = "BodyGroupChoice"
								name = "empty"
								meshes = [  ]
							},
						]
					},
				]
			}'''

start, end = _block_span(text, "BodyGroupList")
new_text = text[:start] + cleaned_bodygroup + text[end:]

csdk_vmdl = Path(r"E:\CSDK12\content\citadel_addons\windrunner_classic\models\heroes_staging\archer\archer.vmdl")
csdk_vmdl.write_text(new_text, encoding="utf-8")
print(f"[OK] Archer VMDL written to {csdk_vmdl}")
