import re, os
paper = {"ar":29.88,"da":52.20,"de":57.20,"en":66.34,"es":50.44,"fr":52.32,"hi":35.19,"hr":31.59,"id":41.80,"ja":41.06,"ko":27.46,"nl":47.59,"pt":49.50,"ru":39.89,"sk":46.75,"sv":53.30,"sw":27.61,"th":43.33,"tr":37.65,"vi":33.06,"zh":47.24}
def get(path):
    if not os.path.exists(path): return None
    t = open(path, encoding="utf-8-sig", errors="ignore").read()
    o = re.findall(r"Results of fixed output\s*\n\{[^}]*'f1': ([0-9.e-]+)", t)
    return 100*float(o[-1]) if o else None
print("lang  paper  base   copy   copy-base")
rows = []
for l in sorted(paper):
    b = get(rf"results_log\full\{l}.txt"); c = get(rf"results_log\copy\{l}.txt")
    if b is None or c is None:
        print(l, "missing"); continue
    rows.append((b, c, paper[l]))
    print(f"{l:4} {paper[l]:6.2f} {b:6.2f} {c:6.2f} {c-b:+7.2f}")
if rows:
    n = len(rows)
    print(f"avg  {sum(r[2] for r in rows)/n:6.2f} {sum(r[0] for r in rows)/n:6.2f} {sum(r[1] for r in rows)/n:6.2f} {sum(r[1]-r[0] for r in rows)/n:+7.2f}")
