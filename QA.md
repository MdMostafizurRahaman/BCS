# Verification

## Year/subject archive exams (latest)

23 automated tests pass in the local workspace, including exact BCS 35 Bangla count, original-paper identity, multi-year/subject selection, optional cross-year deduplication, blank-answer-key exclusion, safe image paths, grading and complete-health-paper gating. Source-dependent tests explicitly skip on checkouts without the ignored research artifacts.

Browser verified: BCS 35 Bangla starts with 35 questions; one selected answer and the timer survive reload; submission produces 1 correct / 34 skipped. BCS 35 full set starts with 200 questions after preflighting source images; original question 178 renders a loaded 414px-wide diagram; submitting an unanswered full paper produces 200 skipped. A two-year Bangla/English selection previews 138 unique exact-stem items and a requested limit of 10 previews 10 exam questions. BCS 42 full-set button is disabled while its complete general-part button is enabled. No browser error logs were present in the final mixed-selection check.

This verifies local personal-study operation. The source corpus is not bundled for public hosting; archived keys/dates/notes are not independently authenticated. Source-image URLs need network access. Missing source explanations are disclosed. Archive records opened by the user persist separately in IndexedDB; progress backups do not include that raw archive.

## Expanded-bank verification (latest)

The active collection has 10,264 items: 264 starter items plus 10,000 MedMCQA records. Thirteen automated tests pass, including attribution, 1,000-per-medical-topic counts, source/subtopic filters, and conversion of every selected raw 1-based answer key. The raw-key test is skipped explicitly when the ignored 147 MB research source is not present in a fresh checkout; it was run against the source in this workspace.

Browser checks on the expanded version: dashboard displays 10,264; Anatomy + MedMCQA filters return 1,000; a sourced clinical anatomy answer shows the explanation and provenance/review disclosure; the history panel displays the 41-exam/5,350-entry research aggregates and the general-only scope of the three health exams. No browser error logs were present after that practice check.

These checks verify integration and source-key preservation, not independent factual review of 10,000 medical answers, historical medical-paper pattern analysis, guaranteed semantic uniqueness or future-exam predictions. Earlier sections below record the initial prototype checks.

Local verification: 3 November 2026.

## Automated

`npm test`: 7 tests passed. Covers active-bank validation and deduplication, all 200-question subject/subtopic quotas, negative marking and skipped answers, repeat-answer revision behaviour, compound filters, malformed imports/unsafe links and Dhaka date boundaries.

`npm run check`: JavaScript syntax checks passed.

`git diff --check`: passed after line-ending normalization.

## Browser checks

Verified against the application served over HTTP locally:

- Dashboard renders actual counts and progress.
- Medical practice shows wrong-answer marking and an explanation immediately.
- A correct retry in the wrong-question queue shows its explanation and updates latest-answer accuracy.
- Bookmark state is retained across navigation.
- Subject, Pharmacology topic and the search `half-lives` combine to produce one matching question.
- A custom five-question exam allows an answer and restores it and the absolute countdown after reload.
- Submission confirmation leads to a scored result with one correct answer and four skipped questions and explanations for all five.
- A subsequent one-minute custom exam automatically submits at its deadline with five skipped answers and a zero score. This checks the timer continues to work after a previous submission.
- 390px mobile layout exposes the menu and opens the navigation drawer; document width does not exceed viewport width.
- Desktop dashboard inspected at 1280px; screenshot saved under `artifacts/dashboard.png` (ignored by Git).
- No browser JavaScript error logs were present at the end of the practice/search check.

Browser tests create demonstration progress in the local preview browser only. Backup/restore and file imports have schema/logic coverage but were not exercised end-to-end through a file picker. No hosted deployment, multi-user backend, account sync, medical editorial review or complete historical-paper verification was performed.


3 November medical correction: 25 Node tests pass. Browser verified the actual 48th medical-only exam (100 questions), navigation to printed question 200, reload recovery, answer submission, 1 correct/99 skipped scoring, and review notes. Verified immediate wrong-answer feedback during practice and the 100-item year filter. Coverage UI accurately states 48th 100, 39th 7, 42nd 1. The default Python process did not serve; bundled Python served port 5175 for QA. No public deployment. Remaining full medical-paper content gaps are documented in RESEARCH.md.

Mobile browser check at 390px: loaded archive medical controls present, document scroll width equals viewport width (375px after scrollbar), no horizontal overflow. Screenshot: artifacts/special-medical-mobile.png.
