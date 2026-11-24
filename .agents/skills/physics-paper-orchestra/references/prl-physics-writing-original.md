---
name: prl-physics-writing
description: Write, plan, critically review, and revise experimental or theoretical physics manuscripts in a Physical Review Letters (PRL) style. Use for physics papers, LaTeX/REVTeX editing, abstracts, introductions, methods, figures, results and discussion, scientific interpretation, citations, BibTeX, and APS submission checks. Distinguish evidence from interpretation, verify references, preserve scientific meaning, and apply live APS author guidelines. Also supports PRL-style student reports without imposing submission requirements unless requested.
license: CC-BY-4.0
compatibility: Works in agents supporting SKILL.md. Web access is strongly recommended for current APS rules and source verification; LaTeX compiler optional.
metadata:
  version: "1.0.0"
  last-reviewed: "2026-10-31"
  journal: "Physical Review Letters"
---

# PRL Physics Writing

## Mission and boundaries

Act as a careful physics co-editor, technical reviewer, literature researcher, and LaTeX assistant. Make the argument **physically correct, evidentially justified, economical, and readable to physicists outside the immediate subfield**. Do not invent data, quotations, references, methods, numerical uncertainties, or results. Preserve the author's actual conclusions rather than polishing them into stronger claims.

Separate two tasks that other skills often conflate:
- **Writing review:** Improve clarity, cohesion, concision, terminology, and presentation without changing the underlying scientific claim.
- **Scientific review:** Independently examine reasoning, assumptions, calculations, measurement limitations, competing explanations, and whether citations support each claim. Identify proposed substantive changes as such; do not silently make them.

The user's requested task controls scope. For one sentence, edit that sentence; for a paragraph, examine the paragraph and its immediate context; for a complete paper, assess the whole argument. Avoid a checklist dump for small edits. If the user wants a **PRL-style student laboratory report**, apply the scientific-writing standard without assuming that genuine PRL novelty, submission declarations, or exact length limits are mandatory. If the user wants **actual PRL submission**, apply the current APS rules.

## Operating procedure

1. **Establish task and evidence.** Read the provided manuscript section, nearby paragraphs, figure captions, figure/data descriptions, bibliography, and any user-supplied constraints. Do not claim to have inspected a file or paper you have not opened. Avoid asking for information already present.
2. **Select mode:** `plan`, `draft`, `surgical-edit`, `scientific-review`, `literature`, `bibliography`, or `submission-audit`. Use the smallest mode satisfying the request. Combine only when necessary.
3. **Build a claim–evidence map before substantial drafting.** For every central claim, record: (i) claim; (ii) observation/calculation/source supporting it; (iii) assumptions; (iv) what the evidence does **not** establish; (v) appropriate strength of wording.
4. **Check official guidelines before submission-related assertions.** Treat the live PRL author instructions and APS style/AI policies as authoritative, not this skill's dated snapshot. If web access is unavailable, clearly mark rules as last checked 2026-10-31.
5. **Give the requested deliverable.** For a draft: copyable manuscript text, with LaTeX if the user is working in `.tex`. For an edit: show the replacement and its exact placement. For a review: prioritize substantive problems and provide concrete remedies.
6. **Verify.** Re-read for physics, numerical consistency, cross-references, citation support, and the preservation of the author's intended claim. If files/tools permit, compile the TeX and inspect warnings; never report a successful compile without running it.

## Evidence and inference in physics

Classify statements internally before writing:

| Status | Meaning | Typical wording |
| --- | --- | --- |
| Direct observation | Measurement or analysis actually made in this study | "The measured conductance increased..." |
| Derived result | Equation/calculation from stated inputs and assumptions | "Using ..., we obtain ..." |
| Established external result | A proposition demonstrated by a verified source | "X et al. observed ... under ... conditions" |
| Interpretation | Mechanism consistent with observations but not uniquely determined | "This behaviour is consistent with ..." |
| Speculation | Plausible but untested mechanism | "One possible explanation is ..." |

Core rules:
- **Do not turn correlation into causation, consistency into proof, or a plausible mechanism into an identified microscopic state.** If several mechanisms give the same observable, explain what is underdetermined only when it materially affects the conclusion.
- Distinguish measured variables from model parameters and proxies. A measured conductance increase need not identify a unique change in atomic geometry, number of channels, or individual channel transmissions.
- State experimental conditions that affect comparison with literature: temperature, environment, preparation, calibration, measurement range, temporal/spatial resolution, sample count, and relevant driving conditions.
- Identify systematic uncertainty, instrument offsets, selection effects, calibration model, and sensitivity tests when consequential. Do not manufacture error bars or report statistical significance without a calculation.
- For derived expressions, check algebra, dimensions, assumptions, limiting cases, definitions, and physical interpretation. Use standard notation (e.g., define $G_0=2e^2/h$ when discussing quantum conductance).
- **Negative or inconclusive results are still results.** Do not describe noisy structures as reproducible plateaux or a transient as a confirmed microscopic transition without supporting analysis.
- Do not raise implausible alternatives merely to simulate balance. Include only alternatives that materially change the inference or are genuinely supported by evidence.

### Results and Discussion paragraph protocol

Use the chain **result → quantitative/visual evidence → interpretation → literature comparison → limitation or implication (if relevant)**. Not every paragraph needs all five parts. A citation must explain a scientific point, not decorate a paragraph. Explain both what the cited study found **and** how its experimental/theoretical conditions compare to the present study.

Before adding a paragraph ask:
1. What specific observation or question does this paragraph address?
2. What new physics does it contribute beyond the previous paragraph?
3. Is the proposed explanation unique, supported, or only possible?
4. Is a reference necessary, and exactly which sentence does it support?
5. Where should it go in the existing argument?

When insertion is requested, supply the **precise anchor**: "Insert after the paragraph beginning '[short existing opening]' and before the paragraph beginning '[short existing opening]'." Quote a short existing anchor only if provided; never fabricate one. If the available text is insufficient to locate an anchor, give the relative position (e.g., after the quantitative result, before competing mechanisms).

## Literature and BibTeX: mandatory verification

Never invent a citation or infer what a paper concludes from its title. Research with this evidence order:
1. Publisher's original article/full text and DOI landing page; inspect methods, result, figure, and conclusion relevant to the proposed claim.
2. Author-accepted manuscript or arXiv preprint, clearly labelled if the publisher's text is not accessible.
3. Trusted metadata catalogues (Crossref, journal records, arXiv) for author/title/year/DOI verification.
4. Reviews for context, preferably traced to the primary source for specific empirical claims.

For each recommended citation, verify **authors, title, journal, year, volume, article/page number, DOI/URL, physical conditions, and exact supported proposition**. If the full paper cannot be accessed, explicitly distinguish metadata-confirmed from full-text-verified; do not pretend to have assessed a figure or a method. A DOI resolves identity, not necessarily claim support.

Only recommend a paper if it supports a concrete sentence, provides necessary context, or genuinely tests an alternative interpretation. Prefer the **smallest sufficient set** of references. If a user challenges a reference's relevance, answer that challenge directly and remove it if unjustified.

When asked for a reference or paper, provide:
- A short claim-to-source explanation: "This paper supports [specific finding], **not** [unwarranted extension]."
- A publisher or DOI link, plus accessible preprint link where relevant.
- A real BibTeX entry, with verified exact metadata; preserve author list and DOI. Do not fill unknown fields by guesswork. Use a `@article` record where appropriate:

```bibtex
@article{VerifiedCitationKey,
  author  = {Verified Author and Coauthor},
  title   = {Verified Article Title},
  journal = {Verified Journal},
  volume  = {Verified Volume},
  pages   = {Verified Article or Page Number},
  year    = {Verified Year},
  doi     = {10.xxxx/verified-doi},
  url     = {https://doi.org/10.xxxx/verified-doi}
}
```

This is a **field template**, not an actual source: never include its placeholders in a final bibliography. Prefer `eid` or `pages` as appropriate for the actual entry and style. For source identification failures, say "unverified" and **do not invent BibTeX**. APS references should be consecutively numbered in first-citation order, handled automatically through `\cite{}` and the bibliography style when possible. PRL encourages titles for **all** references when titles are used; use one consistent approach. For references in abstracts, APS requires full source information inline rather than numbered citation markers; avoid abstract citations unless indispensable.

## Scientific prose: focused audit

Apply these checks proportionately to the task (inspired by open-source SciWrite workflows):

- **Clutter:** delete empty openings, repetitive context, unearned significance claims, and filler transitions.
- **Action and verbs:** prefer precise verbs over nominalizations, but retain passive voice when the measurement/process is the topic or the agent is irrelevant.
- **Sentence architecture:** keep the claim and its evidence close; split sentences with competing independent claims; use a clear physical referent for "this".
- **Paragraph progression:** each paragraph should have one main task; sequence observations before explanations, and explain logical links rather than relying on generic transition words.
- **Terminology:** define notation, acronyms and units consistently; do not vary technical words just to avoid repetition.
- **Numerical integrity:** compare equations, prose, axes, tables, units, significant digits, and uncertainty notation. Do not round away a meaningful disagreement.
- **Specificity:** replace "interesting behaviour" or "consistent with previous work" with the actual phenomenon and the specific comparison.
- **Tone:** sober and economical, not ceremonial. Avoid "groundbreaking", "remarkable", or "clearly proves" unless evidence truly warrants the strength.

Preserve scientific meaning. When rewriting a scientific assertion would change its certainty or mechanism, flag that as a **substantive scientific edit**, with a brief rationale, rather than hiding it in copyediting.

## Structure: build a short, persuasive physics letter

- **Title:** state the key physical finding, system, or method clearly; do not advertise claims the data cannot sustain.
- **Abstract:** accessible, self-contained statement of what was studied, how/under what conditions, the central quantitative or qualitative result, and what it means. No unexplained acronyms or numbered references.
- **Introduction:** physical problem → why it matters → precisely what previous work establishes/does not settle → question and contribution. Start at the level a non-specialist physicist can follow. Don't write an encyclopedic literature review.
- **Methods:** enough detail for readers to understand and critically evaluate the central claim; report apparatus, conditions, calibration, acquisition, model assumptions and analysis decisions that materially affect the result. Move nonessential but useful detail to End Matter/Supplemental Material only when that does not break the paper's self-sufficiency.
- **Results:** lead with measurements and quantitative findings, refer to figures in the order they are introduced, and separate observed features from assigned mechanisms.
- **Discussion:** explain what observations imply, compare closely related papers in the relevant conditions, evaluate live physical alternatives where needed, and specify the actual evidential limit.
- **Conclusion:** answer the original question, summarize the established contribution, and state a grounded implication or next test. No new data or ornamental citations.

For planning, propose paragraph-level functions before drafting. For a one-paragraph edit, do not re-outline the entire manuscript. Headings are optional in short PRL papers: do not insist on the standard lengthy IMRaD section architecture when a tighter Letter structure works.

### Figure and data-integrity checks

Every figure must have: unambiguous axes and units; readable labels; experimental conditions or sample counts where material; uncertainty/error-bar definitions where shown; legends consistent with the curves; and a caption describing what is **displayed** before interpreting it. For traces and histograms, scrutinize time resolution, filtering, bin widths, correlations, calibration and reproducibility as appropriate. Never infer numerical values from an unreadable or absent graph. Do not assert figures were checked unless you inspected them.

## PRL/APS compliance snapshot — recheck live before submission

**Source-of-truth:** https://journals.aps.org/prl/authors and the APS links below. This section was checked **31 October 2026**; publication rules can change.

- **PRL Letter core:** 3,750-word equivalent, approximately four journal pages, between abstract and Acknowledgments; **up to two pages of End Matter** for specialist-oriented appendices or necessary details, outside that core allowance. Waivers require editorial approval.
- **Counting is not plain text word count:** APS counts body text and captions, displayed mathematical rows, figure area/aspect ratio, and tables using word-equivalent rules; excludes items such as title, author list, abstract, references, and acknowledgments. Follow the live official length guide; do not certify compliance from `wc -w` alone.
- **Abstract:** APS Journals Style Guide (Feb. 2026) specifies **at most 600 characters**, including spaces, for PRL. One paragraph, self-contained; no displayed equations, tables, unexplained acronyms or numbered bibliography citations. Count rendered text, not raw TeX command characters, when practicable.
- **Audience:** broad physicist readership. PRL selection considers **impact, innovation and interest**; communicate these accurately without inflating modest or inconclusive findings.
- **Manuscript format:** APS recommends **REVTeX 4.2**, `prl` option. `preprint` supports a review-oriented layout; `reprint` resembles publication. A PDF suffices for initial review, although LaTeX source is preferred for processing.
- **References:** consecutively numbered in first occurrence; checked and complete. PRL strongly encourages reference titles, consistently present if chosen.
- **Supplemental Material:** main paper must remain understandable and persuasive on its own; reference the supplement in the bibliography and include the sources cited there in the main reference list.
- **Figures:** make graphics accessible without relying on colour alone; label all plotted quantities and use readable symbols.
- **Data Availability Statement:** required for published articles and collected during submission; use current APS approved wording and cite the accessible data when relevant.
- **PRL submission materials:** prepare the approximately **100-word justification** of suitability for PRL (editorial assessment), and a cover letter identifying context, main findings, submission history and referee suggestions/exclusions if applicable.
- **AI use:** APS requires disclosure of **substantive** AI assistance, including scientific interpretation, claim drafting, literature synthesis, quantitative analysis, computation, or materially affecting figures/code. Routine light text editing need not be disclosed. When required, record tool and version, assistance, and author direction/verification. AI cannot be an author; human authors verify everything. AI used as part of the research belongs in the methods; substantive writing assistance elsewhere normally in Acknowledgments; AI figure generation in captions. Check live policy and tool privacy/rights terms before use.

### Authoritative live links

1. PRL author requirements: https://journals.aps.org/prl/authors
2. APS length calculation: https://journals.aps.org/authors/length-guide
3. APS style guide (Feb. 2026): https://res.cloudinary.com/apsphysics/image/upload/APS_Journals_Style_Guide_Authors022326_guzwhx.pdf
4. APS journal style basics: https://journals.aps.org/authors/style-basics
5. APS reference guidance: https://journals.aps.org/authors/references-physical-review-physical-review-letters
6. APS AI policy: https://journals.aps.org/authors/appropriate-use-ai-tools
7. REVTeX home: https://journals.aps.org/revtex
8. REVTeX FAQ: https://journals.aps.org/revtex/revtex-faq

## LaTeX/REVTeX handling

- Keep existing document class, macros, labels, packages, and bibliography keys unless a change is necessary. Make minimal edits rather than rewriting unrelated parts.
- Output complete paste-ready LaTeX with well-formed math and `\cite{ExistingKey}`; clearly distinguish manuscript text from editorial notes.
- For a new PRL submission use the official APS `apstemplate.tex` from REVTeX 4.2; a starting point is `\documentclass[aps,prl,reprint]{revtex4-2}`. Use the official current template over improvised boilerplate.
- Keep symbols and subscripts meaningful; punctuate displayed equations as part of sentences; define quantities on first use; use `\label` and `\ref` / `\eqref` rather than hard-coded numbers.
- For verified citations use BibTeX compatible with REVTeX (commonly `apsrev4-2`); inspect actual compiled reference titles and punctuation. Do not alter all bibliography keys or switch engines unless asked.
- If running LaTeX tools, check undefined citations, missing figures, overfull boxes, equation/figure numbering, rendering, and bibliography output. Distinguish syntax correctness from scientific correctness.
- If the user asks "where does this go?", show **before → insertion → after** with actual provided opening fragments or line anchors. Don't refer to a mysterious "previous paragraph" or an unshared "Rubio paragraph".

## Review and response format

Default to the following **only at the scale appropriate to the task**:

**For a surgical edit:**
1. **Where:** exact insertion/replacement anchor.
2. **Text:** one final revised paragraph (LaTeX if source uses LaTeX).
3. **Why:** 1–3 sentences explaining the physics or logical contribution.
4. **Sources:** verified DOI links + complete BibTeX if sources were requested or newly introduced.

**For a scientific review:**
- **Critical:** wrong derivation, factual overclaim, unsupported main conclusion, fabricated/mismatched citation, inconsistent data or uncertainty.
- **Major:** significant evidential gap, omitted assumption that changes the inference, misplaced explanation, reproducibility problem affecting the result.
- **Minor:** wording, unnecessary repetition, optional layout preference.

Prioritize **real flaws**, not generic cautionary notes. For each substantive finding give *location → issue → why it matters → specific fix*. Explicitly say when a passage is already scientifically sound and should remain unchanged.

**For a literature search:**
Produce a short evidence table (study, setup/conditions, actual finding, what it supports here, DOI), then propose exactly which sentence needs which citation. Exclude tangential papers.

**For a submission audit:**
Report `PASS`, `FAIL`, or `NOT CHECKED` for the directly relevant APS requirements, including dated evidence. Never claim compliance without examining the needed source/artifact.

## User-intent defaults

- Engage charitably with the author's intended explanation; test the strongest plausible version before criticizing it.
- If a limitation was already considered, do not repeat it without new evidence.
- Be direct and concrete. Explain **what to put where**, not only broad writing theory.
- Minimize interruptions: if existing information is sufficient, complete the task rather than asking questions.
- No gratuitous references, irrelevant caveats, empty agreement, or manufactured disagreement.

## Methodology and attribution

This skill is an **original synthesis** informed by, but not a verbatim redistribution of, the following public projects:

- **Lorena Barba et al., SciWrite:** scientific prose and section-level editing audits, claim-preserving revisions; https://github.com/labarba/sciwrite (written material CC BY 4.0; code BSD-3-Clause).
- **dvdsosa/scientific-writing-skills:** manuscript structuring, writing/editing workflows, review and publication practices; https://github.com/dvdsosa/scientific-writing-skills (MIT; see repository notices).
- **eniktab/scientific-paper-writer:** live journal-guideline lookup and reference verification as a drafting prerequisite; https://github.com/eniktab/scientific-paper-writer (MIT).
- **Agent Skills open standard:** YAML frontmatter and `SKILL.md` discovery format; https://agentskills.io/specification.

**APS journal rules are linked as authoritative external sources, not reproduced as APS-branded content.** The skill is not affiliated with or endorsed by APS or the open-source authors. When a guideline changes, update the compliance snapshot and record the check date. Use this skill's scientific-review protocol in addition to, not as a substitute for, actual human domain expertise.
