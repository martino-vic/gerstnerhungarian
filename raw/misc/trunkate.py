"""will remove rows that can't be linked to concepticon"""

from pathlib import Path
import re

import pandas as pd
from pysem.glosses import to_concepticon

in_path = Path.cwd().parent / "Gerstner-2016-9926.tsv"
out_path = in_path

def gg(d):
    """dict vals to tuples (ID, Gloss) or ("", "")"""
    return {k: (d[k][0][0], d[k][0][1]) if d[k] else ("", "") for k in d}
    
def main():
    """"
    read Gerstner-2016-10085.tsv,
    link data to concepticon,
    write concepts.tsv
    """
    # read file and clean column "sense"
    dfuesz = pd.read_csv(in_path, sep="\t", usecols=["form", "sense", "year", "origin", "Loan"]).dropna(subset=["sense"])

    # define list of dictionaries and plug into to_concepticon()
    glo = [{"gloss": g, "year": y, "origin": o} for g,y,o in zip(dfuesz.sense, dfuesz.year, dfuesz.origin)]
    G = gg(to_concepticon(glo, language="de", max_matches=1))

    # map dictionary to new columns
    newcols = ["Concepticon_ID", "Concepticon_Gloss"]
    dfuesz[newcols] = dfuesz['sense'].map(G).tolist()
    
    dfuesz.to_csv(out_path, index=False, encoding="utf-8", sep="\t")
    pd.read_csv(out_path, sep="\t").dropna(subset=["Concepticon_ID"]).to_csv(out_path, index=False, encoding="utf-8", sep="\t")


if __name__ == "__main__":
    main()
