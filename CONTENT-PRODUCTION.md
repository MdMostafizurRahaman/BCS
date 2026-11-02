# Required content scope — revised user requirement

The requested deliverable is **not complete**. The active collection now has 10,264 questions, including 10,000 sourced supplemental medical records. This meets the latest numeric minimum of 10,000 total, but does not establish the earlier 500-per-topic goal for general subjects, original pattern-based authorship, comprehensive medical review or verified past-paper completeness.

## Binding minimum

- Authentic previous-year special health BCS papers, initially 39th (2018), 42nd (2021), 48th (2025), with separate General/Medical/Dental identification.
- Analysis of those papers before claiming a historical pattern.
- At least 500 useful MCQs **per topic**, including explanations for both correct and incorrect attempts.
- Current coarse taxonomy: 34 topics, therefore 17,000 questions minimum. A complete syllabus microtopic taxonomy would increase this requirement. Do not silently reduce this to 500 per subject.
- Repeated stems, cosmetic rewrites, answer-option reorderings and simple parameter permutations must not be counted as independent conceptual coverage.

## Evidence record for each historical question

Preserve exam number, year, track, section, original scan URL/file hash, scan page, printed question number, exact stem/options, source answer, independently checked answer, explanation references, transcription check, and disputed-answer status. Preserve historical context for time-dependent GK rather than replacing the historical key with a current fact.

Question set/code must be recorded: multiple codes of the same examination can reorder questions and should not be counted as different questions. A source advertising 100 general questions must not be presented as a complete 200-question health paper.

## Analysis to compute from the reconciled corpus

1. Subject and topic counts per exam with denominators and a separate unclassified/disputed count.
2. Learning objectives: recall, mechanism, clinical vignette, calculation, interpretation, exception/negative stem.
3. Cross-year exact repeats versus repeated concepts; do not conflate these.
4. Distractor design, wording ambiguity, outdated facts and disputed keys.
5. Syllabus coverage and topics absent from the sample. Frequency is descriptive of the inspected papers, not a prediction guarantee.

Until the corpus is reconciled, no numerical historical frequency is established.

## Original-question record

Retain existing q/o/a/e fields, plus `learningObjective`, `subtopic`, `difficulty`, `questionForm`, `patternEvidence` (historical item IDs), `reference`, and `review` with reviewer, review date and reference locator. The explanation should explain the answer and distinguish plausible distractors. Clinical items require context sufficient for a single best answer and current supporting evidence.

Author questions across learning objectives rather than multiplying a small set of stems. Use source material within its permissions; commercial explanation banks are not a reusable licence for this project. Write original explanations and obtain reusable original papers rather than copying third-party solution collections wholesale.

## Release gate

`node scripts/audit-content.mjs` writes `data/research/coverage.json`.

`node scripts/audit-content.mjs --require-complete` must fail until every current topic contains 500 reviewed questions, all three historical papers contain 200 verified items, and normalized duplicate groups are resolved. This gate is deliberately stricter than structural JSON validity. A successful app test suite must not be reported as successful content completion.

Source discovery is recorded in `data/research/sources.json`; none of those candidates is certified as an original government paper. Do not silently promote candidate content to verified historical questions.
