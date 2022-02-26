import pandas as pd
from numpy import nan
from pathlib import Path

in_path = Path.cwd().parent / "wordlist.tsv"
out_path = Path.cwd().parent / "wordlist.tsv"

dfwl = pd.read_csv(in_path, sep="\t").dropna()
# "†×∆" means archaism, so can be dropped
dfwl["FORM"] = [nan if any(i in w for i in "†×∆") else w for w in dfwl["FORM"]]
dfwl = dfwl.dropna()
dfwl = dfwl.groupby('CONCEPTICON_ID').head(2)  # keep max two
dfwl.to_csv(out_path, sep="\t", encoding="utf-8", index=False)
