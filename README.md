# Undergraduate Physics Paper Starter

Turn your notes, results and figures into a physics paper with Codex. The included **Physics PaperOrchestra** skill adapts [Google Research’s PaperOrchestra](https://research.google/pubs/paperorchestra-a-multi-agent-framework-for-automated-ai-research-paper-writing/) for undergraduate physics. It includes five named Codex specialists and three author approvals.

1. Clone the repository or extract the starter ZIP, then open the project root in Codex.
2. Fill in [the project brief](inputs/brief.md). Add your notes, results, analysis code, figures, sources and any assignment brief to `inputs/`. Organise them however you like.
3. Tell Codex: `Use $physics-paper-orchestra to read my project inputs and prepare the plan for my approval. Use the specialist agents if available.`
4. Approve the scientific plan before drafting. Review the complete first draft jointly with any collaborators and agree on scoped revisions. After the final audit, explicitly approve the compiled PDF identified by its SHA-256. A changed PDF needs fresh approval. Codex resumes from the decisions in `paper/review.md`.

| Location | Contents |
| --- | --- |
| `AGENTS.md` | Gives Codex the project entry point |
| [Physics PaperOrchestra](.agents/skills/physics-paper-orchestra/SKILL.md) | Named skill with the full workflow and approval rules |
| [`.codex/agents/`](.codex/agents/) | `outline`, `literature`, `figures`, `writer` and `reviewer` specialists |
| `inputs/` | Your brief, notes and evidence |
| `guidance/` | The Warwick third-year laboratory report rubric and APS guide, plus an adapted APS quick reference |
| `paper/` | `paper.tex`, `bibliography.bib`, manuscript figures, `plan.md`, `review.md` and the compiled `paper.pdf` |

The current assignment’s requirements take precedence for length, format, assessment and permitted AI assistance. Use the bundled [Warwick third-year laboratory report rubric](guidance/warwick-marking-sheet.pdf) where applicable and the APS guidance for style. For an actual journal submission, check the target journal's current instructions.

## Build the PDF

The bundled REVTeX template is the default. If your assignment supplies its own LaTeX template, use it as `paper/paper.tex` and place its supporting files under `paper/`. Use the toolchain required by that template and keep the working PDF at `paper/paper.pdf`.

For the bundled template, install a TeX distribution with REVTeX 4.2, pdfLaTeX, BibTeX, latexmk and the packages loaded by the template. From the repository root, run the following.

```sh
cd paper
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error paper.tex
```

This writes `paper/paper.pdf`. The starter contains example text and bibliography entries for replacement. In Overleaf, upload the contents of `paper/` so `paper.tex`, `bibliography.bib`, and `figures/` are at the project root, then select `paper.tex` as the main document.

The checkpoint workflow was adapted from the [Ising reference project](https://github.com/Fortune12376/ising-paper), a private repository.
