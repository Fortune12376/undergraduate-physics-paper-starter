---
name: physics-paper-orchestra
description: Plan, draft, revise, and verify physics reports and manuscripts. Use for undergraduate physics coursework, lab and simulation reports, or physics papers that need evidence checking, literature and figure specialists, LaTeX drafting, and author approval checkpoints.
---

# Physics PaperOrchestra

Apply the physics adaptation of Google Research’s five-agent PaperOrchestra workflow. The coordinating thread owns the plan, integrations, and approvals. Use the three checkpoints below for a full paper. For a targeted edit, literature check or review, work on the requested scope. For a paper in this workflow, keep the relevant approvals and return any affected version for author review.

For assessed reports, consult [the physics report principles](references/warwick-report-principles.md). For PRL-style writing or submission work, consult [the physics writing reference](references/prl-physics-writing-original.md) as needed. Give the current assignment or verified journal rules precedence.

## 1. Plan and stop for approval

- Start with `inputs/brief.md` and the relevant material under `inputs/`. Establish the research question, intended audience, deliverables, permitted assistance and exact length rules. The current assignment’s requirements take precedence. Consult the [Warwick third-year laboratory report rubric](../../../guidance/warwick-marking-sheet.pdf) and [APS style notes](../../../guidance/aps-style.md) as applicable. For journal submissions, verify the live venue requirements.
- Use the bundled REVTeX template as the default. If the assignment supplies its own LaTeX template, use it as `paper/paper.tex` and place any files it needs under `paper/`. Keep the working PDF at `paper/paper.pdf` with either template.
- Use notes to locate the evidence. Check consequential numbers, uncertainties and methods against the relevant results and code. Flag gaps and discrepancies, including proposed analyses that have yet to run.
- Use the `outline` specialist to prepare the plan when delegating. Create `paper/plan.md` with the scientific argument, section and page budget, planned figures and tables, and literature to verify. Map each major claim to its source path and the relevant table, rows, code or derivation. State the assumptions and what the evidence supports.
- Present the plan and any consequential decisions. Stop for explicit author approval before drafting. Apply requested changes to the plan and return it for approval.
- Preserve the initial plan and outline specialist findings or author feedback in `paper/plan.md`. Append concise decisions and amendments so the initial version stays identifiable.

## 2. Draft and stop for approval

- Delegate to `literature` and `figures` when subagents are available and permitted. Run the two specialists in parallel when their work is independent, then integrate their outputs before delegating the full draft to `writer`. Use `reviewer` for independent review. Carry out the same five roles in sequence when delegation is unavailable or the author prefers a single thread.
- Verify the literature against the specific claims it will support and check the BibTeX metadata. Reuse or generate figures from traceable inputs, keeping plots in `paper/figures/` and recording their source data and processing in the plan or review notes.
- Draft in `paper/paper.tex`. Use `paper/bibliography.bib` with the default template and follow any bibliography requirements of the assignment template. Write methods, results and figures first, then discussion, introduction and theory, conclusion, abstract and title. Arrange the finished draft in the required reading order. Keep observations, derivations and interpretations distinct. Mark unresolved evidence gaps and use wording proportional to the available evidence.
- Review scientific support, notation, units, uncertainties, figures, citations and rubric coverage. Use up to two focused internal review passes as needed. Build using the README command or the assignment template’s required toolchain and inspect the rendered `paper/paper.pdf` and build log. Report any gap, warning or build problem that affects review. If a build fails, identify which current files can be reviewed and treat any older PDF as stale.
- Before applying internal review edits, capture the first complete draft in `paper/.local/` or identify a local Git revision with its source and supporting files. In `paper/review.md`, reference that version, summarize the initial reviewer findings and edits applied, and identify the draft presented for joint review.
- Present the complete draft TeX and inspected PDF for joint author review, along with the figure and reference inventory, substantive open issues and any build limitations. Invite comments from all participating authors and collaborators. Stop for explicit agreement on the draft disposition and revision scope before revising. Record the agreed revisions and decisions in `paper/review.md`. For multiple contributors, assign separate sections or deliverables and use separate task branches for concurrent Git work.

## 3. Revise, verify and stop for final PDF approval

- Make scoped, human-led revisions to the assigned sections, figures or references. Invoke only the specialists relevant to the agreed work. Integrate the accepted changes into the single working manuscript before the final audit. Authors resolve conflicts that affect scientific intent. Bring consequential changes to the research question, methods or conclusions back to the author before treating them as settled. Keep one working TeX file and bibliography.
- Run one combined audit of the revised paper. Use the `reviewer` specialist when delegating. Check claims against results and code, method reproducibility, equations and uncertainties, citations and bibliography, figure and table order and captions, placeholder removal, and the active rubric and page limit. Report main-text and total length as applicable. Rebuild, check the build log for unresolved references, citations and layout issues, and inspect the rendered PDF page by page.
- With the default template, run the [structural audit](scripts/audit_manuscript.py) using `python .agents/skills/physics-paper-orchestra/scripts/audit_manuscript.py paper/paper.tex paper/bibliography.bib`. Use the compile log for the current template’s full citation and cross-reference checks.
- Record the edits actually made against the checkpoint 2 scope and the combined verification in `paper/review.md`. Identify the near-final PDF by its SHA-256.
- When the author has explicitly opted in for this paper, the assignment permits it, and the audit, build and inspection are complete, automatically run `python scripts/deep_review.py --checkpoint-3` from the repository root in local Codex in VS Code. Store the opt-in in `paper/plan.md` or `paper/review.md`. Follow the [README setup](../../../README.md#optional-google-deep-review-at-checkpoint-3). Run the command again to retrieve a pending operation. If no free slot is available, report the next time when supplied and let the author choose to wait or finish. Record the choice. Resume only when the author returns to the pending step.
- Read the full saved Google review and verify material findings against the exact reviewed PDF, manuscript, analysis and sources. Record concise dispositions and present proposed edits for author agreement. Apply agreed changes, record what changed, and rebuild and recheck affected verification before presenting the final PDF. The saved local review and exact reviewed PDF remain linked in `paper/review.md`. Use one free review by default and keep the existing review attached to its original version across rebuilds.
- Present `paper/paper.pdf` with a short change summary and any outstanding limitations. Record its SHA-256 in `paper/review.md` so approval refers to the exact file reviewed. Stop for explicit author approval of that PDF. Final approval requires a successful build and inspection of the current PDF.
- The approved deliverable is that same `paper/paper.pdf`. After approval, leave it in place. If a requested edit or rebuild changes the PDF bytes, present the new PDF for approval.

## Approval record across sessions

Keep a chronological record in `paper/review.md`. On resumption, read it alongside `paper/plan.md` and the current manuscript. Identify the last explicitly approved checkpoint, any pending decision and the agreed work still open before continuing.

Keep actual snapshots and review outputs local unless the author explicitly chooses to publish them. Use `paper/.local/` for file snapshots and Google artifacts. If using a local Git revision for a snapshot, keep its commits off any branch that will be pushed without explicit publication authorization.

For each checkpoint, record the date, checkpoint name, artifact paths and reviewed version (commit or file hash where available), pending or approved status, and any open issues. Record approval only after the author explicitly gives it, with the date and who approved. At joint draft review, record agreed changes, their owners and assigned sections or branches. At final review, record the SHA-256 of the PDF presented and tie the approval to that exact hash. On resumption, compare the current PDF hash with the approved hash before relying on final approval.

Return a materially changed plan or draft to its checkpoint for fresh approval. Any change to the PDF bytes requires fresh final approval. Never invent evidence, references, or checks.
