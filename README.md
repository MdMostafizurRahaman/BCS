# BCS Master — Medical preparation

A responsive Bangla study application for doctors preparing for special BCS. Plain HTML, CSS and ES modules; no runtime dependencies or build step. The current track uses the BPSC **48th special BCS (2025) Medical** syllabus as its reference.

## Run locally

```sh
npm run dev
```

Open http://127.0.0.1:5173. Python 3 is required for this convenience command. Any static HTTP server works. Opening `index.html` with `file://` does not support JSON fetching/ES modules reliably.

## Implemented

- Dashboard with actual question counts, distinct answered questions, latest-answer accuracy and daily goal.
- Seven subjects; topic filters, full-text search and unseen/wrong/bookmarked/due-question filters.
- Instant correctness and explanations for every practice answer, including correct answers.
- Wrong-question revision, bookmarks and simple spaced revision (1 day after a wrong answer, 3 after a correct answer).
- Medical/general quick tests, configurable tests and a 200-question mock matching subject and medical subtopic quotas.
- Timers based on an absolute deadline; reload recovery, question navigator, answer changes/clearing, confirmation before submission and automatic submission on expiry.
- Configurable negative marking; result review with explanations, skipped counts and examination history.
- Year/paper-based exams for imported past-paper JSON. Source metadata is mandatory; imported questions are explicitly user supplied.
- Per-subject analytics, 7-day activity, a syllabus map, introductory 7-day study plan and content/source disclosures.
- Local persistence, backup download/restore, schema-validated bank imports, daily goal and dark theme.
- Responsive mobile navigation, keyboard focus styles and text feedback alongside correctness colours.

## Question bank and limitations

The original 1,000-entry bank was only 76 unique Bangla questions repeated. It is preserved as `data/legacy-questions.json`. The active bank has **264 distinct practice questions**, including **100 medical**. The 188 new questions are original practice content, not reconstructed historical papers. All entries are labelled as requiring editorial review; only specific inspected references are linked to matching questions.

The previous-year archive intentionally contains no fabricated papers. Real papers can be imported from Settings using the downloadable JSON template, adding `type: "past"`, `year`, `paper`, and a valid HTTP(S) `source`. An import does not constitute independent verification.

This is a functional local-first study application and starting content bank. It does **not** yet have accounts, shared/server data, a multi-user editorial dashboard, a comprehensive historical question corpus, complete syllabus depth, independent medical review, or viva training. It must not be marketed as guaranteeing BCS selection or complete preparation. See [RESEARCH.md](RESEARCH.md) for audit results, evidence, limitations and the publication checklist.

## Data format

```json
{
  "id": "custom-001",
  "subject": "english",
  "topic": "Grammar",
  "type": "practice",
  "q": "Choose the correct article: ___ apple.",
  "o": ["A", "An", "The only", "No article"],
  "a": 1,
  "e": "Apple starts with a vowel sound, so use an."
}
```

`a` is zero-based. Supported subject IDs: `medical`, `bangla`, `english`, `bangladesh`, `international`, `math`, `mental`. Source links accept HTTP(S) only. IDs and exact stems must be unique and every question must have four different nonempty options and an explanation. Full mock allocation is defined in `core.js`.

Rebuild the bundled bank with `npm run build:bank` (Python 3). This always starts from the preserved legacy bank and the authored source rows, so manually added production questions should be maintained in a separate reviewed source before rebuilding.

Local storage keys: `bcs-master-v2` and `bcs-active-exam`. The older `bcs-progress` key is left untouched because its index-based counters cannot be reliably mapped after deduplication. Backups include imported questions. Do not put sensitive personal information into question imports or backup files.

## Validation

```sh
npm test
npm run check
```

Node 22+ runs the built-in test suite without installing dependencies. Tests cover bank integrity, full mock quotas, negative marking, skipped answers, latest-answer revision behaviour, filters, import rejection and Dhaka date boundaries.

## Deploy to Vercel

Import this existing folder/repository. Framework preset: **Other**. Build command: leave empty. Output directory: leave empty (project root). No secrets or backend are needed for the current local-first functionality. Deploying a new version updates the shared bundled questions; users' progress stays in their individual browsers.

No production deployment has been performed as part of this local implementation.
