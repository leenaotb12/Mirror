from pathlib import Path
import zipfile
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT.with_suffix(".zip")
with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED) as z:
    for p in ROOT.rglob("*"):
        if p.is_file() and "__pycache__" not in p.parts and ".pytest_cache" not in p.parts: z.write(p,p.relative_to(ROOT.parent))
print(OUT)
