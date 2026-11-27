"""Regression tests for the manuscript audit and citation coverage."""
import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest


AUDIT_SCRIPT = (Path(__file__).resolve().parents[1]
                / ".agents/skills/physics-paper-orchestra/scripts/audit_manuscript.py")
SPEC = importlib.util.spec_from_file_location("audit_manuscript", AUDIT_SCRIPT)
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


class CitationAuditTests(unittest.TestCase):
    def setUp(self):
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.tex = self.root / "paper.tex"
        self.bib = self.root / "bibliography.bib"
        self.keys = [f"Paper{i}" for i in range(32)]
        self.bib.write_text("\n".join(
            f"@article{{{key}, title = {{Paper {i}}}}}"
            for i, key in enumerate(self.keys)
        ), encoding="utf-8")

    def write(self, body):
        self.tex.write_text(
            "\\begin{document}\n" + body + "\n\\end{document}\n", encoding="utf-8"
        )

    def use_keys(self, count):
        self.write(r"\cite{" + ",".join(self.keys[:count]) + "}")

    def audit(self, **kwargs):
        return AUDIT.audit(self.tex, self.bib, **kwargs)

    def test_active_citations_in_includes_with_optional_subsections(self):
        (self.root / "included.tex").write_text(
            r"\subsection{Optional}\citeauthor*{Paper2}\citeyearpar{Paper3}"
            r"\onlinecite{Paper4}\input nested", encoding="utf-8"
        )
        (self.root / "nested.tex").write_text(r"\Citet{Paper5}", encoding="utf-8")
        self.write(r"\citep[see][p.~1]{Paper0, Paper1}\citet{Paper0}\include{included}"
                   "\n% \\cite{Comment}\n"
                   r"\verb|\cite{Verbatim}|"
                   r"\begin{comment}\input{nonexistent}\end{comment}"
                   r"\iffalse\cite{Inactive}\else\citealt{Paper6}\fi"
                   r"\nocite{Paper7,*}\bibliography{bibliography}"
                   r"\appendix\cite{Paper8}\cite{Paper0}")
        report = self.audit(pages=1)
        self.assertEqual(report["unique_cited_publications"], 7)
        self.assertNotIn("missing_bib_entries", report)
        self.assertIn("Paper7", report["unused_bib_entries"])
        self.assertNotIn("Paper8", report["unused_bib_entries"])

    def test_duplicate_identifiers_and_missing_keys(self):
        self.bib.write_text(
            '@article{a, DOI = {https://doi.org/10.1234/ABC}}\n'
            '@article(b, doi = "10.1234/abc", pmid = {987})\n'
            '@article{c, pmid = {987}}\n'
            '@article{d, title = {Unused}}',
            encoding="utf-8",
        )
        self.write(r"\cite{a,b,c,missing}\appendix\cite{missingAppendix}")
        report = self.audit(pages=1)
        self.assertEqual(report["unique_cited_publications"], 1)
        self.assertEqual(report["duplicate_publications"], [["a", "b", "c"]])
        self.assertEqual(report["missing_bib_entries"], ["missing", "missingAppendix"])
        self.assertEqual(report["unused_bib_entries"], ["d"])
        self.assertEqual(report["citation_coverage"], "FAIL")

    def test_thresholds_without_subsections(self):
        for count, status in [(11, "FAIL"), (12, "WARNING"), (19, "WARNING"),
                              (20, "PASS"), (32, "PASS")]:
            with self.subTest(count=count):
                self.use_keys(count)
                report = self.audit(pages=4)
                self.assertEqual(report["citation_coverage"], status)
                self.assertEqual(report["minimum_publications"], 12)
                self.assertEqual(report["target_publications"], [20, 32])

    def test_compiled_boundary_and_missing_artifacts(self):
        self.write(r"\cite{Paper0}\bibliography{bibliography}\appendix\cite{Paper1}")
        self.assertEqual(self.audit()["citation_coverage"], "INCOMPLETE")
        self.tex.with_suffix(".aux").write_text(
            r"\newlabel{citation-coverage:last-scientific-page}{{4}{4}{}{section.4}{}}"
            "\n" + r"\gdef\@abspage@last{7}", encoding="utf-8"
        )
        self.tex.with_suffix(".pdf").touch()
        report = self.audit()
        self.assertEqual(report["scientific_pages"], 4)
        self.assertEqual(report["unique_cited_publications"], 1)
        self.assertEqual(self.audit(pages=5)["scientific_pages"], 5)

    def test_omissions_exclusions_and_explicit_exception(self):
        self.write(r"\cite{Paper0}\appendix\cite{Paper1}")
        config = {
            "author_supplied": ["Paper1", "Paper2"],
            "recommended": ["Paper3", "Paper4"],
            "reference_exclusions": {"Paper2": "Studies a different regime",
                                     "Paper4": "Superseded by the cited experiment"},
        }
        report = self.audit(pages=1, config=config)
        self.assertEqual(report["missing_author_supplied_references"], ["Paper1"])
        self.assertEqual(report["missing_recommended_references"], ["Paper3"])
        self.assertEqual(report["documented_reference_exclusions"], config["reference_exclusions"])
        self.assertEqual(report["citation_coverage"], "FAIL")
        config["approved_density_exception"] = {"reason": "Narrow replication"}
        with self.assertRaises(ValueError):
            self.audit(pages=1, config=config)
        config["approved_density_exception"].update(
            approved_by="Author", approval_record="paper/review.md, checkpoint 2"
        )
        self.assertEqual(self.audit(pages=1, config=config)["citation_coverage"], "WARNING")
        self.assertEqual(self.audit(config=config)["citation_coverage"], "INCOMPLETE")
        self.assertEqual(self.audit(pages=1, config={"minimum_per_page": 1,
                                                    "target_per_page": [1, 2]})["citation_coverage"],
                         "PASS")

    def test_structural_failures_still_fail(self):
        self.write(r"\begin{figure}\end{table}\input{missing}")
        report = self.audit()
        self.assertEqual(report["citation_coverage"], "FAIL")
        self.assertEqual(len(report["structural_issues"]), 2)
