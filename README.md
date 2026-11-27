# Undergraduate Physics Paper Starter

Turn your notes, results and figures into a physics paper with Codex. The included **Physics PaperOrchestra** skill adapts [Google Research’s PaperOrchestra](https://research.google/pubs/paperorchestra-a-multi-agent-framework-for-automated-ai-research-paper-writing/) for undergraduate physics. It includes five named Codex specialists and three author approvals.

1. Clone the repository or extract the starter ZIP, then open the project root in Codex.
2. Fill in [the project brief](inputs/brief.md). Add your notes, results, analysis code, figures, sources and any assignment brief to `inputs/`. Organise them however you like.
3. Start with the checkpoint 1 prompt below. The skill handles the specialist work, build and optional external review between your decisions.

| Location | Contents |
| --- | --- |
| `AGENTS.md` | Gives Codex the project entry point |
| [Scientific writing and review](guidance/scientific-writing.md) | Shared guidance for experimental, theoretical and computational reports |
| [Physics PaperOrchestra](.agents/skills/physics-paper-orchestra/SKILL.md) | Named skill with the full workflow and approval rules |
| [`.codex/agents/`](.codex/agents/) | `outline`, `literature`, `figures`, `writer` and `reviewer` specialists |
| `inputs/` | Your brief, notes and evidence |
| `guidance/` | The Warwick third-year laboratory report rubric and APS guide, plus an adapted APS quick reference |
| `paper/` | `paper.tex`, `bibliography.bib`, manuscript figures, `plan.md`, `review.md` and the compiled `paper.pdf` |

The current assignment’s requirements take precedence for length, format, assessment and permitted AI assistance. Use the bundled [Warwick third-year laboratory report rubric](guidance/warwick-marking-sheet.pdf) where applicable and the APS guidance for style. For an actual journal submission, check the target journal's current instructions.

## Prompts and approval checkpoints

Use these in Codex in VS Code from the repository root. Replace bracketed text with your own decisions. In a continuous session, you can use plain language after the first prompt.

The [stored prompt bank](.agents/skills/physics-paper-orchestra/references/prompts.md) includes the author prompts and the assignments Codex gives each specialist. Put past marker or supervisor feedback under `inputs/` and link it in the brief. Workers use the active rubric, relevant feedback and applicable APS guidance to rank evidence-backed uses for remaining pages.

| When | What Codex brings you | What to say |
| --- | --- | --- |
| Start checkpoint 1 | An evidence map, section and page budget, figure plan and Google Deep Review setting in `paper/plan.md` | `Use $physics-paper-orchestra. Read inputs/brief.md and my evidence, prepare the paper plan, and stop for my approval.` |
| Approve the plan | The current plan and any open decisions | `I approve the current plan. Build the complete draft and stop for joint review.` |
| Agree on scope at checkpoint 2 | The inspected draft PDF, reviewer findings, edits already applied and issues for discussion | `I approve proceeding with these revisions [list agreed changes]. Apply them, verify the paper and bring me the final PDF for approval.` |
| Review proposed Google edits, if any | Findings checked against the paper, analysis and sources | `Apply [accepted changes]. Record my decisions, rebuild and show me the resulting PDF.` |
| Approve checkpoint 3 | The inspected final PDF, change summary, remaining limitations and SHA-256 | `I approve paper/paper.pdf with SHA-256 [hash] as the final version.` |

To return in a new session, say `Use $physics-paper-orchestra. Read paper/plan.md and paper/review.md and resume from the last approved checkpoint.` If Google quota was exhausted, say `Resume the pending Deep Review and check free quota again.` or `Finish checkpoint 3 with internal verification only and show me the PDF for approval.`

For example, a pendulum report with an eight-page main-text limit might budget space for the small-angle model, measurement method, plots and uncertainty analysis. After reading the draft, you might agree to add the fitted intercept and explain how its uncertainty affects the interpretation. Codex records that scope, checks the revision against the fit and confirms the counted page length from the compiled PDF. At checkpoint 3, it checks for a free external review if enabled and then brings you the exact PDF to approve.

## Build the PDF

The bundled REVTeX template is the default. If your assignment supplies its own LaTeX template, use it as `paper/paper.tex` and place its supporting files under `paper/`. Use the toolchain required by that template and keep the working PDF at `paper/paper.pdf`.

For the bundled template, install a TeX distribution with REVTeX 4.2, pdfLaTeX, BibTeX, latexmk and the packages loaded by the template. From the repository root, run the following.

```sh
cd paper
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error paper.tex
```

This writes `paper/paper.pdf`. The starter contains example text and bibliography entries for replacement. In Overleaf, upload the contents of `paper/` so `paper.tex`, `bibliography.bib`, and `figures/` are at the project root, then select `paper.tex` as the main document.

The checkpoint workflow was adapted from the [Ising reference project](https://github.com/Fortune12376/ising-paper), a private repository.

## Optional Google Deep Review at checkpoint 3

Google Deep Review is **Yes** by default in `inputs/brief.md`. The checkpoint 1 plan states that Google will receive the complete near-final PDF if a free slot is available and the applicable rules allow external AI review. Approving that plan confirms the setting for the paper. To skip it, set the brief to **No** or tell Codex directly:

> Skip Google Deep Review for this paper and record my decision.

Once the internal audit, build and PDF inspection are complete, Codex runs this from the repository root and uses the same command to resume a pending review.

```sh
python scripts/deep_review.py --checkpoint-3
```

### One-time Google Cloud setup

Install the Google Cloud CLI and choose a Google Cloud project. Google's quickstart requires billing enabled on the project. Use your own signed-in Google user with permission to enable the API or have a project administrator enable it. The user also needs permission to use the project for quota, typically the Service Usage Consumer role. Run the following locally and select the intended Google account for the ADC login. Keep ADC in its standard local location and leave `GOOGLE_APPLICATION_CREDENTIALS` unset. [Google quickstart](https://developers.google.com/deep-review/docs/quickstart) · [Authentication](https://developers.google.com/deep-review/docs/authentication)

```sh
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud services enable deepreview.googleapis.com
gcloud auth application-default login --scopes=https://www.googleapis.com/auth/cloud-platform
gcloud auth application-default set-quota-project YOUR_PROJECT_ID
```

The integration uses Google's rolling free review allowance through user ADC. It requires a confirmed free slot before uploading the full PDF and checks quota again before creating the review. The create request uses a fixed payload with no Gemini API key or paid fallback. At zero quota, Codex records Google's next available time when supplied and asks whether to wait or finish with internal verification. A later retry checks quota again. These safeguards apply to this Deep Review integration. Billing and other services on the Cloud project are managed separately. [Google quotas and limits](https://developers.google.com/deep-review/docs/rate-limits)

Use the same Google user when resuming. A lost review submission response is reconciled against the reviews already listed for the uploaded document. If Google still shows no matching review, the run stays pending to avoid duplicate quota use. If the upload response itself is lost, the command pauses so the remote document can be reconciled before proceeding. A rebuild leaves the review tied to its original PDF. Keep the local state to preserve that association across sessions.

### Local paper history

Keep `paper/paper.tex` and `paper/paper.pdf` as the working files. Use concise chronological entries in `paper/plan.md` and `paper/review.md` to record the initial plan and feedback, first complete draft version, initial findings and applied edits, checkpoint 2 agreement and actual changes, combined verification, Google review and its disposition when used, and final approved PDF hash. Put file snapshots in `paper/.local/`. The two records, working PDF and local snapshot directory are Git-ignored by default. The Google step saves the full JSON response, including the report and anchored comments, and links it to a local copy of the reviewed PDF by SHA-256. Codex presents checked findings and proposed edits for author agreement, then stops for explicit final approval of the resulting PDF.

Run the offline integration tests with `python -m unittest discover -s tests`.
