# Content audit and preparation model

Research date: 3 November 2026 (Asia/Dhaka).

## Existing project audit

The inherited `questions.json` had 1,000 rows. Exact text comparison found 152 distinct stems, but half of those were the same stems with a `[রিভিশন]` prefix. Removing that prefix left **76 original questions, all Bangla**. The original README acknowledged revision entries. The previous interface counted repeated answers as new progress, had no subject/topic metadata, and could not run an exam or grade a paper.

The original file is preserved in `data/legacy-questions.json`. `scripts/build-bank.py` reproducibly normalizes it and adds original practice questions. Nothing in the new bank is labelled as an authentic past-paper question.

## Primary framework

[BPSC: 48th special BCS examination syllabus, 2025](https://bpsc.portal.gov.bd/sites/default/files/files/bpsc.portal.gov.bd/psc_exam/2ece87ae_8b68_40a5_93e5_0b4c425e35e6/বিসিএস%20%28বিশেষ%29%20পরীক্ষা-২০২৫%20%20এর%20সিলেবাস.pdf)

The Medical Science track allocates 100 marks to medical subjects and 100 to general subjects. General allocation: Bangla 20, English 20, Bangladesh affairs 20, international affairs 20, mathematics 10, mental ability 10.

Medical allocation: Anatomy 12, Physiology 13, Biochemistry 5, Pharmacology 5, Forensic Medicine 5, Community Medicine/Public Health 5, Pathology 5, Medicine 17, Surgery 17, Obstetrics/Gynaecology 16. The full mock generator checks every quota; it refuses to generate an incorrectly balanced paper when a quota cannot be met. Mock duration (120 minutes) and scoring (+1 / −0.5) are preparation settings, not a claim about future recruitment rules.

This is explicitly a **48th special BCS Medical reference track**, not a claim that the latest special examination has the same syllabus. Dental Science has a separate syllabus and is not implemented as a separate track here.

## What the available past-question sample supports

[Live MCQ's published 48th special BCS solution samples](https://web.livemcq.com/blog/48th-special-bcs-question-pdf) were inspected for question forms, not copied as a bank or used as an official answer key. The visible samples include short clinical presentations, mechanisms/associations, adverse effects and factual recall. Some publicly indexed solutions are clinically oversimplified; they should not automatically be treated as definitive keys.

**Inference:** preparation should combine recall with understanding of mechanisms and discrimination between plausible options. Original questions therefore explain the concept and common confusion; mathematical items show working, and language items explain the applicable rule.

**Not established:** year-by-year frequency, repeated-topic percentages, predicted common questions, or comparative patterns across the 39th, 42nd and 48th exams. No complete original multi-year question corpus or official answer-key set was available in this workspace. Claims of a comprehensive historical pattern analysis would be unsupported. The archive intentionally starts empty and supports explicit user-supplied paper imports with provenance.

## New bank

264 distinct questions:

| Subject | Questions |
|---|---:|
| Medical Science | 100 |
| Bangla (inherited) | 76 |
| English | 20 |
| Bangladesh affairs | 20 |
| International affairs | 20 |
| Mathematics | 16 |
| Mental ability | 12 |

The 188 newly authored questions are **practice content requiring editorial review**. The inherited 76 are also explicitly marked unreviewed. A deterministic per-ID option permutation avoids answer-position cues. This is a starting bank with sufficient quotas for one complete mock, not sufficient breadth for complete exam preparation. Medical subtopic labels are coarse; a production bank should add organ-system and microtopic tags, more clinical vignettes, curriculum mapping and difficulty calibration.

Some specific supporting references inspected:

- [SA node physiology, NCBI Bookshelf](https://www.ncbi.nlm.nih.gov/books/NBK459238/)
- [OpenStax: tubular reabsorption](https://openstax.org/books/anatomy-and-physiology-2e/pages/25-6-tubular-reabsorption)
- [FDA: diagnostic-test sensitivity and specificity](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/statistical-guidance-reporting-results-studies-evaluating-diagnostic-tests-guidance-industry-and-fda)
- [US National Library of Medicine: incidence and prevalence](https://www.nlm.nih.gov/nichsr/stats_tutorial/section1/mod2_conditions.html)

These are attached only to the matching questions; the rest do not receive invented source citations. General source suggestions do not mean every clinical item was independently verified. Medical content is for examination practice, not patient-care decisions.

## Requirements before presenting this as comprehensive public preparation

1. Obtain original permitted question papers and reliable keys for each claimed year; independently reconcile disputed answers.
2. Have medical and language subject editors review answers and explanations, including the inherited content.
3. Expand coverage beyond one question per syllabus mark. Map each syllabus bullet to multiple recall and application questions; add missing English, reasoning and clinical topics.
4. Add a reviewed publication workflow and a correction/report system with server persistence.
5. If multi-device/student accounts are required, add authenticated backend storage and user-level access control. Current data stays in each browser and can be exported/imported; it is not a shared multi-user database.
6. Refresh the selected examination's circular and syllabus, and separately plan viva preparation if claiming end-to-end cadre preparation.
