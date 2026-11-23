import glob, re
from data_utils import _safe_parse
bad = 0
for f in glob.glob(r"data\tasd\restaurant\*\*.txt"):
    for i, line in enumerate(open(f, encoding="utf-8")):
        line = line.strip()
        if "####" not in line:
            continue
        lab = line.split("####")[-1]
        expected = len(re.findall(r"'(?:positive|negative|neutral)'\s*\]", lab))
        got = len(_safe_parse(lab))
        if expected != got:
            bad += 1
            print(f, i + 1, expected, got, lab[:120])
print("mismatched lines:", bad)
