# Physics PaperOrchestra prompts

## Author prompts

| When | Prompt |
| --- | --- |
| Start | Use $physics-paper-orchestra. Read inputs/brief.md, the marking scheme, any past feedback and my evidence. Prepare a section and page budget that prioritises gaps in assessed criteria. Stop for plan approval. |
| Approve the plan | I approve the current plan. Build the complete draft and stop for joint review. |
| Agree on revisions | I approve these revisions [list]. Use any remaining counted pages for these agreed priorities. Verify the paper and bring me the final PDF. |
| Decide on Google findings | Apply [accepted changes]. Record my decisions, rebuild and show me the resulting PDF. |
| Approve the final PDF | I approve paper/paper.pdf with SHA-256 [hash] as the final version. |
| Resume in a new session | Use $physics-paper-orchestra. Read paper/plan.md and paper/review.md and resume from the last approved checkpoint. |
| Resolve exhausted Google quota | Resume the pending Deep Review and check free quota again. / Finish checkpoint 3 with internal verification only and show me the PDF for approval. |

## Coordinator prompts for specialists

Use the role prompts below at the stages specified in the skill. Supply paths to the current brief, evidence, rubric or journal requirements, relevant past feedback, and applicable APS guidance. Include the approved scope, section budget and latest compiled length where available. The current assignment or verified venue rules take precedence. Map prior feedback to the current work where it applies.

- **outline · checkpoint 1.** Map each relevant marking criterion and recurring feedback item to a section and evidence path. Flag missing coverage, hard-to-find coverage and gaps that require evidence. Rank proposed additions by their importance to the rubric and estimate the space they need. Return a section budget within the counted limit, with room for floats. Identify APS conventions that affect presentation.
- **literature · checkpoint 2.** For your assigned gaps in theory, comparison or interpretation, verify primary sources and identify the exact claim each supports. Propose a concise addition and its location. Flag unsupported claims or unavailable sources.
- **figures · checkpoint 2.** For your assigned gaps in analysis, uncertainty or presentation, inspect the actual data, code and figures. Propose a plot, table, caption or calculation with evidence paths, estimated space and the criterion or feedback addressed. Flag analysis that still needs to be done.
- **writer · checkpoint 2.** Use the approved budget and verified specialist outputs. Draft the assigned sections and use remaining space first for the highest-priority supported gaps. Follow the active template and applicable APS conventions. Report what you added, what still needs evidence, and any sections that may exceed their budget.
- **reviewer · checkpoints 2 and 3.** Independently compare the draft and inspected PDF against the current rubric, applicable APS guidance and relevant past feedback. For each material gap, give the criterion or source, manuscript location, supporting evidence, likely impact, proposed fix and approximate space needed. Identify low-value material that could be cut if the draft is at the cap. At checkpoint 3, verify the agreed edits and flag any further change for the author.
