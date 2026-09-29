#!/usr/bin/env python3
"""Fjerner EXIF (inkl. GPS) fra bilder og lager nettklare kopier.

Bruk:
  1. Legg nye bilder i mappen "originaler" (den ligger i .gitignore og blir aldri publisert).
  2. Kjør:  python3 rens_bilder.py
  3. Rensede bilder havner i "bilder" som .jpg, maks 2000 px på lengste side.

Krever Pillow:  pip3 install pillow
"""
import sys
from pathlib import Path
from PIL import Image, ImageOps

MAKS = 2000
KVALITET = 88
HER = Path(__file__).parent
INN = HER / "originaler"
UT = HER / "bilder"
ENDELSER = {".jpg", ".jpeg", ".png", ".webp"}


def rens(kilde: Path, mal: Path) -> None:
    with Image.open(kilde) as im:
        icc = im.info.get("icc_profile")
        im = ImageOps.exif_transpose(im)  # bruk rotasjonen før metadata forsvinner
        im = im.convert("RGB")
        im.thumbnail((MAKS, MAKS), Image.LANCZOS)
        # Lagrer bare piksler og fargeprofil. EXIF, GPS og XMP skrives ikke.
        im.save(mal, "JPEG", quality=KVALITET, optimize=True, progressive=True,
                icc_profile=icc)


def sjekk(fil: Path) -> bool:
    with Image.open(fil) as im:
        return not im.getexif() and "xmp" not in im.info and "exif" not in im.info


def main() -> int:
    UT.mkdir(exist_ok=True)
    INN.mkdir(exist_ok=True)
    filer = sorted(f for f in INN.iterdir() if f.suffix.lower() in ENDELSER)
    if not filer:
        print("Ingen bilder i originaler.")
        return 0
    feil = 0
    for f in filer:
        mal = UT / (f.stem + ".jpg")
        rens(f, mal)
        ok = sjekk(mal)
        feil += not ok
        print(("OK   " if ok else "FEIL ") + mal.name)
    return 1 if feil else 0


if __name__ == "__main__":
    sys.exit(main())
