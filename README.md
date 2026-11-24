# Undergraduate Physics Paper Starter

Turn your notes, results and figures into a physics paper with Codex. This standalone adaptation of the source repository's PaperOrchestra workflow keeps three author approvals in one place.

1. Extract this ZIP and open the project root in Codex.
2. Fill in [the project brief](inputs/brief.md). Add your notes, results, analysis code, figures, sources and any assignment brief to `inputs/`. Organise them however you like.
3. Tell Codex: “Follow AGENTS.md. Read my project inputs and prepare the plan for my approval.”
4. Review the plan, draft, then final PDF as Codex presents them. Give explicit approval at each checkpoint or name the changes you want. Codex records decisions in `paper/review.md`.

| Location | Contents |
| --- | --- |
| `AGENTS.md` | The full workflow and approval rules |
| `inputs/` | Your brief, notes and evidence |
| `guidance/` | The Warwick third-year laboratory report rubric and APS guide, plus an adapted APS quick reference |
| `paper/` | `paper.tex`, `bibliography.bib`, manuscript figures and the compiled `paper.pdf` |

The current assignment’s requirements take precedence for length, format, assessment and permitted AI assistance. Use the bundled [Warwick third-year laboratory report rubric](guidance/warwick-marking-sheet.pdf) where applicable and the APS guidance for style. For an actual journal submission, check the target journal's current instructions.

## Build the PDF

The bundled REVTeX template is the default. If your assignment supplies its own LaTeX template, use it as `paper/paper.tex` and place its supporting files under `paper/`. Use the toolchain required by that template and keep the working PDF at `paper/paper.pdf`.

For the bundled template, install a TeX distribution with REVTeX 4.2, pdfLaTeX, BibTeX, latexmk and the packages loaded by the template. From the repository root, run the following.

```sh
cd paper
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error paper.tex
```

This writes `paper/paper.pdf`. The starter contains example text and bibliography entries for replacement. In Overleaf, upload the contents of `paper/` so `paper.tex`, `bibliography.bib`, and `figures/` are at the project root, then select `paper.tex` as the main document.

[Source repository](https://github.com/Fortune12376/ising-paper)
