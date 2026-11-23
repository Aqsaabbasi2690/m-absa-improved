import re, os
held = ["ar","da","es","fr","hi","hr","id","ja","ko","nl","pt","sk","sv","sw","th","tr","vi"]
def g(p):
    if not os.path.exists(p): return None
    t = open(p, encoding="utf-8-sig", errors="ignore").read()
    m = re.findall(r"f1\s*:\s*([0-9.]+) / ([0-9.]+)", t)
    return 100*float(m[-1][1]) if m and "* Results *" in t else None
print("lang  joint  joint+copy  diff")
a=[];b=[]
for l in held:
    j = g(rf"results_log\joint\{l}.txt"); c = g(rf"results_log\jointcopy\{l}.txt")
    if j is None or c is None: print(l, "missing"); continue
    print(f"{l:4} {j:6.2f} {c:9.2f} {c-j:+7.2f}"); a.append(j); b.append(c)
if a: print(f"avg over {len(a)}: joint {sum(a)/len(a):.2f}  joint+copy {sum(b)/len(b):.2f}")
