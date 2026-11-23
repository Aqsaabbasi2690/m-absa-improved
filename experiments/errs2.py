import re, json
T = re.compile(r"\((.*?), ([^,()]*), (positive|negative|neutral)\)")
def f1(path, key):
    t = open(path, encoding="utf-8-sig", errors="ignore").read()
    if key == "raw":
        m = re.findall(r"Results of raw output\s*\n\{[^}]*'f1': ([0-9.e-]+)", t)
    elif key == "fixed":
        m = re.findall(r"Results of fixed output\s*\n\{[^}]*'f1': ([0-9.e-]+)", t)
    else:
        m = re.findall(r"Results of STRICT[^\n]*\nraw:[^\n]*\nfixed: \{[^}]*'f1': ([0-9.e-]+)", t)
    return 100 * float(m[-1])
print("lang  raw   fixed  strict(fixed)  gold_dup%")
for l in ["de", "es", "sk", "en"]:
    p = rf"results_log\copy\{l}.txt"
    d = json.load(open(rf"results_log\preds\copy_restaurant_{l}_544_544.json", encoding="utf-8"))
    n = dup = 0
    for r in d:
        g = T.findall(r["gold"]); n += len(g); dup += len(g) - len(set(g))
    print(f"{l:4} {f1(p,'raw'):5.1f} {f1(p,'fixed'):6.1f} {f1(p,'strict'):12.1f} {100*dup/n:9.1f}")
