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

## Optional Google Deep Review at checkpoint 3

From the local Codex session in VS Code, tell Codex for the current paper:

> Use $physics-paper-orchestra and enable one free Google Deep Review for this paper at checkpoint 3. Record my opt-in in paper/plan.md or paper/review.md.

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

The integration uses Google's rolling free review allowance through user ADC and checks `GET /v1/userQuota` before uploading the full PDF. The request has no Gemini API key or paid fallback. At zero quota, Codex records Google's next available time when supplied and asks whether to wait or finish with internal verification. A later retry checks quota again. [Google quotas and limits](https://developers.google.com/deep-review/docs/rate-limits)

Use the same Google user when resuming. A lost review submission response is reconciled against the reviews already listed for the uploaded document. If Google still shows no matching review, the run stays pending to avoid duplicate quota use. If the upload response itself is lost, the command pauses so the remote document can be reconciled before proceeding. A rebuild leaves the review tied to its original PDF. Keep the local state to preserve that association across sessions.

### Local paper history

Keep `paper/paper.tex` and `paper/paper.pdf` as the working files. Use concise chronological entries in `paper/plan.md` and `paper/review.md` to record the initial plan and feedback, first complete draft version, initial findings and applied edits, checkpoint 2 agreement and actual changes, combined verification, Google review and its disposition when used, and final approved PDF hash. Put file snapshots in `paper/.local/`. The two records, working PDF and local snapshot directory are Git-ignored by default. The Google step saves the full JSON response, including the report and anchored comments, and links it to a local copy of the reviewed PDF by SHA-256. Codex presents checked findings and proposed edits for author agreement, then stops for explicit final approval of the resulting PDF.

Run the offline integration tests with `python -m unittest discover -s tests`.
