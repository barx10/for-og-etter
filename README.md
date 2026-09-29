# Før og etter

Legge til nye bilder:

1. Legg originalene i mappen `originaler` (ligger i `.gitignore`, publiseres aldri).
2. Kjør `python3 rens_bilder.py` (krever `pip3 install pillow`). Skriptet fjerner EXIF, GPS og annen metadata og lager nettklare kopier i `bilder`.
3. Legg en linje i listen `rom` i `index.html`.
4. Commit og push.

Navn: `rom-nummer-for.jpg` og `rom-nummer-etter.jpg`.
