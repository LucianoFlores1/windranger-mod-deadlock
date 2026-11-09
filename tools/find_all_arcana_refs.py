from pathlib import Path

base = Path("custom_mod_source")
for f in base.rglob("*"):
    if f.is_file():
        name = f.name.lower()
        if "arcana" in name:
            print("File name with arcana:", f.relative_to(base))
        elif f.suffix in [".vmat_c", ".vmdl_c", ".vpcf_c"]:
            try:
                content = f.read_bytes()
                if b"arcana" in content:
                    print(f"Content contains arcana: {f.relative_to(base)}")
            except Exception:
                pass
