"""cd to folder `misc` and run `python reconstruct.py` from terminal"""

from pathlib import Path
import re

import pandas as pd

from loanpy import adrc

def main():
    """adds col with backward-reconstructions to forms.csv"""

    # define in and output paths and name of the output column
    in_path1 = Path.cwd().parent.parent / "cldf" / "forms.csv"
    in_path2 = Path.cwd().parent.parent.parent / "ronatasbertawot" / "etc" / "soundchangesH_EAH.txt"
    out_path = in_path1
    outcolname = "rc"

    #read in forms.csv with pandas
    dfforms = pd.read_csv(in_path1)
    #add new column of backward-reconstructions with loanpy
    Sc = adrc.Adrc(scdict=in_path2)
    dfforms[outcolname] = [Sc.reconstruct(i.replace(" ", ""), fp=10)
                           for i in dfforms["Segments"]]
    #write new file
    dfforms.to_csv(out_path, encoding="utf-8", index=False)

if __name__ == "__main__":
    main()
