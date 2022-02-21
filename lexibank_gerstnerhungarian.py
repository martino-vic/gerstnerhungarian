import pathlib
import re

import attr
from clldutils.misc import slug
from pylexibank import Dataset as BaseDataset
from pylexibank import FormSpec, Concept

REP = [(x, "") for x in "†×∆-¹²³⁴’"]


@attr.s
class CustomConcept(Concept):
    year = attr.ib(default=None)
    origin = attr.ib(default=None)
    Loan = attr.ib(default=None)

class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "streitberggothic"

    form_spec = FormSpec(separators=",", first_form_only=True,
                         replacements=REP)

    concept_class = CustomConcept

    def cmd_makecldf(self, args):

        # add bib
        args.writer.add_sources()
        args.log.info("added sources")

        # add concept
        concepts = {}
        for i, concept in enumerate(self.concepts):
            idx = str(i + 1) + "_" + slug(concept["sense"])
            concept["year"] = int(float(concept["year"])) if concept["year"] else ""  # get rid of ".0"
            args.writer.add_concept(
                ID=idx,
                Name=concept["sense"],
                year=concept["year"],
                origin=concept["origin"],
                Concepticon_ID=concept["Concepticon_ID"],
                Concepticon_Gloss=concept["Concepticon_Gloss"]
            )
            concepts[concept["sense"], concept["origin"]] = idx
        args.log.info("added concepts")

        # add languages
        args.writer.add_languages()
        args.log.info("added languages")

        # add forms
        for idx, row in enumerate(self.raw_dir.read_csv(
                "Gerstner-2016-3532.tsv", delimiter="\t", dicts=True)[1:]):
            row["Loan"] = True if row["Loan"] == "True" else False
            args.writer.add_forms_from_value(
                Local_ID=idx,
                Language_ID="Hungarian",
                Parameter_ID=concepts[row["sense"], row["origin"]],
                Value=row["form"],
                Source="uesz",
                Loan = row["Loan"])

        args.log.info("added forms")

