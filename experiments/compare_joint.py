import re, os
paper = {"ar":29.88,"da":52.20,"de":57.20,"en":66.34,"es":50.44,"fr":52.32,"hi":35.19,"hr":31.59,"id":41.80,"ja":41.06,"ko":27.46,"nl":47.59,"pt":49.50,"ru":39.89,"sk":46.75,"sv":53.30,"sw":27.61,"th":43.33,"tr":37.65,"vi":33.06,"zh":47.24}
seen = {"en","de","ru","zh"}
def get(p):
    if not os.path.exists(p): return None
    t = open(p, encoding="utf-8-sig", errors="ignore").read()
    if "* Results *" not in t: return None
    m = re.findall(r"f1\s*:\s*([0-9.]+) / ([0-9.]+)", t)
    return 100*float(m[-1][1]) if m else None
print("lang  paper  base   copy   joint  joint-base  seen?")
rb=[];rj=[]
for l in sorted(paper):
    b = get(rf"results_log\full\{l}.txt"); c = get(rf"results_log\copy\{l}.txt"); j = get(rf"results_log\joint\{l}.txt")
    if None in (b,c,j): print(l, "missing", b, c, j); continue
    print(f"{l:4} {paper[l]:6.2f} {b:6.2f} {c:6.2f} {j:6.2f} {j-b:+8.2f}   {'TRAIN' if l in seen else 'zero-shot'}")
    if l not in seen: rb.append(b); rj.append(j)
if rb: print(f"avg over {len(rb)} held-out langs: base {sum(rb)/len(rb):.2f}  joint {sum(rj)/len(rj):.2f}")
