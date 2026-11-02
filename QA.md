# Verification

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
