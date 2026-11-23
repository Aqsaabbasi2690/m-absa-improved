import re, glob, os, csv
paper = {"ar":29.88,"da":52.20,"de":57.20,"en":66.34,"es":50.44,"fr":52.32,"hi":35.19,"hr":31.59,"id":41.80,"ja":41.06,"ko":27.46,"nl":47.59,"pt":49.50,"ru":39.89,"sk":46.75,"sv":53.30,"sw":27.61,"th":43.33,"tr":37.65,"vi":33.06,"zh":47.24}
rows = []
for f in sorted(glob.glob(r"results_log\full\*.txt")):
    lang = os.path.basename(f)[:-4]
    t = open(f, encoding="utf-8-sig", errors="ignore").read()
    o = re.findall(r"Results of fixed output\s*\n\{[^}]*'f1': ([0-9.e-]+)", t)
    s = re.findall(r"Results of STRICT[^\n]*\nraw:[^\n]*\nfixed: \{[^}]*'f1': ([0-9.e-]+)", t)
    if o and s:
        rows.append((lang, 100*float(o[-1]), 100*float(s[-1]), paper[lang]))
    else:
        print(lang, "-> no results found (check the file)")
print("lang  ours_official  ours_strict  paper  diff(official-paper)")
for l, a, b, p in rows:
    print(f"{l:4}  {a:12.2f}  {b:11.2f}  {p:5.2f}  {a-p:+.2f}")
if rows:
    print(f"avg   {sum(r[1] for r in rows)/len(rows):12.2f}  {sum(r[2] for r in rows)/len(rows):11.2f}  {sum(r[3] for r in rows)/len(rows):5.2f}")
    with open(r"..\..\..\results\baseline\restaurant_tasd_zero_shot.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["lang","ours_official_f1","ours_strict_f1","paper_f1"]); w.writerows(rows)
