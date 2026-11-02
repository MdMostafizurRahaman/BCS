# Question-bank attribution and changes

## Supplemental medical collection: MedMCQA

10,000 selected records in `questions.json` have `collection: medmcqa`. They are sourced, not newly authored by this project and not represented as historical BCS questions.

- Authors: Ankit Pal, Logesh Kumar Umapathi and Malaikannan Sankarasubbu.
- Work: *MedMCQA: A Large-scale Multi-Subject Multi-Choice Dataset for Medical domain Question Answering*, CHIL / PMLR 174, 2022, pp. 248–260.
- Paper: https://proceedings.mlr.press/v174/pal22a.html
- Upstream: https://github.com/medmcqa/medmcqa
- Download mirror: https://huggingface.co/datasets/awinml/medmcqa
- Pinned mirror revision: `ae3036c873dbd3bc9f33078616cffd20611eb9b1`
- Raw `train.json` SHA256: `afa1b32379409fce3090a39411a769e5f1739d8bd2c43acb0806a3e070f711ba`

The upstream repository's `LICENSE.md` states **MIT, Copyright (c) 2022 MedMCQA**; a copy is preserved in `licenses/MedMCQA-MIT.txt`. The mirror declares **Apache-2.0**, despite its README pointing to an upstream `LICENSE` path that does not exist. Both notices are retained and the standard Apache text is included in `licenses/Apache-2.0.txt`; the discrepancy is recorded rather than asserting that both upstream files say the same thing. These are publisher licence declarations, not independent verification of rights in every source book/examination.

Changes made: selected 1,000 items for each of ten medical subjects; removed HTML; normalized whitespace; excluded missing/short explanations, compound answer choices, duplicate options, many country-specific/legal references, missing visual dependencies, selected corrupted words, normalized exact repeats and high-overlap stems. Raw JSON answer keys are **1-based**; converted to the application's **0-based** answer indices without permuting these sourced options. Source ID, revision, split and original subject are preserved per record. Source subtopics are retained; macro subjects are mapped to the app's Medical syllabus labels. The sampling method spreads selection over subtopics.

The raw source is India-oriented AIIMS/NEET preparation material. It does not supply historical BCS evidence. Every selected answer/explanation remains publisher-provided and has not undergone independent clinical editorial review. Cleaning is not medical verification. Some terminology, guidelines and reference editions may be outdated. Subject-level mapping is not proof that each item matches the current Bangladesh syllabus. This collection is exam practice, not clinical guidance. No future-exam probability or endorsement is claimed.

## Historical BCS analysis corpus

Local exam adapter update: `archive-exams.js` and `archive-ui.js` can read the already downloaded corpus from the user's ignored local workspace for personal study, without adding its questions/notes to the published `questions.json`. The local browser renders those personal records and can retain a user-selected archive in IndexedDB. `.vercelignore` excludes the source artifacts from hosting. This is not a licence to publish the downloaded corpus as this site's public coaching bank. Aggregate research remains separate from authenticated original papers.

Source: SangbitDas/bcs-dataset, https://github.com/SangbitDas/bcs-dataset, compiled from Uttoron Academy question pages. Its `DATA_LICENSE.md` explicitly does **not** grant MIT rights to question text, explanations or images. The downloaded corpus remains in ignored local research artifacts. This project publishes aggregate counts and methods only in `data/research/historical-patterns.json`; it does not wholesale republish that corpus's question text, solution notes or images in the active bank.

Counts describe this third-party compilation, not authenticated original PSC papers. In particular, the special-health entries cover general parts only. Text-exact repeats and keyword-form counts must not be described as clinical-paper pattern analysis, a human-reviewed topic census or future-exam predictions.

## Bengali job-exam dataset inspected but not imported

`azminetoushikwasi/bangla-bcs-qs` was inspected at revision `c77be759069d0841073bb50c33e551ddea64edc2`. It has 3,938 entries, no teaching explanations in its question records, broad mixed BCS/bank provenance and no reliable per-item exam identity. It was excluded from the active bank. A dataset licence tag alone does not resolve its underlying commercial-PDF provenance.

## Existing project content

The 76 inherited Bangla items and 188 previously authored items retain their existing editorial labels. They are not relabelled as independently verified merely because a larger collection has been added.
