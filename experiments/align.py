import json, re
T = re.compile(r"\((.*?), ([^,()]*), (positive|negative|neutral)\)")
def cs(s): return sorted((c.strip().lower(), p) for _, c, p in T.findall(s))
en = json.load(open(r"results_log\preds\restaurant_en_544_544.json", encoding="utf-8"))
for lang in ["es", "ru", "tr"]:
    d = json.load(open(rf"results_log\preds\restaurant_{lang}_544_544.json", encoding="utf-8"))
    same = sum(cs(a["gold"]) == cs(b["gold"]) for a, b in zip(en, d))
    print(lang, f"{same}/{len(d)} gold label sets identical to English")
