# Physics paper workflow

Use the three checkpoints below for a full paper. For a targeted edit, literature check or review, work on the requested scope. For a paper in this workflow, keep the relevant approvals and return any affected version for author review.

## 1. Plan and stop for approval

- Start with `inputs/brief.md` and the relevant material under `inputs/`. Establish the research question, intended audience, deliverables, permitted assistance and exact length rules. The current assignment’s requirements take precedence. Consult the [Warwick third-year laboratory report rubric](guidance/warwick-marking-sheet.pdf) and [APS style notes](guidance/aps-style.md) as applicable. For journal submissions, verify the live venue requirements.
- Use the bundled REVTeX template as the default. If the assignment supplies its own LaTeX template, use it as `paper/paper.tex` and place any files it needs under `paper/`. Keep the working PDF at `paper/paper.pdf` with either template.
- Use notes to locate the evidence. Check consequential numbers, uncertainties and methods against the relevant results and code. Flag gaps and discrepancies, including proposed analyses that have yet to run.
- Create `paper/plan.md` with the scientific argument, section and page budget, planned figures and tables, and literature to verify. Map each major claim to its source path and the relevant table, rows, code or derivation. State the assumptions and what the evidence supports.
- Present the plan and any consequential decisions. Stop for explicit author approval before drafting. Apply requested changes to the plan and return it for approval.

## 2. Draft and stop for approval

- PaperOrchestra specialist delegation is optional. When subagents are available and you use them, delegate literature verification and figure preparation to separate specialists. Run them in parallel when their tasks are independent. Once the draft is complete, use a separate reviewer. Handle these tasks directly when working without subagents.
- Verify the literature against the specific claims it will support and check the BibTeX metadata. Reuse or generate figures from traceable inputs, keeping plots in `paper/figures/` and recording their source data and processing in the plan or review notes.
- Draft in `paper/paper.tex`. Use `paper/bibliography.bib` with the default template and follow any bibliography requirements of the assignment template. Write methods, results and figures first, then discussion, introduction and theory, conclusion, abstract and title. Arrange the finished draft in the required reading order. Keep observations, derivations and interpretations distinct. Mark unresolved evidence gaps and use wording proportional to the available evidence.
- Review scientific support, notation, units, uncertainties, figures, citations and rubric coverage. Use up to two focused internal review passes as needed. Build using the README command or the assignment template’s required toolchain and inspect the rendered `paper/paper.pdf` and build log. Report any gap, warning or build problem that affects review. If a build fails, identify which current files can be reviewed and treat any older PDF as stale.
- Present the draft TeX and available current PDF, with material issues and decisions. Stop for explicit author approval of the draft and any agreed revisions. Put the author's decisions and revision scope in `paper/review.md`.

## 3. Revise, verify and stop for final PDF approval

- Apply the agreed revisions in place. Bring consequential changes to the research question, methods or conclusions back to the author before treating them as settled. Keep one working TeX file and bibliography.
- Audit the whole revised paper once. Check claims against results and code, method reproducibility, equations and uncertainties, citations and bibliography, figure and table order and captions, placeholder removal, and the active rubric and page limit. Report main-text and total length as applicable. Rebuild, check the build log for unresolved references, citations and layout issues, and inspect the rendered PDF page by page.
- Present `paper/paper.pdf` with a short change summary and any outstanding limitations. Record its SHA-256 in `paper/review.md` so approval refers to the exact file reviewed. Stop for explicit author approval of that PDF. Final approval requires a successful build and inspection of the current PDF.
- The approved deliverable is that same `paper/paper.pdf`. After approval, leave it in place. If a requested edit or rebuild changes the PDF bytes, present the new PDF for approval.

Record each approval in `paper/review.md` only after the author explicitly gives it. Include the date, artifact reviewed and any agreed revisions. When resuming work, check these records and continue from the current checkpoint. Keep a material change to an approved plan or draft at the affected checkpoint until the author approves it again. Never invent evidence, references, or checks.
