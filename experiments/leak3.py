import json, re
T = re.compile(r"\((.*?), ([^,()]*), (positive|negative|neutral)\)")
def trips(s):
    return [(a.strip().lower(), c.strip().lower(), p) for a, c, p in T.findall(s)]
def f1(tp, npred, ngold):
    p = tp/npred if npred else 0; r = tp/ngold if ngold else 0
    return 100*2*p*r/(p+r) if p+r else 0
en = json.load(open(r"results_log\preds\restaurant_en_544_544.json", encoding="utf-8"))
print("lang  fullF1  noTermF1  notInSent%  englishLeak%")
for lang in ["en", "es", "ru", "tr"]:
    d = json.load(open(rf"results_log\preds\restaurant_{lang}_544_544.json", encoding="utf-8"))
    tp = npd = ng = tp2 = npd2 = ng2 = tot = miss = leak = 0
    for i, r in enumerate(d):
        g, p = set(trips(r["gold"])), set(trips(r["pred"]))
        tp += len(g & p); npd += len(p); ng += len(g)
        g2, p2 = {(c, s) for _, c, s in g}, {(c, s) for _, c, s in p}
        tp2 += len(g2 & p2); npd2 += len(p2); ng2 += len(g2)
        sent = " ".join(r["sent"]).lower()
        ens = " ".join(en[i]["sent"]).lower()
        for t, _, _ in p:
            if t and t != "null":
                tot += 1
                if t not in sent:
                    miss += 1
                    if t in ens: leak += 1
    print(f"{lang:4} {f1(tp,npd,ng):7.1f} {f1(tp2,npd2,ng2):9.1f} {100*miss/tot:10.0f} {100*leak/tot:12.0f}")
